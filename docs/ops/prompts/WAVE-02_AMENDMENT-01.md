# WAVE-02 Amendment 01 — network blockers at P0.4 (Steps 1.2, 1.4, 1.6)

**Date:** 2026-11-20 · **Author:** advisor (Claude Code), applied with the owner's delegation · **Applies to:** `docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md`
**Status:** in force. It overrides the cited W2-D8 and AUTHORIZATION lines only. Every other rule in the order still applies.

## Advisor diagnosis (host, 2026-11-20)

| Endpoint | Result |
|---|---|
| pypi.org, files.pythonhosted.org | reachable |
| registry-1.docker.io, hub.docker.com, quay.io | reachable |
| github.com and api.github.com at the system-DNS answer (57.155.223.240) or the Singapore edge (20.205.243.x) | TCP 443 timeout |
| ghcr.io at 20.205.243.164 | TCP 443 timeout |
| objects/release-assets/pkg-containers.githubusercontent.com (185.199.108–110.x) | TCP 443 timeout |
| github.com and api.github.com at GitHub US addresses (140.82.112.3, 140.82.112.5) | HTTP 200, TLS verified |

The fault is the ISP route to GitHub's Asian edge and its CDN. No proxy is configured and the hosts file has no override. This is a host network condition, not a project defect. The amendments below avoid depending on it wherever there is a principled reason to do so.

## A1-1 — S3-compatible store: NOT_PINNED (this is W2-D8 as written, not an exception)

- The MinIO community image is no longer maintained. Its successor needs a license file.
- W2-D8 requires an "official, maintained image" and forbids third-party rebuilds. Neither MinIO image satisfies that.
- Do **not** request a license. That would mean registering with a vendor and accepting non-OSS terms, which is outside DEC-0010.
- **Do:**
  - mark the `artifacts` profile NOT_PINNED in `TOOLCHAIN_PINS.md` and ADR-006, with the reason and the source URLs read;
  - leave the profile out of `full`;
  - record "artifact-store choice moves to P3".
- **Effect on the measurement:** the full-lab memory figure covers postgres, kafka, connect and flink JM/TM only. State that in the receipt.

## A1-2 — dbt-core pinned to the 1.11 line (supersedes "latest stable dbt-core")

- **Finding:**
  - dbt-core ≥ 1.12.0 depends on `dbt-core-experimental-parser` (2.0.11).
  - On PyPI that package is only a 4.7 KB sdist, and building it downloads a binary from a GitHub release.
  - The `uv.lock` hash covers the stub, not the binary. That breaks lock integrity and the P0.4 "clean checkout runs offline" verification, on any network.
  - dbt-core 1.11.x does not have this dependency (checked against PyPI JSON for 1.11.0, 1.11.6 and 1.11.17).
- **Rule (replaces the dbt-core line of W2-D8):**
  - Pin `dbt-core>=1.11.17,<1.12` and keep `dbt-postgres` at the latest 1.11.x.
  - Python stays 3.13: both packages declare 3.13.
  - **General rule:** no locked package may fetch code at build or install time from outside the locked, hashed artifacts.
- **Verify:**
  - re-lock;
  - `uv.lock` does not contain `dbt-core-experimental-parser`;
  - list every sdist-only package in `uv.lock` and show that it builds without network (the step 1.13 offline clean-checkout run is the proof);
  - `uv run dbt --version` reports 1.11.x and the postgres adapter.
- **Record:**
  - in `TOOLCHAIN_PINS.md` and ADR-006, list dbt-core 1.12 as a rejected option with this reason;
  - reopen condition: the parser ships hashed wheels on PyPI for win_amd64 and manylinux.

## A1-3 — gitleaks from its official Docker Hub repository (replaces `ghcr.io/gitleaks/gitleaks`)

- The gitleaks README lists two official images: `zricethezav/gitleaks` on Docker Hub (the maintainer's account) and `ghcr.io/gitleaks/gitleaks`.
- Use `zricethezav/gitleaks:v8.30.1@sha256:<digest>` both locally and in CI, so there is one pin. The advisor read the Docker Hub index digest as `sha256:c00b6bd0aeb3071cbcb79009cb16a60dd9e0a7c60e2be9ab65d25e6bc8abbb7f` (amd64 and arm64). Re-verify it from the pull or `docker buildx imagetools inspect`.
- Read the README to confirm that both images are listed. See A1-4 for how to fetch it.
- **STOP** if:
  - the README does not list the Docker Hub image; or
  - the digest differs and you cannot explain the difference.

## A1-4 — read-only GitHub access through a per-command address override (for Action SHAs and official pages)

- **Authorized:** read-only access to github.com and api.github.com using a per-command override that points at a GitHub-owned address in 140.82.112.0/20:
  - `git -c http.curloptResolve=github.com:443:140.82.112.3 ls-remote …`
  - `curl --resolve github.com:443:140.82.112.3 …`, and the same pattern for api.github.com with 140.82.112.5.
- **Rules:**
  - TLS verification stays on. Never use `-k`, `--insecure` or `http.sslVerify=false`.
  - No global git config, hosts-file, DNS, proxy or Docker Desktop change.
  - Record the override in the receipt as an environment limitation.
- **Not covered:** `githubusercontent.com` and `ghcr.io` downloads. Nothing in this wave should need them after A1-2 and A1-3. If something still does, STOP for that item only and continue with independent work.

## A1-5 — mypy 1.19.1 (a consequence of A1-2; supersedes "latest stable" for mypy only)

- **Finding (advisor, from PyPI JSON):**
  - dbt-core 1.11.17 requires `pathspec>=0.9,<0.13`.
  - mypy 1.20.0, 1.20.2, 2.0.0 and 2.4.1 all require `pathspec>=1.0.0`.
  - mypy 1.19.1 requires `pathspec>=0.9.0` and declares Python 3.13 support.
  - So 1.19.1 is the newest mypy that resolves in the single lock.
- **Rule:**
  - Pin `mypy==1.19.1`.
  - Keep one lock and one environment. Do not split lint into a separate or conflicting uv group: `uv sync --locked --all-groups` and CI must stay a single resolve.
  - The general W2-D8 rule becomes: "latest stable release **that resolves in the single lock** with the pinned dbt line".
- **Record:**
  - In `TOOLCHAIN_PINS.md`, list mypy 2.4.1 as rejected, with the pathspec conflict as the reason.
  - Reopen condition: the dbt-core pin moves to a line that allows `pathspec>=1.0`.
- **STOP** if any other package hits the same kind of conflict and has no compatible release.

## A1-6 — Step 1.6 gitleaks finding: false positive, cleared with a path- and shape-scoped allowlist

- **Advisor review of the STOP:**
  - The redacted re-run reports a single finding: `ai-agent-workspace-pack/PACK_MANIFEST.json` line 102, rule `generic-api-key`, commit `2b5f203`.
  - The match is the key `"harness/TOKEN_RISK_MATRIX.md"`. The word TOKEN in the file name triggers the rule.
  - The value is that file's SHA-256 digest. Recomputing `sha256sum ai-agent-workspace-pack/harness/TOKEN_RISK_MATRIX.md` gives the identical 64-hex value.
  - It is not a secret. No history rewrite is needed.
  - The manifest belongs to the pack and must not be edited (DEC-0007).
- **Rule:** add `.gitleaks.toml` at the repository root with exactly this content:

  ```toml
  title = "METERPROOF gitleaks config"

  [extend]
  useDefault = true

  [[allowlists]]
  description = "PACK_MANIFEST.json values are SHA-256 file digests (key names such as TOKEN_RISK_MATRIX.md trip generic-api-key)"
  condition = "AND"
  regexTarget = "secret"
  paths = ['''^ai-agent-workspace-pack/PACK_MANIFEST\.json$''']
  regexes = ['''^[0-9a-f]{64}$''']
  ```

  - Pass `--config .gitleaks.toml` explicitly in local runs, in `DEV_BOOTSTRAP.md` and in the CI secret-scan job.
  - Do not use a `.gitleaksignore` fingerprint, a rule disable, a broader path, or `--no-git` instead.
- **Advisor pre-check** (pinned image `c00b6bd0…`, run in the advisor scratchpad):
  - full-history `git` scan with the config: no leaks found;
  - working-tree `dir` scan with the config: no leaks found;
  - negative control, a throwaway repo, still exits 1 and reports both:
    - a token-shaped non-hex value inside `ai-agent-workspace-pack/PACK_MANIFEST.json` (shape not allowlisted);
    - the same 64-hex digest under an `api_token` key in another file (path not allowlisted).
- **Codex reproduces** all four results and records them in `P0.4_receipt.md`, in the same redacted form.
- **STOP** if any other finding appears.
- **Then** resume Step 1.6 with the working-tree scan, and continue to Step 1.7 and onward.

## Record-keeping (Codex)

- Append **DEC-0011** to `_agent_ops/DECISION_LOG.md`: "WAVE-02 Amendment 01 (A1-1..A1-6): S3 store NOT_PINNED → P3; dbt-core 1.11 line, no build-time network fetch; gitleaks via the official Docker Hub repo; read-only GitHub via per-command address override with TLS verification; mypy 1.19.1 for a single-lock resolve with dbt 1.11; PACK_MANIFEST digest false positive cleared by a path- and shape-scoped `.gitleaks.toml` allowlist, with negative controls".
- Cite this file in `P0.4_receipt.md`, `TOOLCHAIN_PINS.md` and ADR-006.
- Commit this file in the first P0.4 commit, by explicit path.
- If the owner restores normal GitHub access later, A1-2 and A1-3 still stand, because they rest on integrity and single-pin grounds. A1-4 simply becomes unnecessary.
