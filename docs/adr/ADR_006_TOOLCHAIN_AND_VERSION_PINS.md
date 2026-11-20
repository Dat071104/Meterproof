# ADR-006 — Local toolchain, immutable image pins and reproducible CI

## Status

Proposed — implementation evidence incomplete; owner accepts at G0.

## Context

P0.4 must give a clean checkout a repeatable offline baseline while preserving the independent Core path and avoiding cloud/provider cost. The host exposes Python 3.14.4 and an Oracle Java 23 shim that hangs; the Docker Desktop engine has 20 CPUs and about 7.61 GiB allocated. Flink/Kafka connector releases do not move in lockstep, and dbt compatibility must be read from current package metadata. Risks RISK-0001 through RISK-0004 cover these toolchain, connector, Python and local-resource issues.

## Decision

**Proposed:** pin the project to Python 3.13 with `uv` and a committed `uv.lock`; keep the required WAVE-01 test packages exact, and resolve the remaining packages as recorded at lock time. Per owner-delegated Amendment 01 A1-2, constrain dbt-core to `>=1.11.17,<1.12` and use the latest stable 1.11.x dbt-postgres adapter so no package fetches code at build or install time from outside its hashed artifacts. Use JDK 17 only inside the pinned Maven/Flink containers. Pin each official image as `name:tag@sha256:digest`. Use the newest Flink/Kafka connector combination that has an officially released compatible connector and an official Java 17 image, plus a Kafka version compatible with Debezium and the Flink client. Keep Docker services local-only with bounded, measured profile runs. Source URLs, checked date, metadata, digests, sizes and verification commands are recorded in `docs/architecture/TOOLCHAIN_PINS.md`.

PyPI metadata lists Python 3.13 for dbt-core 1.11.17 and dbt-postgres 1.11.0; `uv sync --locked --all-groups` completes with the amended dbt pin. Latest stable dbt-core 1.12.7 is rejected because its experimental parser sdist fetches a binary from GitHub during build. Per Amendment A1-5, mypy 1.19.1 is pinned as the newest release resolving in the single lock: dbt-core 1.11.17 requires `pathspec<0.13`; mypy 2.4.1 (and the 1.20.x/2.x line) requires `pathspec>=1.0.0`. This resolves the D8 constraint; reopen if dbt-core moves to a line allowing `pathspec>=1.0`. Flink 2.3 is not selected because its official Kafka connector is not released yet; Flink 2.2.1 with `flink-connector-kafka:5.0.0-2.2` is the newest evidenced pair. The selected Kafka broker and Debezium Connect versions are recorded in the pin manifest; any compatibility inference is labelled and must pass the local `cdc` smoke.

Per Amendment 01 A1-1, the artifacts profile is `NOT_PINNED`, omitted from Compose and `full`, and the artifact-store choice moves to P3. MinIO OSS is unmaintained; AIStor is the maintained official successor but requires a license and vendor terms, which the owner directed us not to request or accept in this wave.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Compatibility evidence | 35 | Runtime and connector versions must have primary-source support. | 1 | 5 | 3 | 3 |
| Reproducibility and offline checkout | 30 | A clean checkout must recover the same toolchain without network access. | 1 | 5 | 2 | 3 |
| Host isolation and secret boundary | 20 | The host JDK/Python and public repo must not become hidden dependencies. | 1 | 5 | 4 | 1 |
| Local resource and operating cost | 15 | One owner must run the lab within the existing Docker allocation. | 5 | 3 | 3 | 4 |
| **Weighted total / 5** | **100** |  | **1.60** | **4.70** | **2.90** | **2.75** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | Leave versions floating and use host tools | No setup work | Host JDK 23/Python 3.14 drift; resolution and images change between checkouts | Low | Two-way, but evidence cannot be reproduced | This fails when a later checkout silently resolves a different adapter or cannot run Flink | S | Baseline clean-checkout test would be unstable |
| A | W2-D8 pins (as amended), Python 3.13 via uv, containerized JDK 17, official images pinned by digest | Most reproducible and isolates host dependencies; source-backed compatibility and offline lock | More metadata to maintain; local lab may exceed the measured Docker allocation; artifact-store choice deferred to P3 | Medium | Two-way before P0.4 acceptance; new pins require lock, smoke and ADR review | This fails if the lock no longer resolves or image digests are not available offline | M | `uv sync --locked`, offline clean clone, per-profile smoke, migration/negative controls |
| B | Pin packages and image tags, but omit image digests and offline clean-clone validation | Lower setup work while keeping readable versions | Tags can move and a fresh checkout may fetch different bytes; weaker evidence chain | Low | Two-way until reports depend on those image versions | This fails when a tag moves after the receipt is written | M | Repeat image pulls later and compare resolved digests |
| C | Pin packages and digests, but install/use JDK 17 on the host | Avoids a Maven JDK image | Adds a host toolchain requirement and can diverge from CI/clean checkout | Medium | Two-way before users depend on host setup | This fails when a developer's PATH selects the Java 23 shim or a different JDK | M | Host diagnosis plus environment-specific build checks |

## Consequences

- The P0.4 baseline is local-only. A passing local smoke does not prove a CDC connector, replication slot, Flink job, sink guarantee or G0 signature.
- `uv.lock`, `.python-version`, CI and the runbook must use the same project toolchain and plugin-autoload settings.
- The full lab excludes an object store and measured approximately 2.20 GiB across the five Meterproof containers using the sum of rounded `docker stats` values, under the current 20-CPU / 7.61-GiB Docker allocation. An unrelated `dataforge-postgres` container was excluded. Global `docker system df` totals were unchanged before/after teardown; Docker Desktop settings were not changed.
- The artifacts profile is `NOT_PINNED`; the full-lab footprint will exclude an object store, and the choice moves to P3.
- Gitleaks uses the owner-authorized maintainer image `zricethezav/gitleaks` pinned by the Docker Hub manifest digest, per Amendment A1-3. The Gitleaks README confirms both Docker Hub and GHCR images.
- Per Amendment A1-6, `.gitleaks.toml` extends the default rules and allows only a 64-character lowercase hex value under the exact `ai-agent-workspace-pack/PACK_MANIFEST.json` path. It does not disable a rule or allow other paths. The advisor-reviewed manifest digest false positive is cleared; full-history and working-tree scans report no leaks, and controls prove a non-hex manifest value plus a digest under `api_token` elsewhere are still detected.
- GitHub Actions are pinned to full SHAs resolved by `git ls-remote` through the Amendment A1-4 per-command address override, with TLS verification enabled; no global networking configuration changed.

## Failure modes → evidence that will test them

- Python/dbt/adapter resolution conflicts or changes at a clean checkout → locked uv sync and offline clean-clone run.
- JDK/connector/runtime mismatch → official compatibility source, digest-pinned images and the in-container Java/Flink version checks.
- Docker resource exhaustion or retained WAL → profile health checks, full-run memory/disk measurement, slot-retention settings and teardown proof.
- Broken secret scan wiring → synthetic-token negative control and full-history scan.
- Migration failure leaves partial schema state → invalid 0002 negative control verifies transaction rollback and revision remains 0001.

## Invariants

Preserve independent SQL/dbt and Flink implementations, the test-only Python oracle, source-consistent comparison, local-only data, no paid/cloud calls, least privilege and honest evidence boundaries. Keep INV-01 through INV-12 intact.

## Reopen conditions

Reopen if the dbt-core 1.11 pin conflicts with another required tool, the selected Kafka connector is not officially compatible with the pinned Flink image, a digest is unavailable, a Gitleaks finding appears outside the A1-6 exception, the offline clone cannot reproduce the baseline, or the full profile exceeds the measured host allocation. Reconsider the artifact-store choice at P3. A changed runtime/version requires updated source evidence, lock and smoke receipts before acceptance. See `docs/ops/prompts/WAVE-02_AMENDMENT-01.md` for the owner-delegated overrides A1-1..A1-6.
