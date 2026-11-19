# WAVE-01 — P0.1 fix-up → P0.2 → P0.3 (Codex work order)

Paste everything inside the fence into Codex, started from the repository root.
**Owner note:** pasting this order approves DEC-0007 (Step 0), decisions **D1–D9** (P0.2) and the listed downloads. Edit them before pasting if you disagree. Size: **Heavy** (three subphases, sequential, one writer).

```text
@start-here Execute METERPROOF WAVE-01 exactly as written below: Step 0 (P0.1 FIX1), then P0.2, then P0.3.

ROLE
You are the EXECUTOR. Claude Code is the advisor/reviewer; the repository owner approves. The advisor wrote this order and
the owner pasted it: it authorizes everything under AUTHORIZATION and nothing else.

Repo root: D:\DATA_ENGINEER\METERPROOF\Meterproof
Expected start: branch p0/p0.1-preflight @ f3fb3d404370a6ce342a87f8aee81db9130b3a66 with exactly these advisor-authored
uncommitted paths (commit them unchanged in Step 0; do not edit them):
  docs/ops/reviews/P0.1_REVIEW.md                         (new)
  docs/ops/prompts/WAVE-01_P0.2-P0.3_CODEX.md             (new, this order)
  docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md                   (modified: waves, skill loading)
  .claude/skills/meterproof-advisor/SKILL.md              (modified: wave mode)
  ai-agent-workspace-pack/_agent_ops/IMPLEMENTATION_LOG.md (advisor entry appended)
  ai-agent-workspace-pack/_agent_ops/DECISION_LOG.md       (DEC-0006 appended)
  ai-agent-workspace-pack/_agent_ops/RISK_REGISTER.md      (RISK-0001/0003 updated)
Anything else uncommitted or a different HEAD -> STOP.

MODE: Heavy. Sequential, single writer, no subagents. Autonomous mode is confirmed for the in-scope work of this wave:
write your plan into CURRENT_TASK.md and proceed; do not wait for build-team step-7 confirmation. Stop only on a STOP
condition or a failed checkpoint.

=== SESSION START AND SKILL LOADING (Context Intake Tiers of ai-agent-workspace-pack/START_HERE.md) ===
Tier 0, once:
  1. AGENTS.md (root) -> ai-agent-workspace-pack/AGENTS.md -> ai-agent-workspace-pack/START_HERE.md
  2. python ai-agent-workspace-pack/_agent_ops/tools/session_start.py --root .     (must report OWNED)
  3. ai-agent-workspace-pack/_agent_ops/SESSION_BRIEF.md, OPERATING_RULES.md, CURRENT_TASK.md
  4. docs/ops/PROJECT_STATUS.md; docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md (Waves, EXECUTION REPORT);
     docs/ops/reviews/P0.1_REVIEW.md
  5. ai-agent-workspace-pack/TEAM_ROUTER.md. Routing is pre-decided below; do not load other teams.
Tier 1, per step: read these SKILL.md files when the step starts, not before.
  | Step          | Pack team: ai-agent-workspace-pack/<team>/SKILL.md | Project skill: .agents/skills/<name>/SKILL.md           |
  | 0  P0.1 FIX1  | repo-hygiene-team                                   | none                                                    |
  | 1  P0.2       | build-team                                          | $meterproof-evidence                                    |
  | 2  P0.3       | analyze-team (option rules for every ADR)           | $meterproof-architecture, $meterproof-differential-replay (source cut, comparison, CAS) |
Tier 2: only the templates you use: build-team/PONYTAIL_RULES.md + SELF_REVIEW_CHECKLIST.md (P0.2);
  analyze-team/OPTIONS_DEBATE_TEMPLATE.md (P0.3).
Tier 3: the project files in each step's READ list.
Business rules source for build-team step 2: the "Business Rules & Acceptance Criteria" section of
_agent_ops/PROJECT_CONTEXT_CARD.md + docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md + D1–D9 below. Anything they do not
cover is a STOP question, never a guess. List every skill/template file you read in the final report.

=== STEP 0 — P0.1 FIX1 (branch p0/p0.1-preflight) ===
Why: docs/ops/reviews/P0.1_REVIEW.md, findings F1–F3.
0.1 Commit A: stage exactly the seven advisor paths above. Message: "docs(advisor): P0.1 review, WAVE-01 order, wave workflow".
0.2 F2, idempotence. Reproduce, do not trust the advisor: run the overlay dry run twice (never --apply):
      python D:\DATA_ENGINEER\METERPROOF\METERPROOF_v3_4_Architecture_Milestones_Agent_Overlay\METERPROOF_v3_4_Execution_Overlay\install_overlay.py --target .
    Capture stdout+stderr of each run to files in a temp dir outside the repo. Record the process exit code of each run
    (expected 2), the SHA-256 of both captures (expected identical) and `git status --porcelain` afterwards (expected:
    nothing but your own in-progress edits). Re-run the PACK_MANIFEST check (expected 145 checked, 0 mismatches). Read
    install_overlay.py and cite the lines showing that the collision return precedes every write.
    Append DEC-0007 to _agent_ops/DECISION_LOG.md: "Overlay installer retired for this repository after the first import
    (2026-11-19). Future overlay revisions are merged by reviewed diff under a work order; install_overlay.py --apply is
    never run here. The two ADD lines for data/fixtures/ are plan output of a refused run, not writes." Add the decision to
    the collision register in docs/ops/REPO_OWNERSHIP_MAP.md.
    Only if both runs are identical, exit 2, and no writes: tick P0.1 "Verification" in docs/milestones/core/P0.md.
0.3 F1, exit codes: wherever the installer exit is recorded as 1 (P0.1 receipt rows for both dry runs,
    REPO_OWNERSHIP_MAP.md, PROJECT_STATUS.md session log), replace it with the observed process exit code. Add one receipt
    line naming the shell used and stating that exit codes are process exit codes ($LASTEXITCODE in PowerShell, $? in bash),
    not PowerShell's $? boolean. IMPLEMENTATION_LOG.md is append-only: add a correction entry; do not rewrite TASK-0002.
0.4 F3: in P0.md set the header "Evidence:" to the receipt link and update the card's RESUME_POINT section. In
    PROJECT_STATUS.md change the Setup log heading "unverified until P0.1 reproduces it" to
    "verified by P0.1, docs/gates/G0/P0.1_receipt.md".
0.5 Receipt docs/gates/G0/P0.1_receipt.md: add the Step 0 commands to "Observed commands"; Status:
    "IN_PROGRESS — evidence complete; advisor re-review pending". Nobody writes PASS on a subphase receipt.
0.6 Run the validator, the hygiene check and git diff --check (all exit 0), then Commit B with explicit paths:
    "fix(p0.1): verify installer idempotence, correct exit codes, retire overlay installer".
CHECKPOINT 0: continue only if 0.2 matched expectations. If not, stop the wave and report.

=== BRANCH FOR P0.2 AND P0.3 ===
git switch -c p0/wave-01-p0.2-p0.3     (from p0/p0.1-preflight after Commit B). Record both SHAs.

=== STEP 1 — P0.2 Data authority and money contract (gate G0) ===
Skills: build-team + $meterproof-evidence (read both SKILL.md files now).
READ: docs/milestones/core/P0.md (P0.2 + Reviewer note "P0.2"); docs/milestones/core/P1.md (P1.2–P1.4: what the spike
  needs from these contracts); docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md; docs/architecture/ARCHITECTURE_DECISIONS.md
  §1, §4, §5; docs/architecture/SOURCE_CUT_PROTOCOL.md (§8, §12); docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md (T02, T08,
  MP-004); contracts/jsonschema/*.json; tests/fixtures/*.
GOAL: freeze contract v1 (identities, attempts, money, logical-unit policy, timeout uncertainty, provider/invoice scope,
origin) as a spec + JSON Schemas + three hand-verified fixtures. Every new schema rule is backed by a negative fixture
that the pre-change schema wrongly accepted.

DECISIONS PRE-APPROVED BY THE OWNER. Implement them; do not re-decide. If one contradicts a frozen statement in
DOMAIN_AND_EVIDENCE_CONTRACT.md or SOURCE_CUT_PROTOCOL.md, STOP and report file:line instead of choosing.
D1 Freeze model. The four v1 schemas are pre-release drafts until P0.2 is approved: edit v1 in place and log every change
   in contracts/jsonschema/CHANGELOG.md (change -> reason -> invariant -> negative fixture id). After merge, any change
   needs a new version file.
D2 Identities. Spec table columns: id -> issuer -> uniqueness scope -> nullable -> stable across retry/redelivery.
   - logical_request_id: unique per tenant, stable across retries.
   - provider_attempt_id: issued by the app before dispatch, new for each actual outbound attempt, unique per tenant.
   - provider_generation_id: provider-issued, unique per (provider, account), nullable, maps to at most one attempt.
   - source_event_id: the outbox row identity, unique per (tenant, source), stable across redelivery.
   - source_receipt_id: one persisted observation, unique per tenant.
   - tenant_id: derived on the server from verified auth.
   - transport_delivery_id: transport coordinates (Kafka topic, partition, offset), never a business key. It is recorded in
     the raw-delivery audit and in the manifest's kafka_offset_vector, and it is NOT a field of source_receipt.v1.
D3 Billing period. billing_period_id is an opaque id that resolves to {start, end, time_zone}, half-open [start, end).
   Fixtures declare all three. This wave uses UTC 2026-11: [2026-11-01T00:00:00Z, 2026-12-01T00:00:00Z).
D4 Receipt rules (source_receipt.v1, if/then):
   - APP: outcome in {REQUEST_INTENT, APP_OBSERVED_SUCCESS, APP_OBSERVED_FAILURE, UNKNOWN_PROVIDER_OUTCOME};
     logical_request_id required; provider_attempt_id required except for REQUEST_INTENT.
   - PROVIDER: outcome in {PROVIDER_CONFIRMED_BILLED, PROVIDER_CONFIRMED_NOT_BILLED}; provider_generation_id required.
     BILLED also requires known_provider_cost_usd and provider_amount_evidence_id. provider_attempt_id and
     logical_request_id are either both present (linked) or both null (unlinked provider record).
   - INVOICE: outcome = INVOICE_OBSERVED; logical_request_id may be null; billing_period_id, source_reference and a new
     money field invoice_amount_usd are required; provider_* fields must be null.
   - Any other source_kind/outcome pair is invalid.
D5 Money (INV-05).
   - Format: USD decimal strings with no sign, no exponent, at most 12 integer and 12 fractional digits:
     ^(0|[1-9][0-9]{0,11})(\.[0-9]{1,12})?$ on every *_usd field in all four schemas.
   - Observed amounts are stored exactly as observed; a value that does not fit is rejected, never rounded.
   - Arithmetic uses Decimal / NUMERIC(24,12) / BigDecimal, never float.
   - Only customer_charge is rounded: once per (tenant, billing period, price_policy_version) total, to 0.01, with the
     policy's rounding mode (demo-v1: ROUND_HALF_EVEN).
   - Canonical digest form: 12 fractional digits for spend and invoice amounts, 2 for customer_charge.
D6 Policy demo-v1 (SYNTHETIC).
   - billable_units = number of distinct logical_request_id with at least one APP_OBSERVED_SUCCESS (max one per logical
     request).
   - customer_charge = billable_units x unit_price_usd.
   - known_provider_spend = sum of cost over distinct provider_generation_id with PROVIDER_CONFIRMED_BILLED. It sums
     attempts, never logical requests (INV-02).
   - invoice_delta = invoice_amount - customer_charge.
D7 Unknowns (INV-04).
   - An attempt with UNKNOWN_PROVIDER_OUTCOME and no linked provider receipt adds nothing to known spend, is listed in
     unresolved_items, and makes the spend scope UNDETERMINED: never VERIFIED and never "zero cost".
   - An unlinked billed provider record is reported as unattributed known spend and never assigned to a request. Its interim
     verdict for that scope is UNDETERMINED. Record it as OPEN-Q-1 for G1 (P1.2); the owner confirms it there.
D8 Decision and report rules.
   - verification_decision.v1 gains a required origin field (INV-06).
   - published_eligible = true => business_verdict = VERIFIED AND comparison_status = EQUAL.
   - business_verdict = VERIFIED => comparison_status = EQUAL AND unresolved_items is empty.
   - published_read_report.v1: business_verdict is const VERIFIED (SOURCE_CUT_PROTOCOL §12: only VERIFIED reaches
     publication); D5 money pattern on its *_usd fields.
D9 Gate states. Add HUMAN_CONDITIONAL_GO to the "Gate state" line of DOMAIN_AND_EVIDENCE_CONTRACT.md (that one line only),
   matching P1.5, MILESTONE_INDEX and the validator.

1.1 OSS inputs (bounded, at most 45 minutes each). They feed notes and OPEN-Qs only and never override D1–D9.
    - Register #1 OpenMeter: event identity and dedup scope.
    - Register #3 Lago: billing event idempotency key and corrections; read lago-api or Lago docs only. Study-only, AGPL:
      copy nothing.
    Shallow-clone (git clone --depth 1) into a temp dir outside the repo, pin the commit, and write
    docs/research/openmeter-review.md and docs/research/lago-review.md using the template in
    docs/research/OSS_REFERENCE_REGISTER.md. Update the register's Review column. If there is no network, mark the review
    BLOCKED with the reason; never write a review from memory.
1.2 Test-first negative control. Before editing any schema, write the negative fixtures, put the main versions
    (git show main:contracts/jsonschema/<file>) in a temp dir outside the repo, and run the negative checks against them.
    Record which N-fixtures the OLD schemas wrongly accepted. After your edits, every one must be rejected.
1.3 Spec docs/contracts/DOMAIN_SPEC_v1.md. It must contain:
    - a field-authority table (field -> authoritative source -> not authoritative for -> unknown handling);
    - the D2 identity table;
    - the D3–D8 rules;
    - the provider outcome state machine (allowed transitions only, no fabricated transitions);
    - the verdict truth table per scope;
    - hand-worked arithmetic for F1/F2/F3, written before any code runs;
    - an OPEN-Q list (at least OPEN-Q-1);
    - a section "What contract v1 does not claim".
1.4 Schemas: apply D4, D5 and D8 to contracts/jsonschema/*.v1.schema.json; write CHANGELOG.md. Apply D9 to the contract
    line.
1.5 Fixtures in tests/fixtures/contracts/, origin SYNTHETIC, period per D3. Each file holds receipts that validate against
    source_receipt.v1, the policy, hand-computed expected facts, and the expected verdict per scope with its reason.
    - F1_two_billed_attempts_one_request.json: the MP-004 F1 case, using the values of tests/fixtures/MP004_F1_SYNTHETIC.json.
      Expected: known_provider_spend 0.0210, billable_units 1, customer_charge 0.05, invoice_delta 0.05, verdict MISMATCH.
    - F2_unlinked_timeout.json: one attempt times out with no generation id and the retry succeeds. Known spend excludes the
      unknown attempt, unresolved_items lists it, and the spend scope is UNDETERMINED, never VERIFIED.
    - F3_invoice_late_duplicate_wrong.json: three synthetic invoice cases. A duplicated delivery (same source_event_id) is
      counted once. A late line first observed after the cut is excluded with a reason in source_exclusions. A wrong amount
      gives MISMATCH. Sub-cases are allowed, each with its own expected facts.
    Keep tests/fixtures/MP004_F1_SYNTHETIC.json byte-identical. Add one line to tests/fixtures/README.md saying that F1
    supersedes it for contract tests.
    Negative fixtures in tests/fixtures/contracts/negative/, one file per rule, each of which must be rejected:
      N01 published_eligible true + UNDETERMINED
      N02 VERIFIED + NOT_COMPARABLE
      N03 VERIFIED with a non-empty unresolved_items
      N04 decision without origin
      N05 PROVIDER_CONFIRMED_BILLED without known_provider_cost_usd
      N06 PROVIDER_CONFIRMED_BILLED without provider_generation_id
      N07 provider receipt with an attempt id but a null logical_request_id
      N08 APP receipt without logical_request_id
      N09 INVOICE without billing_period_id
      N10 INVOICE without invoice_amount_usd
      N11 source_kind APP with outcome PROVIDER_CONFIRMED_BILLED
      N12 money "0.0000000000001" (13 fractional digits)
      N13 money "1e-3"
      N14 published report with business_verdict MISMATCH
      N15 occurred_at "2026-13-45T00:00:00Z" (proves that format checks actually run)
1.6 Tests in tests/contracts/ (pytest):
    - test_contract_schemas.py: every schema passes Draft202012Validator.check_schema; every positive record validates;
      every negative fixture is rejected for its intended reason. Use format_checker=Draft202012Validator.FORMAT_CHECKER.
    - test_expected_facts.py: recomputes the F1/F2/F3 expected facts from the fixture records with decimal.Decimal and the
      D5–D7 rules, and asserts equality with the hand values. It is inline and self-contained. It is a contract
      self-check, NOT the independent oracle (P1.4): do not place it in independent_oracle/ and do not import it from
      anywhere else.
    - Determinism controls inside the tests:
      - float 0.012 + 0.009 must differ from the Decimal result 0.0210;
      - Decimal("0.125") quantized to 0.01 must give 0.12 with HALF_EVEN and 0.13 with HALF_UP;
      - two computations of the canonical facts digest must be identical.
    RUN (exact; if uv needs different flags, record the command you actually used and why):
      uv run --no-project --python 3.13 --with jsonschema==4.23.0 --with rfc3339-validator==0.1.4 --with pytest==8.3.5 python -m pytest tests/contracts -q
    Record sys.executable and sys.version from inside that environment in the receipt.
1.7 Self-review with build-team/SELF_REVIEW_CHECKLIST.md. Receipt docs/gates/G0/P0.2_receipt.md (from the template;
    origin SYNTHETIC; input = SHA-256 of every schema and fixture file; negative control = the 1.2 results plus the float
    and rounding controls).
1.8 Commit. Run pytest (green), the validator (0) and hygiene (0). Stage the explicit paths, then run
      python ai-agent-workspace-pack/_agent_ops/tools/refresh_repo_map.py --root . --ops-folder ai-agent-workspace-pack/_agent_ops --stage
    review the staged REPO_MAP.md, and commit without --no-verify:
    "feat(p0.2): freeze contract v1 (spec, schemas, F1-F3, negative fixtures)".
ACCEPTANCE P0.2 (each needs an evidence path in the receipt):
  [ ] Build/inspect: identities, attempts, Decimal rounding, logical-unit policy, timeout uncertainty, provider/invoice scope,
      origin labels frozen -> DOMAIN_SPEC_v1.md + CHANGELOG.md
  [ ] Artifacts: spec, versioned schemas, F1/F2/F3 expected facts -> paths
  [ ] Verification: F1 = 2 charged attempts / 1 billable request; F2 never VERIFIED; deterministic Decimal -> pytest output
  [ ] Evidence receipt -> docs/gates/G0/P0.2_receipt.md
CHECKPOINT 1: continue to P0.3 only if all four P0.2 boxes have evidence. Otherwise stop the wave and report.

=== STEP 2 — P0.3 Architecture ADR and schema graph (gate G0) ===
Skills: analyze-team (+ OPTIONS_DEBATE_TEMPLATE.md) + $meterproof-architecture; add $meterproof-differential-replay for the
source-cut, comparison and CAS publication parts. Read each SKILL.md now.
READ: P0.md (P0.3 + Reviewer note "P0.3"); docs/architecture/{ARCHITECTURE_DECISIONS,SOURCE_CUT_PROTOCOL,
  SECURITY_PRIVACY_COST,STACK_AND_CAPABILITIES,BRANCH_AND_RELEASE_POLICY}.md; docs/adr/*.md;
  docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md; the P0.2 outputs; the .drawio file only to check consistency.
GOAL: ADR-001..004 written out and review-ready, the outbox/CDC decision recorded, an ERD and a lineage map, and a written
trace that a reviewer can follow from source event to published report without meeting an unsupported guarantee.
2.1 OSS input #2, Debezium outbox example (design read only; the runnable lab belongs to P2.2/P4.1). Shallow-clone
    debezium/debezium-examples to a temp dir, pin the commit, and read outbox/ only. Write
    docs/research/debezium-outbox-review.md covering the outbox table, Outbox Event Router config, event id vs Kafka
    offset, consumer idempotency and restart. Same BLOCKED rule as 1.1.
2.2 ADR-001..004: expand each one-liner into these sections:
    - Status
    - Context
    - Decision
    - Alternatives: Option 0 plus at least 2 more, weighted criteria summing to 100, reversibility, pre-mortem
    - Consequences
    - Failure modes -> the T-IDs that will prove them
    - Invariants
    - Reopen conditions
    Keep each decision's meaning. Sharpening is fine; a change of meaning is a STOP. Status line:
    "Proposed — review-ready; owner accepts at G0". Only the owner writes "Accepted".
2.3 ADR-005 (new): docs/adr/ADR_005_OUTBOX_CDC_AND_TRANSPORT_IDENTITY.md.
    - Compare the Debezium Outbox Event Router, capturing the receipt tables directly, and app-side publishing. Say why
      "no CDC" is not an allowed Option 0 under Core scope.
    - Cover topic and key design for app/provider/invoice events. Invoice rows may have no logical_request_id (D4).
    - Cover the snapshot -> stream handoff and the replication slot / WAL retention lifecycle.
    - Explain how source_event_id and transport_delivery_id (D2) stay separate.
2.4 docs/architecture/ERD.md: Mermaid erDiagram for the tables in ARCHITECTURE_DECISIONS §4. Show the PK and the unique
    key that distinguishes each D2 identity (a partial unique index where the column is nullable), tenant-composite keys
    and append-only marks. Add a table mapping each v1 schema field to its column. Mark the whole ERD as planned, not
    implemented.
2.5 docs/architecture/LINEAGE_AND_TRACE.md:
    (a) Mermaid flowchart with trust boundaries marked: source event -> outbox -> manifest/cut -> SQL/dbt path and
        Debezium -> Kafka -> Flink path, plus the oracle -> comparator -> decision -> CAS publication -> read API ->
        Atlas/Lite.
    (b) Per-hop table: artifact, identities carried, the evidence that proves the hop, and where NOT_COMPARABLE,
        INCOMPLETE or UNDETERMINED is decided.
    (c) F1 walked hop by hop with its real ids and values from the P0.2 fixture.
2.6 Diagrams: .drawio/.dot/.svg stay unchanged unless an ADR changes the topology. If one does, STOP (the regeneration
    tooling belongs to P0.4).
2.7 Claims audit:
      rg -n -i "exactly[- ]once|guarantee|completeness|real[- ]time|production[- ]ready" docs contracts README.md
    Put the results in the receipt as a table: hit -> qualified/unqualified -> action. Fix unqualified wording only in
    files this wave owns; list the rest as findings. Negative control: run the same pattern on a temp file outside the repo
    containing "end-to-end exactly-once guarantee" and show that it is found.
2.8 Receipt docs/gates/G0/P0.3_receipt.md. Commit with explicit paths (docs only, so no repo-map refresh unless code
    changed): "docs(p0.3): ADR-001..005, ERD, lineage and F1 trace".
ACCEPTANCE P0.3:
  [ ] Build/inspect: source cut, engine independence, WAL/outbox, CAS, Atlas/Lite trust boundaries reviewed; editable diagrams
  [ ] Artifacts: ADR-001–004 review-ready, ADR-005, ERD, lineage map
  [ ] Verification: F1 trace complete end to end; claims audit shows 0 unqualified claims in owned files
  [ ] Evidence receipt -> docs/gates/G0/P0.3_receipt.md

=== CLOSE THE WAVE ===
- P0.md: tick only boxes whose evidence path exists. Set the Evidence line to the receipt list and update RESUME_POINT.
  P0 stays IN_PROGRESS (P0.4 and G0 remain); milestones.json is unchanged.
- PROJECT_STATUS.md: session log lines and RESUME_POINT (branches, SHAs, next: `/meterproof-advisor review WAVE-01`).
- _agent_ops, per SESSION_PROTOCOL (this list never waives a triggered record):
  - IMPLEMENTATION_LOG: one entry per step.
  - CURRENT_TASK, SESSION_BRIEF.
  - PROJECT_CONTEXT_CARD: durable state.
  - DECISION_LOG: DEC-0007. Any other material decision should have been a STOP instead.
  - RISK_REGISTER: only if a risk changed.
  Then run: python ai-agent-workspace-pack/_agent_ops/tools/closure_check.py --root . --compact, and resolve every row.
- Final checks: pytest green, validator 0, hygiene 0, git diff --check 0, git status clean.
- Final message: one EXECUTION REPORT block per step (Step 0, P0.2, P0.3) in the format of ADVISOR_EXECUTOR_WORKFLOW.md,
  then the list of skill/template files read and a 5-line wave summary.

IN SCOPE (create/edit):
  Step 0: docs/gates/G0/P0.1_receipt.md, docs/ops/REPO_OWNERSHIP_MAP.md, docs/milestones/core/P0.md, docs/ops/PROJECT_STATUS.md
  P0.2: docs/contracts/DOMAIN_SPEC_v1.md; docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md (Gate state line only);
        contracts/jsonschema/*.v1.schema.json; contracts/jsonschema/CHANGELOG.md; tests/fixtures/contracts/**;
        tests/fixtures/README.md (one line); tests/contracts/**; docs/research/{openmeter,lago}-review.md;
        docs/research/OSS_REFERENCE_REGISTER.md (Review column only); docs/gates/G0/P0.2_receipt.md
  P0.3: docs/adr/ADR_00{1,2,3,4}_*.md (rewrite); docs/adr/ADR_005_OUTBOX_CDC_AND_TRANSPORT_IDENTITY.md;
        docs/architecture/ERD.md; docs/architecture/LINEAGE_AND_TRACE.md; docs/research/debezium-outbox-review.md;
        register Review column; unqualified-claim wording in files this wave owns; docs/gates/G0/P0.3_receipt.md
  All steps: P0.md checkboxes/Evidence/RESUME_POINT; PROJECT_STATUS.md; ai-agent-workspace-pack/_agent_ops/
        {IMPLEMENTATION_LOG,DECISION_LOG,RISK_REGISTER,PROJECT_CONTEXT_CARD,CURRENT_TASK,SESSION_BRIEF,REPO_MAP}.md
OUT OF SCOPE:
  - P0.4 work: pyproject/lockfile, the CI workflow, toolchain pins, Docker, LICENSE.
  - Implementation dirs: services/, core/, pipelines/, independent_oracle/, products/, infra/.
  - Everything in ai-agent-workspace-pack/ except the _agent_ops records above.
  - .agents/ .claude/ .codex/ (apart from committing the advisor files unchanged).
  - The overlay package folder; .drawio/.dot/.svg; milestones.json; every other milestone card; tests/fixtures/MP004_F1_SYNTHETIC.json.
STOP AND ASK IF:
  - session_start is not OWNED, or the start state differs from "Expected start".
  - A D-decision conflicts with a frozen contract/protocol statement.
  - A change would alter Core v3.1–v3.3 meaning (an invariant removed or weakened, shared SQL/Flink logic, the oracle
    importing production code).
  - A checkpoint fails.
  - uv needs packages beyond the listed three (and their dependencies).
  - A task needs an out-of-scope path.
  - You would have to invent a business rule.
AUTHORIZATION
  Git: Step 0 commits A and B on p0/p0.1-preflight; create p0/wave-01-p0.2-p0.3 and commit there. Always stage explicit
       paths (never `git add .`); never use --no-verify. NO push, merge, rebase, tag, amend or history rewrite.
  Network (free downloads only):
    - uv may download jsonschema==4.23.0, rfc3339-validator==0.1.4 and pytest==8.3.5 (+ their dependencies) into its cache.
    - git clone --depth 1 of openmeterio/openmeter, getlago/lago and getlago/lago-api (study-only), and
      debezium/debezium-examples, into a temp dir outside the repo.
    - Nothing else.
  Cost: none. No paid API, no provider call, no cloud, no Docker.
Do not claim anything you did not run. Then stop; the advisor reviews with `/meterproof-advisor review WAVE-01`.
```

## After Codex finishes
1. In Claude Code: `/meterproof-advisor review WAVE-01` (re-reviews P0.1 Step 0, then P0.2 and P0.3 separately).
2. After APPROVE the owner merges: first `p0/p0.1-preflight` if it is approved on its own, then `p0/wave-01-p0.2-p0.3` (which contains it), and pushes.
3. Next: WAVE-02 = P0.4 (toolchain pins, lockfile, CI, offline smoke) + the G0 gate packet. It needs the LICENSE decision and an approval for Docker image downloads.
