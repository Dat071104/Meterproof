"""Opt-in migration smoke and transactional-DDL negative control."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import psycopg
import pytest

ROOT = Path(__file__).resolve().parents[2]
DB_DIR = ROOT / "infra" / "db"
DATABASE_URL = os.getenv(
    "METERPROOF_DATABASE_URL",
    "postgresql://meterproof_local:meterproof_local_only@127.0.0.1:54329/meterproof",
)
PSYCOPG_DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://", 1)


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("METERPROOF_DB_SMOKE") != "1",
        reason="set METERPROOF_DB_SMOKE=1 to run against the local Compose database",
    ),
]


def run_alembic(directory: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(directory / "alembic.ini"), *arguments],
        cwd=directory,
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "METERPROOF_DATABASE_URL": DATABASE_URL},
    )


def scalar(query: str) -> Any:
    with psycopg.connect(PSYCOPG_DATABASE_URL) as connection:
        row = connection.execute(query).fetchone()
        assert row is not None
        return row[0]


def require_success(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, f"exit={result.returncode}\n{result.stdout}\n{result.stderr}"


def test_baseline_upgrade_downgrade_upgrade() -> None:
    require_success(run_alembic(DB_DIR, "upgrade", "head"))
    assert scalar("SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname='meterproof')") is True
    assert scalar("SELECT version_num FROM alembic_version") == "0001"

    require_success(run_alembic(DB_DIR, "downgrade", "base"))
    assert scalar("SELECT EXISTS (SELECT FROM pg_namespace WHERE nspname='meterproof')") is False

    require_success(run_alembic(DB_DIR, "upgrade", "head"))
    assert scalar("SELECT version_num FROM alembic_version") == "0001"


def test_invalid_revision_rolls_back_transactional_ddl() -> None:
    require_success(run_alembic(DB_DIR, "upgrade", "head"))
    with tempfile.TemporaryDirectory(prefix="meterproof-bad-migration-") as temporary:
        clone = Path(temporary) / "db"
        shutil.copytree(DB_DIR, clone)
        revision = clone / "versions" / "0002_invalid_control.py"
        revision.write_text(
            """from alembic import op
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None
def upgrade():
    op.execute('CREATE TABLE transient_should_rollback (id integer PRIMARY KEY)')
    op.execute('SELECT meterproof_intentionally_invalid(')
def downgrade():
    op.execute('DROP TABLE transient_should_rollback')
""",
            encoding="utf-8",
        )
        result = run_alembic(clone, "upgrade", "head")
        assert result.returncode != 0, f"invalid revision unexpectedly succeeded: {result.stdout}"

    assert (
        scalar(
            "SELECT EXISTS (SELECT FROM information_schema.tables "
            "WHERE table_schema='public' AND table_name='transient_should_rollback')"
        )
        is False
    )
    assert scalar("SELECT version_num FROM alembic_version") == "0001"
