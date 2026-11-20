# Implementation Log Archive 2026-11

Rotated out of `IMPLEMENTATION_LOG.md`. Append-only; read only when the
retained window and the summary are not enough.

## 2026-11-20 — Advisor review WAVE-01 and WAVE-02 order (Claude Code, advisor)

### Date

`2026-11-20`

### Task ID

`not assigned (advisor session)`

### Phase / Task

`/meterproof-advisor review WAVE-01` + `next wave` (WAVE-02 = WAVE-01 fix-up + P0.4 + G0 gate packet)

### Files Touched

- `docs/ops/reviews/WAVE-01_REVIEW.md` (new), `docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md` (new)
- `docs/milestones/core/P0.md` (Reviewer note only)
- `ai-agent-workspace-pack/_agent_ops/DECISION_LOG.md` (DEC-0008–0010), `RISK_REGISTER.md` (RISK-0003/0008 updated, RISK-0011 added), this log

### What Changed / Evidence Produced

- Verdicts:
  - Step 0 / P0.1 is APPROVE.
  - P0.2 is CHANGES_REQUESTED. The verification decision accepts MISMATCH with a non-EQUAL comparison status; empty-string identities pass; money fields cross source authority; the cut applies only to invoices; `customer_charge` scale is unbounded.
  - P0.3 is CHANGES_REQUESTED. ADR-003/005 weighted totals are miscomputed, and the lineage/F1 trace mixes the two verdict axes.
- Owner decisions:
  - DEC-0008: comparison and business verdict are two axes; only EQUAL permits VERIFIED or MISMATCH.
  - DEC-0009: Apache-2.0.
  - DEC-0010: local Docker pulls and one full-lab measurement.
  - Bundle the fix as WAVE-02 Step 0.
- No source, schema or test file was edited by the advisor.

### Why

Contract v1 freezes when `p0/wave-01-p0.2-p0.3` merges; the gaps must close first (RISK-0011).

### Tests Run

```text
python tools/meterproof/validate_overlay.py -> exit 0
python ai-agent-workspace-pack/_agent_ops/tools/check_repo_hygiene.py --root . --ops-folder ai-agent-workspace-pack/_agent_ops -> exit 0 (324 tracked, 0 artifacts)
git diff --check main...HEAD -> exit 0
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 C:/Python313/python.exe -m pytest -p no:cacheprovider -q tests/contracts -> 8 passed (jsonschema 4.26.0, pytest 9.1.1); without the env var pytest crashed on a broken user-site dash plugin
claims-audit pattern (order 2.7) -> 76 hits, equal to the P0.3 receipt
scratchpad adversarial schema probe -> 17 contract-invalid mutants accepted
scratchpad ADR score recomputation -> ADR-003 A 3.00 (stated 3.30), C 4.15 (stated 3.60); ADR-005 B 2.85 (stated 2.95)
```

### Results

WAVE-01 partly approved. The merge of `p0/wave-01-p0.2-p0.3` waits for the WAVE-02 Step 0 re-review.

### Next Step

Owner pastes `docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md` into Codex; then `/meterproof-advisor review WAVE-02` and `/meterproof-advisor gate G0`.

## 2026-11-20 — WAVE-02 Step 0: WAVE-01 P0.2/P0.3 fix-up (Codex)

### Date

`2026-11-20`

### Task ID

`TASK-0004`

### Phase / Task

`WAVE-02 Step 0 — P0.2 contract v1 gaps and P0.3 ADR/lineage corrections`

### Files Touched

- `contracts/jsonschema/*.v1.schema.json`, `contracts/jsonschema/CHANGELOG.md`, `docs/contracts/DOMAIN_SPEC_v1.md`
- `tests/fixtures/contracts/negative/N21`–`N33`, `schema_examples.json`; `tests/contracts/test_contract_schemas.py`, `test_expected_facts.py`
- ADR-003/005 scores, `docs/architecture/LINEAGE_AND_TRACE.md`, `tools/meterproof/check_adr_scores.py`, `tests/unit/test_check_adr_scores.py`
- P0.2/P0.3 receipts, `_agent_ops/PROJECT_CONTEXT_CARD.md`, and this log

### What Changed / Evidence Produced

- Committed the six unchanged advisor paths as Commit A2 `231d9d72e1ed8c5e6879d00b061c21c1bb1c770c` on `p0/wave-01-p0.2-p0.3`.
- Wrote N21–N33 first; all 13 were accepted by schema copies from HEAD `706563c`, then rejected at their declared validator/path by the fixed schemas. No top-level schema fields or root required lists changed.
- Applied the source cut to every receipt before calculating facts and added an APP success-after-cut control. The five computed F1–F3 fact/verdict records match the saved baseline; F1–F3 fixture bytes are unchanged.
- Added a 115-line stdlib Decimal ADR scorer and two inline-table unit tests. Baseline identified only ADR-003/005 arithmetic errors; after correction all five tables pass and the chosen options remain ranked first.
- Updated the contract spec, changelog, lineage/F1 trace, and both P0.2/P0.3 receipts with controls, outputs and changed schema/fixture hashes.

### Tests Run

```text
uv run --no-project --python C:\Python313\python.exe --with jsonschema==4.23.0 --with rfc3339-validator==0.1.4 --with pytest==8.3.5 python -m pytest -p no:cacheprovider tests/contracts tests/unit -q -> 12 passed, exit 0 (Python 3.13.2; PYTEST_DISABLE_PLUGIN_AUTOLOAD=1; PYTHONDONTWRITEBYTECODE=1)
HEAD-706563c negative baseline N21-N33 -> all 13 accepted, exit 0; fixed-schema probe -> all 13 rejected at declared validator/path, exit 0
check_adr_scores.py baseline -> exit 1 for ADR-003/005 only; corrected tables -> exit 0 for ADR-001..005
validate_overlay.py -> exit 0; check_repo_hygiene.py -> exit 0 (326 tracked, 0 artifacts); git diff --check -> exit 0
F1-F3 computed fact snapshot comparison -> equal; F1/F2/F3 fixture bytes equal HEAD 706563c
```

### Results

The WAVE-01 fix-up checkpoint passes. P0.2 and P0.3 remain `IN_PROGRESS` pending advisor re-review; P0/G0 is not a PASS. No runtime pipeline, Docker lab, paid service, cloud, provider, push or merge was used in Step 0.

### Remaining Risks

- OPEN-Q-1 on unlinked billed provider records remains for G1/P1.2 owner confirmation.
- P0.4 has not begun; verify Docker Engine availability before its authorized image pulls.

### Next Step

Completed: refreshed the repo map for Commit C and D, verified Checkpoint 0, and created `p0/wave-02-p0.4-g0`.
