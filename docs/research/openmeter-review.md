# openmeterio/openmeter review

Studied: https://github.com/openmeterio/openmeter/tree/55759ef876f6326d57550ca982f8ac131a9d13ff @ `55759ef876f6326d57550ca982f8ac131a9d13ff`, 2026-11-19; license confirmed: Apache-2.0; maintenance: active (HEAD commit dated 2026-11-19).
Feeds: P0.2 → event identity and dedup scope for D2/D4.

| Component studied | Lesson | Decision for METERPROOF | Trade-off | Test that proves it |
|---|---|---|---|---|
| `docs/event-ingestion.md` Event Deduplication; `docs/architecture.md`; `app/config/dedupe.go`; `openmeter/dedupe/{dedupe,memorydedupe,redisdedupe}` | CloudEvents identify a distinct event by `(source, id)`. The ingestion guide says 32-day dedup; architecture and config show dedup is optional and defaults off, with memory or Redis drivers. The code key includes namespace, source, and id; Redis expiry is configurable. | Keep METERPROOF `source_event_id` distinct from transport delivery coordinates; scope it by `(tenant_id, source)` and preserve it across redelivery. Do not rely on a cache TTL as durable evidence identity or claim OpenMeter's 32-day behavior as universal. | Durable outbox identity and database uniqueness add persistence work; they avoid a process-local/LRU or configurable Redis window becoming the evidence ledger. | P0.2 F3 asserts a repeated delivery with the same `source_event_id` is counted once; T01 later verifies raw redelivery and one canonical side effect. |

Not adopted and why: no dependency or implementation code. OpenMeter's optional in-process/Redis dedup is operational duplicate suppression, not METERPROOF's immutable source receipt or transport audit. The docs' 32-day statement is qualified by the current code's disabled-by-default configuration; effective deployment configuration matters.

Attribution / license obligations: No code copied. Apache-2.0 source was studied only; no dependency added.
