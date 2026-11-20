# ADR-003 — Immutable report versions, CAS publication, consumer isolation

## Status

Proposed — review-ready; owner accepts at G0.

## Context

Late evidence and corrections must not rewrite what a reviewer previously saw. Concurrent publishers can finish out of order. Core reports also have different trust levels from Lite's local outputs and Atlas's AI explanations; consumers must not write Core state.

## Decision

Store immutable report versions in isolated candidate/report namespaces. A scoped decision may publish only when `published_eligible` is true under the VERIFIED/EQUAL/no-unresolved rules. Update the current pointer with compare-and-swap/fencing against its expected version; retain the prior version. Expose a versioned read-only API. Lite remains local to user-supplied data. Atlas receives read-only credentials for published reports and can write only its own drafts/traces.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Stale-writer prevention | 30 | A slower publisher must not overwrite a newer approved version. | 1 | 2 | 5 | 4 |
| Historical auditability | 25 | Corrections must preserve prior reports. | 1 | 5 | 5 | 5 |
| Tenant/consumer isolation | 20 | Atlas and Lite cannot write Core truth. | 1 | 2 | 5 | 4 |
| Fail-closed publication | 15 | Unknown or incomplete cases cannot publish. | 1 | 3 | 5 | 4 |
| Operational simplicity | 10 | Versioning/CAS adds storage and transaction work. | 5 | 3 | 2 | 3 |
| **Weighted total / 5** | **100** |  | **1.40** | **3.30** | **4.70** | **3.60** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | Do nothing: mutate one current report in place | Lowest schema and storage cost | Loses history and lets late/stale writes rewrite prior truth | Low | One-way after old values are overwritten | This fails when a late invoice correction changes the only report record | S | T05 history assertion immediately fails |
| A | Keep immutable report versions but use last-write-wins pointer updates | Preserves history | A stale publisher can still move the pointer backward | Medium | Two-way before users depend on pointer semantics | This fails when the older candidate commits last | M | T09 concurrent publisher race |
| B | Immutable versions plus scoped CAS/fencing pointer and strict read-only consumer API | Preserves history, blocks stale writers and separates trust | More DB/control-plane state and transaction logic | High | Two-way before release; migration required once clients depend on version IDs | This fails when CAS checks an unscoped pointer or a consumer gets write credentials | L | T05/T09/T12 plus Atlas non-interference |
| C | Immutable versions with a manual operator-controlled pointer | Clear human gate | Manual step does not solve concurrent automation or auditable CAS semantics | Medium | Two-way, but the operating process can drift | This fails when two operators publish based on stale state | M | T09 under concurrent candidates |

## Consequences

- The prior approved report remains addressable after a correction.
- Publication consumes a VERIFIED, EQUAL, fully resolved decision; MISMATCH, INCOMPLETE and UNDETERMINED candidates do not move the pointer.
- Atlas cannot hold Core write credentials. Lite output remains local and never masquerades as a Core report.

## Failure modes → T-IDs that will prove them

- A late correction overwrites the earlier public report → T05.
- Two candidates race and the stale one wins → T09.
- Cross-tenant read/write is possible → T12.
- Atlas changes canonical report digest or pointer → H4 / AI non-interference regression.

## Invariants

INV-06, INV-08 and INV-12; only a covered VERIFIED report is published; CAS is tenant/scope/version fenced.

## Reopen conditions

Reopen if a real concurrent-write test shows CAS is not atomic, tenant/scope keys do not fence the pointer, or consumers can mutate Core versions. Any replacement must retain immutable history and prove stale-write rejection before adoption.
