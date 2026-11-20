# ADVISOR REVIEW — WAVE-01 (Step 0 P0.1 FIX1, P0.2, P0.3)

Reviewed: branch `p0/wave-01-p0.2-p0.3` @ `706563cb94eea3daeb2b6de58347c8a892ca1e84` (contains `p0/p0.1-preflight` @ `f895e2d680d58257a9cd2f64c5f9cab356d19c1c`) vs `main` @ `2b5f2031c27103fc7f098da6cf073ee3bd547a1a` — 2026-11-20.

| Subphase | Verdict |
|---|---|
| Step 0 — P0.1 FIX1 | **APPROVE** |
| P0.2 — Data authority and money contract | **CHANGES_REQUESTED** (fix before merge: contract v1 freezes at merge, D1) |
| P0.3 — Architecture ADR and schema graph | **CHANGES_REQUESTED** (small) |

Fix-up: Step 0 of `docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md` (owner chose to bundle it with P0.4, as in WAVE-01). Owner decisions taken in this review: DEC-0008, DEC-0009, DEC-0010 in `_agent_ops/DECISION_LOG.md`.

## Checks I re-ran (advisor, owner's host, Git Bash)

| Command | Result |
|---|---|
| `git status --porcelain` | empty; HEAD `706563c` |
| `git diff main...HEAD --stat` | 63 files, +4580/−71. Per-commit file lists match the in-scope lists of the order. `.drawio/.dot/.svg`, `replay_manifest.v1`, MP004 fixture unchanged by the wave. `milestones.json` and the MP004 move come from P0.1 commit `9d5c09f`, which was authorized. |
| `python tools/meterproof/validate_overlay.py` | exit 0 |
| `python …/_agent_ops/tools/check_repo_hygiene.py --root . --ops-folder …/_agent_ops` | exit 0, 324 tracked, 0 artifacts. I removed my own `tests/contracts/__pycache__` afterwards, then re-checked: 0. |
| `git diff --check main...HEAD` | exit 0 |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 C:/Python313/python.exe -m pytest -p no:cacheprovider -q tests/contracts` | **8 passed**, exit 0. Environment: Python 3.13.2, jsonschema **4.26.0**, pytest **9.1.1**, which differs from the receipt pins. Without the env var, pytest crashed while autoloading a broken user-site `dash` plugin (`ModuleNotFoundError: click.core`). See I1. |
| Claims-audit pattern from order 2.7 over `docs contracts README.md` (excluding `docs/ops/prompts|reviews`) | 76 hits, the same count as the P0.3 receipt |
| Adversarial schema probe (`scratchpad/probe/probe.py`, outside the repo, mutates F1 and `schema_examples.json` records) | 17 mutants that the contract says are invalid were **accepted** (MISMATCH+DIFFERENT was not probed but is also invalid under DEC-0008). See C1–C3, C5. |
| ADR weighted-score recomputation (`scratchpad/probe/adr_math.py`) | weights = 100 in all 5 ADRs; **arithmetic wrong in ADR-003 and ADR-005** (A1) |

## Step 0 — P0.1 FIX1 — APPROVE

- F1 is fixed. The exit codes are recorded as process exit 2 via `$LASTEXITCODE`, and the shell is named (`docs/gates/G0/P0.1_receipt.md:51-52,65,71`). No "exit 1" remains in the receipt, the ownership map or the status file.
- F2 is fixed with a stronger method than the one I ordered:
  - the per-stream hashes matched across two runs (`P0.1_receipt.md:65`);
  - the earlier merged-capture mismatch is kept, and the fallback that was not run is reported honestly (`:66-67`);
  - DEC-0007 is recorded in `DECISION_LOG.md:42` and `REPO_OWNERSHIP_MAP.md:83`.
- F3 is fixed: the P0.md header, the RESUME_POINT and the status heading were all updated.
- Merge note: `p0/p0.1-preflight` is an ancestor of the wave branch, so merging the wave branch carries it.

## P0.2 — CHANGES_REQUESTED

The spec (`docs/contracts/DOMAIN_SPEC_v1.md`), the CHANGELOG, F1–F3 and N01–N20 are good work. The hand arithmetic is correct, the negative fixtures assert validator+path+property, and the old-schema baseline control is real. The issues below are holes in what the schemas enforce. They must be closed before the merge freezes v1.

- **[High] C1 — business verdict vs comparison status.**
  - `contracts/jsonschema/verification_decision.v1.schema.json:95+` accepts `business_verdict=MISMATCH` together with `comparison_status=NOT_COMPARABLE`, `ERROR` or `DIFFERENT`; the probe accepted all three. `MISMATCH + NOT_COMPARABLE` contradicts `SOURCE_CUT_PROTOCOL.md:16` (§9) and the hard constraint in root `AGENTS.md` ("not-comparable is not mismatch").
  - Root cause: `DOMAIN_SPEC_v1.md:82` and `LINEAGE_AND_TRACE.md:86` merge two axes. They map "invoice differs from policy charge" to comparator `DIFFERENT`. But `DOMAIN_AND_EVIDENCE_CONTRACT.md:23` says the comparator (batch vs stream vs oracle) "is not the business decision". At runtime, F1's SQL, Flink and oracle all compute charge 0.05 against invoice 0.10, so they *agree* (`EQUAL`) while the business verdict is `MISMATCH`.
  - Owner decision **DEC-0008** settles this: `comparison_status` records whether the independent computations agree on a comparable cut. Only `EQUAL` allows a positive conclusion (`VERIFIED` or `MISMATCH`). `DIFFERENT`, `NOT_COMPARABLE` and `ERROR` allow only `INCOMPLETE` or `UNDETERMINED`, and they block the candidate.
  - Required fix: the schema rule, two negatives, the spec truth table, the lineage row and the F1 trace, and a CHANGELOG row.
- **[Medium] C2 — empty-string identities pass "required" rules.** The probe accepted:
  - `provider_generation_id: ""`, `provider_attempt_id: ""` and `provider_amount_evidence_id: ""` on a BILLED receipt;
  - `provider_attempt_id: ""` on APP_OBSERVED_SUCCESS;
  - `billing_period_id: ""` and `source_reference: ""` on INVOICE;
  - `scope: ""` and `coverage_summary: ""` on a VERIFIED decision;
  - `tenant_id: ""` and `coverage_note: ""` on a published report.

  Because generation IDs can be empty, distinct-generation dedup (INV-02) can count every empty generation as the same one. A VERIFIED decision with an empty scope breaks "VERIFIED applies to a declared scope". Fix: add `minLength: 1` to every identity, reference, scope and coverage string, and to the items of the string arrays, in all four schemas.
- **[Medium] C3 — fields cross source authority.** The probe accepted:
  - an APP receipt carrying `known_provider_cost_usd`, `provider_amount_evidence_id`, `provider_generation_id` or `invoice_amount_usd`;
  - a PROVIDER receipt carrying `invoice_amount_usd`;
  - `PROVIDER_CONFIRMED_NOT_BILLED` with `known_provider_cost_usd: "0.0120"`.

  The spec's field-authority table (`DOMAIN_SPEC_v1.md`, rows `known_provider_cost_usd` and `invoice_amount_usd`) says these fields are not authoritative from an app response. This gap comes from the advisor's D4, which only constrained INVOICE; the executor implemented D4 as written. Fix: decision W2-D3 in the WAVE-02 order.
- **[Low] C4 — the self-check cut applies to invoice receipts only.** `tests/contracts/test_expected_facts.py:27,44` (billable and provider facts) ignore `as_known_at`; only invoice facts apply it (`:92`). D3 says a cut includes only receipts first observed at or before `as_known_at`. F1–F3 pass because every APP and PROVIDER receipt is before the cut. Fix: apply the cut to every receipt and add one inline control.
- **[Low] C5 — `customer_charge_usd` scale.** `published_read_report.v1.schema.json:70` accepts `"0.050000"`, but D5 rounds `customer_charge` to 0.01. Fix: add a second constraint of at most 2 fractional digits inside `allOf`, keeping the frozen D5 pattern on the property so the existing pattern test still holds.
- **[Info] I1 — environment drift.** The suite also passes on jsonschema 4.26.0 and pytest 9.1.1, which is good robustness evidence. On this host, though, pytest autoloads plugins from the user site, and one of them is broken. P0.4 must run every check inside the uv-locked environment and set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` in the runbook and CI.
- **[Info] I2.** The digest-determinism test hashes twice in the same process, which proves only purity. P1.4 should compare the oracle's digest against an expected digest pinned in the fixture.
- **[Info] I3.** Cross-field time rules (`first_observed_at` before `occurred_at`) cannot be expressed in JSON Schema. They belong to ingestion validation (P1.1/P2.1). Not a v1 schema defect.

## P0.3 — CHANGES_REQUESTED (small)

The five ADRs have every required section, Option 0 plus at least two alternatives, pre-mortems, T-ID failure modes and reopen conditions. All five stay `Proposed`. ADR-005 (outbox, topic/key design, `source_event_id` vs `transport_delivery_id`, slot/WAL lifecycle) is strong. The ERD maps the D2 identities to keys, including the partial unique index on `provider_generation_id`, and is marked planned. The F1 trace ends at a publication denial and claims no runtime result. The diagrams are unchanged and the claims audit reproduces.

- **[Medium] A1 — weighted totals not actually computed.**
  - `docs/adr/ADR_003_PUBLICATION_AND_ISOLATION.md:26` states A = 3.30 and C = 3.60. Recomputed, they are **3.00** and **4.15**. C's stale-writer score of 4 (`:21`) also contradicts its own pre-mortem: "two operators publish based on stale state" (`:33`).
  - `ADR_005_OUTBOX_CDC_AND_TRANSPORT_IDENTITY.md:51` states B = 2.95; recomputed it is **2.85**.
  - The chosen options still win: ADR-003 B is 4.70 and ADR-005 A is 4.45. But a reviewer who recomputes these tables finds invented numbers, which damages the credibility of evidence that is otherwise accurate. Fix: re-score ADR-003 C consistently with its pre-mortem, recompute every table with a script, and paste the script output into the receipt.
- **[Medium] A2 — C1 carries into P0.3.** `LINEAGE_AND_TRACE.md:86` and the F1 hop-by-hop table must use the DEC-0008 axes: F1 is comparator `EQUAL` on a comparable cut and business verdict `MISMATCH`. A `DIFFERENT` result blocks the candidate as `UNDETERMINED`/`INCOMPLETE` and produces a failure slice (§11). That is the MP-004 regression case.

## Acceptance checks

| Card item | Evidence | Verdict |
|---|---|---|
| P0.1 Verification | `P0.1_receipt.md:51-52,65-71`; advisor re-run | ok |
| P0.2 Build/inspect | `DOMAIN_SPEC_v1.md`, `CHANGELOG.md` | ok after C1/C3 |
| P0.2 Artifacts | 4 schemas; F1–F3; N01–N20; `schema_examples.json` | ok after C1–C3, C5 |
| P0.2 Verification | pytest 8 passed (receipt and advisor re-run); probe found 17 accepted invalid mutants | **missing** until C1–C3 negatives exist and fail first |
| P0.2 Receipt | `docs/gates/G0/P0.2_receipt.md` | ok; append FIX evidence |
| P0.3 Build/inspect + Artifacts | ADR-001…005, ERD, LINEAGE | ok after A1 |
| P0.3 Verification | F1 trace, claims audit 76/0 unqualified, negative control | ok after A2 |
| P0.3 Receipt | `docs/gates/G0/P0.3_receipt.md` | ok; append FIX evidence |

Scope, hygiene and claims:
- Only in-scope paths changed, and the pack files changed only inside `_agent_ops`.
- No secrets, raw provider data or real invoices were committed; all fixtures are `SYNTHETIC`.
- Nothing was pushed or merged, no paid call was made, and `--apply` was never run.
- No PASS was written. The ADRs remain Proposed.

## Owner decisions (taken 2026-11-20, recorded in DECISION_LOG)

- **DEC-0008:** comparator and business verdict are two axes; only `EQUAL` allows `VERIFIED` or `MISMATCH`.
- **DEC-0009:** LICENSE Apache-2.0.
- **DEC-0010:** P0.4 may pull pinned official Docker images (free, local) and run the full local lab once to measure it, then tear down. No cloud, no image push.

Still owner-only after WAVE-02:
- push the branches to trigger CI;
- merge;
- move ADR-001…006 from Proposed to Accepted;
- sign G0.

## Next

1. Paste `docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md` into Codex. Step 0 fixes C1–C5 and A1–A2 on `p0/wave-01-p0.2-p0.3`. P0.4 and the G0 gate packet then run on `p0/wave-02-p0.4-g0`.
2. Then `/meterproof-advisor review WAVE-02` re-reviews P0.2 and P0.3 together with P0.4.
3. Merge `p0/wave-01-p0.2-p0.3` into `main` only after P0.2 and P0.3 are APPROVED.
