# METERPROOF

Failure-aware data reconciliation for AI usage, provider spend and customer charges, with independent batch/stream verification, deterministic replay and evidence-backed release gates.

> **Status:** architecture and execution contract only (v3.4). No implementation milestone has passed yet. Every claim in this repository is backed by an executed gate receipt in [`docs/gates/`](docs/gates/) or it is not claimed.

## What it is

METERPROOF verifies AI-app usage and billing from three evidence sources (owner application, provider generation records, invoice/export) through two independently implemented paths:

- **SQL/dbt batch** reference on PostgreSQL
- **PostgreSQL WAL → Debezium → Kafka → Flink (Java)** streaming shadow

Both are compared on a **source-consistent cut** against an **independent pure-Python oracle**. A result is `VERIFIED` only inside an explicitly covered scope; missing or unattributable evidence yields `INCOMPLETE` or `UNDETERMINED`, never a silent zero. Reports are immutable and published through a CAS-fenced pointer.

## Products

| Track | Milestones | Scope |
|---|---|---|
| Core | P0–P7 | Evidence model, durable ingestion, temporal replay, CDC/Flink shadow, differential verifier, fault lab T01–T12, MP-004 incident |
| Lite | L0–L3 | Local-first CLI/SDK/GitHub Action over the same contracts, no cluster required |
| Atlas | A0–A5 | Read-only governed analytics and evidence-grounded AI incident analyst |
| Adoption | U0–U2 | Problem validation, onboarding, repeat-usage evidence |

## Start here

- Project authority and reading order: [`docs/METERPROOF_START_HERE.md`](docs/METERPROOF_START_HERE.md)
- Current status and resume point: [`docs/ops/PROJECT_STATUS.md`](docs/ops/PROJECT_STATUS.md)
- Architecture: [`docs/architecture/ARCHITECTURE_DECISIONS.md`](docs/architecture/ARCHITECTURE_DECISIONS.md)
- Milestones and gates: [`docs/milestones/MILESTONE_INDEX.md`](docs/milestones/MILESTONE_INDEX.md)
- How the AI advisor/executor workflow runs: [`docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`](docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md)

## License

Not yet selected; see the P0 decision log. Third-party components keep their own licenses.
