# Domain, evidence and business invariants — frozen from v3.1/v3.2/v3.3

## Fundamental identities
- `logical_request_id`: a customer business action; stable across retry.
- `provider_attempt_id`: app-owned outbound request attempt; **new per actual attempt**; may lack provider generation ID.
- `provider_generation_id`: returned provider ID; absent in genuine timeout does **not** prove provider did nothing.
- `source_receipt_id`: one persisted observation from app/provider/invoice.
- `source_event_id`: stable source change/outbox identity; distinct from Kafka delivery ID.
- `billing_period_id`: explicit timezone and half-open period [start,end).
- `tenant_id`: from verified auth in private writes; never trust caller body as identity source.

## Financial quantities
- `known_provider_spend`: sum of distinct confirmed **charged provider attempts** with matched evidence. Unknown attempts are unresolved, NOT zero.
- `billable_units`: policy-versioned, max one **server-confirmed successful logical request** for MVP. Not a client-delivery guarantee.
- `customer_charge`: business pricing policy × billable units, one currency USD, fixed-point/Decimal, declared rounding.
- `invoice_amount`: observed export. For synthetic fixture mark `SYNTHETIC`, not real invoiced customer money.

## State machines
**Provider outcome**: `NOT_DISPATCHED`, `APP_OBSERVED_SUCCESS`, `APP_OBSERVED_FAILURE`, `UNKNOWN_PROVIDER_OUTCOME`, `PROVIDER_CONFIRMED_BILLED`, `PROVIDER_CONFIRMED_NOT_BILLED` (where supported by positive evidence); keep separate app and provider observation facts, no fabricated transitions.

**Business decision**: `VERIFIED` (checked tests pass *only within declared covered scope*), `MISMATCH` (positive evidence of contradiction), `INCOMPLETE` (known mandatory segment missing/pending), `UNDETERMINED` (available evidence cannot disambiguate unknown attribution/coverage). Store exclusion reasons and source references.

**Comparator result**: `EQUAL`, `DIFFERENT`, `NOT_COMPARABLE`, `ERROR`; it is not the business decision. Batch vs stream `EQUAL` + source gaps can result in `UNDETERMINED`.

**Gate state**: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `FAILED`, `PASS`, `HUMAN_GO`, `HUMAN_CONDITIONAL_GO`, `HUMAN_NO_GO`. No PASS without real evidence.

## Invariant registry
- INV-01: stable logical request and distinct provider attempts preserve cardinality across retries.
- INV-02: known confirmed provider spend sums **attempts**, never logical requests.
- INV-03: customer billable logical units use pinned versioned server-success rule (not provider spend).
- INV-04: genuine timeout with no attributable generation = unknown; never infer free/billed from an aggregate.
- INV-05: all money uses Decimal/fixed point, USD, explicit rounding and timezone.
- INV-06: source coverage, observation window, origin, exceptions are mandatory in decisions.
- INV-07: SQL/Flink comparisons require same frozen source scope, policy, correction boundary and finalized sink evidence.
- INV-08: immutable historical observations and published report versions; CAS publication prevents stale overwrite.
- INV-09: oracle independent of production transformation logic, with mutation detection.
- INV-10: tenant isolation, authenticated private writes, sanitized read-only public demo, no leaked management keys.
- INV-11: Lite local audit never claims full Kafka/Flink reliability or complete provider attribution absent evidence.
- INV-12: Atlas LLM read-only/abstain policy; enable/disable cannot change Core report hash/verdict/publication.

## MVP domain boundary retained
One AI provider (start OpenRouter if workable), one owner app, one USD period, provider generation records when retrievable and one controlled billing export. No payment collection, tax, FX or fake invoice claims. Core science remains required even when user-facing mode is small.
