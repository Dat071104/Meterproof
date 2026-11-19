---
name: meterproof-differential-replay
description: Use for METERPROOF immutable source manifests, temporal queries, SQL/dbt versus Flink comparison, source-consistent cut, independent oracle, deterministic replay and safe report publication.
---

# METERPROOF — Differential Replay

## Trigger
Replay, effective/observed time modeling, data cut protocols, CDC to Flink, canonical comparison, independent verification, pricing restatement and publication versioning.

## Invariants
- Share a **written business specification**, but implement SQL/dbt and Flink independently; a small Python fixture oracle must not call production transformation functions.
- Compare only same tenant, period, *source population*, external provider observation scope, code/policy revision, timezone, correction policy and finalized event-time boundary.
- PostgreSQL LSN does not prove coverage of external API generations or invoice records. Declare separate manifest hashes and missing scope.
- Kafka partition offsets, DB/outbox event IDs, sink evidence, Flink checkpoint and event-time close must establish progress through the source cut. One topic's trailing event is not a global barrier.
- A Flink checkpoint is not proof of exactly-once external sink writes; require idempotent sink / transaction + crash-after-commit test.
- Canonicalize rows by stable business keys and Decimal values; exclude execution timestamps, generated run IDs and row ordering when hashing.
- Comparator disposition `NOT_COMPARABLE` (unequal cuts) is distinct from business decision `VERIFIED|MISMATCH|INCOMPLETE|UNDETERMINED`.
- Candidate publication must be atomic/CAS-fenced, retain historical report versions, and fail closed on uncertainty.

## Workflow
1. Write a replay manifest with source IDs, SHA256, offsets/LSN, provider scope, exclusions, policy SHA, code SHA, timezone and cutoff.
2. Verify a frozen input population; pin external observations independently.
3. Run SQL and Flink independently, waiting for documented source-cut coverage and completed stable-finalization checkpoint.
4. Compare row-level and aggregate canonical outcomes; apply independent oracle fixtures.
5. Inject semantic mutants into each implementation to prove comparator catches differences.
6. Re-run identical manifest >=3 times, check deterministic digest and store actual receipts.
7. Test new report version and stale-writer rejection, never overwrite old report data.

## STOP and output
Stop if cuts, schemas, evidence scopes, cutoffs, watermarks or policies cannot be aligned; report `NOT_COMPARABLE`, not false mismatch/success. Output manifest ID, scope, comparison decision, row diffs, oracle, hashes, tests and limitations.
