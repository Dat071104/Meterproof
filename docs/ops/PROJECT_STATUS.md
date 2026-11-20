# METERPROOF project status (project-specific; pack still owns generic handoff)

- **Contract revision:** v3.4 Architecture & Milestone Overlay
- **Design status:** planning only; imported from v3.1/v3.2/v3.3 plus Lite and Atlas extensions
- **Repository:** `D:\DATA_ENGINEER\METERPROOF\Meterproof` → `github.com/Dat071104/Meterproof` (public), branch `main`
- **Roles:** owner approves; Claude Code = advisor/reviewer; Codex = executor (`docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`)
- **Current Core milestone:** P0 / G0 — `IN_PROGRESS` (P0.1–P0.4 evidence complete; unsigned G0 packet drafted; not a gate PASS)
- **Current Lite milestone:** L0 / LG0 — `NOT_STARTED` (requires G2 released contracts)
- **Current Atlas milestone:** A0 / AG0 — `NOT_STARTED` (requires G3 verified read model)
- **Current Adoption milestone:** U0 / UG0 — `NOT_STARTED` (no users claimed)
- **Spike decision:** NOT EXECUTED, NOT APPROVED
- **Approved provider/cloud budget:** none recorded (default: no paid calls/deployment)
- **Approved Git actions for agents:** Codex may commit locally on its work-order branch only; push/merge are owner actions
- **Core tests T01–T12:** all `NOT_RUN`
- **Known external evidence:** none

## Setup log (advisor bootstrap, 2026-11-19 — verified by P0.1, `docs/gates/G0/P0.1_receipt.md`)
1. Cloned the empty GitHub repository; root commit with `README.md`, `.gitignore`, `.gitattributes` (LF normalization for Docker/shell).
2. Embedded the workspace pack from the source checkout `D:\DATA_ENGINEER\METERPROOF\ai-agent-workspace-pack` (clean, version `d4df794`) with `scripts/embed_pack.py --target .` → `ai-agent-workspace-pack/` + fresh `_agent_ops/`, root `AGENTS.md` managed block, `CLAUDE.md`, `GEMINI.md`, `.claude/`, `.codex/`. The first embed came from a CRLF working tree (62/145 manifest hashes would not survive Git's LF normalization), so before any commit the pack folder and generated adapters were removed and re-embedded from a `core.autocrlf=false` clone of the same commit; result 145/145 manifest hashes match, 0 CRLF files (`_agent_ops/DECISION_LOG.md` DEC-0005).
3. Overlay package checksums verified: 86/86 entries of `PACKAGE_MANIFEST_SHA256.json` matched.
4. `install_overlay.py --target .` dry run: 81 ADD, 0 conflicts; then `--apply`; `validate_overlay.py` → PASS (structural only).
5. **Intentional post-install edits to overlay-provided files** (a later installer dry run must list exactly these as CONFLICT):
   - `docs/ops/PROJECT_STATUS.md` — this file: real repository state, roles, setup log, RESUME_POINT.
   - `docs/milestones/core/P0.md` — advisor findings added under "Reviewer note / blockers" only.
   - `tools/meterproof/validate_overlay.py` — status check no longer requires every milestone to be `NOT_STARTED` (that would fail CI as soon as P0 legitimately starts); `PASS`/`HUMAN_GO`/`HUMAN_CONDITIONAL_GO` now require `docs/gates/<GATE>/<GATE>_GATE_RECEIPT.md`; UTF-8 stdout. Tested: positive, PASS-without-receipt (exit 3), unknown status (exit 3).
   - `.github/workflows/meterproof-overlay-contracts.yml` — installs `jsonschema==4.23.0` so schema meta-validation actually runs (it was silently skipped); also runs on push to `main`.
6. **Collision C-1:** pack hygiene forbids tracked `data/*`; overlay ships `data/fixtures/`. The two fixture files are on disk but **not committed**; P0.1 relocates them to `tests/fixtures/`. Until then the hygiene check reports `data/` as a filesystem artifact.
7. Project-authored additions: `docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`, `docs/ops/prompts/P0.1_CODEX.md`, `docs/research/OSS_REFERENCE_REGISTER.md`, `.claude/skills/meterproof-advisor/SKILL.md`, a repository-notes section appended to root `AGENTS.md` outside both managed blocks, Claude-specific lines in `CLAUDE.md`, filled `_agent_ops` memory.

## Recent session log
- 2026-11-19 — advisor bootstrap (above). No implementation code exists. No gate evidence exists.
- 2026-11-19 — Codex completed WAVE-01 Step 0 on `p0/p0.1-preflight` (Commit A `95be8bfe4bf5b934e9727784b534f1bbbd181bbb`; baseline main SHA `2b5f2031c27103fc7f098da6cf073ee3bd547a1a`). P0.1 Verification is checked: installer process exit 2 on both final dry runs; stdout and stderr hashes match independently; two refused `ADD` plans and six conflicts; no installer writes; PACK_MANIFEST 145/145; validator, hygiene, and `git diff --check` pass. Earlier merged-capture hashes differed due stdout buffering/stderr interleaving; retained in the receipt. DEC-0007 retires the installer; `--apply` is never run here. Receipt: `docs/gates/G0/P0.1_receipt.md` (`IN_PROGRESS — evidence complete; advisor re-review pending`). No product tests or paid/cloud calls.

- 2026-11-19 — Codex completed P0.2 on `p0/wave-01-p0.2-p0.3` from Commit B `f895e2d680d58257a9cd2f64c5f9cab356d19c1c`, committed as `5551b243aaed0c81d58aa650ce9e73e5f852ba3b`:  froze the pre-release contract spec, conditional v1 schemas, F1/F2/F3 synthetic fixtures, 20 negative fixtures and contract self-checks. Pre-change control accepted N01-N06, N09-N14 and N16-N20; N07/N08/N15 were already rejected. Final contract suite: 8 passed in Python 3.13.2; validator, hygiene and `git diff --check` rechecks are recorded in the P0.2 receipt. OSS notes: `docs/research/openmeter-review.md` and `lago-review.md` (Lago API checkout path-length limitation recorded; no code copied). Receipt: `docs/gates/G0/P0.2_receipt.md` (`IN_PROGRESS`, advisor review pending); OPEN-Q-1 remains for G1/P1.2. No production/provider calls, real invoices, paid/cloud calls, or product pipeline runs.

- 2026-11-20 — Codex completed P0.3 on `p0/wave-01-p0.2-p0.3` based on P0.2 commit `5551b243aaed0c81d58aa650ce9e73e5f852ba3b`: ADR-001–005 are review-ready Proposed, planned ERD/lineage and F1 trace added, claims audit found 0 unqualified claims in owned files and the negative control was found. Existing editable diagrams were unchanged. Receipt: `docs/gates/G0/P0.3_receipt.md` (`IN_PROGRESS — evidence complete; advisor review pending`). No runtime CDC/Flink, provider/invoice data, paid/cloud calls, or gate sign-off.

- 2026-11-20 — Codex completed WAVE-02 Step 0 (P0.2/P0.3 fix-up) on `p0/wave-01-p0.2-p0.3`: A2 `231d9d72e1ed8c5e6879d00b061c21c1bb1c770c`, C `2c935d6f1f215e125143e9a3f65c4e2426bace63`, D `a75fdba4bf956d6ea601df1e284829d6a74fc951`; Checkpoint 0 passes and advisor re-review is pending. WAVE-02 P0.4 on `p0/wave-02-p0.4-g0` is at implementation/evidence commits `31eb5cd42a32f97f09fcaf0f1ab3e8c1a89bab6d`, `76bf22dfb87dcccdd2f61a7435a13e277437cb53`, `8d656b365151835bd883734f10b57d5391c12e54`, `d5b2a1eed3de1865f0f832bc5abbe4038e4c6e64`, `8acfabf316bd8d4ba2cfc8b47df1a6b9afbf95a1`, `aff1b2f8809b8d52349d8452767c3e96428cb4cd`. The unsigned G0 packet is committed at `c566c5e20e3a74a79006482f89d9327f179f08bd`. Steps 1.5–1.13 pass on a no-hardlinks offline clone at `aff1b2f`; P0.4 receipt: `docs/gates/G0/P0.4_receipt.md`. The full lab (no object store) used ~2.20 GiB across five Meterproof containers; all project containers/volumes were removed. Local CI commands pass; GitHub CI remains NOT RUN until owner push. G0 remains unsigned; ADR-001…006 remain Proposed. No provider/cloud/paid service used, no push or merge.

## RESUME_POINT
- **Current branches / evidence bases:** `p0/wave-01-p0.2-p0.3` at D `a75fdba4bf956d6ea601df1e284829d6a74fc951` (A2 `231d9d72e1ed8c5e6879d00b061c21c1bb1c770c`, C `2c935d6f1f215e125143e9a3f65c4e2426bace63`); `p0/wave-02-p0.4-g0` has clean-checkout source cut `aff1b2f8809b8d52349d8452767c3e96428cb4cd` and G0 packet commit `c566c5e20e3a74a79006482f89d9327f179f08bd`. Earlier P0.1 A/B commits: `95be8bfe4bf5b934e9727784b534f1bbbd181bbb`, `f895e2d680d58257a9cd2f64c5f9cab356d19c1c`; original main base `2b5f2031c27103fc7f098da6cf073ee3bd547a1a`.
- **Current state:** P0.1–P0.4 evidence receipts are present; Checkpoint 0 and Checkpoint 1 pass. G0 packet is drafted unsigned; ADR-001…006 remain Proposed; advisor review and owner signature pending. P0 / G0 remains `IN_PROGRESS`.
- **Known risks/open items:** OPEN-Q-1 on unlinked billed provider records remains deferred to G1/P1.2; artifacts/object store is NOT_PINNED and moves to P3; GitHub CI is not run until owner push; no CDC connector, slot, topic contract or Flink job was exercised. See `RISK_REGISTER.md` and all four G0 receipts.
- **Cost:** no paid API, cloud, or package installation.
- **Last validation:** Fresh no-hardlinks offline clone at `aff1b2f8809b8d52349d8452767c3e96428cb4cd` passed the full runbook; 14 unit/contract tests, two migration tests, all Compose configs, hygiene, validator and ADR score checks passed; no project Docker resources remain. See `docs/gates/G0/P0.4_receipt.md`.
- **Next exact steps:** owner: fast-forward main, push, CI; then `/meterproof-advisor gate G0`
- No provider call, cloud action, push or merge is authorized for agents.

### Update protocol
On every phase transition update per-subphase status, evidence receipt link, open risks, cost tracker, current branch/SHA, last command and exact next command. Do not replace `_agent_ops` handoff; link this file from it.
