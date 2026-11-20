# Project Context Card / The ngu canh du an

## Project Name

`METERPROOF` (contract revision v3.4)

## One-Paragraph Summary

English: Failure-aware, evidence-aware verification of AI-app usage, provider spend and customer charges. Three evidence sources (owner app, provider generation records, invoice/export) are processed by two independent engines (SQL/dbt batch; PostgreSQL WAL → Debezium → Kafka → Flink Java shadow), compared on a source-consistent cut against an independent pure-Python oracle, and published as immutable, CAS-fenced report versions. Extensions: Lite (local CLI/SDK/GitHub Action), Atlas (read-only analytics + grounded AI analyst), Adoption (real user evidence). Portfolio target: middle-level data engineering rigor proven by executed evidence.

Vietnamese: Kiem chung usage AI, chi phi provider va tien tinh khach hang tu 3 nguon bang chung, qua 2 engine doc lap (SQL/dbt va CDC→Kafka→Flink) cong voi oracle Python doc lap; ket qua chi VERIFIED trong pham vi co du bang chung; bao cao bat bien, publish bang CAS.

## Current Phase / State

P0 / G0 remains `IN_PROGRESS`. WAVE-01 fix-up Checkpoint 0 passes; P0.2/P0.3 receipts await advisor re-review. ADR-001–005 remain Proposed. Amendment 01 A1-5 pins mypy 1.19.1 compatible with dbt-core 1.11.17 in the single lock; Step 1.5 passes. A1-6 clears the advisor-reviewed PACK_MANIFEST SHA-256 false positive with an exact path-and-shape allowlist; configured history/working-tree scans pass and both negative controls detect their expected findings. Step 1.7 full profile passed with ~2.20 GiB across five Meterproof containers; in-container Java 17.0.21 verified. The first Step 1.13 clone failed hygiene on tracked `.env.example`; the owner authorized an exact-path exception in the pack helper (DEC-0012), now covered by regression tests. Repeat the clean offline checkout before Checkpoint 1. P0.4 and G0 are not signed; no product implementation exists. Authoritative status: `docs/ops/PROJECT_STATUS.md`.

## Tech Stack

- Language: Python 3.13 (`uv`, dbt-core 1.11.17 / dbt-postgres 1.11.0, mypy 1.19.1); Java for Flink (JDK 17 toolchain; host JDK 23 is not supported by Flink), SQL
- Framework: FastAPI + Pydantic + Alembic; dbt Core; Flink DataStream; Debezium/Kafka Connect
- Runtime: Docker Compose local lab (host Docker 29.9.3, Windows 11)
- Database: PostgreSQL (logical WAL, ≥14), Kafka; DuckDB/SQLite for Lite
- Test tools: pytest, dbt tests, Testcontainers where justified, fault drills T01–T12

## Architecture

Write plane → dual processing (SQL/dbt, Flink) → verification plane (comparator + oracle + coverage) → immutable reports + CAS pointer → read-only API (Core UI, Atlas). Lite is local and separate. Canonical: `docs/architecture/ARCHITECTURE_DECISIONS.md`, `docs/architecture/SOURCE_CUT_PROTOCOL.md`, `docs/architecture/REPOSITORY_STRUCTURE.md`.

## Business Rules & Acceptance Criteria

Canonical: `docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md` (INV-01..INV-12), `docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md` (T01–T12, MP-004).

- Rule: provider spend sums attempts, not logical requests -> Accept when: F1 fixture yields 2 charged attempts, 1 billable request.
- Rule: timeout without generation ID is unknown -> Accept when: F2 is never VERIFIED and never zero-cost.
- Rule: SQL vs Flink compared only on equal source cut -> Accept when: unequal cut yields NOT_COMPARABLE, not MISMATCH.
- Decision axes (DEC-0008): only EQUAL permits VERIFIED or MISMATCH; DIFFERENT, NOT_COMPARABLE and ERROR permit only INCOMPLETE or UNDETERMINED, and a DIFFERENT candidate requires a failure slice.
- Rule: stale publisher never wins -> Accept when: T09 concurrent CAS test blocks the stale writer.

## Key Decisions

- DEC-0001 repo layout (repo at `Meterproof/`, source pack kept outside); DEC-0002 advisor/executor split; DEC-0003 just-in-time OSS study; DEC-0004 validator status rule; DEC-0007 overlay installer retired after first import. See `DECISION_LOG.md`.

## Current Branch / Commit

- Branch: `p0/wave-02-p0.4-g0`; latest commit `31eb5cd` (Apache-2.0 license commit); remaining P0.4 artifacts are uncommitted while the W2-D8 conflict awaits direction.
- WAVE-01 evidence base: Commit A2 `231d9d72e1ed8c5e6879d00b061c21c1bb1c770c`; Commit C `2c935d6f1f215e125143e9a3f65c4e2426bace63`; Commit D `a75fdba4bf956d6ea601df1e284829d6a74fc951`.

## How to Run

```bash
python tools/meterproof/validate_overlay.py
python ai-agent-workspace-pack/_agent_ops/tools/session_start.py --root .
```

## How to Test

```bash
python tools/meterproof/validate_overlay.py   # structural only; no product tests exist yet
```

## Known Risks

See `RISK_REGISTER.md` (toolchain/mypy compatibility, Docker memory, G1 provider correlation, scope size, public repo hygiene, licensing).

## Next Step

Rerun Step 1.13 on a fresh clone after committing DEC-0012's exact-path exception and regression test. Step 2 and `/meterproof-advisor review WAVE-02` remain downstream of that checkpoint.

## Do Not Do

- Mark any gate/test PASS without executed evidence; edit pack-managed files; push/merge as an agent; paid API or cloud calls without an approved cap; share one transformation reducer between SQL, Flink and the oracle.

## Last Verified Commit

`31eb5cd — latest committed baseline. P0.4 Steps 1.5–1.9 evidence is recorded in docs/gates/G0/P0.4_receipt.md; remaining worktree changes are uncommitted.`

## Last Updated

`2026-11-20`
