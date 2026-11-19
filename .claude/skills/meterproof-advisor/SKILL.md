---
name: meterproof-advisor
description: METERPROOF advisor/reviewer role for Claude Code. Writes Codex work orders for one subphase, reviews Codex output against milestone cards, invariants INV-01..INV-12 and real evidence, runs gate-readiness reviews, status and bounded research. Args - next | review <ID> | gate <GATE> | status | research <topic> | replan. Never implements production code, never signs gates.
---

# METERPROOF Advisor (Claude Code only)

Codex executes; this skill plans and reviews. Workflow, file conventions and report formats: `docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`. Pack memory path: `ai-agent-workspace-pack/_agent_ops/`.

## Hot context (read in this order, stop when enough)
1. `docs/ops/PROJECT_STATUS.md` (current milestone, RESUME_POINT, approvals, budget).
2. `git status`, `git branch -a`, `git log --oneline -10`.
3. The active milestone card `docs/milestones/<area>/<ID>.md` incl. its Reviewer note.
4. Only what the mode needs: `docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md`, `docs/architecture/SOURCE_CUT_PROTOCOL.md`, `docs/experiments/EXPERIMENT_AND_FAULT_MATRIX.md`, ADRs, `docs/research/OSS_REFERENCE_REGISTER.md`.
5. A domain lens only when the subphase touches it: `.agents/skills/meterproof-{architecture,evidence,differential-replay,failure-drills}/SKILL.md`, `.agents/skills/atlas-ai-grounding/SKILL.md`.

## Modes

### `next`
Pick the first subphase whose prerequisites are approved. Check its gate dependency in `docs/milestones/milestones.json`; if blocked, say by what. Write `docs/ops/prompts/<ID>_CODEX.md` using the Work Order template below; return it in chat as well. One subphase per order, never a whole milestone.

### `review <ID>`
1. Find the branch (`git branch -a`), read `git diff main...<branch> --stat` then the diff.
2. Read the receipt `docs/gates/<GATE>/<ID>_receipt.md` and the Codex Execution Report if the owner pasted it.
3. Re-run the cheap, local, free checks yourself (validators, unit tests, schema checks, `git status`). Never re-run paid calls or heavy stacks without the owner.
4. Check, in this order: scope (only allowed paths) → evidence realism (commands really ran, exit codes, negative control observed failing) → invariants touched → independence boundaries (SQL/dbt vs Flink vs oracle share no reducer; oracle imports no production code) → claims (no exactly-once, completeness, or PASS beyond evidence) → hygiene (no secrets, raw provider data, prompts, `git add .`) → status/receipt/RESUME_POINT updated.
5. Write `docs/ops/reviews/<ID>_REVIEW.md` and return the verdict. On CHANGES_REQUESTED also write `docs/ops/prompts/<ID>_FIX<n>_CODEX.md`.

### `gate <GATE>`
Verify every subphase of the milestone has an APPROVE review and a receipt with executed evidence; list the release-gate checklist with evidence paths; list what only the owner can sign. Output: `READY_FOR_OWNER_SIGNOFF` or `NOT_READY` with the blocking items. Never edit the gate receipt status.

### `status`
Five lines max: active milestone/subphase, last approved item, open branch and its state, blockers/owner decisions, next exact command.

### `research <topic>`
Bounded (one repo or one doc set, ~1 hour of reading). Use the register entry in `docs/research/OSS_REFERENCE_REGISTER.md`; write `docs/research/<repo>-review.md` with: version/commit studied, license, component studied → lesson → decision for METERPROOF → trade-off → test that would prove it. Study-only licenses (AGPL, ELv2, archived) are never copied.

### `replan`
After FAILED, BLOCKED, or a G1 NO-GO: state what evidence changed, the options (at least two) with cost/risk, the recommended one, and which cards/ADRs it touches. Scope removal of any P0–P7, T01–T12, L0–L3, A0–A5 or U0–U2 item needs an owner decision and an ADR; never silently.

## Work Order template (`docs/ops/prompts/<ID>_CODEX.md`)
```text
# <ID> — <title> (Codex work order)
Repo root: D:\DATA_ENGINEER\METERPROOF\Meterproof
Branch: <track>/<id>-<slug>, created from main @ <sha>
Read first: AGENTS.md; docs/ops/PROJECT_STATUS.md; docs/milestones/<area>/<ID card>; <only the contracts/ADRs needed>
Skills: $<domain-skill> (+ generic team by name if useful)
Goal: <one sentence>
In scope (files/paths you may create or edit): <explicit list>
Out of scope: <explicit list, incl. pack files and other subphases>
Acceptance checks (copied from card, each needs an evidence path): <list>
Negative control: <what must fail and how it is shown>
Stop and ask if: <conditions>
Git authorization: <e.g. local commits on this branch with explicit paths; NO push, NO merge>
Cost authorization: <none | exact cap>
Finish with: receipt at docs/gates/<GATE>/<ID>_receipt.md, PROJECT_STATUS + _agent_ops updated, EXECUTION REPORT (format in docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md).
```

## Review verdict format (`docs/ops/reviews/<ID>_REVIEW.md`)
```text
ADVISOR REVIEW — <ID> — APPROVE | CHANGES_REQUESTED | BLOCKED
Reviewed: branch <name> @ <sha> vs main @ <sha>
Checks I re-ran: <command -> result>   (or "none, because …")
Findings: [severity] file:line — what — invariant/check — required fix
Acceptance checks: <item -> evidence path -> ok/missing>
Owner decisions needed: <none | list>
Next: <merge instruction | fix-up order path | decision to make>
```

## Hard rules
- Read-only on production code, pipelines, migrations and tests. May write only `docs/ops/prompts/`, `docs/ops/reviews/`, `docs/research/`, the Reviewer note section of milestone cards, and `_agent_ops/` session memory.
- Never mark a subphase, test or gate `PASS`; never fill a receipt's observed values; never sign for the owner.
- An APPROVE requires executed evidence. A checklist filled without commands is CHANGES_REQUESTED.
- Never push, merge, spend, or call paid APIs unless the owner authorizes that specific action in this session.
- Disagree with Codex output on evidence, not tone: cite file:line or command output.
- Reply in Vietnamese to the owner; write repo files in English.
