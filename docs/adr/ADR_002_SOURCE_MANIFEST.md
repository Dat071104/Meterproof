# ADR-002 — Immutable source-consistent manifest across async sources

## Status

Proposed — review-ready; owner accepts at G0.

## Context

The application database, Debezium/Kafka stream, provider evidence and invoice exports advance on different clocks. A PostgreSQL LSN describes the database cut only; it does not prove that external provider generations or invoice rows are complete. The source-cut protocol requires equal populations, policy, correction boundary and finalized sink evidence before comparison.

## Decision

Seal one immutable, tenant-scoped manifest for each replay. Record the consistent application snapshot and its source-event-ID hash, PostgreSQL snapshot/LSN, provider and invoice scopes and exclusions, policy/schema versions, code/artifact SHAs, timezone and correction policy, Kafka topic/partition offset vector, completed Flink checkpoint and sink commit receipt. Keep external scope explicit; a database LSN never stands in for it. If required identity or finalization evidence is absent, do not mark the cuts comparable.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Application population equivalence | 35 | Batch and stream must use the same committed source events. | 1 | 3 | 5 | 2 |
| External provider/invoice scope | 25 | LSN/offsets do not establish external completeness. | 1 | 1 | 5 | 1 |
| Replay and audit determinism | 20 | A reviewer needs pinned inputs and hashes. | 1 | 2 | 5 | 3 |
| Recovery/coverage clarity | 10 | A gap must stop a false comparison. | 1 | 2 | 5 | 2 |
| Complexity/cost | 10 | More manifest metadata adds operational work. | 5 | 4 | 2 | 4 |
| **Weighted total / 5** | **100** |  | **1.40** | **2.30** | **4.70** | **2.15** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | Do nothing: compare current live batch tables and stream totals | Minimal setup | Population changes during runs; no scoped external evidence | Low | Two-way, but cannot satisfy the current Core gate | This fails when one path sees a late row or a missing provider export | S | T10 replay without a manifest is expected to fail |
| A | Freeze only a PostgreSQL consistent snapshot/LSN for app sources | Gives a transactionally consistent app cut | Leaves provider and invoice scopes unbounded | Medium | Two-way; external scopes can be added later | This fails when equal app cuts hide an unknown provider attempt | M | Compare LSN-only evidence with a provider/invoice gap control |
| B | Seal a source-aware manifest containing app/outbox, external scopes, offsets, checkpoint and sink evidence | Strongest comparable-input and audit trail | Most fields to collect; a missing item blocks comparison | High | Two-way at design time; run artifacts remain immutable | This fails when offsets or external scope are guessed rather than captured | L | T01/T04/T08/T10 and source-cut negative controls |
| C | Use a Kafka offset vector as the global cut | Captures broker progress | Offsets omit the app snapshot boundary and provider/invoice completeness | Medium | Two-way, but does not become a full source manifest by itself | This fails when Kafka is caught up while an external export is incomplete | M | T08 with an intentionally missing provider record |

## Consequences

- A manifest names both the source population and evidence that proves each hop.
- A mismatched source cut yields comparison status NOT_COMPARABLE. A known missing required scope may be INCOMPLETE; unresolved attribution is UNDETERMINED.
- Every run retains the same manifest bytes and hashes; corrections create a new manifest/report version.

## Failure modes → T-IDs that will prove them

- A duplicate outbox/Kafka delivery has two raw offsets but one canonical event → T01.
- Out-of-order app/provider observations cross an unrecorded cut → T04.
- Provider ID is missing and scope is unknown → T08.
- Replaying the same sealed manifest changes the digest → T10.

## Invariants

INV-04, INV-06, INV-07 and INV-09; follow SOURCE_CUT_PROTOCOL §§1–12.

## Reopen conditions

Reopen if a source cannot export stable identities, a connector cannot prove snapshot-to-stream continuity, external evidence scope cannot be represented, or a failure drill shows the manifest falsely marks incomparable cuts as equal. Do not weaken the source-cut protocol to make a run publishable.
