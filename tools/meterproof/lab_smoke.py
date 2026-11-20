#!/usr/bin/env python3
"""Check the health contracts for the local Compose profiles."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
COMPOSE_FILE = ROOT / "infra" / "compose" / "compose.yaml"
EXPECTED_POSTGRES_MAJOR = "18"
EXPECTED_FLINK_VERSION = "2.2.1"


def compose_exec(service: str, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "exec",
            "-T",
            service,
            *command,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def check_db() -> bool:
    query = (
        'exec psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc '
        "\"SHOW wal_level; SELECT current_setting('server_version_num')::int / 10000;\""
    )
    result = compose_exec("postgres", "sh", "-ec", query)
    values = result.stdout.splitlines()
    expected_major = os.getenv("METERPROOF_POSTGRES_MAJOR", EXPECTED_POSTGRES_MAJOR)
    passed = result.returncode == 0 and len(values) >= 2
    passed = passed and values[0].strip() == "logical"
    passed = passed and values[1].strip() == expected_major
    if passed:
        print(f"PASS db: wal_level=logical; PostgreSQL major={values[1].strip()}")
    else:
        print(
            f"FAIL db: exit={result.returncode}; output={result.stdout.strip()!r}; error={result.stderr.strip()!r}"
        )
    return passed


def check_cdc() -> bool:
    broker = compose_exec(
        "kafka",
        "/opt/kafka/bin/kafka-topics.sh",
        "--bootstrap-server",
        "kafka:9092",
        "--list",
    )
    if broker.returncode != 0:
        print(f"FAIL cdc: Kafka topic list exit={broker.returncode}; {broker.stderr.strip()}")
        return False

    port = os.getenv("METERPROOF_CONNECT_PORT", "8083")
    url = f"http://127.0.0.1:{port}/connector-plugins"
    try:
        with urlopen(url, timeout=10) as response:
            plugins = json.loads(response.read())
    except (OSError, URLError, json.JSONDecodeError) as error:
        print(f"FAIL cdc: Connect plugin endpoint: {error}")
        return False
    postgres_plugin = any(
        item.get("class") == "io.debezium.connector.postgresql.PostgresConnector"
        for item in plugins
        if isinstance(item, dict)
    )
    if not postgres_plugin:
        print("FAIL cdc: PostgreSQL connector plugin is absent")
        return False
    print(f"PASS cdc: Kafka topic list answered; PostgreSQL connector plugin is present at {url}")
    return True


def check_stream() -> bool:
    port = os.getenv("METERPROOF_FLINK_PORT", "8081")
    url = f"http://127.0.0.1:{port}/overview"
    try:
        with urlopen(url, timeout=10) as response:
            overview = json.loads(response.read())
    except (OSError, URLError, json.JSONDecodeError) as error:
        print(f"FAIL stream: Flink overview endpoint: {error}")
        return False

    taskmanagers = int(overview.get("taskmanagers", 0))
    slots = int(overview.get("slots-total", 0))
    version = compose_exec("flink-jobmanager", "/opt/flink/bin/flink", "--version")
    expected = os.getenv("METERPROOF_FLINK_VERSION", EXPECTED_FLINK_VERSION)
    version_matches = version.returncode == 0 and expected in version.stdout + version.stderr
    passed = taskmanagers >= 1 and slots >= 1 and version_matches
    if passed:
        print(f"PASS stream: taskmanagers={taskmanagers}; slots={slots}; Flink={expected}")
    else:
        print(
            f"FAIL stream: taskmanagers={taskmanagers}; slots={slots}; "
            f"version_exit={version.returncode}; version_output={version.stdout.strip()!r}"
        )
    return passed


def check_full() -> bool:
    results = (check_db(), check_cdc(), check_stream())
    passed = all(results)
    if passed:
        print("PASS full: db, cdc and stream checks passed")
    else:
        print("FAIL full: one or more profile checks failed")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("db", "cdc", "stream", "full"), required=True)
    args = parser.parse_args()
    checks = {
        "db": check_db,
        "cdc": check_cdc,
        "stream": check_stream,
        "full": check_full,
    }
    return 0 if checks[args.profile]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
