# Decision Log / Nhat ky quyet dinh

## DEC-0001 — Repository layout (2026-11-19)

- **Context:** GitHub repo was empty; `D:\DATA_ENGINEER\METERPROOF` held the source pack clone (with its own `.git` and the pack's own `_agent_ops`), the overlay zip/extraction and PDFs.
- **Options:** A) make `D:\DATA_ENGINEER\METERPROOF` the repo (nested pack `.git`, foreign memory, zip/PDF in tree); B) clone into `D:\DATA_ENGINEER\METERPROOF\Meterproof` and embed the pack from the outside source checkout.
- **Decision:** B.
- **Rationale:** fresh project-owned memory, no nested repository, source pack stays updatable with `embed_pack.py --update`, source material stays out of the public repo.
- **Consequences:** the parent folder is a workspace for source material; the repo root is `Meterproof/`.

## DEC-0002 — Advisor/executor split (2026-11-19)

- **Context:** owner wants Claude Code as advisor from start to finish and Codex as executor.
- **Decision:** one subphase per work order; Codex implements on a branch and commits locally; Claude reviews diff + receipt and re-runs cheap checks; owner merges, pushes, signs gates. Defined in `docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md`; Claude skill `.claude/skills/meterproof-advisor/`.
- **Consequences:** slower per subphase, but each merge on `main` has an independent review and an evidence trail.

## DEC-0003 — Just-in-time open-source study (2026-11-19)

- **Context:** an external research pass proposed studying 12+ repositories, partly inside P0.
- **Decision:** keep the list in `docs/research/OSS_REFERENCE_REGISTER.md`; study each only at the milestone that needs it, bounded, with a review file; AGPL/ELv2/archived are study-only.
- **Rationale:** P0 must freeze contracts, not become a reading phase; the proposed "new ideas" already exist in v3.4 (P5.4 capsule, publication gate).

## DEC-0004 — Validator status rule (2026-11-19)

- **Context:** `validate_overlay.py` asserted every milestone is `NOT_STARTED`, so CI would fail as soon as P0 legitimately started.
- **Decision:** allow the contract's gate states; `PASS`/`HUMAN_GO`/`HUMAN_CONDITIONAL_GO` require `docs/gates/<GATE>/<GATE>_GATE_RECEIPT.md`. CI installs `jsonschema==4.23.0` so schema checks run.
- **Evidence:** positive run exit 0; PASS without receipt exit 3; unknown status exit 3 (scratch copy, 2026-11-19).

## DEC-0005 — Re-embed the pack from an LF checkout (2026-11-19)

- **Context:** `PACK_MANIFEST.json` hashes raw bytes. The source pack checkout uses `core.autocrlf=true`, so 62/145 shipped files were CRLF on disk while Git stores LF (this repo's `.gitattributes` forces `eol=lf`). Fresh clones would mismatch 62 manifest hashes and `embed_pack.py --update` would treat them as host-modified.
- **Decision:** before the first commit, removed the just-created pack folder and generated root adapters, re-ran `embed_pack.py` from a `core.autocrlf=false` clone of the same commit `d4df794` (scratch dir), restored the filled memory files.
- **Consequences:** manifest hashes equal Git-normalized bytes. Future `--update` must also run from an LF checkout. Upstream fix recommended in the pack repository: ship a `.gitattributes` (`* text=auto eol=lf`) or hash normalized bytes.

## DEC-0006 — Waves allowed (owner, 2026-11-19)

- **Context:** after P0.1 the owner allowed larger prompts ("prompt phase lớn / wave lớn cũng được") and asked that every prompt load its skills explicitly.
- **Decision:** a work order may run several consecutive subphases as a wave. It never crosses an owner-signed gate or an unapproved cost. Each subphase keeps its own receipt, commit, checkpoint and review verdict. Policy decisions are pre-approved in the order as D1…Dn. Every order starts with `@start-here` and a START_HERE tiered skill-loading block. Rules: `docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md` → Waves.
- **Trade-off:** fewer round-trips and less copy-paste, but larger diffs per review and a later stop when something goes wrong. The per-subphase checkpoints and verdicts contain that risk.
- **First use:** WAVE-01 = P0.1 FIX1 + P0.2 + P0.3. P0.4 stays separate (dependencies, Docker downloads, LICENSE).

## DEC-0007 — Overlay installer retired (owner, 2026-11-19)

- **Context:** After the first import, a refused dry run still planned two `ADD` entries for `data/fixtures/`, which had been relocated to `tests/fixtures/`; six intentional conflicts caused refusal before any write.
- **Decision:** Overlay installer retired for this repository after the first import (2026-11-19). Future overlay revisions are merged by reviewed diff under a work order; install_overlay.py --apply is never run here. The two ADD lines for data/fixtures/ are plan output of a refused run, not writes.
- **Evidence:** Final clarified dry-run pair returned process exit 2 twice; stdout SHA-256 matched across runs (`F23FA1BCE8BEFBDEA0461BDEA48D53834E20D4CFF35F2DCA9D2C71E73C4F270A`), stderr SHA-256 matched (`C60AE641A8E3E398CC7437F768C781CD10713BB235B2B02553FA93352F45BD97`); no installer-created Git changes; PACK_MANIFEST 145/145.
- **Consequences:** Do not run this installer with `--apply` in this repository. Merge future overlay changes only as a reviewed diff under an owner-authorized work order.

## DEC-0008 — Comparison status and business verdict are two axes (owner, 2026-11-20)

- **Context:** WAVE-01 review C1. `DOMAIN_SPEC_v1.md` truth table and `LINEAGE_AND_TRACE.md` mapped "invoice differs from policy charge" to comparator `DIFFERENT`, while `DOMAIN_AND_EVIDENCE_CONTRACT.md:23` says the comparator (batch vs stream vs oracle) is not the business decision. `verification_decision.v1` accepted `MISMATCH` with `NOT_COMPARABLE`/`ERROR`/`DIFFERENT`, contradicting SOURCE_CUT_PROTOCOL §9.
- **Decision:** `comparison_status` states whether the independent computations (SQL/dbt, Flink, oracle where applicable) agree on a comparable cut. `business_verdict` states what the evidence says about the declared scope. Only `EQUAL` permits a positive conclusion, `VERIFIED` or `MISMATCH`. `DIFFERENT`, `NOT_COMPARABLE` and `ERROR` permit only `INCOMPLETE` or `UNDETERMINED`, block the candidate and require a failure slice (§11). F1 = `EQUAL` + `MISMATCH`. The MP-004 wrong-rule regression = `DIFFERENT` + `UNDETERMINED` (or `INCOMPLETE` when a known segment is missing).
- **Options rejected:** allow `DIFFERENT` + `MISMATCH` (an engine disagreement is not evidence about the bill); keep the spec table and patch only §9 (still contradicts contract line 23 when F1 runs for real).
- **Consequences:** contract v1 is edited in place before freeze (WAVE-02 Step 0). A positive claim, in either direction, needs independent agreement.

## DEC-0009 — License Apache-2.0 (owner, 2026-11-20)

- **Decision:** the public repository is licensed Apache-2.0 (patent grant; same family as the Flink/Kafka/Debezium references). WAVE-02 adds the canonical `LICENSE` text. Study-only references (AGPL/ELv2) are still never copied.
- **Closes:** RISK-0008 once `LICENSE` is committed and merged.

## DEC-0010 — P0.4 local Docker authorization (owner, 2026-11-20)

- **Decision:** WAVE-02 may pull pinned official images (PostgreSQL, Kafka, Debezium Connect, Flink, an S3-compatible store only if an official maintained image exists, gitleaks, and a JDK 17 build image), run per-profile smoke checks, and run the full local lab once to measure memory/disk. It must then tear everything down (`down -v`, no leftover containers/volumes). No cloud, registry push, paid API or public port. Host ports bind to 127.0.0.1 only.

## DEC-0011 — WAVE-02 Amendment 01, P0.4 dependency, network route and Gitleaks allowlist (owner-delegated advisor amendment, 2026-11-20)

- **Context:** WAVE-02 P0.4 could not complete `uv sync` with dbt-core 1.12.7 because `dbt-core-experimental-parser` builds by fetching an unhashed binary from GitHub. The host's normal route to GitHub and GHCR also times out. The advisor issued `docs/ops/prompts/WAVE-02_AMENDMENT-01.md` with the owner's delegation; A1-1 through A1-6 override only the cited W2-D8 and AUTHORIZATION lines.
- **Decision:** apply A1-1..A1-6: artifacts `NOT_PINNED`, omitted from `full`, object-store choice P3 and no license request; dbt-core `>=1.11.17,<1.12` with the latest dbt-postgres 1.11.x and Python 3.13; Gitleaks via the maintainer's Docker Hub image at its verified digest; official GitHub reads by per-command address override to `140.82.112.3` with TLS verification; mypy pinned to 1.19.1, the newest version resolving in the one lock with dbt 1.11; `.gitleaks.toml` has exactly one AND allowlist scoped to the pack manifest path and 64-lowercase-hex digest shape. Do not split the uv groups or edit the pack manifest/history.
- **Evidence:** the Gitleaks README lists both images; Docker Hub reports the v8.30.1 index digest `sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f`; `git ls-remote` resolves both action tags through the approved override. Full lock sync has 69 packages; `dbt --version` reports core 1.11.17 and postgres 1.11.0; lock scan finds no experimental parser and 0 sdist-only entries. Mypy 2.4.1's `pathspec>=1.0.0` conflicts with dbt-core 1.11.17's `pathspec<0.13`; A1-5 authorizes 1.19.1. A1-6 classifies the original `PACK_MANIFEST.json` digest hit as a false positive; configured history and working-tree scans report no leaks, and controls detect the non-hex manifest token and digest under `api_token` elsewhere (2 findings, exit 1).
- **Consequences:** no license request, GHCR pull, global Git/network/DNS/hosts/proxy setting, or Docker Desktop setting change. The full-lab measurement excludes an object store. Gitleaks false positive is cleared with no pack manifest or history changes; configured scans and negative controls pass. Step 1.7 full profile and measurement pass; any new finding triggers STOP.

## DEC-0012 — Exact hygiene exception for the required Compose placeholder (owner, 2026-11-20)

- **Context:** W2-D9 requires a tracked `infra/compose/.env.example`, but the existing `ai-agent-workspace-pack/_agent_ops/tools/check_repo_hygiene.py` treated every tracked `.env.*` file as forbidden. In the first offline clean clone, the runbook hygiene command exited 1 on this required placeholder, so Checkpoint 1 could not pass.
- **Decision:** allow only the exact path `infra/compose/.env.example` in the tracked-file and filesystem-artifact checks. Keep all other `.env.*` paths forbidden; do not change the placeholder path or loosen the pattern globally.
- **Evidence:** added an exact one-path exception and unit controls for the allowed Compose example, `infra/compose/.env.local`, and `other/.env.example`. The 14-test Step 1.5 suite and local hygiene check pass. The offline clean checkout must be repeated.
- **Consequences:** this owner-authorized exception is narrow and tied to the W2-required placeholder. Checkpoint 1 remains pending until Step 1.13 passes with the updated checker.
