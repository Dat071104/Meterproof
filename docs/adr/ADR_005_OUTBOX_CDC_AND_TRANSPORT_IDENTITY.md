# ADR-005 — Transactional outbox, CDC routing and transport identity

## Status

Proposed — review-ready; owner accepts at G0.

## Context

Core's dual processing path requires committed source events to reach Debezium/Kafka/Flink while the SQL/dbt candidate uses the same frozen source population. App, provider and invoice observations have separate authority and some invoice rows have no `logical_request_id`. A transport offset identifies one Kafka delivery, not the source event. The source-cut protocol requires the snapshot/stream handoff and each external scope to be proven rather than inferred from a lag or checkpoint display.

The pinned Debezium `outbox/` example shows a business write emitting outbox events within a transactional service method, the Outbox Event Router publishing an aggregate-routed topic, and a consumer event-ID log checked in the same receiver transaction before manual ACK. Its `test.yaml` demonstrates connector startup and event flow but uses a fixed snapshot wait and does not stop/restart the connector; it is a wiring example, not a recovery proof. See `docs/research/debezium-outbox-review.md`.

## Decision

**Proposed:** keep one transactional `outbox_events` row in the same PostgreSQL transaction as each persisted app/provider/invoice observation, and capture the allowlisted outbox table with the Debezium PostgreSQL connector and Outbox Event Router. This preserves the existing architecture's PostgreSQL WAL → Debezium → Kafka → Flink topology. Router/connector configuration and the exact schema version remain implementation work for P2.2/P4.1 and P0.4 compatibility pins.

### Topic and key design

| Source | Topic (proposed) | Kafka key / partition grouping | Durable event identity carried |
|---|---|---|---|
| APP | `meterproof.app.events.v1` | `(tenant_id, logical_request_id)` to keep a request's actual attempts together | `source_event_id`; `provider_attempt_id` is a separate attempt identity |
| PROVIDER | `meterproof.provider.observations.v1` | `(tenant_id, source_event_id)` for transport partitioning; the manifest-scoped provider/account plus `provider_generation_id` is the later spend-dedup key | `source_event_id`; the optional linked `provider_attempt_id`/`logical_request_id` remain payload fields |
| INVOICE | `meterproof.invoice.observations.v1` | `(tenant_id, billing_period_id, source_event_id)`; do not require `logical_request_id` | `source_event_id`; `source_reference` remains the invoice-row reference |

These keys group messages for processing; they do not replace `source_event_id`. The outbox row ID is stable across redelivery and unique per `(tenant_id, source)`. A duplicate event may be written to a new Kafka offset. Provider spend aggregation deduplicates by the declared provider/account scope plus generation ID; transport-level canonical effects deduplicate on the stable source event identity and records each `transport_delivery_id` separately as `(topic, partition, offset)` in raw-delivery audit. The manifest stores the Kafka high-watermark vector; `transport_delivery_id` is not added to `source_receipt.v1`.

### Consumer idempotency and restart

The receiver uses an inbox/consumed-event record keyed by `(tenant_id, source_event_id)` and commits that record with the canonical side effect before acknowledging Kafka. A duplicate delivery still produces a raw-delivery audit record but does not repeat the canonical effect. If the receiver crashes after its sink commit and before ACK, replay is expected and the idempotency boundary must suppress a second effect. The Debezium example illustrates the pattern; it does not prove METERPROOF's transaction boundary or external-sink behavior.

### Snapshot-to-stream handoff and WAL lifecycle

- Seal the application/outbox population at a documented consistent snapshot/high-watermark, retaining source-event IDs, snapshot reference, LSN and hashes. Pin provider and invoice scopes separately; an LSN does not cover them.
- Record Debezium snapshot metadata and the stream handoff position. Prove that the Kafka source-event set covers the committed outbox events through that cut, tolerate duplicate boundary deliveries by source-event id, and store per-partition offsets. The F1 contract fixture alone has no real LSN/vector and does not prove this handoff.
- Flink consumes through the manifest offset vector, applies the declared correction/finalization policy, then records a completed checkpoint and sink commit receipt. Without those artifacts, the comparison is NOT_COMPARABLE/BLOCKED.
- Use a dedicated logical replication slot. Monitor retained WAL/slot lag and disk against an owner-approved threshold; a stalled consumer can retain WAL. If a slot becomes invalid or required WAL is gone, stop that cut and create a new manifest/snapshot rather than stitching a missing range. Retire the slot only after connector decommission and an explicit cleanup check.

These are planned lifecycle controls, not evidence that Debezium or the sink has delivered an end-to-end guarantee. Recovery and retention behavior must be exercised in the authorized P2.2/P4.1 lab.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Atomic source write and event capture | 30 | Committed evidence must not be detached from its event. | 1 | 5 | 3 | 2 |
| Stable event identity and duplicate handling | 25 | Redelivery must not create a second business effect. | 1 | 5 | 3 | 2 |
| Snapshot/recovery/source-cut evidence | 20 | The two engines need the same committed population. | 1 | 4 | 3 | 2 |
| Data minimization and source isolation | 15 | CDC must not expose unrelated rows or tenant data. | 4 | 4 | 2 | 4 |
| Operational simplicity | 10 | Connector/slot costs must remain bounded and observable. | 5 | 3 | 3 | 3 |
| **Weighted total / 5** | **100** |  | **1.85** | **4.45** | **2.95** | **2.40** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | No CDC; run only the batch path | Lowest infrastructure burden | Not an allowed Core option: removes the required real Debezium/Kafka/Flink comparison and T01/T03 path | Low | Two-way as a prototype choice, but cannot satisfy Core scope | This fails when batch-only output is presented as independent stream verification | S | Structural check shows the required CDC path is absent |
| A | Transactional outbox plus Debezium Outbox Event Router | Atomic write/event intent, semantic event envelope, routing and stable event ID | Requires outbox schema, connector/slot operations and explicit consumer dedup | High | Two-way before published contracts; changes later require schema evolution and a new cut | This fails when a duplicate delivery is mistaken for a new source event or slot lag exhausts disk | L | P2.2/P4.1 real connector, T01/T03/T10 and source-cut receipt |
| B | Capture receipt tables directly with Debezium | Reuses persisted receipt tables and WAL | Couples topic schema to internal table evolution; can expose unrelated columns or updates; lacks a dedicated event envelope unless added | Medium | Two-way before consumers depend on table-shaped topics; later migrations are harder | This fails when a routine receipt-table change silently changes downstream event semantics | L | CDC schema-evolution, allowlist and T01/T03 tests |
| C | Publish to Kafka from the application after committing receipts | Direct control over event payload and key | A post-commit publish can be lost; reliable retries require a durable outbox/publisher and idempotent sink, while still not satisfying the Debezium path by itself | Medium | Two-way before topic consumers exist; dual-publish migration is costly | This fails when the process exits after DB commit but before publish | M | Kill between DB commit and publish; prove recovery from durable event state |

## Consequences

- Source identity and transport coordinates remain separate through the manifest and raw-delivery audit.
- Invoice records can be routed and reconciled without a logical request ID.
- Outbox tables, topic contracts and slot lifecycle are planned; none is implemented by this ADR.
- The full Core path remains required. A local fixture or diagram cannot be described as CDC recovery evidence.

## Failure modes → T-IDs that will prove them

- Duplicate CDC delivery repeats a side effect → T01.
- Crash after sink commit and before ACK repeats work → T03.
- Late/out-of-order events cross finalization → T04.
- Missing provider ID is mistaken for zero spend → T08.
- Replaying a frozen manifest changes the digest → T10.

## Invariants

INV-01, INV-04, INV-06, INV-07 and INV-08; SOURCE_CUT_PROTOCOL §§2–8 and §§9–12; transport coordinates never replace source/business identity.

## Reopen conditions

Reopen if a real P2.2/P4.1 lab shows the chosen router cannot preserve source IDs, the snapshot/stream handoff cannot be tied to the same committed event set, WAL retention exceeds the measured cap, or a direct-table/app-publisher alternative proves safer while preserving the mandatory independent Debezium/Kafka/Flink path. Owner accepts this ADR at G0; do not change implemented topic/identity semantics without a new ADR and migration/rollback plan.
