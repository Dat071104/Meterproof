# Domain Specification v1 — METERPROOF evidence and money contract

**State:** Pre-release draft until P0.2 is approved at G0. These v1 schema files may be edited in place only during P0.2; after approval, any contract change requires a new version file. **Origin of all fixtures below:** `SYNTHETIC`.

## Authority by field

| Field | Authoritative source | Not authoritative for | Unknown handling |
|---|---|---|---|
| `tenant_id` | Server identity from verified authentication | Caller-supplied request body or cross-tenant data | Reject a private write if verified tenant identity is absent; never substitute a payload value. |
| `logical_request_id` | Owner application’s business action identity | Provider charge count or client delivery | Required for APP receipts; may be null for unlinked PROVIDER records and for INVOICE rows. |
| `provider_attempt_id` | Owner application, allocated before each actual outbound attempt | Logical request identity or provider generation identity | Required for APP outcomes after request intent; a missing/unlinked provider record does not imply zero cost. |
| `provider_generation_id` | Provider-issued generation/charge record | App attempt count or invoice completeness | Nullable when the provider ID was not observed; an unknown timeout remains unresolved without a linked provider receipt. |
| `source_event_id` | METERPROOF outbox row for the originating tenant and source | Kafka topic/partition/offset or per-delivery identity | Stable across redelivery; the durable event row is the deduplication identity. |
| `source_receipt_id` | METERPROOF evidence persistence service, one persisted observation | Source event identity or transport delivery | A new persisted observation gets a distinct ID; unique within a tenant. |
| `transport_delivery_id` | Transport metadata, e.g. Kafka topic/partition/offset | Business/source-event identity | Retain in raw-delivery audit and `replay_manifest.kafka_offset_vector`; it is not a `source_receipt.v1` field. |
| `source_kind`, `outcome` | The source-specific observation persisted by METERPROOF | Another source’s conclusion or a derived billing verdict | Any unsupported source/outcome pair is rejected; do not infer a missing observation. |
| `occurred_at` | Source event time with source provenance | Ingestion or first-observed time | Invalid RFC3339 values are rejected; unknown event time is not fabricated. |
| `source_committed_at` | Source database commit time only when genuinely observable | Event time or an inferred receipt time | Nullable; leave unknown when the source cannot provide it. |
| `first_observed_at` | METERPROOF’s first durable observation time | Source event time or a later replay time | Immutable; late evidence remains late relative to a pinned cut. |
| `billing_period_id` | Versioned period registry resolving the opaque ID | A period inferred from event time | INVOICE receipts require an ID; fixtures resolve it to explicit start/end/time zone. |
| `known_provider_cost_usd` and `provider_amount_evidence_id` | Provider-side billed evidence | App response, customer charge, or aggregate-only inference | Required for PROVIDER_CONFIRMED_BILLED; otherwise unknown is not zero. |
| `invoice_amount_usd`, `source_reference` | Imported invoice/export bytes and row reference | Correctness of customer pricing policy | Required on INVOICE receipts; retain observed value exactly. |
| `price_policy_version`, unit price and rounding mode | Versioned METERPROOF billing policy | Provider charges or invoice truth | Missing policy means the calculation scope cannot be VERIFIED. |
| `origin` | Explicit source/fixture classification label | Proof that an external record is complete or authentic | Preserve PRODUCTION, PILOT, SANDBOX and SYNTHETIC as separate scopes. |

## Identity contract

| id | issuer | uniqueness scope | nullable in a receipt | stable across retry/redelivery |
|---|---|---|---|---|
| `logical_request_id` | Owner application | Per tenant | Required for APP; nullable for unlinked PROVIDER and INVOICE records | Yes for retries of the same customer action |
| `provider_attempt_id` | Owner application before dispatch | Per tenant | Null/absent only for REQUEST_INTENT or sources with no app attempt | No across actual retries: each outbound attempt gets a new ID; yes for redelivery of the same attempt observation |
| `provider_generation_id` | Provider | Per provider account | Yes when not observed | Stable for the same provider generation across redelivery; a new actual attempt may produce a different generation ID; maps to at most one attempt |
| `source_event_id` | Transactional outbox writer | Per `(tenant_id, source)` | No for persisted source receipts | Yes across redelivery of that same outbox event |
| `source_receipt_id` | METERPROOF receipt persistence | Per tenant | No for a persisted receipt | No: it identifies one persisted observation; a separately persisted observation receives another ID |
| `tenant_id` | Server, from verified auth | Tenant namespace | No on private persisted records | Yes for the tenant; never trust an unverified caller value |
| `transport_delivery_id` | Transport | `(topic, partition, offset)` for Kafka | Absent from source receipt; present only in raw-delivery/manifest records when applicable | Stable for that transport record, but a replay/redelivery may have different coordinates; never a business key |

A provider generation may be linked to at most one app attempt. The two linked fields on a PROVIDER receipt are either both populated or both null; an unlinked provider record is never attached to a request by timing or aggregate amount.

## Billing period and time (D3)

`billing_period_id` is opaque and resolves to `{start, end, time_zone}`. The interval is half-open: `[start, end)`. All three v1 fixtures resolve `2026-11-01_UTC` to UTC `[2026-11-01T00:00:00Z, 2026-12-01T00:00:00Z)`. `occurred_at` is event/effective time; `first_observed_at` is immutable knowledge time. A source cut includes only receipts first observed at or before its declared `as_known_at` instant.

## Source receipt rules (D4)

| source_kind | allowed outcome and conditional fields |
|---|---|
| APP | Outcomes: `REQUEST_INTENT`, `APP_OBSERVED_SUCCESS`, `APP_OBSERVED_FAILURE`, `UNKNOWN_PROVIDER_OUTCOME`. `logical_request_id` is required. `provider_attempt_id` is required for every listed outcome except `REQUEST_INTENT`. `provider_generation_id` may be an app-observed correlation hint only; `known_provider_cost_usd` and `provider_amount_evidence_id` are absent or null, and `invoice_amount_usd` is absent. |
| PROVIDER | Outcomes: `PROVIDER_CONFIRMED_BILLED`, `PROVIDER_CONFIRMED_NOT_BILLED`; `provider_generation_id` is required. BILLED also requires `known_provider_cost_usd` and `provider_amount_evidence_id`. `provider_attempt_id` and `logical_request_id` are either both linked or both null. `invoice_amount_usd` is absent; NOT_BILLED has `known_provider_cost_usd` absent or null. |
| INVOICE | Outcome: `INVOICE_OBSERVED`; `logical_request_id` may be null. `billing_period_id`, `source_reference`, and `invoice_amount_usd` are required. Provider attempt, generation, cost and provider-amount-evidence fields are null when present; INVOICE receipts carry no provider data. |

No other source-kind/outcome pair is valid. `transport_delivery_id` is deliberately excluded from `source_receipt.v1`.

## Provider outcome observations

The workflow may be `NOT_DISPATCHED` before an outbound attempt. It creates no provider attempt and is not a fabricated receipt outcome. Persist `REQUEST_INTENT` before dispatch where feasible. After a real dispatch, the app may separately observe `APP_OBSERVED_SUCCESS`, `APP_OBSERVED_FAILURE`, or `UNKNOWN_PROVIDER_OUTCOME`; a timeout does not prove that the provider did or did not charge. The provider may later supply an independent `PROVIDER_CONFIRMED_BILLED` or `PROVIDER_CONFIRMED_NOT_BILLED` receipt, linked only by explicit identifiers. These facts are appended separately; no response, provider charge, or non-charge transition is inferred from another source’s silence. A retry is a new `provider_attempt_id` under the same logical request.

## Money and arithmetic (D5)

Every schema field ending in `_usd` is a decimal string matching `^(0|[1-9][0-9]{0,11})(\.[0-9]{1,12})?$`: no sign, exponent, leading-zero integer padding, or more than 12 integer/12 fractional digits. Observed provider and invoice amounts are stored exactly; values outside the declared representation are rejected, never rounded. Arithmetic uses `Decimal`, database `NUMERIC(24,12)`, or `BigDecimal`, never binary float. Only `customer_charge` is rounded, once after totaling `(tenant, billing period, price_policy_version)`, to 0.01 using the policy mode; `demo-v1` uses `ROUND_HALF_EVEN`. Canonical facts digests use 12 fractional digits for provider spend and invoice amounts, and 2 for `customer_charge`.

## demo-v1 policy and expected-fact definitions (D6)

- `billable_units` = number of distinct `logical_request_id` values with at least one `APP_OBSERVED_SUCCESS`; a logical request contributes at most one unit.
- `customer_charge` = `billable_units × unit_price_usd`, with only the final total rounded once as above.
- `known_provider_spend` = sum of costs for distinct `provider_generation_id` values with `PROVIDER_CONFIRMED_BILLED`; it counts provider attempts/generations, never logical requests.
- `invoice_delta` = observed invoice amount minus `customer_charge`. A nonzero delta is a positive contradiction for that scoped comparison.

## Unknowns and attribution (D7)

An `UNKNOWN_PROVIDER_OUTCOME` attempt with no linked provider receipt contributes nothing to the known-spend subtotal, appears in `unresolved_items`, and makes the provider-spend scope `UNDETERMINED`; it is neither zero cost nor VERIFIED. An unlinked billed provider record contributes to an explicitly unattributed known-spend subtotal, is never assigned to a request, and makes that spend scope `UNDETERMINED`. Record the unlinked-billed decision as OPEN-Q-1 for G1/P1.2 owner confirmation.

## Decision, publication and origin rules (D8)

`verification_decision.v1` requires `origin`. `published_eligible: true` requires `business_verdict: VERIFIED` and `comparison_status: EQUAL`. Any `VERIFIED` decision requires `comparison_status: EQUAL` and an explicitly empty `unresolved_items` array. `published_read_report.v1` permits only `business_verdict: VERIFIED`; only a covered and explicitly checked VERIFIED candidate reaches publication. No report implies global provider completeness.

## Comparison status vs business verdict (DEC-0008)

`comparison_status` describes whether the independent candidate computations agree on a comparable source cut. `business_verdict` describes the evidence for the declared business scope. Only `EQUAL` permits `VERIFIED` or `MISMATCH`. `DIFFERENT`, `NOT_COMPARABLE` and `ERROR` permit only `INCOMPLETE` or `UNDETERMINED`; each blocks publication. A `DIFFERENT` candidate requires a failure slice under `SOURCE_CUT_PROTOCOL.md` §11. F1 is `EQUAL` + `MISMATCH`: the candidates are expected to agree on the comparable fixture while its invoice contradicts the policy charge. The MP-004 wrong-rule regression is `DIFFERENT` + `UNDETERMINED`, or `DIFFERENT` + `INCOMPLETE` when a known source segment is missing.

## Verdict truth table by declared scope

| Evidence condition in this scope | Comparison status | Business verdict | Publish eligible | Reason |
|---|---|---|---|---|
| Comparable source cut, declared coverage complete, no unresolved items, and independent results agree | `EQUAL` | `VERIFIED` | May be true | Verification is limited to the declared covered scope. |
| Comparable, complete scope; independent results agree that positive contradictory evidence exists (e.g. invoice differs from policy charge; F1) | `EQUAL` | `MISMATCH` | False | A mismatch is a business conclusion from the agreed computation, not candidate disagreement. |
| Independent candidates disagree on a comparable cut (e.g. MP-004 wrong-rule regression) | `DIFFERENT` | `UNDETERMINED`, or `INCOMPLETE` if a known required segment is missing | False | Block the candidate and produce the §11 failure slice; disagreement alone does not establish a business mismatch. |
| Known mandatory source segment is missing or pending | `NOT_COMPARABLE` or `ERROR` as applicable | `INCOMPLETE` | False | The missing segment is known and must be named. |
| Timeout without linked provider evidence, or unlinked billed amount | May be `EQUAL` for compared known rows; never by itself enough to resolve spend | `UNDETERMINED` for affected spend scope | False | Preserve known subtotal and unresolved/unattributed item; never infer zero or assignment. |
| Cuts, policy versions, correction boundary or finalized inputs differ | `NOT_COMPARABLE` | `INCOMPLETE` if a known required segment is missing; otherwise `UNDETERMINED` | False | Unequal inputs are not a business mismatch. |
| Comparator/internal failure | `ERROR` | `INCOMPLETE` or `UNDETERMINED` based on evidence | False | Preserve the failure reason; do not publish. |

The comparison status describes the comparison; the business verdict describes evidence for the declared scope. `VERIFIED` is not a global completeness claim.

## Hand-worked arithmetic before contract self-checks

All amounts below are synthetic and use `demo-v1`, unit price USD 0.05, half-even rounding, and the period above.

| Fixture / subcase | Provider spend | Billable units | Customer charge | Invoice amount included at cut | Invoice delta | Expected verdict by scope |
|---|---:|---:|---:|---:|---:|---|
| F1: two billed attempts, one request | 0.0120 + 0.0090 = 0.0210 | 1 | 1 × 0.05 = 0.05 | 0.10 | 0.10 − 0.05 = 0.05 | Provider spend VERIFIED in the complete fixture scope; invoice reconciliation MISMATCH; overall fixture MISMATCH. |
| F2: timeout A, retry B succeeds | Known subtotal 0.0090 from B only; A adds nothing and remains unresolved | 1 | 1 × 0.05 = 0.05 | 0.05 | 0.05 − 0.05 = 0.00 | Provider spend UNDETERMINED; customer-charge/invoice scope VERIFIED; overall UNDETERMINED. |
| F3 duplicate delivery | Not evaluated in invoice-only case | 1 | 0.05 | Duplicate `source_event_id` contributes once: 0.05 | 0.00 | Invoice reconciliation VERIFIED. |
| F3 late line | Not evaluated in invoice-only case | 1 | 0.05 | On-time 0.05; late 0.02 excluded after cut | 0.00 | As-known-at-cut invoice reconciliation VERIFIED with a recorded exclusion. |
| F3 wrong amount | Not evaluated in invoice-only case | 1 | 0.05 | 0.04 | 0.04 − 0.05 = −0.01 | Invoice reconciliation MISMATCH. |

## OPEN-Q list

- **OPEN-Q-1 (G1/P1.2):** How should the owner classify an unlinked billed provider record when no app attempt can be correlated? Until the owner confirms: include it only as unattributed known spend, never attach it to a request, and keep the affected provider-spend verdict `UNDETERMINED`.

## What contract v1 does not claim

- No global or provider-side completeness, no proof that a provider did nothing from a timeout, and no zero-cost conclusion for an unknown attempt.
- No customer delivery/receipt guarantee from an app-observed success without a separate client acknowledgement.
- No actual production charge, invoice, savings, adoption, or provider behavior from any `SYNTHETIC` fixture.
- No comparison guarantee when manifests, source cuts, policies, correction boundaries, or finalized sinks differ.
- No exactly-once delivery guarantee, no automatic correction finalization, and no payment collection, tax, or FX behavior.

## Gate state vocabulary note (D9)

The existing gate-state line adds `HUMAN_CONDITIONAL_GO` to the validator's accepted `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `FAILED`, `PASS`, `HUMAN_GO`, and `HUMAN_NO_GO` values. This is a state label only; it does not grant agent authority to sign a human gate.
