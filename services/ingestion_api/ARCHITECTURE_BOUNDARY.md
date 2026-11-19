# services/ingestion_api — module boundary (PLANNED, NOT IMPLEMENTED)

**Milestone:** P2 · **Ownership:** Private authenticated receipt ingestion.

**Non-negotiable:** May write Postgres intents/attempts/source receipts and transactional outbox only. Derive tenant from auth; validate source and immutable event IDs; never accept management secrets from pilot users.

**Verification responsibility:** tests/contracts + tests/integration + T01/T12.

This marker preserves a clean intended repository structure for Codex. It is not a claim that code, runtime or tests already exist. Follow the active milestone and inspect actual existing project source before adding implementation.
