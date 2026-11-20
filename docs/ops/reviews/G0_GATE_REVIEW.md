# ADVISOR GATE REVIEW — G0 (Core P0) — NOT_READY

Reviewed: `p0/wave-02-p0.4-g0` @ `f1d28e5`; packet `docs/gates/G0/G0_GATE_RECEIPT.md` (commit `c566c5e`, unsigned).
Date: 2026-11-20 · Reviewer: advisor (Claude Code). The advisor never signs and never edits the receipt status.

## Verdict

**NOT_READY.** Two items block it. When both are closed, G0 becomes READY_FOR_OWNER_SIGNOFF without another full review: the advisor re-runs the probe and the test suite only.

| # | Blocking item | Closed by |
|---|---|---|
| B1 | C6: contract v1 accepts `VERIFIED` with `policy_version = null`, contrary to `DOMAIN_SPEC_v1.md:23`. The contract freezes at merge, so this must be fixed first. | Codex: `docs/ops/prompts/WAVE-02_FIX1_CODEX.md` |
| B2 | GitHub CI has never run. The card's P0.4 artifact list names CI, and the release gate needs evidence linked to the merged commit. | Owner: fast-forward `main` to the branch, push, and confirm `meterproof-ci` (python-checks, secret-scan, compose-and-migrations) and `meterproof-overlay-contracts` are green on that SHA |

## Subphase status

| Subphase | Receipt | Advisor review | State |
|---|---|---|---|
| P0.1 | `docs/gates/G0/P0.1_receipt.md` | `WAVE-01_REVIEW.md`: APPROVE | ok |
| P0.2 | `docs/gates/G0/P0.2_receipt.md` (FIX1 section) | `WAVE-02_REVIEW.md`: CHANGES_REQUESTED (C6 only) | **B1** |
| P0.3 | `docs/gates/G0/P0.3_receipt.md` (FIX1 section) | `WAVE-02_REVIEW.md`: APPROVE | ok |
| P0.4 | `docs/gates/G0/P0.4_receipt.md` | `WAVE-02_REVIEW.md`: APPROVE | ok; CI is **B2** |

## Release-gate checklist (`docs/milestones/core/P0.md`)

| Item | Evidence | State |
|---|---|---|
| All subphases have real, executed evidence linked to the commit and source version | the four receipts; the advisor re-ran 14 tests, lint, types, validator, hygiene, ADR checks and gitleaks | ok after B1 and B2 |
| Negative and failure paths reported; no unsupported completeness or accuracy claims | N01–N33 (N34 after FIX1); the `wal_level` and bad-migration controls; the gitleaks controls; the claims audit with its own negative control. The G0 receipt's limitation table is honest: design-only lineage, synthetic data, no runtime cut | ok |
| Security, cost and scope check; agent and human review recorded | Pinned gitleaks: history and working tree clean, A1-6 controls pass. Cost is none: local Docker only, everything torn down. No cloud and no paid call. Agent review is this file plus `WAVE-02_REVIEW.md`. Human review is the owner signoff | agent part ok; human part = owner |
| G0 receipt PASS with authorized signoff | `G0_GATE_RECEIPT.md`, owner block | owner only |

## What only the owner can do

1. **Accept or reject ADR-001..006**, currently all Proposed:
   - 001: independent processing;
   - 002: source manifest;
   - 003: publication and isolation;
   - 004: two deployment profiles;
   - 005: outbox, CDC and transport identity;
   - 006: toolchain pins.

   The weighted scores are now tool-checked, and every chosen option ranks first.
2. **Push and merge:**
   - `git switch main`;
   - `git merge --ff-only p0/wave-02-p0.4-g0`;
   - `git push origin main`.

   This brings in P0.1–P0.4 and wave-01, because every earlier branch is an ancestor. Then confirm that CI is green.
3. **Sign G0** in the owner block of `docs/gates/G0/G0_GATE_RECEIPT.md`:
   - name, date, `Decision: PASS` (or NO_GO with reasons);
   - notes listing the ADRs accepted;
   - the CI run URL and SHA.

   Set the Status line yourself. Signing means accepting the carried limitations: synthetic-only P0, artifacts NOT_PINNED → P3, OPEN-Q-1 deferred to G1/P1.2, and RISK-0013.

## After signoff

The bookkeeping becomes Step 0 of the next wave, so no separate order is needed:
- ADR statuses → Accepted;
- tick P0.4 Verification and the release-gate boxes in `P0.md`;
- `PROJECT_STATUS` → P1;
- run the validator.

The next wave is P1 (G1 technical spike, P1.1–P1.4). It needs an owner budget and data-source decision before the advisor writes it.
