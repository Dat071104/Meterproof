# ADR-001 — Independent SQL/dbt and Flink implementations

## Status

Proposed — review-ready; owner accepts at G0.

## Context

Core needs a deterministic SQL/dbt batch candidate, a real independently authored Debezium/Kafka/Flink shadow candidate, and a small pure-Python oracle for bounded fixtures. Agreement is evidence only when each path has a separate implementation and the same frozen source cut. The v3.1-v3.3 invariants prohibit a shared transformation reducer and prohibit importing production transformation code into the oracle.

## Decision

Share the wire schemas and human-reviewed business specification. Author SQL/dbt pricing and reconciliation logic and Flink Java event-time logic independently. Keep the Python oracle fixture-only and independent of both production paths. The comparator consumes their outputs and the same manifest; it is not another business reducer.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Independent failure detection | 35 | Common-mode bugs invalidate parity evidence. | 1 | 1 | 5 | 4 |
| Source/coverage correctness | 25 | A correct reducer on the wrong scope is not verification. | 1 | 3 | 5 | 3 |
| Failure localization | 20 | The workflow must explain differing keys and inputs. | 1 | 2 | 5 | 3 |
| Maintenance simplicity | 10 | More implementations cost more to keep aligned. | 5 | 4 | 2 | 3 |
| Runtime cost | 10 | Local bounded checks should remain affordable. | 5 | 4 | 2 | 3 |
| **Weighted total / 5** | **100** |  | **1.80** | **2.30** | **4.40** | **3.35** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | Do nothing beyond one SQL/dbt path; defer the shadow/oracle | Lowest setup cost | Fails the Core differential/recovery scope; parity is not tested | Low | Two-way before implementation; blocks Core acceptance | This fails when a SQL regression is described as independently verified | S | Review P0 acceptance; no runtime test can establish parity |
| A | Feed SQL and Flink from one shared executable reducer | Less duplicated code | Correlated defects can make both outputs agree incorrectly | Medium | Two-way early; high refactor cost after both paths depend on it | This fails when a wrong shared rounding or dedup rule passes parity | M | Mutate the shared rule and show both paths miss it |
| B | Independent SQL/dbt and Flink implementations share only spec/schema; Python oracle is test-only | Strongest independent evidence and diagnosable mutations | Duplicated policy code and more maintenance | High | Two-way at design time; later changes need compatibility and replay evidence | This fails when specs drift and independent paths silently implement different policies | L | T02, T06, T07, T11 plus aligned-cut tests |
| C | Separate SQL and Flink implementations without an independent oracle | Two engines can catch some divergence | A common misunderstanding in the spec can survive both implementations | Medium | Two-way early; adding an oracle later is feasible | This fails when both engines encode the same mistaken business rule | M | T06/T07 show divergence but do not test an independent oracle |

## Consequences

- A run pins policy/schema and each engine's code artifact independently.
- A difference is surfaced as row/key evidence; an unequal source cut is NOT_COMPARABLE, not a business mismatch.
- The oracle remains a small test artifact; product calculations do not import it.

## Failure modes → T-IDs that will prove them

- One attempt is deduplicated by logical request and provider spend is understated → T02.
- A SQL pricing mutation escapes the comparator → T06.
- Flink produces a different state without a useful failure slice → T07.
- The verifier and oracle share a defect and rubber-stamp it → T11.
- The same frozen input is not deterministic → T10.

## Invariants

INV-01, INV-02, INV-03, INV-07 and INV-09; preserve SQL/Flink independence and the pure-Python test-only oracle.

## Reopen conditions

Reopen only if executed mutation/replay evidence shows the independent implementations cannot be compared reliably, or a proposed shared primitive is proven to be representation-only and cannot encode billing policy. A change of meaning requires owner/advisor review and a new ADR/version after G0.
