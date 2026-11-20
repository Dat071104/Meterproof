# G0 — Core P0 release-gate receipt

| Field | Observed value |
|---|---|
| Gate + subphases | `G0 / P0.1–P0.4` |
| Status | `PASS` — signed by owner Dat, 2026-11-21 (block below) |
| Git branch & SHA | `p0/wave-02-p0.4-g0`; evidence source cut at `aff1b2f8809b8d52349d8452767c3e96428cb4cd` |
| Origin | `SYNTHETIC / N/A — no provider or invoice data used in P0` |
| Owner signoff | Signed PASS by Dat on 2026-11-21 (see block below). |

## Subphase evidence and review

| Subphase | Receipt | Commit SHA(s) | Advisor review path / verdict |
|---|---|---|---|
| P0.1 — Repository preflight | `docs/gates/G0/P0.1_receipt.md` | `95be8bfe4bf5b934e9727784b534f1bbbd181bbb`; `f895e2d680d58257a9cd2f64c5f9cab356d19c1c` | `docs/ops/reviews/WAVE-01_REVIEW.md` — APPROVE; WAVE-02 advisor review covers the full fix-up and P0.4 work. |
| P0.2 — Data authority and money contract | `docs/gates/G0/P0.2_receipt.md` | `231d9d72e1ed8c5e6879d00b061c21c1bb1c770c`; `2c935d6f1f215e125143e9a3f65c4e2426bace63` | `docs/ops/reviews/WAVE-01_REVIEW.md` — CHANGES_REQUESTED; WAVE-02 FIX1 evidence complete, advisor re-review pending. |
| P0.3 — Architecture ADR and schema graph | `docs/gates/G0/P0.3_receipt.md` | `2c935d6f1f215e125143e9a3f65c4e2426bace63`; `a75fdba4bf956d6ea601df1e284829d6a74fc951` | `docs/ops/reviews/WAVE-01_REVIEW.md` — CHANGES_REQUESTED; WAVE-02 FIX1 evidence complete, advisor re-review pending. |
| P0.4 — Local reproducibility and CI bootstrap | `docs/gates/G0/P0.4_receipt.md` | `31eb5cd42a32f97f09fcaf0f1ab3e8c1a89bab6d`; `76bf22dfb87dcccdd2f61a7435a13e277437cb53`; `8d656b365151835bd883734f10b57d5391c12e54`; `d5b2a1eed3de1865f0f832bc5abbe4038e4c6e64`; `8acfabf316bd8d4ba2cfc8b47df1a6b9afbf95a1`; `aff1b2f8809b8d52349d8452767c3e96428cb4cd` | `docs/ops/reviews/WAVE-01_REVIEW.md` P0.4 reviewer note — inputs only; WAVE-02 advisor review pending. |

P0.2/P0.3 remain on `p0/wave-01-p0.2-p0.3`; P0.4 is on `p0/wave-02-p0.4-g0`. Checkpoint 0 and Checkpoint 1 evidence are recorded in their subphase receipts. This draft does not mark any release gate complete.

## P0 release-gate items

| Release-gate item | Evidence / remaining owner action |
|---|---|
| All subphases have executed evidence linked to their commit and source version | `docs/gates/G0/P0.1_receipt.md` through `P0.4_receipt.md`; advisor re-review pending. |
| Negative/failure paths reported; no unsupported source-completeness or global-accuracy claim | Negative controls and claims audit are recorded in the four receipts; Step 2 whole-wave claims audit is recorded below. No runtime provider/invoice evidence is claimed. |
| Security, cost and scope checked; agent and human review recorded | `docs/gates/G0/P0.4_receipt.md`: configured Gitleaks history/working-tree scans and A1-6 controls pass; local Docker-only cost is none; no provider, cloud or paid call. Advisor review and owner review remain pending. |
| G0 receipt has authorized reviewer and owner signature | `OWNER` — advisor gate review and human signoff remain outstanding. |

## ADRs awaiting owner acceptance

ADR-001, ADR-002, ADR-003, ADR-004, ADR-005 and ADR-006 are all `Proposed`. No owner acceptance is recorded.

## Open items and limitations

- GitHub CI: `NOT RUN` until an owner push; local CI commands and offline clean-checkout evidence are in `docs/gates/G0/P0.4_receipt.md`.
- OPEN-Q-1 on unlinked billed provider records is deferred to G1/P1.2.
- Artifacts/object store is `NOT_PINNED`, omitted from Compose and the full profile; the choice moves to P3. No license request was made.
- No CDC connector registration, replication slot, Kafka topic contract, Flink job, dbt project, provider call, invoice data, cloud service, or paid service was exercised.
- The one full-profile measurement excludes an object store and used approximately 2.20 GiB across the five Meterproof containers from rounded `docker stats` values; Docker system disk totals were unchanged before/after teardown.

| Receipt | Limitations carried into G0 |
|---|---|
| P0.1 | Structural preflight only; no product suites/Core pipeline were run. Java was unobserved at preflight (diagnosed later in P0.4). The overlay installer is retired by DEC-0007. Earlier merged captures differed due stdout/stderr buffering/interleaving; final per-stream hashes matched and no installer writes occurred. |
| P0.2 | All fixtures/facts are synthetic; no provider account, invoice export, database or runtime source cut was exercised. The fixture self-check is not the independent P1.4 oracle. OPEN-Q-1 is deferred to G1/P1.2. The receipt records a partial Lago API checkout due Windows path limits. |
| P0.3 | ADR/ERD/lineage artifacts are design-only; no SQL/dbt versus Flink replay was executed, and there is no runtime LSN/offset vector, checkpoint, sink receipt or published report. ADR-001..006 remain Proposed. |
| P0.4 | GitHub CI is NOT RUN until owner push. No connector registration, replication slot, Kafka topic contract, Flink job or dbt project was exercised. `artifacts` is NOT_PINNED → P3; the measured full profile excludes an object store. No provider, invoice, cloud or paid-service data was used. |
| P0.4 human gate item | Verification remains unticked in `P0.md` until the owner signs G0. |

## Whole-wave repository hygiene

| Check | Result |
|---|---|
| Gitleaks full history and working tree | Configured scans report no leaks; the only initial hit was the advisor-reviewed PACK_MANIFEST SHA-256 false positive, cleared by A1-6's exact path-and-shape allowlist. |
| A1-6 negative controls | Both expected controls detected (manifest-path non-hex token and same 64-hex digest under `api_token` in another file), exit 1; values redacted. |
| Generated artifacts and tracked secrets/raw data | Hygiene sweep and clean checkout found no generated caches, lab volumes, raw provider data, invoices or personal data tracked. The only exact placeholder exception is `infra/compose/.env.example`; all other `.env.*` paths remain forbidden. |
| `.gitignore` coverage | `git check-ignore -q` exited 0 for `.venv/placeholder`, `infra/compose/.env`, `__pycache__/placeholder.pyc` and `.pytest_cache/placeholder`. |
| Claims audit scope / command | Generated 54 changed text paths from `git diff 706563cb94eea3daeb2b6de58347c8a892ca1e84..HEAD` plus modified/untracked files; excluded `docs/ops/prompts/` and `docs/ops/reviews/` per WAVE-01 §2.7. Pattern: `exactly[- ]once|guarantee|completeness|real[- ]time|production[- ]ready` (case-insensitive). Local ripgrep lacks `--files-from`, so the same pattern ran against an explicit path argument list. Exit 0; 20 hits across 8 files. |
| Claims-audit hit table | `docs/contracts/DOMAIN_SPEC_v1.md:12,75,93,113-117` (7) — contract scope limits and explicit non-claims; `docs/architecture/LINEAGE_AND_TRACE.md:89` (1) — scope limitation; `docs/adr/ADR_005_OUTBOX_CDC_AND_TRANSPORT_IDENTITY.md:38` and `ADR_006_TOOLCHAIN_AND_VERSION_PINS.md:40` (2) — planned/runtime limitations; `docs/gates/G0/P0.3_receipt.md:16,35,44,53` (4) — audit evidence, command self-reference and diagram caveat; `ai-agent-workspace-pack/_agent_ops/IMPLEMENTATION_LOG.md:710,716,791` (3) — procedural review/verification text; `docs/milestones/core/P0.md:35` and this receipt's release-gate criterion (2) — acceptance requirements. This receipt's pattern literal is hit 20 (line 59, self-reference); no unqualified factual product claim found in changed Markdown. |
| Claims-audit negative control | The same pattern matched the synthetic line in temporary `claims-negative-control-wave02.txt`; exit 0. Temp file removed. |

## Owner signoff

Name: Dat

Date: 2026-11-21

Decision: PASS

Notes:
- **ADRs accepted:** ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006.
- **Green GitHub CI on `main` @ `20ebe5a976db4bc4633aaf52bb154aad979e4bb3`:**
  - meterproof-ci run 44787656181: python-checks, secret-scan and compose-and-migrations all succeeded;
  - overlay run 44787656169 succeeded.
  - Links: https://github.com/Dat071104/Meterproof/actions/runs/44787656181 and https://github.com/Dat071104/Meterproof/actions/runs/44787656169
- **CI fixes made before the green run:**
  - `0cc09bf`: `runner.temp` is not allowed in workflow-level env;
  - `20ebe5a`: shebang scripts marked executable, for ruff EXE001 on Linux.
- **Limitations carried forward:** synthetic-only P0; artifacts NOT_PINNED → P3; RISK-0013.
- Recorded by the advisor (Claude Code) at the owner's explicit instruction in session on 2026-11-21 ("ký", name "Dat"). The decision is the owner's.
