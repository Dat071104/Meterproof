# services/durable_worker — module boundary (PLANNED, NOT IMPLEMENTED)

**Milestone:** P2 · **Ownership:** Durable job leases, retries and DLQ.

**Non-negotiable:** Use persistent queue/leased jobs, bounded retry and idempotent effects; never untracked serverless background threads as the guarantee.

**Verification responsibility:** tests/integration + crash-before-ack.

This marker preserves a clean intended repository structure for Codex. It is not a claim that code, runtime or tests already exist. Follow the active milestone and inspect actual existing project source before adding implementation.
