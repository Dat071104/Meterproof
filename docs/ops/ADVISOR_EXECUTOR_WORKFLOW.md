# Advisor ↔ Executor workflow (Claude Code advises, Codex executes)

This file defines who does what on METERPROOF from P0 to the last gate, and the exact loop used for every subphase. It adds roles on top of `AGENTS.md`; it never relaxes a rule stated there.

## Roles

| Role | Who | Owns | Never does |
|---|---|---|---|
| **Owner / approver** | the repository owner | scope, budget, G1 `HUMAN_GO`, every gate signoff, push/merge to `main`, paid API or cloud spend | delegate a gate signoff to an agent |
| **Advisor / reviewer** | Claude Code (`/meterproof-advisor`) | work orders (the Codex prompt for one subphase), reviews against milestone card + invariants INV-01..INV-12, gate-readiness reviews, research notes, plan corrections | write production code, sign a gate, mark anything `PASS`, push |
| **Executor** | Codex | implementation of exactly the subphase(s) of one work order (one subphase, or one owner-approved wave), running tests, gate receipts, status updates, local commits on the work-order branch | widen scope, push, merge, spend, edit pack-managed files |

Both agents read the same repository on the same machine, so nothing needs to be copy-pasted between them except the work order text and the Codex execution report.

## The loop (one subphase at a time)

```text
 Owner                     Claude Code (advisor)                Codex (executor)
   |  /meterproof-advisor next  |                                    |
   |--------------------------->| reads status + milestone card      |
   |                            | writes docs/ops/prompts/<ID>_CODEX.md
   |<---------------------------| returns work order                 |
   |  paste work order ----------------------------------------------->|
   |                            |                    branch, implement, test,
   |                            |                    receipt, status, local commit
   |<------------------------------------------------ EXECUTION REPORT|
   |  /meterproof-advisor review <ID>                                  |
   |--------------------------->| reads diff + receipt, re-runs checks|
   |<---------------------------| APPROVE / CHANGES_REQUESTED / BLOCKED
   |  (APPROVE) owner merges/pushes; (CHANGES) paste fix-up order ---->|
```

1. **Work order.** `/meterproof-advisor next` produces `docs/ops/prompts/<ID>_CODEX.md`: scope, files allowed, acceptance checks copied from the milestone card, negative control, stop conditions, git authorization and the required report format.
2. **Execute.** Owner pastes the work order into Codex from the repository root. Codex works only on branch `<track>/<id>-<slug>` (for example `p0/p0.1-preflight`).
3. **Report.** Codex ends with the Execution Report below and writes the receipt under `docs/gates/<GATE>/<ID>_receipt.md`.
4. **Review.** `/meterproof-advisor review <ID>` reads `git diff main...<branch>`, the receipt and the card, re-runs the cheap checks itself, and returns one verdict.
5. **Close.** On `APPROVE` the owner merges the branch into `main` (or authorizes the advisor to do it) and pushes. On `CHANGES_REQUESTED` the advisor writes `docs/ops/prompts/<ID>_FIX<n>_CODEX.md`. On `BLOCKED` the owner decides.
6. **Gate.** When every subphase of a milestone is approved, `/meterproof-advisor gate <GATE>` runs a gate-readiness review. Only the owner turns `docs/gates/<GATE>/<GATE>_GATE_RECEIPT.md` into `PASS` (or `HUMAN_GO` for G1).

Subphase receipts never say `PASS`. The executor writes `IN_PROGRESS — evidence complete; advisor review pending` (or `BLOCKED`/`FAILED` with the reason). The pass record of a subphase is the advisor's `APPROVE` in `docs/ops/reviews/` plus the owner's gate signature.

## Waves (owner-approved, 2026-11-19 — DEC-0006)

A wave is one work order that runs several consecutive subphases, to cut round-trips.

- **Boundaries:** a wave never crosses a gate that needs an owner signature (G0 sign-off, G1 `HUMAN_GO`) or a cost or authorization the owner has not granted. A wave may start with a fix-up of the previous subphase (Step 0).
- **Inside the wave:** each subphase keeps its own acceptance checks, receipt, commit(s) and status update. There is a **checkpoint** after each subphase: if any acceptance check lacks evidence, the wave stops there and reports.
- **Decisions:** the advisor puts every business or policy decision the wave needs into the order as numbered pre-approved decisions (D1…Dn). Pasting the order approves them. A conflict with a frozen contract statement is a STOP, never a choice made by the executor.
- **Files and branch:**
  - order: `docs/ops/prompts/WAVE-<nn>_<first>-<last>_CODEX.md`
  - branch: `<track>/wave-<nn>-<first>-<last>`
  - review: `docs/ops/reviews/WAVE-<nn>_REVIEW.md`, with one verdict per subphase. A wave can be partly approved.
- **Mode:** sequential, single writer. The order states that autonomous mode is confirmed for its in-scope paths, so the executor does not stop for per-slice plan confirmation.

## Skill loading block (required in every work order)

Every order starts with `@start-here <one line>`. It then lists the Context Intake Tiers from `ai-agent-workspace-pack/START_HERE.md`:

- **Tier 0:** root and pack `AGENTS.md`, `START_HERE.md`, `session_start.py` (must report OWNED), `SESSION_BRIEF`/`OPERATING_RULES`/`CURRENT_TASK`, `PROJECT_STATUS.md`, this file.
- **Tier 1, per step:** the pack team `ai-agent-workspace-pack/<team>/SKILL.md` and the project skill `$meterproof-*` (`.agents/skills/<name>/SKILL.md`). Each is read when its step starts.
- **Tier 2:** only the templates those skills reference that are actually used.
- **Tier 3:** the project files named in the step's READ list.

The executor lists every skill/template file it read in the report. Default routing:

| Work | Pack team | Project skill |
|---|---|---|
| contracts, schemas, fixtures, pricing, evidence states | `build-team` | `$meterproof-evidence` |
| ADRs, architecture, CDC/Kafka/Flink design | `analyze-team` | `$meterproof-architecture` |
| source cut, SQL vs Flink comparison, CAS publication | `build-team` | `$meterproof-differential-replay` |
| T01–T12, crash/restart, fault receipts | `tester-team` / `bug-fix-team` | `$meterproof-failure-drills` |
| Atlas read-only AI | `build-team` | `$atlas-ai-grounding` |
| staging, commits, public-repo checks | `repo-hygiene-team` | — |

## File conventions

| Artifact | Path | Written by |
|---|---|---|
| Work order | `docs/ops/prompts/<ID>_CODEX.md` | advisor |
| Fix-up order | `docs/ops/prompts/<ID>_FIX<n>_CODEX.md` (or Step 0 of the next wave) | advisor |
| Wave order / wave review | `docs/ops/prompts/WAVE-<nn>_<first>-<last>_CODEX.md` / `docs/ops/reviews/WAVE-<nn>_REVIEW.md` | advisor |
| Subphase receipt | `docs/gates/<GATE>/<ID>_receipt.md` (from `docs/gates/GATE_RECEIPT_TEMPLATE.md`) | executor |
| Advisor review | `docs/ops/reviews/<ID>_REVIEW.md` | advisor |
| Gate receipt | `docs/gates/<GATE>/<GATE>_GATE_RECEIPT.md` | executor drafts, owner signs |
| Project status | `docs/ops/PROJECT_STATUS.md` | executor, after each subphase |
| Session memory / handoff | `ai-agent-workspace-pack/_agent_ops/` | whichever agent ran the session |
| Research notes | `docs/research/<repo>-review.md` | executor or advisor, per register |

`ai-agent-workspace-pack/_agent_ops/` is the path that overlay docs call `_agent_ops/`.

## Codex Execution Report (required at the end of every work order)

```text
EXECUTION REPORT — <ID>
Branch / HEAD SHA:        <branch> / <sha>
Files changed:            <explicit list>
Commands run:             <command> -> exit <code>   (one per line, real only)
Acceptance checks:        [x]/[ ] each card item -> evidence path
Negative control:         <what should fail, did it fail, evidence>
Receipt:                  docs/gates/<GATE>/<ID>_receipt.md
Deviations from order:    <none | what and why>
Open questions:           <none | for advisor/owner>
Status written:           PROJECT_STATUS.md + _agent_ops updated (yes/no)
RESUME_POINT:             <exact next command>
```

## Advisor verdicts

- **APPROVE** — every acceptance check has executed evidence; negative control observed failing; no invariant regression; scope respected.
- **CHANGES_REQUESTED** — fixable inside the same subphase; comes with a fix-up order.
- **BLOCKED** — needs an owner decision (budget, policy, scope, pivot) or evidence that cannot be produced locally.

A verdict never upgrades a gate. "Reviewed by advisor" is recorded in the receipt's reviewer row alongside, not instead of, the owner signoff.

## How to call things

**Claude Code (advisor, in VS Code or terminal):**

| Need | Type |
|---|---|
| Next work order | `/meterproof-advisor next` (one subphase) or `/meterproof-advisor next wave` |
| Review executed subphase / wave | `/meterproof-advisor review P0.1` / `/meterproof-advisor review WAVE-01` |
| Gate readiness | `/meterproof-advisor gate G0` |
| Where are we / what is blocked | `/meterproof-advisor status` |
| Bounded research before an ADR | `/meterproof-advisor research debezium-outbox` |
| Re-plan after a failure or NO-GO | `/meterproof-advisor replan` |
| Domain lenses during review | `/meterproof-architecture`, `/meterproof-evidence`, `/meterproof-differential-replay`, `/meterproof-failure-drills`, `/atlas-ai-grounding` |
| Generic pack teams | `/advisor-team`, `/analyze-team`, `/tester-team`, `/repo-hygiene-team`, `/handoff-team` |

**Codex (executor, from the repository root):**

| Need | Type |
|---|---|
| Run a work order | paste the content of `docs/ops/prompts/<ID>_CODEX.md` |
| Domain skill explicitly | `$meterproof-evidence`, `$meterproof-architecture`, `$meterproof-differential-replay`, `$meterproof-failure-drills`, `$atlas-ai-grounding` (or `/skills`) |
| Generic pack team | name it in the prompt: `Use build-team …`, `Use bug-fix-team …`, `Use tester-team …` (routed through `AGENTS.md`) |
| Pause / resume | `docs/ops/PAUSE_RESUME.md` |

## Git policy for this workflow

- `main` only receives reviewed, approved subphases. One branch per subphase or per wave.
- Exit codes in receipts are process exit codes (`$LASTEXITCODE` in PowerShell, `$?` in bash), never PowerShell's `$?` boolean.
- Codex may commit on its work-order branch with explicit paths (never `git add .`) when the work order says so. Codex never pushes, merges, force-pushes, or rewrites history.
- Push and merge are owner actions. The owner may authorize the advisor for a specific merge.
- Any commit containing project code runs `python ai-agent-workspace-pack/_agent_ops/tools/refresh_repo_map.py --stage` after tests (pack rule).
