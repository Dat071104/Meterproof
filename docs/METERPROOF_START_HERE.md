# METERPROOF v3.4 — Project authority & reading order

**Status:** architecture/execution contract drafted; NONE of the implementation phases is passed by installing this overlay.

## Priority
1. **Core**: failure-aware, evidence-aware reconciliation and independent SQL/dbt ↔ Flink differential replay; Core may run without Lite and Atlas.
2. **Lite**: free local-first CLI/SDK/CI wrapper over reusable **input contracts and evidence checks**; no false claim that Lite executes/validates full Kafka/Flink pipeline.
3. **Atlas**: governed analytics and read-only AI Incident Analyst. **No writes** into Core business facts, verdicts, or publication pointers.
4. **Adoption**: 200–300 verified user activations is a goal, not a result; measure repeat use and real integrations separately.

## Canonical files
- `docs/architecture/ARCHITECTURE_DECISIONS.md` — bounded contexts, topology, data plane vs control plane, failure model.
- `docs/architecture/SOURCE_CUT_PROTOCOL.md` — exact replay equivalence protocol.
- `docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md` — identities, source authority, billability, verdicts, temporal dimensions.
- `docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md` — T01–T12, mutation, comparative baselines, honest metrics.
- `docs/milestones/MILESTONE_INDEX.md` + `docs/milestones/*/*.md` — subphases, acceptance criteria and gates.
- `docs/ops/PROJECT_STATUS.md` — project status and exact next step; generic pack `_agent_ops` remains session/handoff authority.
- `docs/ops/CODEX_START_PROMPT.md` — one-task agent entrypoint.
- `docs/adr/` — architectural decisions; change Core scientific claims only with ADR and gate regression.

## Must never regress from v3.1/v3.2/v3.3
Three evidence sources, provider timeout uncertainty, separate provider attempts, billing policy versioning; frozen source+coverage manifest; real PostgreSQL WAL/Debezium/Kafka/Flink; independent SQL/dbt & pure-Python oracle; historical correction, CAS publication, T01–T12 with true faults, MP-004 incident, read-only sanitized public demonstration, honest operational provenance.

**Allowed scope expansion:** Lite CLI/SDK/CI, optional user-paid managed offering only after validation, Atlas analytics/RAG/agent with verified read API. None may mutate or dilute Core.

## Agent startup checklist
- [ ] Read repository-specific AGENTS and only relevant domain skill, plus generic pack's routing/handoff.
- [ ] Verify Git status, current branch, relevant test environment, resource/cost status.
- [ ] Pick exactly one subphase; cite its files, missing decisions, acceptance tests, approved budget.
- [ ] Execute bounded change or STOP on uncertainty; never fake observed evidence.
- [ ] Write a gate receipt for executed tests; update project status and pack handoff with exact RESUME_POINT.
