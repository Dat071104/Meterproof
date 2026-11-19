# Source-consistent cut & differential replay protocol (mandatory)

## Scope definition BEFORE processing
1. Pin `tenant_id`, UTC-normalized `billing_period`, one `currency`, `policy_version`, `schema_version`, correction finalization and event-time/watermark policy.
2. Define **application source set** by transactionally consistent, immutable export of source receipts and outbox rows at a documented database snapshot/high-watermark. Capture LSN and data/materialization checksums **without pretending an LSN covers provider records**.
3. Define **external evidence scope** independently: exact provider generations/IDs retrievable, time range of owner export, unresolved/unlinked attempts, import/extract time and checksum; same for invoice rows. Record exclusions and why.
4. Seal manifest and immutable object references. No mutation of source population between SQL and Flink paths.

## Source materialization / checkpoint handshake
5. SQL/dbt references the frozen manifest/export or a transactionally equivalent source snapshot, not a continuously changing live table. Store model Git SHA, policy version and candidate output digest.
6. CDC snapshot stream must be matched to **the same committed source event identities** at the cut. Persist Kafka `topic-partition-offset` high-watermark vector; ensure source events through the cut were emitted and acknowledged. Do NOT equate simply “Kafka caught up” with provider-side completeness.
7. Flink must consume through the offset vector, finalize event-time/correction windows under declared policy, successfully complete a checkpoint that covers these inputs, and provide sink commit receipts. Persist job artifact digest, checkpoint ID, watermark and sink keys/digests. Catch any unsupported end-to-end guarantee as NOT_COMPARABLE/BLOCKED.
8. Canonicalize stable keys (`tenant_id`, `period`, `logical_request_id` etc.), Decimal strings, ordering, nulls and source provenance. Exclude runtime-generated IDs, ingest/replay timestamps not part of business semantics.

## Decision contract
9. Check manifest equality, source cut overlap, coverage/exclusions, policy V, code versions and finalization first. **If not equivalent, result = NOT_COMPARABLE** (comparison status), not a business `MISMATCH`.
10. Compare independent SQL vs Flink, independent Python hand-reviewed oracle for bounded fixture cases, negative mutants, source counts and reconciled business totals. If both agree but evidence is missing, business verdict remains `INCOMPLETE` or `UNDETERMINED`.
11. Produce row-level or dependency-relevant failure slice, impacted business keys, source links and explicit unknowns. A digest alone is insufficient to diagnose the issue.
12. Only a covered, explicitly checked `VERIFIED` candidate can reach the scoped CAS publication process. Failed or ambiguous cases cannot silently change the public pointer.

## Manifest fields
`run_id`, `tenant_id`, `billing_period_id`, `origin`, `schema_version`, `app_source_snapshot`, `app_snapshot_sha256`, `postgres_snapshot_cut`, `postgres_lsn`, `cdc_snapshot_metadata`, `kafka_offset_vector`, `provider_scope`, `provider_unlinked_attempts`, `invoice_scope`, `source_exclusions`, `price_policy_version`, `sql_git_sha`, `flink_git_sha`, `flink_artifact_sha256`, `oracle_fixture_sha256`, `time_zone`, `money_precision`, `rounding_mode`, `correction_window_policy`, `previous_publication_id`, `created_at`.

**Unsafe shortcuts:** comparing current batch to live stream; comparing totals only; comparing two paths that share the exact same pricing reducer; claiming Flink checkpoint proves sink exactly-once; calling absent provider receipt zero cost; retroactively changing original first_observed_at.
