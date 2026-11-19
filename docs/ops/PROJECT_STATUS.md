# METERPROOF project status (project-specific; pack still owns generic handoff)

- **Contract revision:** v3.4 Architecture & Milestone Overlay
- **Design status:** planning only; imported from v3.1/v3.2/v3.3 plus Lite and Atlas extensions
- **Repository:** `D:\DATA_ENGINEER\METERPROOF\Meterproof` → `github.com/Dat071104/Meterproof` (public), branch `main`
- **Roles:** owner approves; Claude Code = advisor/reviewer; Codex = executor (`docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`)
- **Current Core milestone:** P0 / G0 — `IN_PROGRESS` (P0.1 evidence complete; WAVE-01 P0.2/P0.3 remain; not a gate PASS)
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

## RESUME_POINT
- **Current branch / evidence base:** `p0/p0.1-preflight`, WAVE-01 Step 0 checked at Commit A `95be8bfe4bf5b934e9727784b534f1bbbd181bbb`, based on main SHA `2b5f2031c27103fc7f098da6cf073ee3bd547a1a`.
- **Current state:** P0 / G0 is `IN_PROGRESS`; P0.1 evidence is complete in `docs/gates/G0/P0.1_receipt.md`; continue P0.2/P0.3 on the WAVE-01 branch, then request advisor review; no gate is signed.
- **Known risk:** the external overlay package still ships the two fixtures under `data/`; its refused plan lists them as ADD. DEC-0007 retires the installer here: never run `--apply`; future changes use reviewed diffs. See `docs/ops/REPO_OWNERSHIP_MAP.md`.
- **Cost:** no paid API, cloud, or package installation.
- **Last validation:** WAVE-01 Step 0 validator exit 0; repo-hygiene exit 0; `git diff --check` exit 0; pack manifest 145/145.
- **Next exact command:** after Commit B, `git switch -c p0/wave-01-p0.2-p0.3`.
- No provider call, cloud action, push or merge is authorized for agents.

### Update protocol
On every phase transition update per-subphase status, evidence receipt link, open risks, cost tracker, current branch/SHA, last command and exact next command. Do not replace `_agent_ops` handoff; link this file from it.
