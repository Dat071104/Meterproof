# Mandatory gate policy

Gate source of truth: linked receipt files in `docs/gates/` plus real executed tests/CI SHA, not this roadmap. Phase card status starts `NOT_STARTED` and can become `IN_PROGRESS`, `BLOCKED`, `FAILED` or `PASS` only with evidence. Core G1 additionally requires `HUMAN_GO` to authorize continued product work; no program-level cloud/API permissions implied.

Per PR: one bounded subphase owner, expected failing negative control, test tier, source/policy scope, real result/uncertainty, no secrets, and pack handoff. Invariants INV-01–INV-12 apply; `NOT_COMPARABLE` is comparison state, not a reason to mark VERIFIED.
