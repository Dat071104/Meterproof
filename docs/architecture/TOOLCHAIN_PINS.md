# P0.4 toolchain pins

**Status:** IN_PROGRESS — Amendment 01 A1-1..A1-6 applied. dbt-core 1.11.17 and mypy 1.19.1 are explicitly pinned in the single lock; latest mypy 2.4.1 is rejected because its `pathspec>=1.0.0` conflicts with dbt-core's `pathspec<0.13`. A1-6's exact path-and-shape Gitleaks allowlist clears the advisor-reviewed manifest digest false positive; configured history and working-tree scans and both negative controls pass. P0.4 verification remains underway.

**Amendment:** [WAVE-02_AMENDMENT-01.md](../ops/prompts/WAVE-02_AMENDMENT-01.md) (owner-delegated A1-1 through A1-6). It is included by explicit path in the first post-amendment P0.4 documentation commit; the pre-amendment Apache license commit `31eb5cd` is unchanged.

## Host inventory

| Tool/resource | Observed |
|---|---|
| Python | `py -0p`: 3.14.4 at `C:\Python314\python.exe`; 3.13.2 at `C:\Python313\python.exe`. Shell `python --version`: 3.14.4. |
| uv | `uv 0.11.20 (9252ba6b5 2026-06-10 x86_64-pc-windows-msvc)` |
| Docker | Engine 29.9.3, Linux, 20 CPUs, 8,171,610,112 bytes (7.61 GiB); Docker root `/var/lib/docker`. |
| Docker Compose | 5.7.0 |
| Git | 2.53.0.windows.2 |
| Free disk | C: 70.47 GiB; D: 127.63 GiB. |
| Java path | `where.exe java` resolves `C:\Program Files\Common Files\Oracle\Java\javapath\java.exe`; file metadata is Oracle Java Platform SE 23 / `shimconsole.exe`, version 23.0.0.0. Hidden `java -version` timed out after 20 seconds with empty stdout/stderr; the diagnostic PID was absent on follow-up. Host PATH/JDK were not changed. |
| Existing project Docker resources | No container or volume with label `com.docker.compose.project=meterproof` existed before P0.4. |

Commands: `py -0p`; each listed interpreter with `-c "import sys; print(sys.executable); print(sys.version)"`; `python --version`; `uv --version`; `docker --version`; `docker compose version`; `git --version`; elevated read-only `docker info`; `Get-PSDrive`; `where.exe java`; `Get-Command java -All`; hidden 20-second Java version probe; project-label container/volume listing.

## Python project selection

Python 3.13 is selected because PyPI metadata for dbt-core 1.11.17 and dbt-postgres 1.11.0 lists Python 3.13 support. Per Amendment 01 A1-2, dbt-core is constrained to `>=1.11.17,<1.12`; the latest stable 1.11 release is 1.11.17. The earlier latest-stable dbt-core 1.12.7 choice is rejected because its experimental parser build downloads an unhashed binary from GitHub. Per A1-5, mypy 1.19.1 is pinned as the newest release resolving in the same environment. `uv lock --upgrade` resolves 69 packages and `uv sync --locked --all-groups` exits 0.

| Package | Locked version | Official source / observed metadata (checked 2026-11-20) | Local verification command |
|---|---|---|---|
| `jsonschema` | `4.23.0` | [PyPI JSON](https://pypi.org/pypi/jsonschema/json); pinned by WAVE-01 evidence. | `uv run python -c "import importlib.metadata as m; print(m.version('jsonschema'))"` |
| `rfc3339-validator` | `0.1.4` | [PyPI JSON](https://pypi.org/pypi/rfc3339-validator/json); pinned by WAVE-01 evidence. | `uv run python -c "import importlib.metadata as m; print(m.version('rfc3339-validator'))"` |
| `pytest` | `8.3.5` | [PyPI JSON](https://pypi.org/pypi/pytest/json); pinned by WAVE-01 evidence. | `uv run pytest --version` |
| `ruff` | `0.17.6` | [PyPI JSON](https://pypi.org/pypi/ruff/json); latest stable metadata lists Python 3.13. | `uv run ruff --version` |
| `mypy` | `1.19.1` | [PyPI JSON 1.19.1](https://pypi.org/pypi/mypy/1.19.1/json) declares Python 3.13 and requires `pathspec>=0.9.0`; this intersects dbt-core 1.11.17's `pathspec<0.13`. Per Amendment A1-5, latest stable mypy 2.4.1 is rejected because it requires `pathspec>=1.0.0`; mypy 1.20.x/2.x do not resolve with dbt 1.11.17. Reopen if dbt-core moves to a line allowing `pathspec>=1.0`. | `uv run --locked mypy --version` |
| `alembic` | `1.20.1` | [PyPI JSON](https://pypi.org/pypi/alembic/json); latest stable metadata lists Python 3.13. | `uv run alembic --version` |
| `SQLAlchemy` | `2.1.9` | [PyPI JSON](https://pypi.org/pypi/SQLAlchemy/json); latest stable metadata lists Python 3.13. | `uv run python -c "import sqlalchemy; print(sqlalchemy.__version__)"` |
| `psycopg[binary]` | `3.3.9` | [PyPI JSON](https://pypi.org/pypi/psycopg/json); latest stable is 3.x and metadata lists Python 3.13. | `uv run python -c "import psycopg; print(psycopg.__version__)"` |
| `dbt-core` | `1.11.17` | [PyPI JSON 1.11.17](https://pypi.org/pypi/dbt-core/1.11.17/json); Python 3.13 classifier; latest stable within the owner-authorized 1.11 line; no `dbt-core-experimental-parser` dependency. [PyPI JSON 1.12.7](https://pypi.org/pypi/dbt-core/1.12.7/json) is rejected under Amendment A1-2 because its parser sdist downloads a binary from a GitHub release. | `uv run --locked dbt --version` -> core 1.11.17 |
| `dbt-postgres` | `1.11.0` | [PyPI JSON](https://pypi.org/pypi/dbt-postgres/json); latest stable metadata lists Python 3.13, `Requires-Python >=3.10.0`, and `dbt-core <2.0`. | `uv run dbt --version` |

`uv run --locked dbt --version` exits 0 and reports core 1.11.17 plus the postgres 1.11.0 adapter. A `uv run --locked --no-sync` TOML inspection reports 69 locked packages, `dbt-core-experimental-parser` absent, and 0 sdist-only packages (`sdist` present with no wheel entry). The offline clean-checkout run remains required. The rejected 1.12.7 parser package is a 4.7 KB PyPI sdist whose backend downloads a binary from GitHub, so the lock hash does not cover the fetched executable artifact. The original 1.12.7 sync attempt failed with WinError 10060 as expected under the host's GitHub route.

## Container image pins

All chosen images are pinned as `name:tag@sha256:digest`. Local size is the byte count from `docker image inspect`; tag/registry sources and local pull/inspect commands are recorded. The Docker daemon reports `linux/x86_64`.

| Role | Pin | Official source and version evidence | Local pull / size |
|---|---|---|---|
| Flink | `flink:2.2.1-java17@sha256:55ccb2ad4b98362c3f3503c5a6d7cd00b92eb25e38815ddaf0be5903ade54ffe` | [Flink downloads](https://flink.apache.org/downloads/) lists 2.3.0 newest stable; [connector compatibility](https://flink.apache.org/downloads/) lists Kafka connector 5.0.0 for Flink 2.1.x/2.2.x; [stable Kafka docs](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/) say no 2.3 connector exists. Official Hub tag `2.2.1-java17` was checked. | `docker pull flink:2.2.1-java17` -> success; `docker image inspect` -> 1,563,969,706 bytes. Kafka connector artifact: `org.apache.flink:flink-connector-kafka:5.0.0-2.2`. |
| PostgreSQL | `postgres:18.7@sha256:eb63372c1e05c755f55fa30cbd07aecc443676fc6c0fa90b9002d01537841e1a` | [Debezium 3.7 tested versions](https://debezium.io/releases/3.7/) lists PostgreSQL 14–18; the [PostgreSQL project](https://www.postgresql.org/about/press/faq/) says 19 is newest, so 18 is the newest major supported by the chosen Debezium series. Docker Official Image lists tag 18.7. | `docker pull postgres:18.7` -> success; `docker image inspect` -> 669,652,646 bytes. |
| Kafka | `apache/kafka:4.3.2@sha256:852a0d49fc4e656b022e7f23785411802c9a088c78a7c5e39f33969de9c227a7` | [Apache Kafka downloads](https://kafka.apache.org/downloads/) lists 4.3.2 as the supported 4.3 patch and its Docker image. Debezium 3.7.1 tested 4.3.1; its support matrix lists Kafka Connect 3.1 and later, and [Flink Kafka docs](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/) say clients support brokers 2.1+. Choosing broker 4.3.2 with Connect 4.3.1 is an inference within the same Kafka 4.3 line; the local CDC smoke verifies startup. | `docker pull apache/kafka:4.3.2` -> success; `docker image inspect` -> 687,507,092 bytes. KRaft mode; no ZooKeeper. A preliminary 4.3.1 image remains cached but is not selected. |
| Debezium Connect | `quay.io/debezium/connect:3.7.1.Final@sha256:1589366704e1e016bad42b15fbdb364ba48780c61d0094197ca8632cb1271539` | [Debezium 3.7 release notes](https://debezium.io/releases/3.7/release-notes) list 3.7.1.Final as the newest Final release and Kafka Connect/broker 4.3.1 test version. [Release overview](https://debezium.io/releases/) lists PostgreSQL 14–18. | `docker pull quay.io/debezium/connect:3.7.1.Final` -> success; `docker image inspect` -> 2,463,584,450 bytes. |
| Maven / JDK check | `maven:3.10-eclipse-temurin-17@sha256:0362bf77ae7b21e3e0a0f4b211e85eb973e2cf9a680b2d36210e580336bb2255` | [Docker Official Maven tags](https://hub.docker.com/_/maven/tags?name=17&page=1) lists 3.10 with Eclipse Temurin 17. | `docker pull maven:3.10-eclipse-temurin-17` -> success; `docker image inspect` -> 826,364,744 bytes. In-container `java -version` remains Step 1.9. |
| Gitleaks | `zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f` (manifest index) | Amendment A1-3. The [official Gitleaks README](https://github.com/gitleaks/gitleaks/blob/master/README.md) lists both `zricethezav/gitleaks` and `ghcr.io/gitleaks/gitleaks`. Docker Hub tag metadata reports this index digest and linux/amd64 child digest `sha256:b109bc5f8f76a38196a3e413704fc5b9e3c32360bce4e4b603bd6f45b3721dbb` (25,037,736 bytes). README fetched with `curl --resolve github.com:443:140.82.112.3`; TLS verification remained enabled. | `docker pull zricethezav/gitleaks:v8.30.1@sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f` -> success; `docker image inspect` -> digest confirmed, 76,584,831 bytes. Full history and working-tree scans with `.gitleaks.toml` -> no leaks; A1-6 negative controls -> exactly 2 expected detections, exit 1. |

### S3-compatible object store

`artifacts` is **NOT_PINNED** and is omitted from Compose and `full`; the artifact-store choice moves to P3 per Amendment A1-1. The [MinIO OSS repository](https://github.com/minio/minio) says it is no longer maintained. Its maintained [AIStor container](https://docs.min.io/aistor/installation/container/install/) requires a license file and vendor terms; the owner directed that no license be requested. No object-store image is pulled.

## GitHub Actions

| Action | Version comment | Full commit SHA | Official source / local resolution |
|---|---|---|---|
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` | Resolved by `git -c http.curloptResolve=github.com:443:140.82.112.3 -c http.sslVerify=true ls-remote --tags https://github.com/actions/checkout.git 'refs/tags/v7.0.1*'`; exact tag is lightweight. TLS verification on; per-command override only. |
| `astral-sh/setup-uv` | `v10.3.3` | `68559e99cc807c1eb7e9238fd43a15bba460eec2` | Resolved by `git -c http.curloptResolve=github.com:443:140.82.112.3 -c http.sslVerify=true ls-remote --tags https://github.com/astral-sh/setup-uv.git 'refs/tags/v10.3.3*'`; exact tag is lightweight. TLS verification on; per-command override only. |

Amendment A1-4 records the environment limitation: normal routing to GitHub timed out, while the owner-approved per-command override to GitHub address `140.82.112.3` succeeded. No global Git config, hosts file, DNS, proxy, or Docker Desktop setting was changed.

## License

Canonical Apache-2.0 text fetched from `https://www.apache.org/licenses/LICENSE-2.0.txt` unchanged. `LICENSE` SHA-256 is `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` (11,358 bytes).

## Verification status

`uv.lock` and full sync pin dbt-core 1.11.17 and mypy 1.19.1 under A1-5; Step 1.5 passes. The initial unconfigured Gitleaks finding in `PACK_MANIFEST.json` was reviewed by the advisor as a false positive: its 64-hex value equals the SHA-256 of `harness/TOKEN_RISK_MATRIX.md`. A1-6 adds the exact one-path/one-shape allowlist without editing the manifest or history. Configured full-history and working-tree scans report no leaks; the two configured negative controls detect the non-hex manifest token and the digest under `api_token` elsewhere (2 findings, exit 1). Step 1.7 passes; the five Meterproof services used ~2.20 GiB by the sum of rounded `docker stats` values on a 7.61 GiB Docker allocation. An unrelated `dataforge-postgres` container was excluded. Global `docker system df` totals were unchanged before/after teardown. The in-container Maven image reports Temurin 17.0.21. The clean no-hardlinks checkout passed offline sync, all Python checks, all Compose config profiles and db migration smoke; its temporary clone and venv were deleted. The full-lab measurement excludes an object-store service because `artifacts` is NOT_PINNED and deferred to P3.
