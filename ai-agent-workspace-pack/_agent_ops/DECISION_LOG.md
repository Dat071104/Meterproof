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
