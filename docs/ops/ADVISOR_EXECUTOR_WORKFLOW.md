# Advisor ↔ Executor workflow (Claude Code advises, Codex executes)

This file defines who does what on METERPROOF from P0 to the last gate, and the exact loop used for every subphase. It adds roles on top of `AGENTS.md`; it never relaxes a rule stated there.

## Roles

| Role | Who | Owns | Never does |
|---|---|---|---|
| **Owner / approver** | the repository owner | scope, budget, G1 `HUMAN_GO`, every gate signoff, push/merge to `main`, paid API or cloud spend | delegate a gate signoff to an agent |
| **Advisor / reviewer** | Claude Code (`/meterproof-advisor`) | work orders (the Codex prompt for one subphase), reviews against milestone card + invariants INV-01..INV-12, gate-readiness reviews, research notes, plan corrections | write production code, sign a gate, mark anything `PASS`, push |
| **Executor** | Codex | implementation of exactly one subphase per work order, running tests, gate receipts, status updates, local commits on the work-order branch | widen scope, push, merge, spend, edit pack-managed files |

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

## File conventions

| Artifact | Path | Written by |
|---|---|---|
| Work order | `docs/ops/prompts/<ID>_CODEX.md` | advisor |
| Fix-up order | `docs/ops/prompts/<ID>_FIX<n>_CODEX.md` | advisor |
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
| Next work order | `/meterproof-advisor next` |
| Review executed subphase | `/meterproof-advisor review P0.1` |
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

- `main` only receives reviewed, approved subphases. One branch per subphase.
- Codex may commit on its work-order branch with explicit paths (never `git add .`) when the work order says so. Codex never pushes, merges, force-pushes, or rewrites history.
- Push and merge are owner actions. The owner may authorize the advisor for a specific merge.
- Any commit containing project code runs `python ai-agent-workspace-pack/_agent_ops/tools/refresh_repo_map.py --stage` after tests (pack rule).
