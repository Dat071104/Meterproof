# Repository Ownership Map — P0.1

## Inventory basis

- Repository: `D:\DATA_ENGINEER\METERPROOF\Meterproof`
- Branch: `p0/p0.1-preflight`, created from `main` at `2b5f2031c27103fc7f098da6cf073ee3bd547a1a`.
- Pack session check: `OWNED` by this project; embedded pack version `d4df794`.
- Embedded pack manifest: 145 entries checked from a temporary directory with `python -I`; 0 mismatches.
- Overlay package manifest: 86 entries checked from a temporary directory with `python -I`; 0 mismatches.
- Baseline overlay dry run, before P0.1 edits: exactly four `CONFLICT (no overwrite)` entries listed below; every other overlay entry was `SKIP_IDENTICAL`; `AGENTS.md` was `SKIP_IDENTICAL`; no files were written.
- Post-change overlay dry run: exit 1 and no writes; six conflicts (the original four plus the authorized `REPOSITORY_STRUCTURE.md` and `milestones.json` edits) and two `ADD` plans for the moved fixtures under `data/`; `AGENTS.md` remained `SKIP_IDENTICAL`.
- Baseline overlay validator: exit 0. Its negative control set P0 to `PASS` in a temporary repository copy without a G0 gate receipt; validator exit 3 with the expected failure.
- Hygiene check: initially found only the untracked `data/` artifact; after C-1 relocation it exited 0 with no filesystem artifacts.

This map classifies what was present and how it is maintained. The architecture tree is a target proposal; it does not mean the listed implementation exists.

## Ownership inventory

| Path | Owner class / observed contents | Who may edit | How it is updated | Evidence |
| --- | --- | --- | --- | --- |
| `.agents/skills/{atlas-ai-grounding,meterproof-architecture,meterproof-differential-replay,meterproof-evidence,meterproof-failure-drills}/SKILL.md` | Overlay-provided; project-owned after install | Project owner or authorized executor under a work order | Manual project change; overlay installer only after a dry run and review | All five paths were `SKIP_IDENTICAL` in the baseline installer output; overlay manifest matched 86/86. |
| `.claude/agents/{bug_fixer,bug_hunter,repo_hygiene_reviewer,tester}.md` | Pack-managed generated adapters | Pack maintainers own source; project agents do not hand-edit generated pointers | `ai-agent-workspace-pack/scripts/embed_pack.py --target . --update` | Root `AGENTS.md` and pack `BOOTSTRAP.md` identify these as generated pointers; pack manifest matched 145/145. |
| `.claude/skills/{advisor-team,analyze-team,bug-fix-team,build-team,clean-code-team,handoff-team,prompting-team,repo-hygiene-team,tester-team}/SKILL.md` | Pack-managed generated skill pointers | Pack maintainers own source; project agents do not hand-edit generated pointers | `embed_pack.py --target . --update` | Root `AGENTS.md` and `BOOTSTRAP.md`; embedded pack hashes match. |
| `.claude/skills/{atlas-ai-grounding,meterproof-architecture,meterproof-differential-replay,meterproof-evidence,meterproof-failure-drills}/SKILL.md` | Overlay-provided thin references; project-owned after install | Project owner or authorized executor under a work order | Manual project change; overlay installer after dry run and review | Baseline installer reported each as `SKIP_IDENTICAL`; overlay manifest matched. |
| `.claude/skills/meterproof-advisor/SKILL.md` | Project-authored | Project owner/advisor; executor only under an explicit work order | Manual | Listed as a project-authored addition in `PROJECT_STATUS.md` Setup log. |
| `.codex/agents/{bug_fixer,bug_hunter,repo_hygiene_reviewer,tester}.toml` | Pack-managed generated adapters | Pack maintainers own source; project agents do not hand-edit generated pointers | `embed_pack.py --target . --update` | Root `AGENTS.md` and pack `BOOTSTRAP.md`; embedded pack hashes match. |
| `.github/workflows/meterproof-overlay-contracts.yml` | Overlay-provided; project-owned after install | Project owner or authorized executor under a work order | Manual project change; overlay installer after dry run and review | Expected baseline conflict. Diff from package adds `jsonschema==4.23.0` installation and a push-to-main trigger. |
| `.git/` | Generated local Git metadata | Git only, via authorized Git commands | Git operations | `git status`, branch, remote, and log commands; not part of the project file inventory. |
| `.gitattributes` | Project-authored repository configuration | Project owner or authorized executor under a work order | Manual | Present in the root commit and controls line-ending normalization. |
| `.gitignore` | Project-authored repository configuration | Project owner or authorized executor under a work order | Manual; this work order changed only the local-data comment | Current file; comments now describe fixtures under `tests/fixtures/` and local untracked data. |
| `AGENTS.md` | Mixed: pack-managed generated block, overlay project addendum, and project-authored notes | Pack maintainers for the pack block; overlay updates through its installer; project owner for notes | `embed_pack.py --update`, overlay installer after dry run, and manual notes | Baseline dry run reported `AGENTS.md: SKIP_IDENTICAL`; root file contains the managed markers and project addendum/notes. |
| `CLAUDE.md` | Mixed: pack-generated adapter and project-authored Claude role instructions | Pack maintainers for generated adapter; project owner for project-specific lines | `embed_pack.py --target . --update`; manual project-specific lines | Pack bootstrap says it writes the root adapter; setup log records Claude-specific additions. |
| `GEMINI.md` | Pack-managed generated adapter | Pack maintainers own source; project agents do not hand-edit | `embed_pack.py --target . --update` | Pack bootstrap says it writes the root adapter; embedded pack manifest matched. |
| `README.md` | Project-authored | Project owner or authorized executor under a work order | Manual | Present in the root commit. |
| `ai-agent-workspace-pack/` | Pack-managed embedded distribution | Pack maintainers own source; project agents do not edit distribution files | Update from the source pack with `scripts/embed_pack.py --target . --update` | Version `d4df794`; 145/145 manifest entries matched. |
| `ai-agent-workspace-pack/_agent_ops/` | Pack memory: durable project records plus machine-local session scratch | Session agents may update records required by `SESSION_PROTOCOL.md`; do not change pack logic | Manual memory updates; generated reports/maps use their documented helpers | `session_start.py` reported ownership `OWNED`; durable-vs-local tracking follows `repo-hygiene-team` policy. |
| `contracts/` | Overlay-provided schemas; project-owned after install | Project owner/authorized executor for the applicable milestone; P0.2 owns schema changes | Manual, only in an approved milestone | Four schemas were `SKIP_IDENTICAL`; contract changes are outside P0.1. |
| `core/` | Overlay-provided architecture boundary documents; project-owned after install | Project owner/authorized executor in the milestone that authorizes implementation | Manual in the owning milestone | Four boundary docs were `SKIP_IDENTICAL`; executable implementation is absent (see below). |
| `data/` | **ABSENT after C-1.** Initially contained only two untracked overlay fixtures; removed after the move | Local-only manifests/samples may be owner-managed but remain untracked | Local data only; no implementation data is added by P0.1 | Initial hygiene failure named only `data/`; both fixture hashes matched after relocation; final hygiene found 0 artifacts. |
| `docs/` | Mixed: overlay-provided, project-owned after install, and project-authored operations/research docs | Project owner/advisor/executor under the applicable work order | Manual; overlay updates only after dry run and review | Baseline dry run had expected conflicts for `P0.md` and `PROJECT_STATUS.md`; other listed overlay docs were identical. The workflow, prompt, and research register are identified in the setup log; this map is a P0.1 deliverable. |
| `independent_oracle/` | Overlay-provided architecture boundary placeholder; project-owned after install | Project owner/authorized executor in an approved milestone | Manual in the owning milestone | Boundary document was `SKIP_IDENTICAL`; oracle implementation is absent. |
| `infra/` | Overlay-provided architecture boundary placeholders; project-owned after install | Project owner/authorized executor in an approved infrastructure milestone | Manual in the owning milestone | `infra/compose` and `infra/cloud` boundary docs were `SKIP_IDENTICAL`; runnable configuration is absent. |
| `pipelines/` | Overlay-provided architecture boundary placeholders; project-owned after install | Project owner/authorized executor in an approved pipeline milestone | Manual in the owning milestone | dbt, Debezium, and Flink boundary docs were `SKIP_IDENTICAL`; executable pipeline code/config is absent. |
| `products/` | Overlay-provided architecture boundary placeholders; project-owned after install | Project owner/authorized executor in an approved Lite/Atlas milestone | Manual in the owning milestone | Lite and Atlas boundary docs were `SKIP_IDENTICAL`; product implementations are absent. |
| `services/` | Overlay-provided architecture boundary placeholders; project-owned after install | Project owner/authorized executor in an approved service milestone | Manual in the owning milestone | Four service boundary docs were `SKIP_IDENTICAL`; service implementations are absent. |
| `tests/` | Mixed: overlay boundary placeholder plus project-owned fixture files moved from the overlay | Project owner/authorized executor under a test or fixture work order | Manual; preserve synthetic origin and fixture hashes | `tests/fault/ARCHITECTURE_BOUNDARY.md` was `SKIP_IDENTICAL`; the two fixture files were moved unchanged. Executable test suites are absent. |
| `tools/` | Overlay-provided validator; project-owned after install | Project owner/authorized executor under a work order | Manual in the authorized phase; validate with the documented command | Expected baseline conflict; diff confirms status validation and gate-receipt enforcement additions. |

## Planned implementation paths that are absent

The paths below are named by `docs/architecture/REPOSITORY_STRUCTURE.md` as target structure, not as existing code. Where a parent directory exists, it currently contains only an `ARCHITECTURE_BOUNDARY.md` placeholder unless noted.

- **ABSENT — services implementation:** source for `services/ingestion_api/`, `services/durable_worker/`, `services/verification_api/`, and `services/publication/`.
- **ABSENT — Core implementation:** executable code in `core/evidence/`, `core/policy_spec/`, `core/replay/`, and `core/comparator/`.
- **ABSENT — pipelines:** dbt models/config, Debezium runtime configuration, and Flink Java source under `pipelines/dbt/`, `pipelines/debezium/`, and `pipelines/flink_java/`.
- **ABSENT — independent oracle:** the pure Python reducer under `independent_oracle/`.
- **ABSENT — product implementations:** Lite application/CLI/SDK under `products/lite/` and Atlas application under `products/atlas/`.
- **ABSENT — runnable infrastructure:** compose profiles and cloud templates under `infra/compose/` and `infra/cloud/`.
- **ABSENT — executable test suites:** `tests/unit/`, `tests/contracts/`, `tests/integration/`, `tests/cdc/`, `tests/security/`, `tests/mutations/`, and `tests/e2e/`; `tests/fault/` has only its boundary placeholder. `tests/fixtures/` now contains the two relocated synthetic fixture files, not executable tests.
- **ABSENT — local data directories:** `data/manifests/` and `data/samples/`; these remain local-only paths and were not created.
- **ABSENT — root `LICENSE`:** the owner decision recorded in `_agent_ops/SESSION_BRIEF.md` remains open; no license file was created.

## Collision register

### Baseline installer conflicts observed before P0.1 edits

| Path | Observed reason, confirmed by package-to-repository diff | Owner decision |
| --- | --- | --- |
| `.github/workflows/meterproof-overlay-contracts.yml` | Adds schema-checker installation pinned to `jsonschema==4.23.0` and runs the workflow on pushes to `main`. | No decision pending for P0.1; listed as an intentional setup edit. |
| `docs/milestones/core/P0.md` | Replaces the scaffold `NOT_REVIEWED` placeholder with advisor reviewer notes/blockers. | No decision pending for P0.1; listed as an intentional setup edit. |
| `docs/ops/PROJECT_STATUS.md` | Adds repository/role state, the unverified setup log, recent session log, and resume point. | No decision pending for P0.1; listed as an intentional setup edit. |
| `tools/meterproof/validate_overlay.py` | Allows milestone status progression, requires a gate receipt for passing statuses, and configures UTF-8 stdout. | No decision pending for P0.1; listed as an intentional setup edit. |

All four were the only baseline conflicts; all other overlay entries were identical and the installer wrote nothing. The required P0.1 changes to `PROJECT_STATUS.md` and `P0.md` remain project-owned changes. The one-line C-1 update to `docs/architecture/REPOSITORY_STRUCTURE.md` was made **after** this baseline dry run; it is an authorized project edit and will differ from the packaged source on a future installer dry run.

### Additional differences after the authorized P0.1 edits

| Path / installer plan | Reason | Owner decision |
| --- | --- | --- |
| `docs/architecture/REPOSITORY_STRUCTURE.md` — `CONFLICT` | The P0.1 order required the one-line C-1 relocation note; baseline dry run had shown this path identical. | No decision pending for this work order; change is authorized and documented. |
| `docs/milestones/milestones.json` — `CONFLICT` | The P0.1 order required P0 status to advance to `IN_PROGRESS`. | No decision pending for this work order; change is authorized and documented. |
| `data/fixtures/MP004_F1_SYNTHETIC.json`, `data/fixtures/README.md` — `ADD` | The overlay package still contains these paths, while C-1 moved the repository copies to `tests/fixtures/`. The additive installer plans to add any packaged path missing from the target. | No `--apply` was run. Review package-level C-1 maintenance before any future apply. |

These post-change results do not alter the successful baseline no-overwrite check. They show that the current post-change plan still offers the relocated fixtures under `data/`; the installer refuses the plan because of the conflicts and writes nothing. The C-1 re-add plan needs owner/advisor review before any future `--apply`. The P0.1 `Verification` checkbox remains unchecked for that reason.

### C-1 — fixtures under `data/`

Pack hygiene forbids tracking `data/*` and flags a root `data/` directory. The overlay supplied `data/fixtures/README.md` and `data/fixtures/MP004_F1_SYNTHETIC.json`; both were untracked before this work. The work order authorized moving them unchanged to `tests/fixtures/` and removing the empty `data/` tree. Their SHA-256 values were identical before and after the move:

| File | Before SHA-256 | After SHA-256 | Result |
| --- | --- | --- | --- |
| `README.md` | `09DF89F84542035DB8B48F4BC37A3C7276FD78E2C0C52C0A33738729C9E22C6D` | `09DF89F84542035DB8B48F4BC37A3C7276FD78E2C0C52C0A33738729C9E22C6D` | equal |
| `MP004_F1_SYNTHETIC.json` | `11234F3E1541F09F53240334DAF08DB4E165AC9CBC8DC72D7DE1B1C43DD50832` | `11234F3E1541F09F53240334DAF08DB4E165AC9CBC8DC72D7DE1B1C43DD50832` | equal |

The order is the owner approval for this relocation; no further C-1 decision is pending for P0.1. The external overlay package remains unchanged and still contains the original `overlay/data/fixtures/` paths. The post-change dry run confirmed that it plans to add those two files under `data/` again and reports the authorized repository-structure and milestone-status edits as two additional conflicts. Do not reapply the overlay to this repository without reviewing the plan. Resolving package-level reinstallation behavior is outside this work order.
