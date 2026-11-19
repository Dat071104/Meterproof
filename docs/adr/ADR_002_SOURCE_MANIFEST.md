# ADR-002 — Immutable source-consistent manifest across async sources

**Status:** Proposed for G0. **Decision:** seal source-aware manifest containing app/outbox frozen snapshot/LSN, Kafka offsets, completed Flink checkpoint/sink receipts, bounded external provider and invoice snapshots/unknown exclusions. **Reason:** comparing two runs from different populations is invalid, and PG LSN cannot prove provider completeness. **Tradeoff:** finalization can be delayed or NOT_COMPARABLE. **Tests:** T04/T08/T10 + wrong-cut negative control.
