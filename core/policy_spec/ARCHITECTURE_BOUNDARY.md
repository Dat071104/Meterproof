# core/policy_spec — module boundary (PLANNED, NOT IMPLEMENTED)

**Milestone:** P0–P3 · **Ownership:** Immutable versioned billing policy specification.

**Non-negotiable:** Store human-reviewed semantics, rounding and policy effective ranges. SQL/dbt and Flink MUST independently implement, not import a shared executable reducer.

**Verification responsibility:** manual truth tables + oracle mutants.

This marker preserves a clean intended repository structure for Codex. It is not a claim that code, runtime or tests already exist. Follow the active milestone and inspect actual existing project source before adding implementation.
