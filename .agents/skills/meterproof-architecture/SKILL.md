---
name: meterproof-architecture
description: Review or change METERPROOF data architecture, WAL/CDC/Kafka/Flink/dbt contracts, source-cut alignment, replay guarantees, storage schemas and service boundaries. Require real failure semantics and ADRs.
---

# METERPROOF — Architecture Review (DE)

## Trigger
Any change to event ownership/schema, PostgreSQL outbox/WAL, Debezium, Kafka topic keys/retention, Flink keyed state/checkpoints/sink, dbt materialization, immutable manifests, publication boundaries, or Core/Lite/Atlas package layout.

## Read exactly relevant context
Root AGENTS + pack handoff -> `docs/METERPROOF_START_HERE.md` -> `docs/architecture/ARCHITECTURE_DECISIONS.md` + `SOURCE_CUT_PROTOCOL.md` -> active milestone -> affected ADR/contract/test. Generic advisor/build/tester teams continue to handle their normal roles; do not copy their workflow.

## Architecture decision procedure
1. State operational/business problem and which system owns each datum; distinguish app observation, provider evidence and invoice output.
2. Draw data flow with write authority, auth/tenancy, source IDs, time semantics, transaction boundaries, materialization & read surfaces.
3. Compare at least two alternatives on correctness, consistency, recovery, complexity, cost and user access; include reasons for rejection.
4. Model explicit failure path: double delivery, unknown provider outcome, late correction, lost CDC offset, checkpoint/sink gap, concurrent publication and cross-tenant access.
5. Prove source cut: immutable app population + external provider scope/exclusions + Kafka offsets + Flink checkpoint + sink receipt, with honest NOT_COMPARABLE status when proof absent.
6. Protect independent implementation: SQL/dbt and Flink share only contract/spec, NOT the transformation reducer; independent Python oracle test-only.
7. Define instrumentation, runbook, rollback, migration compatibility, security boundaries and *negative* tests before accepting change.
8. Propose ADR + precise changed paths + acceptance gate. Do not turn an architecture document into a claim of tested guarantees.

## Stop conditions
- Unsupported source completeness/exactly-once assertion; unapproved Kafka/cloud rollout; changes that allow Atlas to write Core; missing independent oracle; provider timeout assumed free; transformation shared across SQL/Flink; no reproducible negative test.

## Output format
**Decision:** proposed/blocked; **Before/after graph:** paths and authorities; **Invariants affected:** IDs; **Failure matrix:** trigger→expected→test command; **Cost/security:** risk; **ADR and rollout:** version/migration/rollback; **Gate:** real evidence required.
