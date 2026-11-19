# Branch & release integration — one Core, two extensions

- `main` is authoritative reviewed code; protected PR and smoke gates must prevent silently changing versioned Core semantics.
- `feature/lite` branches after Core G2 and relevant reusable contracts are stable; can evolve concurrently thereafter. Eventually merges back after L0–L3 tests. Lite package is released independently via PyPI/uvx, not by cloning the Core repository.
- `feature/atlas-ai-analytics` branches when an immutable verified read API/report fixture exists (G3 minimum); Atlas remains read-only, publishes only its own drafts/traces. Merges after A0–A5 non-interference regression and approval.
- Architecture/domain contract modifications require a Core ADR/PR and rerun relevant Core gates; no business rule changes hidden in Lite/Atlas PRs.
- Tags (`core-v1.0.0`, `lite-v1.0.0`, `atlas-v1.0.0`) identify versions of deliverables. Avoid permanent branch divergence or copying DBTs/oracles.
- Every merge/PR: diff audit, test command/raw logs, relevant T01–T12 subset, security origin label; release gates demand full T01–T12 receipts for Core.
- A version-tagged read-only report API supports many consumers. A branch name is not a runtime tenant isolation mechanism.
- No agent has blanket permission to commit/push/merge, charge cloud or use provider keys. Explicit user approval and least privilege apply.
