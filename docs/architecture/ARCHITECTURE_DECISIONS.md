# METERPROOF v3.4 — Reference Architecture and DE Review Contract

## System goal and non-goal
**Goal:** Evidence-aware, failure-aware independent verification of AI app usage, provider spend and customer charges through deterministic, source-consistent batch/stream replay. The product blocks unsupported report restatements and explains *why* a result is or is not trustworthy. The same verification contracts underpin a Lite CLI and an Atlas AI explanation layer.

**Non-goals:** payment processing, generalized invoices, FX/tax, global completeness claims, user-uploaded provider management keys, reimplementing Kafka, generic all-purpose data platform, or positioning an LLM as a source of billing truth. All integrations are versioned, not falsely universal.

## 1. Bounded contexts / authority
| Context | Authoritative for | Not authoritative for | Writes |
|---|---|---|---|
| Owner application | request intent, app-generated attempt IDs, server-observed status | provider ledger, client delivery without ACK | app receipts and outbox (private API) |
| Provider adapter | retrievable generation records, observed charges | total charges of inaccessible/unlinked attempts | immutable provider observations |
| Invoice importer | observed invoice/export bytes and scope | correct charge/business policy | immutable invoice observations |
| Billing specification | deterministic policy version, timezone, USD Decimal rounding | what the provider actually did | versioned policy registry |
| SQL/dbt batch | deterministic reference candidate for pinned manifest | ground truth absent oracle/coverage | isolated SQL candidate tables |
| Flink stream shadow | independently implemented event-time candidate | all-world completeness; public billing writes | isolated shadow sink |
| Oracle and comparator | small hand-reviewed fixtures + like-for-like comparisons | actual provider completeness | verdict/evidence receipts only |
| Publication service | approved immutable report versions and pointer | arbitrary upstream unknowns | report versions + CAS pointer |
| Lite | local user export/fixture audit | real-time Kafka/Flink semantics | local files only |
| Atlas | explain verified published reports | independent financial truth, publication | atlas-only draft/trace/cache |

## 2. Logical architecture: write plane, dual processing, verification plane, read plane

```text
[ONE owner-controlled AI app]                         [Provider GET generation / scoped export]     [Invoice CSV]
  intent --> attempts --> response receipts                 may miss genuinely timed-out attempts         declared scope
        | PRIVATE AUTH INGEST + VALIDATION |                        |                               |
        +----> PostgreSQL append-only observations + transactional outbox <---- normalized observations ----+
                            |                             |
            PUBLIC/PRIMARY BATCH PATH         FROZEN IMMUTABLE EVIDENCE / SOURCE CUT
            durable leased worker            manifest: source IDs, LSN, external snapshots, hashes,
                -> SQL/dbt candidates        pricing V, code SHAs, as-known policy, coverage/exclusions
                            |                             |
                            |                     PostgreSQL logical WAL
                            |                           -> Debezium -> Kafka -> Flink keyed state
                            |                                            -> isolated idempotent shadow sink
                            +-------------------> SOURCE-ALIGNED COMPARATOR <---------------------+
                                                    ^      |
                                         INDEPENDENT PURE PYTHON ORACLE
                                                       |
                                      verification state + negative/control receipts
                                                       |
                                      immutable report versions + CAS publication
                                                       |
                                      VERSIONED, READ-ONLY VERIFIED API
                                      /                          |            \
                              Core incident UI             Lite local?       Atlas analytics + agent
                           (no public uploads)         (separate local)    (read-only, no write auth)
```

**Important**: the Lite CLI is **not deployed inside the main platform**. It imports schema contracts and independently selected local rule/coverage primitives; it cannot rewrite production SQL/Flink models or import the independent oracle into production calculations. Atlas accesses the Core versioned read API, not the Core database writer.

## 3. Data plane topology and boundaries
- **Write path:** Private FastAPI authenticates caller, derives tenant from verified auth, validates schema, persists `request_intent`/`attempt`/`observation` and `outbox_event` in ONE PostgreSQL transaction. On external call retry, a new attempt ID is created for each actual outbound attempt; transport redelivery retains the original `source_event_id`.
- **Durable jobs:** lease + retry/backoff/DLQ (Postgres jobs or suitable managed queue only after approval). Never use untracked FastAPI background threads as the durable processing guarantee.
- **Raw evidence:** append-only, retain original source context, origin, timestamp, schema version, correlation confidence and redaction state. Object exports immutable, SHA256; hashes do not prove external completeness.
- **dbt tiers:** `raw` → `staging` (typed, normalized IDs, source validity) → `intermediate` (attempt-to-logical linkage, price V, coverage) → `facts` (`known_provider_spend`, `billable_units`, `customer_charge`, invoice comparison) → `report candidates`. Model contracts/tests: uniqueness, references, domain enums, monetary precision, no silently excluded unknowns.
- **CDC:** PostgreSQL WAL logical replication → Debezium `pgoutput` → Kafka topics keyed by stable source entity/business partition. Explicit snapshot-to-stream protocol, connector LSN/slot lifecycle, WAL retention and restart semantics. No fake polling labelled CDC.
- **Flink:** Java DataStream keyed by `(tenant_id, logical_request_id)` for billing logic, retained attempt-level events, dedup `source_event_id`, event-time/watermark with defined correction handling and bounded state TTL. Consume CDC of authoritative sources; independently code calculation policy; persist to isolated idempotent sink with checkpoint receipts and fencing. Exactly-once **end-to-end** is not asserted until source, operator and sink guarantees are proven together.
- **Object store/artifacts:** one immutable per-run manifest and canonicalized outputs (JSONL/Parquet); hashes, immutable storage location, policy/config versions, replay environment. Do not store unencrypted secrets or user prompts.
- **Read/analytics:** publish only gate-approved report versions; shadow results not public by default. Analytics layer reads published version IDs and surfaces unknowns/exclusions.

## 4. Storage model and constraints
Proposed operational tables: `request_intents`, `provider_attempts`, `source_receipts`, `provider_observations`, `invoice_imports`, `price_policies`, `outbox_events`, `job_leases`, `source_manifests`, `replay_runs`, `batch_candidates`, `shadow_candidates`, `verification_decisions`, `report_versions`, `publication_pointer`, `audit_log`. Mark all origin labels; append-only where historical evidence. Use per-tenant composite unique keys and FK/row-level security as supported; never trust tenant supplied in request body.

Unique keys must distinguish: `logical_request_id`, `provider_attempt_id`, nullable `provider_generation_id`, `source_receipt_id`, `source_event_id`, transport delivery ID; do NOT collapse retries by logical ID. Mutable current views can be derived from immutable receipt history. DDL changes require migration, backwards-compatibility matrix, rollback and CDC schema-evolution tests.

## 5. Time model: bitemporal practical semantics
- `occurred_at`: effective/event time from source, with provenance and timezone.
- `source_committed_at`: source DB commit if genuinely observable (not invented from receipt).
- `first_observed_at`: when verifier first ingested evidence, immutable even on replay.
- `published_at`: when immutable report version went public.
- Queries: **as-known-at T** (only evidence first observed by T) and **effective-for-period P** (business-valid time + price policy V). Historical correction creates a new observation/version; never rewrite original knowledge timeline.
- Event-time watermark is a *declared finalization policy*, not evidence that all external provider records exist.

## 6. Failure and recovery semantics
- At-least-once delivery at boundaries; canonical side effects idempotent on stable event IDs; retain raw deliveries for audit.
- Crash after sink commit before ack must not double apply. Test with a real process kill and restart, checkpoint receipt, sink transaction metadata and reconciliation check, not a simple mock.
- Out-of-order, duplicates, partial provider metadata, late corrected price, DB WAL gap, Kafka retention, stale manifest, stale publication writer, tenant spoof and Atlas prompt-injection are explicit failure types.
- No silent data deletion or overwrite of a previously published report; CAS pointer protected by version/fencing.

## 7. Dev and production separation
**Local full-stack / evidence lab:** Docker Compose PostgreSQL, Kafka, Kafka Connect/Debezium, Flink JobManager/TaskManager, local object storage, dbt and tests. Must start only when active milestone calls for it; WAL/slots and disk are monitored.

**Public budget-safe demonstration:** private API + PostgreSQL + durable job + SQL reference + immutable approved report read API + sanitized read-only UI. The heavyweight streaming shadow runs for reproducible validation; it is never claimed to run 24/7 in a serverless public runtime without proof and budget approval.

**Lite:** Python package, DuckDB or SQLite for local bounded batch analysis, HTML/JSON report, signed/tagged release artifacts and GitHub Action. Vendor-specific adapters are explicit and test fixture-backed.

**Atlas:** read-only FastAPI tools, governed dbt marts, PostgreSQL FTS+pgvector (when justified by measured retrieval tests), LangGraph typed graph, citation/abstention evals, separate AI cache and metrics. Model/API access cost-capped and explicitly approved.

## 8. Core-dependent change gates
Architecture must pass ADR review before adding infra. Changes to source IDs, business policy, source cuts, pricing, verdict state or publication semantics always rerun T01–T12 and independent oracle. Lite/Atlas PRs must run core non-interference regression (stable pinned hashes/versioned outcomes). A claim about reliability needs corresponding failure-injection receipt and negative test, not diagrams alone.

## 9. Review questions a Middle DE should defend
- Which source is authoritative for each observed field? What does missing generation ID mean?
- How do Kafka partitioning, event-time, late correction and Flink state interact with the business key?
- Precisely how is the SQL source snapshot aligned with Kafka offset vector and completed Flink checkpoint?
- What does the sink guarantee after a crash between commit and ACK? Which artifacts prove it?
- Why does the independent oracle avoid common-mode bugs? How do mutation tests verify the verifier?
- Can a concurrent stale publish overwrite a newer approved version? Show the CAS test.
- How would you measure lag, WAL retention, cost, throughput, p95 and recovery with provenance?
- Why does Lite not need the heavy cluster, and what guarantee is intentionally weaker in Lite?
