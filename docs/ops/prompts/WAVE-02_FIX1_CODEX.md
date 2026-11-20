@start-here Execute METERPROOF WAVE-02 FIX1 exactly as written below.

# WAVE-02 FIX1 — VERIFIED requires a policy version (C6) (Codex work order)

Repo root: D:\DATA_ENGINEER\METERPROOF\Meterproof
Branch: stay on `p0/wave-02-p0.4-g0`, expected HEAD `f1d28e5`, clean tree except the advisor files listed under COMMIT 1.
Size: Light. One schema rule, one negative fixture, records. Do not load teams, templates or the code graph beyond Tier 0.

Skill loading (START_HERE Context Intake Tiers):
  Tier 0: AGENTS.md (root + pack), session_start.py (must be OWNED), SESSION_BRIEF / CURRENT_TASK, PROJECT_STATUS.md.
  Tier 1: none. Tier 2: none. Tier 3: only the READ list. Report the files you read.

READ:
  - docs/ops/reviews/WAVE-02_REVIEW.md (finding C6)
  - docs/contracts/DOMAIN_SPEC_v1.md line 23
  - contracts/jsonschema/verification_decision.v1.schema.json
  - tests/fixtures/contracts/negative/N21_verification_decision.json (fixture shape)
  - tests/contracts/test_contract_schemas.py (how negatives are checked)

GOAL: a verification decision with `business_verdict = VERIFIED` must carry a non-empty string `policy_version`. Contract v1
must enforce this before the merge freezes it.

ENVIRONMENT: the DEV_BOOTSTRAP.md environment as in WAVE-02 (external UV_PROJECT_ENVIRONMENT, caches outside the repo,
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1). Never let uv create a repo-local `.venv`.

STEPS
COMMIT 1 — advisor files, as written, explicit paths only:
    docs/ops/reviews/WAVE-02_REVIEW.md, docs/ops/reviews/G0_GATE_REVIEW.md, docs/ops/prompts/WAVE-02_FIX1_CODEX.md,
    docs/milestones/core/P0.md (Reviewer note), ai-agent-workspace-pack/_agent_ops/RISK_REGISTER.md,
    ai-agent-workspace-pack/_agent_ops/IMPLEMENTATION_LOG.md
    Message: `docs(advisor): WAVE-02 review, G0 gate review, FIX1 order`.
1. Test first: create `tests/fixtures/contracts/negative/N34_verification_decision.json` in the N21 shape:
   - `comparison_status` EQUAL, `business_verdict` VERIFIED, `published_eligible` false, `policy_version` null;
   - all other fields valid;
   - `expected_error` validator "type", path ["policy_version"].
   Run the suite against HEAD f1d28e5 schemas and record that N34 is ACCEPTED, so the suite fails on N34.
2. Fix: in the schema's top-level `allOf`, add one rule:
   `if {properties: {business_verdict: {const: "VERIFIED"}}, required: ["business_verdict"]}`
   `then {properties: {policy_version: {type: "string", minLength: 1}}}`.
   Change no field, type, required list or other rule.
3. Re-run: pytest tests/contracts tests/unit (expect 14 passed with N34 included), ruff, mypy, validate_overlay.py,
   check_repo_hygiene.py, check_adr_scores.py, git diff --check. All must exit 0. F1–F3 facts must stay unchanged.
4. Records:
   - contracts/jsonschema/CHANGELOG.md: one line under v1 (pre-freeze fix, C6);
   - docs/gates/G0/P0.2_receipt.md: append a "FIX2 (C6)" section with the commands, exit codes and the N34 before/after result;
   - RISK-0011: status "Closes on merge";
   - IMPLEMENTATION_LOG entry; PROJECT_STATUS and P0.md RESUME_POINT set to "owner: fast-forward main, push, CI; then
     /meterproof-advisor gate G0".
COMMIT 2: `fix(p0.2): VERIFIED requires policy_version (C6)`. Stage explicit paths only, and run the repo-map refresh per
the pack rule.

IN SCOPE: the paths named above.
OUT OF SCOPE: every other schema field or rule; F1–F3; ADRs; compose, CI, pins; the pack (except the _agent_ops records named);
G0_GATE_RECEIPT.md status.

STOP AND ASK IF: N34 is already rejected at HEAD; any existing fixture or example breaks; the fix needs more than the one rule.

AUTHORIZATION: local commits on this branch with explicit paths. NO push, merge, rebase, amend or tag. No network beyond the
locked uv cache. No Docker.

FINISH: one EXECUTION REPORT (format in docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md) and the closure receipt.
RESUME_POINT: owner fast-forwards main to this branch, pushes and checks CI; then `/meterproof-advisor gate G0`.
