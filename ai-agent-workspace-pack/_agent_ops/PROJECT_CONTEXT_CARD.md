# Project Context Card / The ngu canh du an

## Project Name

`METERPROOF` (contract revision v3.4)

## One-Paragraph Summary

English: Failure-aware, evidence-aware verification of AI-app usage, provider spend and customer charges. Three evidence sources (owner app, provider generation records, invoice/export) are processed by two independent engines (SQL/dbt batch; PostgreSQL WAL → Debezium → Kafka → Flink Java shadow), compared on a source-consistent cut against an independent pure-Python oracle, and published as immutable, CAS-fenced report versions. Extensions: Lite (local CLI/SDK/GitHub Action), Atlas (read-only analytics + grounded AI analyst), Adoption (real user evidence). Portfolio target: middle-level data engineering rigor proven by executed evidence.

Vietnamese: Kiem chung usage AI, chi phi provider va tien tinh khach hang tu 3 nguon bang chung, qua 2 engine doc lap (SQL/dbt va CDC→Kafka→Flink) cong voi oracle Python doc lap; ket qua chi VERIFIED trong pham vi co du bang chung; bao cao bat bien, publish bang CAS.

## Current Phase / State

P0 / G0 remains `IN_PROGRESS`. WAVE-01 Step 0 is approved; P0.2/P0.3 received `CHANGES_REQUESTED` and their WAVE-02 FIX1 evidence is complete in the P0.2/P0.3 receipts, awaiting advisor re-review. ADR-001–005 remain Proposed. P0.4 and G0 are not signed; no product implementation exists. Authoritative status: `docs/ops/PROJECT_STATUS.md`.

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
- Decision axes (DEC-0008): only EQUAL permits VERIFIED or MISMATCH; DIFFERENT, NOT_COMPARABLE and ERROR permit only INCOMPLETE or UNDETERMINED, and a DIFFERENT candidate requires a failure slice.
- Rule: stale publisher never wins -> Accept when: T09 concurrent CAS test blocks the stale writer.

## Key Decisions

- DEC-0001 repo layout (repo at `Meterproof/`, source pack kept outside); DEC-0002 advisor/executor split; DEC-0003 just-in-time OSS study; DEC-0004 validator status rule; DEC-0007 overlay installer retired after first import. See `DECISION_LOG.md`.

## Current Branch / Commit

- Branch: `p0/wave-01-p0.2-p0.3` (created from P0.1 Commit B)
- Evidence base: P0.2 commit `5551b243aaed0c81d58aa650ce9e73e5f852ba3b`; P0.1 Commit B `f895e2d680d58257a9cd2f64c5f9cab356d19c1c`; Commit A `95be8bfe4bf5b934e9727784b534f1bbbd181bbb`; original main SHA `2b5f2031c27103fc7f098da6cf073ee3bd547a1a`.

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

After WAVE-02 Step 0 Commit D, create `p0/wave-02-p0.4-g0` and continue P0.4. After the unsigned G0 packet is committed, run `/meterproof-advisor review WAVE-02` in Claude Code.

## Do Not Do

- Mark any gate/test PASS without executed evidence; edit pack-managed files; push/merge as an agent; paid API or cloud calls without an approved cap; share one transformation reducer between SQL, Flink and the oracle.

## Last Verified Commit

`P0.2 contract suite passed 8 tests in Python 3.13.2 on p0/wave-01-p0.2-p0.3; evidence is documented in docs/gates/G0/P0.2_receipt.md.`

## Last Updated

`2026-11-20`
