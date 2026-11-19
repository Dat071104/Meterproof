# Technology stack — purpose, alternatives and constraints

| Layer | Primary | Why | Guarantee/constraint to verify |
|---|---|---|---|
| Runtime & API | Python 3.x, FastAPI, Pydantic, Alembic | typed private ingestion and versioned read API | auth-derived tenant + idempotent transaction |
| Operational/event DB | PostgreSQL + logical WAL | ACID receipt+outbox, versioned evidence | durable source cut; WAL slot lifecycle |
| CDC | Debezium PostgreSQL connector, Kafka Connect | WAL-backed committed change stream | snapshot→stream continuity; restart receipts |
| Log broker | Apache Kafka | replayable topic partitions and offsets | explicit key/partition ordering scope |
| Stream | Apache Flink Java DataStream | keyed state, checkpoints, event-time, restart recovery | sink guarantees independently proven |
| Batch reference | SQL + dbt Core on PostgreSQL | independent versioned business models and tests | fixed manifest/policy, provenance and schema tests |
| Independent oracle | Pure Python + Decimal | hand-reviewed expected facts and mutation tests | no production transformation imports |
| Replay/artifacts | Parquet/JSONL, SHA256, local MinIO or immutable approved object store | sealed manifest and reproducible evidence | integrity ≠ completeness |
| Orchestration | leased durable worker + bounded job queue | replay retries, dead letter, monitoring | no untracked serverless thread assumption |
| Local dev/tests | Docker Compose, pytest, Testcontainers where appropriate, SQL tests | reproducible complete lab | local, approved resources only |
| Lite local tool | Python CLI + DuckDB/SQLite + JSON/HTML + GitHub Action | one-command audit, no cluster | limited guarantees labelled |
| Atlas/AI | governed marts, pgvector/FTS, LangGraph, typed read tools | evidence-grounded investigator | no write tool, citation/abstention eval |
| Metrics/ops | OpenTelemetry, Prometheus-compatible metrics, structured logs | trace provider→receipt→cut→report | privacy/cost guardrails |
| CI/security | GitHub Actions, schema checks, secret/dependency scan | repeatable PR gates | no false "production ready" claim from scaffold CI |

Do not add Spark/Kubernetes/multi-cloud by default. A Middle DE justification is **semantics, failure handling, reproducibility and tradeoffs**, not raw tool count. Pin tested versions in a technology ADR during P0; this document does not invent a compatibility matrix.
