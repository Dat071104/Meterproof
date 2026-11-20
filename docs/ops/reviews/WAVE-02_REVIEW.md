# ADVISOR REVIEW — WAVE-02 (Step 0 re-review · P0.4 · G0 packet)

Reviewed: branch `p0/wave-02-p0.4-g0` @ `f1d28e5` vs `main` @ `2b5f203` (main, `origin/main`, `p0/p0.1-preflight` and `p0/wave-01-p0.2-p0.3` are all ancestors, so the branch fast-forwards).
Inputs: Codex EXECUTION REPORTs (Step 0, P0.4, G0 packet), `docs/gates/G0/P0.2_receipt.md`, `P0.3_receipt.md`, `P0.4_receipt.md`, `G0_GATE_RECEIPT.md`, `docs/ops/prompts/WAVE-02_AMENDMENT-01.md`, DEC-0011, DEC-0012.
Date: 2026-11-20 · Reviewer: advisor (Claude Code)

## Verdicts

| Item | Verdict |
|---|---|
| Step 0 — P0.2 FIX1 (contract v1) | **CHANGES_REQUESTED** (one new gap, C6; the C1–C5 fixes are verified) |
| Step 0 — P0.3 FIX1 (ADR scores, two-axis lineage) | **APPROVE** |
| P0.4 — local reproducibility and CI bootstrap | **APPROVE** (GitHub CI evidence follows the owner push; see the G0 gate review) |
| Step 2 — G0 packet (unsigned) | **APPROVE as a draft**; gate readiness is in `docs/ops/reviews/G0_GATE_REVIEW.md` |

## Checks I re-ran

All checks ran in an external uv environment under the advisor scratchpad, with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and caches outside the repository.

| Command | Result |
|---|---|
| `uv sync --locked --all-groups` | exit 0. Python 3.13.2; `dbt --version` reports core 1.11.17 and postgres 1.11.0 |
| `ruff check` / `ruff format --check` on tests and `tools/meterproof` | All checks passed; 9 files already formatted |
| `mypy tests tools/meterproof` | no issues in 8 source files |
| `pytest tests/contracts tests/unit -q` | **14 passed** |
| `validate_overlay.py --target .` | exit 0 |
| `check_repo_hygiene.py --root .` | 0 findings |
| `check_adr_scores.py --root .` | all six ADR tables PASS. ADR-003 and ADR-005 now match an independent recomputation (`scratchpad/probe/adr_math.py`) |
| `git diff --check main...HEAD` | exit 0 |
| Pack manifest | 145/145 SHA-256 entries match |
| gitleaks, pinned `c00b6bd0…` (before the A1-6 config existed) | full-history scan: one finding, `PACK_MANIFEST.json:102`, key `harness/TOKEN_RISK_MATRIX.md`. Its value equals `sha256sum` of that file, so it is a false positive |
| gitleaks with the A1-6 config | history scan and working-tree scan: no leaks. Negative controls in a throwaway repo: 2 findings, exit 1 |
| Adversarial probe re-run (`scratchpad/probe/probe.py`, same mutants as WAVE-01) | every C1–C5 mutant is now rejected. Still accepted: `VERIFIED` with `policy_version = null` (**C6**); `VERIFIED` with `test_receipts = []` (I4); plus records the contract allows on purpose (APP correlation hint, cross-field time order per I3, valid 12+12 money, MISMATCH+EQUAL, UNDETERMINED+DIFFERENT) |

Every compose port binds 127.0.0.1. Every image is pinned as `tag@sha256`. Every Action is pinned by full SHA with a version comment.

**Advisor's own slip, cleaned up.** One probe invocation lost its environment variables, so uv created a repo-local `.venv`. I deleted it immediately and hygiene is back to 0 findings. The ignored `.ruff_cache/` that existed before my run (13:07) is left as found.

## Findings

### P0.2 FIX1

**C6 [Medium] — VERIFIED is accepted without a policy version.**
- *Where:*
  - `contracts/jsonschema/verification_decision.v1.schema.json:84` types `policy_version` as `["string","null"]`, and no rule ties it to the verdict.
  - `docs/contracts/DOMAIN_SPEC_v1.md:23` says: "Missing policy means the calculation scope cannot be VERIFIED."
  - SOURCE_CUT_PROTOCOL §1 pins `policy_version` for every comparable cut.
- *Failure scenario:* a decision with `business_verdict = VERIFIED`, `comparison_status = EQUAL` and `policy_version = null` validates, and it may carry `published_eligible = true`.
- *Why now:* the WAVE-01 probe did not cover this case, and contract v1 freezes at merge.
- *Required fix (FIX1):*
  - add `if business_verdict = VERIFIED then policy_version: {type: string, minLength: 1}`;
  - add a negative fixture N34 that HEAD `f1d28e5` accepts and the fixed schema rejects;
  - add a CHANGELOG line.
  - No other field changes.

**I4 [Info] — `VERIFIED` with an empty `test_receipts` array validates.**
- No v1 rule requires receipts for a verdict, so this is consistent with the spec.
- The rule belongs to the publication gate (P3), not to the schema.
- Recorded only so that it is not treated as an omission later.

### P0.3 FIX1

No findings.
- The ADR checker failed on the original totals and passes on the corrected ones.
- ADR-003 option C is re-scored consistently with its pre-mortem.
- `LINEAGE_AND_TRACE.md:93,103-104` uses the two axes. F1 is `EQUAL` + `MISMATCH`, and the MP-004 path is `DIFFERENT` + `UNDETERMINED`/`INCOMPLETE`. In both, the claim is labelled expected rather than observed.

### P0.4

**I5 [Low] — the installed pack tool now differs from the pack source.**
- *Where:* `ai-agent-workspace-pack/_agent_ops/tools/check_repo_hygiene.py` gained an exact-path exception for `infra/compose/.env.example` (DEC-0012, owner-authorized in the Codex session). The pack source `ai-agent-workspace-pack/scripts/check_repo_hygiene.py` is unchanged. The manifest does not track the installed copy, so 145/145 still holds.
- *Scope:* the order put the pack out of scope (WAVE-02 order, line 379). The owner authorized the exception, so this is not a breach.
- *Failure scenario:* a future pack update reinstalls the tool and drops the exception. Hygiene then fails *closed* on the placeholder, so there is no silent leak, only a red check.
- *Advice for a later wave, not now:*
  - rename the placeholder to a non-dot name such as `infra/compose/compose.env.example`;
  - restore the installed tool to the pack copy.
- Recorded as RISK-0013.

**I6 [Info] — GitHub CI has not run.**
- The workflow exists and the local equivalent passed in a fresh no-hardlinks offline clone at `aff1b2f`.
- The first CI run happens after the owner pushes. It is a G0 blocker, not a P0.4 defect.

**I7 [Info] — measurement and toolchain scope recorded honestly.**
- The full-lab figure (about 2.20 GiB, five containers) excludes the object store (NOT_PINNED → P3). The receipt says so.
- Host JDK 23 is diagnosed and left unchanged. Temurin 17 runs only in containers.

## Acceptance checks

| Item | Evidence | State |
|---|---|---|
| P0.2: C1–C5 negatives N21–N33 accepted at 706563c and rejected after the fix | `tests/fixtures/contracts/negative/N21..N33`, P0.2 FIX1 section, advisor probe | ok |
| P0.2: F1–F3 facts unchanged | `test_expected_facts.py` passes; fixture files untouched | ok |
| P0.2: no VERIFIED without a policy version | — | **missing (C6)** |
| P0.3: ADR scores recomputed by a tool that failed first | `tools/meterproof/check_adr_scores.py`, unit test, P0.3 FIX1 section | ok |
| P0.4: pins chosen from official sources, with dates and local verification | `docs/architecture/TOOLCHAIN_PINS.md`, ADR-006 (Proposed), Amendment 01 | ok |
| P0.4: isolated Docker profiles; lint, types, secret scan, migration smoke | `infra/compose/compose.yaml`, `lab_smoke.py`, `test_migration_smoke.py`, P0.4 receipt | ok |
| P0.4: negative controls fail as intended | `wal_level=replica` gives exit 1; bad migration 0002 rolls back to 0001; gitleaks synthetic and A1-6 controls give exit 1 | ok |
| P0.4: a new clean checkout runs the baseline offline, with no paid service | P0.4 receipt, clone at `aff1b2f` | ok |
| P0.4: GitHub CI green | — | pending the owner push |
| G0 packet: never PASS, signature blank, limitations listed | `docs/gates/G0/G0_GATE_RECEIPT.md:6,9,47-49` | ok |

## Owner decisions needed

None new. DEC-0011 (Amendment 01) and DEC-0012 are already recorded.

## Next

1. Codex runs `docs/ops/prompts/WAVE-02_FIX1_CODEX.md` (C6 only, Light).
2. The advisor runs a quick re-check: the probe plus `pytest`.
3. The owner fast-forwards `main` to `p0/wave-02-p0.4-g0`, pushes, and confirms the CI is green.
4. The owner accepts ADR-001..006 and signs G0, following `docs/ops/reviews/G0_GATE_REVIEW.md`.
