# ADR-004 — Full CDC failure lab vs budget-safe public read deployment

## Status

Proposed — review-ready; owner accepts at G0.

## Context

The project must demonstrate real PostgreSQL WAL → Debezium → Kafka → Flink behavior and failure recovery, while the public demo has no approved cloud/provider budget. A budget-safe public read service cannot be described as an always-on streaming shadow unless that path is actually run and evidenced.

## Decision

Keep two explicit profiles. The reproducible local/on-demand lab runs the full CDC/Flink shadow and failure drills. The public budget-safe path uses the durable SQL/dbt reference and immutable approved read-only reports; it discloses that continuous Flink parity is not running unless a shadow run is separately executed and receipted. Lite remains local and does not claim Kafka/Flink reliability.

## Alternatives — weighted options debate

Weights sum to 100. Scores are 1–5 (5 is strongest); weighted score is `sum(weight × score) / 100`.

| Criterion | Weight | Why it matters | Option 0 | A | B | C |
|---|---:|---|---:|---:|---:|---:|
| Budget sustainability | 25 | No provider/cloud budget is approved. | 5 | 1 | 5 | 5 |
| Evidence truthfulness | 25 | Runtime claims must match what was run. | 5 | 3 | 5 | 5 |
| Failure/recovery reproducibility | 20 | Core requires real crash/restart evidence. | 1 | 4 | 5 | 5 |
| Security/isolation | 15 | Public read paths must not gain write authority. | 5 | 3 | 5 | 5 |
| Reviewer access | 10 | The portfolio needs a safe inspectable surface. | 1 | 5 | 4 | 2 |
| Operational simplicity | 5 | The system is built by one owner. | 5 | 1 | 3 | 4 |
| **Weighted total / 5** | **100** |  | **3.80** | **2.80** | **4.80** | **4.65** |

| Option | Summary | Pros | Cons / risks | Effort | Reversibility | Pre-mortem | Size | Cost to verify |
|---|---|---|---|---|---|---|---|---|
| 0 | Do nothing beyond design docs; no runnable lab or public read service | No runtime cost or accidental overclaim | Does not demonstrate the required real CDC/Flink failure path or user-facing read boundary | Low | Two-way; no data/runtime commitments | This fails when reviewers cannot distinguish evidence from diagrams | S | No runtime check; marks P0/P4 acceptance unmet |
| A | Operate the entire PostgreSQL/Kafka/Connect/Flink stack continuously in public | One environment for all paths | Unapproved recurring cost, larger attack surface and unsupported always-on reliability claim | XL | One-way after data, resources and users depend on it | This fails when cost or host/runtime limits cause silent downtime | XL | Requires owner-approved budget, SLOs, monitoring and T03/T09 evidence |
| B | On-demand full local failure lab plus separate public SQL/dbt read-only report service | Real failure evidence with a bounded public cost and honest runtime claims | Two profiles and explicit evidence labels to maintain | High | Two-way before public consumers; later API compatibility needs versioning | This fails when the public profile is presented as always-on Flink parity | L | T03/T04/T09, deployment checks, read-only/T12 and claim audit |
| C | Full local lab only; no public read profile | Lowest recurring cost and strong local failure evidence | Reviewers cannot inspect a deployed read boundary; public portfolio is less usable | Medium | Two-way; public surface can be added later | This fails when reviewers need a stable versioned artifact outside the local machine | M | Full local failure suite and local report inspection |

## Consequences

- No paid cloud or provider calls are implied by this ADR.
- A local Flink success proves only that specific run; the public read service cannot claim a running stream shadow by default.
- Profiles share schemas and evidence contracts, not an assertion of equal runtime guarantees.

## Failure modes → T-IDs that will prove them

- Restart after sink commit but before ACK duplicates a side effect → T03.
- Out-of-order events change finalized results → T04.
- A stale public publisher overwrites a newer report → T09.
- Public read/authentication crosses tenants → T12.

## Invariants

INV-07, INV-08, INV-10 and INV-11; preserve the full Core P0–P7 scope and keep Lite/Atlas trust boundaries.

## Reopen conditions

Reopen only after an owner-approved cost cap, measured runtime/host capacity, deployment security review and receipts proving continuous shadow behavior. A green local lab alone does not authorize or imply a public always-on streaming claim.
