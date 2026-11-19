# Project Context Card / The ngu canh du an

## Project Name

`METERPROOF` (contract revision v3.4)

## One-Paragraph Summary

English: Failure-aware, evidence-aware verification of AI-app usage, provider spend and customer charges. Three evidence sources (owner app, provider generation records, invoice/export) are processed by two independent engines (SQL/dbt batch; PostgreSQL WAL → Debezium → Kafka → Flink Java shadow), compared on a source-consistent cut against an independent pure-Python oracle, and published as immutable, CAS-fenced report versions. Extensions: Lite (local CLI/SDK/GitHub Action), Atlas (read-only analytics + grounded AI analyst), Adoption (real user evidence). Portfolio target: middle-level data engineering rigor proven by executed evidence.

Vietnamese: Kiem chung usage AI, chi phi provider va tien tinh khach hang tu 3 nguon bang chung, qua 2 engine doc lap (SQL/dbt va CDC→Kafka→Flink) cong voi oracle Python doc lap; ket qua chi VERIFIED trong pham vi co du bang chung; bao cao bat bien, publish bang CAS.

## Current Phase / State

P0 / G0 `NOT_STARTED`. Repository bootstrapped 2026-11-19 (pack + overlay installed, advisor additions). Work order `docs/ops/prompts/P0.1_CODEX.md` issued, not executed. Authoritative status: `docs/ops/PROJECT_STATUS.md`.

## Tech Stack

- Language: Python (project pin decided in P0.4; host has 3.14), Java for Flink (JDK 17 toolchain; host JDK 23 is not supported by Flink), SQL
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
- Rule: stale publisher never wins -> Accept when: T09 concurrent CAS test blocks the stale writer.

## Key Decisions

- DEC-0001 repo layout (repo at `Meterproof/`, source pack kept outside); DEC-0002 advisor/executor split; DEC-0003 just-in-time OSS study; DEC-0004 validator status rule. See `DECISION_LOG.md`.

## Current Branch / Commit

- Branch: `main`
- Commit: see `git log -1` (setup commit of 2026-11-19)

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

See `RISK_REGISTER.md` (toolchain, Docker memory, G1 provider correlation, scope size, public repo hygiene, license).

## Next Step

Owner pastes `docs/ops/prompts/P0.1_CODEX.md` into Codex; then `/meterproof-advisor review P0.1` in Claude Code.

## Do Not Do

- Mark any gate/test PASS without executed evidence; edit pack-managed files; push/merge as an agent; paid API or cloud calls without an approved cap; share one transformation reducer between SQL, Flink and the oracle.

## Last Verified Commit

`set at setup commit, 2026-11-19`

## Last Updated

`2026-11-19`
