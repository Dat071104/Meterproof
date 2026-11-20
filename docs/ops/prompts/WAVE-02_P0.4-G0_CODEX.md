# WAVE-02 — WAVE-01 fix-up → P0.4 → G0 gate packet (Codex work order)

Paste everything inside the fence into Codex, started from the repository root.

**Owner note.** Pasting this order approves:
- the owner decisions DEC-0008 (two-axis verdicts), DEC-0009 (Apache-2.0) and DEC-0010 (local Docker), already recorded in `_agent_ops/DECISION_LOG.md`;
- the pre-approved decisions W2-D1…W2-D10;
- the downloads listed under AUTHORIZATION.

Edit them before pasting if you disagree.

**Size: Very Heavy.** It has three steps and one Docker lab, runs sequentially with one writer, and can take hours. It stops at a failed checkpoint, so you can paste it and leave it running. Docker Desktop must be running before you paste.

```text
@start-here Execute METERPROOF WAVE-02 exactly as written below: Step 0 (WAVE-01 FIX1 for P0.2/P0.3), then P0.4, then
the G0 gate packet.

ROLE
You are the EXECUTOR. Claude Code is the advisor/reviewer; the repository owner approves. The advisor wrote this order and
the owner pasted it: it authorizes everything under AUTHORIZATION and nothing else.

Repo root: D:\DATA_ENGINEER\METERPROOF\Meterproof
Expected start: branch p0/wave-01-p0.2-p0.3 @ 706563cb94eea3daeb2b6de58347c8a892ca1e84 with exactly these
advisor-authored uncommitted paths (commit them unchanged in Step 0; do not edit them):
  docs/ops/reviews/WAVE-01_REVIEW.md                       (new)
  docs/ops/prompts/WAVE-02_P0.4-G0_CODEX.md                (new, this order)
  docs/milestones/core/P0.md                               (Reviewer note section only)
  ai-agent-workspace-pack/_agent_ops/DECISION_LOG.md       (DEC-0008..0010 appended)
  ai-agent-workspace-pack/_agent_ops/RISK_REGISTER.md      (RISK-0003/0008 updated, RISK-0011 added)
  ai-agent-workspace-pack/_agent_ops/IMPLEMENTATION_LOG.md (advisor entry appended)
Anything else uncommitted or a different HEAD -> STOP.

MODE: Very Heavy. Sequential, single writer, no subagents. Autonomous mode is confirmed for the in-scope work of this
wave: write your plan into CURRENT_TASK.md and proceed; do not wait for build-team step-7 confirmation. Stop only on a
STOP condition or a failed checkpoint.

ENVIRONMENT RULES (all steps; the reason is in WAVE-01_REVIEW I1 and RISK-0003)
- Until the uv project exists (Step 1.4), run Python checks exactly as WAVE-01 did:
    uv run --no-project --python C:\Python313\python.exe --with jsonschema==4.23.0 --with rfc3339-validator==0.1.4 --with pytest==8.3.5 python -m pytest tests/contracts -q
  with a writable UV_CACHE_DIR outside the repo. From Step 1.4 on, use `uv run` inside the locked project only.
- Always set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and PYTHONDONTWRITEBYTECODE=1. Run pytest with -p no:cacheprovider and mypy
  with MYPY_CACHE_DIR outside the repo, so the hygiene check never meets generated caches.
- Record sys.executable and sys.version for every environment that produces evidence.
- Exit codes are process exit codes ($LASTEXITCODE in PowerShell), never PowerShell's $? boolean.

=== SESSION START AND SKILL LOADING (Context Intake Tiers of ai-agent-workspace-pack/START_HERE.md) ===
Tier 0, once:
  1. AGENTS.md (root) -> ai-agent-workspace-pack/AGENTS.md -> ai-agent-workspace-pack/START_HERE.md
  2. python ai-agent-workspace-pack/_agent_ops/tools/session_start.py --root .     (must report OWNED)
  3. ai-agent-workspace-pack/_agent_ops/SESSION_BRIEF.md, OPERATING_RULES.md, CURRENT_TASK.md
  4. docs/ops/PROJECT_STATUS.md; docs/ops/ADVISOR_EXECUTOR_WORKFLOW.md (Waves, EXECUTION REPORT);
     docs/ops/reviews/WAVE-01_REVIEW.md; _agent_ops/DECISION_LOG.md DEC-0008..0010
  5. ai-agent-workspace-pack/TEAM_ROUTER.md. Routing is pre-decided below; do not load other teams.
Tier 1, per step: read these SKILL.md files when the step starts, not before.
  | Step               | Pack team: ai-agent-workspace-pack/<team>/SKILL.md | Project skill: .agents/skills/<name>/SKILL.md |
  | 0  WAVE-01 FIX1    | build-team                                          | $meterproof-evidence, $meterproof-differential-replay |
  | 1  P0.4            | build-team, then tester-team for 1.13 (clean checkout) | $meterproof-failure-drills (lab smoke, teardown) |
  | 2  G0 gate packet  | repo-hygiene-team                                   | $meterproof-evidence                         |
Tier 2: only the templates you use: build-team/PONYTAIL_RULES.md + SELF_REVIEW_CHECKLIST.md; analyze-team/
  OPTIONS_DEBATE_TEMPLATE.md for ADR-006 only; docs/gates/GATE_RECEIPT_TEMPLATE.md.
Tier 3: the project files in each step's READ list.
Business rules source: _agent_ops/PROJECT_CONTEXT_CARD.md "Business Rules & Acceptance Criteria" +
docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md + docs/contracts/DOMAIN_SPEC_v1.md + DEC-0008 + W2-D1..D10 below. Anything
they do not cover is a STOP question, never a guess. List every skill/template file you read in the final report.

=== STEP 0 — WAVE-01 FIX1: P0.2 and P0.3 (branch p0/wave-01-p0.2-p0.3) ===
Why: docs/ops/reviews/WAVE-01_REVIEW.md findings C1–C5 (P0.2) and A1–A2 (P0.3). Contract v1 is still a pre-release
draft (D1 of WAVE-01): edit the v1 files in place and log every change in contracts/jsonschema/CHANGELOG.md.
0.1 Commit A2: stage exactly the six advisor paths above. Message: "docs(advisor): WAVE-01 review, WAVE-02 order, DEC-0008..0010".

DECISIONS PRE-APPROVED BY THE OWNER (Step 0). Implement them; do not re-decide. A conflict with a frozen statement in
DOMAIN_AND_EVIDENCE_CONTRACT.md or SOURCE_CUT_PROTOCOL.md is a STOP; report it with file:line.
W2-D1 (C1, DEC-0008) verification_decision.v1: add to allOf
      if comparison_status in {DIFFERENT, NOT_COMPARABLE, ERROR} then business_verdict in {INCOMPLETE, UNDETERMINED}.
      This makes MISMATCH imply EQUAL; VERIFIED already implies EQUAL.
      DOMAIN_SPEC_v1.md:
      - add a short section "Comparison status vs business verdict (DEC-0008)";
      - rewrite the truth table so that each row names both axes. F1 = EQUAL + MISMATCH. The MP-004 wrong-rule regression
        = DIFFERENT + UNDETERMINED (INCOMPLETE when a known segment is missing): the candidate is blocked and a failure
        slice is required (SOURCE_CUT_PROTOCOL §11). NOT_COMPARABLE/ERROR never yield VERIFIED or MISMATCH.
      Keep every other row's meaning.
W2-D2 (C2) In all four v1 schemas, add minLength 1 to every property typed string or [string, null] that has no
      pattern/enum/const/format, and to the string items of every array of strings. Do not add, remove or rename fields,
      and do not change any required list.
W2-D3 (C3) source_receipt.v1:
      - APP must not carry known_provider_cost_usd, provider_amount_evidence_id or invoice_amount_usd. Each is absent
        or null; invoice_amount_usd is absent. APP may still carry provider_generation_id, because an app can see it in a
        provider response. It is a correlation hint only and not spend evidence (spec field-authority table, P1.2).
      - PROVIDER must not carry invoice_amount_usd.
      - PROVIDER_CONFIRMED_NOT_BILLED: known_provider_cost_usd is absent or null.
      Express "absent" with {"not": {"required": [...]}} and "null" with {"const": null} plus the frozen D5 pattern. The
      D5 walk in test_contract_schemas.py reads child.get("pattern") and breaks on a boolean false schema. Update the
      spec's D4 table to match.
W2-D4 (C5) published_read_report.v1 customer_charge_usd: keep the frozen D5 pattern on the property and add an "allOf"
      inside that property with pattern ^(0|[1-9][0-9]{0,11})(\.[0-9]{1,2})?$ (at most 2 fractional digits, D5).
W2-D5 (C4) tests/contracts/test_expected_facts.py:
      - apply the as_known_at cut to every receipt before any fact is computed;
      - list excluded receipts of every source kind in source_exclusions with their reason;
      - expected facts of F1–F3 must not change; if one does, STOP;
      - add one inline control: an APP_OBSERVED_SUCCESS first observed after the cut adds no billable unit and appears
        in source_exclusions.
W2-D6 (A1) ADR scores:
      - add tools/meterproof/check_adr_scores.py, stdlib only, ≤150 lines. For every docs/adr/ADR_*.md that has a
        "Criterion | Weight" table, it checks that the weights sum to 100 and that each stated weighted total equals
        sum(weight×score)/100 exactly (Decimal). It exits 1 on any mismatch and prints criterion-level detail.
      - add tests/unit/test_check_adr_scores.py with one correct and one wrong inline table.
      - run it on the current ADRs first and record that it fails on ADR-003 and ADR-005 (negative control). Then:
        * re-score ADR-003 option C "Stale-writer prevention" to a value consistent with its own pre-mortem ("two
          operators publish based on stale state") and add one justification sentence;
        * recompute every ADR total;
        * re-run the checker (exit 0).
      - the decisions must not change; if a chosen option no longer ranks first, STOP.
W2-D7 (A2) docs/architecture/LINEAGE_AND_TRACE.md: use the DEC-0008 axes in the comparator row (line 86) and in the F1
      hop-by-hop walk. F1 = independent candidates expected to agree (EQUAL; this is not observed, because there is no
      runtime) + business MISMATCH -> publication denied. Add the DIFFERENT path (MP-004 regression) as a blocked
      candidate. Any ADR sentence that repeats the old mapping gets the same correction.

0.2 Test-first. Before editing any schema, write these negative fixtures. Each must hold target_schema + instance +
    expected_error, like N01–N20:
      N21 MISMATCH + NOT_COMPARABLE            N22 MISMATCH + DIFFERENT             N23 MISMATCH + ERROR
      N24 PROVIDER BILLED provider_generation_id ""   N25 APP_OBSERVED_SUCCESS provider_attempt_id ""
      N26 INVOICE source_reference ""          N27 VERIFIED decision scope ""        N28 published report tenant_id ""
      N29 APP with known_provider_cost_usd     N30 APP with invoice_amount_usd       N31 PROVIDER with invoice_amount_usd
      N32 PROVIDER_CONFIRMED_NOT_BILLED with known_provider_cost_usd "0.0120"
      N33 published report customer_charge_usd "0.050"
    Run them against the schemas at HEAD 706563c (copy them to a temp dir outside the repo) and record that every one
    of N21–N33 is wrongly accepted. Add positive examples to tests/fixtures/contracts/schema_examples.json under a new
    key "additional_verification_decisions": an F1-shaped EQUAL + MISMATCH decision (published_eligible false) and a
    DIFFERENT + UNDETERMINED decision. Extend test_every_positive_contract_record_validates to validate them.
0.3 Apply W2-D1..D7. Afterwards N01–N33 must all be rejected for their declared reason and every positive must validate.
    The F1–F3 expected facts must be unchanged.
0.4 Receipts: append a "WAVE-01 FIX1" section to docs/gates/G0/P0.2_receipt.md (C1–C5) and to P0.3_receipt.md (A1–A2).
    Each section holds commands, exit codes, the HEAD-706563c acceptance list for N21–N33, the checker output before and
    after, and SHA-256 values of the changed schema/fixture files. Keep each Status at "IN_PROGRESS — evidence complete;
    advisor re-review pending".
0.5 Run pytest over tests/contracts AND tests/unit with the ENVIRONMENT RULES command (green), the validator (0), the
    hygiene check (0) and git diff --check (0). Then make two commits with explicit paths:
      Commit C: "fix(p0.2): close contract v1 gaps (DEC-0008 axes, non-empty ids, source-authority fields)"
                (schemas, CHANGELOG, spec, fixtures, tests/contracts, P0.2 receipt). Run
                python ai-agent-workspace-pack/_agent_ops/tools/refresh_repo_map.py --root . --ops-folder ai-agent-workspace-pack/_agent_ops --stage
                before committing, because test code changed.
      Commit D: "fix(p0.3): verified ADR scores, two-axis lineage and F1 trace"
                (ADRs, LINEAGE, check_adr_scores.py + its test, P0.3 receipt; refresh the repo map again).
CHECKPOINT 0: continue only if
- N21–N33 were accepted at 706563c and are rejected now;
- F1–F3 facts are unchanged;
- check_adr_scores failed before and passes now;
- all four checks are green.
Otherwise stop the wave and report.

=== BRANCH FOR P0.4 AND G0 ===
git switch -c p0/wave-02-p0.4-g0     (from p0/wave-01-p0.2-p0.3 after Commit D). Record the SHAs.

=== STEP 1 — P0.4 Local reproducibility and CI bootstrap (gate G0) ===
Skills: build-team + $meterproof-failure-drills (read now); tester-team at 1.13.
READ: docs/milestones/core/P0.md (P0.4 + Reviewer note "P0.4" and "WAVE-01 review"); docs/architecture/
  {STACK_AND_CAPABILITIES,REPOSITORY_STRUCTURE,SECURITY_PRIVACY_COST}.md; docs/adr/ADR_004_*.md, ADR_005_*.md;
  infra/compose/ARCHITECTURE_BOUNDARY.md; .github/workflows/meterproof-overlay-contracts.yml; .gitignore;
  ai-agent-workspace-pack/_agent_ops/RISK_REGISTER.md (RISK-0001..0004, 0007, 0008).
GOAL: a fresh clone reaches a verified local baseline without any paid service: one command set for pinned toolchain,
lint/types/secret scan, contract and fixture validation, migration smoke and Docker lab profiles. CI encodes the same
checks.

DECISIONS PRE-APPROVED BY THE OWNER (Step 1). If no version satisfies a rule, STOP with the evidence; never pick a
version that breaks a rule.
W2-D8 Version selection.
  - Sources: only official sources (project release pages and docs compatibility tables, PyPI JSON metadata, the
    official image registries). For each pin, record in the pin manifest: URL, date checked, what the source states,
    and the command that verified the pin locally.
  - Python: 3.13 if the latest stable dbt-core AND dbt-postgres declare 3.13 support (requires-python/classifiers) and
    the whole lock resolves; otherwise 3.12. Managed by uv: .python-version + requires-python "==3.<minor>.*".
  - Java: JDK 17 (Eclipse Temurin), used only inside containers (Flink image; a maven:*-eclipse-temurin-17 build image).
    Never use the host JDK. Diagnose the host `java -version` hang (where.exe java, PATH shim vs JVM, 20 s timeout) and
    record it only; do not fix the host.
  - Flink: the newest Flink release for which an officially released flink-connector-kafka version declares
    compatibility AND an official flink:<ver>-java17 image exists. Record both versions (RISK-0002).
  - Debezium: the newest stable (Final) release. Its docs must list the chosen PostgreSQL major, and the official image
    quay.io/debezium/connect:<ver> must exist.
  - PostgreSQL: the newest major (≥14) that the chosen Debezium supports; official postgres image.
  - Kafka: official apache/kafka image in KRaft mode (no ZooKeeper). The version must be compatible with the chosen
    Debezium Connect and flink-connector-kafka per their docs.
  - S3-compatible store: only if the project itself publishes an official, maintained image. If none exists, mark the
    "artifacts" profile NOT_PINNED with the reason, leave it out, and record that the artifact-store choice moves to P3.
    Never use a third-party rebuild.
  - gitleaks: official image ghcr.io/gitleaks/gitleaks.
  - Every image is pinned as name:tag@sha256:<digest>.
  - GitHub Actions are pinned by full commit SHA (resolved with git ls-remote), with a version comment.
  - Python packages: keep jsonschema 4.23.0, rfc3339-validator 0.1.4 and pytest 8.3.5 (P0.2 evidence). Everything
    else takes the latest stable release at lock time: ruff, mypy, alembic, SQLAlchemy, psycopg[binary] 3.x,
    dbt-core, dbt-postgres.
W2-D9 Layout.
  - Python project:
    * root pyproject.toml: [project] name "meterproof", version "0.0.0", no runtime deps; [tool.uv] package = false;
      [dependency-groups] test / lint / db / dbt; ruff, mypy and pytest config (pytest: testpaths ["tests"],
      addopts "-p no:cacheprovider", marker "integration");
    * uv.lock and .python-version are committed.
  - Docker:
    * compose file infra/compose/compose.yaml, project name "meterproof", profiles:
      db (postgres) | cdc (postgres, kafka, connect) | stream (kafka, flink-jobmanager, flink-taskmanager) |
      artifacts (object store, only if pinned) | full (all);
    * host ports bind to 127.0.0.1 only;
    * named volumes only, no bind mounts into the repo;
    * every service has a healthcheck;
    * Postgres runs with wal_level=logical, bounded replication settings and max_slot_wal_keep_size set (ADR-005 WAL
      lifecycle);
    * dev credentials come from ${VAR:-default}, with obviously local-only defaults; infra/compose/.env.example holds
      placeholders only; .env stays gitignored.
  - Migrations: Alembic in infra/db/ (alembic.ini, env.py, versions/0001_baseline.py). The baseline creates only
    schema "meterproof" and alembic_version, with no domain tables (ERD tables arrive in P1.1/P2.1). The DSN comes from
    METERPROOF_DATABASE_URL, defaulting to the local compose db.
  - Smoke tooling:
    * tools/meterproof/lab_smoke.py: stdlib + subprocess, ≤300 lines, one function per profile check;
    * tests/integration/test_migration_smoke.py, marked integration and run only when METERPROOF_DB_SMOKE=1. A skipped
      test is never reported as passed.
  - Docs:
    * pin manifest: docs/architecture/TOOLCHAIN_PINS.md;
    * decision: docs/adr/ADR_006_TOOLCHAIN_AND_VERSION_PINS.md (Proposed; same section format as ADR-001..005; weighted
      options must pass check_adr_scores.py);
    * runbook: docs/ops/DEV_BOOTSTRAP.md.
  - CI: new .github/workflows/meterproof-ci.yml. Leave meterproof-overlay-contracts.yml unchanged.
W2-D10 License (DEC-0009): LICENSE at the root = the canonical Apache License 2.0 text from
  https://www.apache.org/licenses/LICENSE-2.0.txt, unmodified. Record its SHA-256. Add one line "License: Apache-2.0 (see
  LICENSE)" to README.md. Add no NOTICE file and no per-file headers.

1.1 Inventory: the host versions of python (each interpreter in py -0p), uv, docker, docker compose, git, the Docker
    Desktop memory/CPU allocation (docker info) and free disk. Also run the java diagnosis from W2-D8.
1.2 Version research and pin manifest (W2-D8). Pull each image, then record its digest and size.
1.3 ADR-006 (Proposed). It compares at least Option 0 (no pins / host toolchain), A (the W2-D8 pins plus containerized
    JDK) and one more. It covers the toolchain risks RISK-0001..0004 and has reopen conditions.
1.4 uv project (W2-D9). uv sync --locked --all-groups. Record uv run python -c "import sys; print(sys.executable,
    sys.version)". Show that uv run dbt --version reports the pinned dbt-core and the postgres adapter.
1.5 Lint/types:
    - ruff check, ruff format --check and mypy (check_untyped_defs = true) over tests/ and tools/meterproof/.
    - Fix findings only when the fix is mechanical and does not change behaviour, then re-run the validator and the
      tests.
    - If tools/meterproof/validate_overlay.py would need more than about 20 changed lines, use a per-file ignore with a
      reason instead and record it.
1.6 Secret scan: run gitleaks through Docker over the full git history and the working tree.
    - Negative control: in a temp dir outside the repo, create a throwaway git repo holding a synthetic token-shaped
      string (e.g. "ghp_" + 36 random alphanumerics). gitleaks must report it, with the leak exit code. Never commit
      that string.
    - If gitleaks finds anything in this repository, STOP. Report only the file, commit and rule, never the matched
      value.
1.7 Compose profiles and lab smoke (DEC-0010). Use docker compose --profile <p> up -d --wait --pull never, after the
    explicit pulls of 1.2. lab_smoke.py checks:
    - db: SHOW wal_level = logical; the server major equals the pin.
    - cdc: the Kafka broker answers a topic list. GET /connector-plugins on Connect includes
      io.debezium.connector.postgresql.PostgresConnector. Do NOT register a connector or create a slot; that belongs to
      P2.2.
    - stream: the Flink REST /overview shows ≥1 taskmanager and ≥1 slot, and flink --version in the container equals
      the pin.
    - artifacts: the health endpoint, only if pinned.
    - full: one run of all profiles together, then docker stats --no-stream (memory per container and total) plus
      docker system df before and after. This is the RISK-0004 measurement. If the full lab cannot become healthy
      within Docker Desktop's current allocation, record the measurements and the failing service, tear down, and
      continue. Never change Docker Desktop settings.
    - After every profile: down -v --remove-orphans, then prove that no container or volume with label
      com.docker.compose.project=meterproof remains.
    - Negative control: start the db profile with wal_level overridden to replica (environment override, no file
      edit). lab_smoke db must exit non-zero. Then tear down.
1.8 Migration smoke against the db profile, with METERPROOF_DB_SMOKE=1:
    - upgrade head -> schema meterproof exists and alembic_version = 0001;
    - downgrade base -> schema absent;
    - upgrade head again.
    - Negative control: copy infra/db to a temp dir outside the repo and add a revision 0002 containing invalid SQL.
      Upgrade must exit non-zero; 0002's objects must be absent and alembic_version must still be 0001 (transactional
      DDL). Tear down afterwards.
1.9 JDK check: docker run --rm <pinned maven-temurin-17 image> java -version prints 17. No Flink job is built in P0.4.
1.10 CI meterproof-ci.yml:
    - triggers: pull_request, push to main and workflow_dispatch; permissions contents: read; a concurrency group;
      every action pinned by SHA.
    - job python-checks: setup-uv, uv sync --locked --all-groups, ruff, ruff format --check, mypy,
      pytest tests/contracts tests/unit, validate_overlay.py, the hygiene check, check_adr_scores.py.
    - job secret-scan: fetch-depth 0, then gitleaks via the pinned image.
    - job compose-and-migrations: docker compose config for every profile; start the db profile; run the 1.8 smoke;
      teardown.
    - Run every job's commands locally and record the results. GitHub execution needs an owner push, so the receipt
      records it as NOT RUN.
1.11 Runbook docs/ops/DEV_BOOTSTRAP.md:
    - prerequisites: Docker Desktop, uv, git; no host JDK or system Python packages needed;
    - environment variables from ENVIRONMENT RULES;
    - commands in order: first-time setup, then an offline re-run (uv sync --locked --offline; compose --pull never),
      then teardown;
    - expected outputs;
    - troubleshooting: the java hang, plugin autoload, git core.longpaths on Windows;
    - the measured lab footprint.
1.12 LICENSE + README line (W2-D10).
1.13 Clean checkout (tester-team): git clone --no-hardlinks this repo at the branch HEAD into a temp dir outside the
     repo. Follow DEV_BOOTSTRAP.md verbatim in OFFLINE mode (uv --offline, compose --pull never): uv sync, all Python
     checks, compose config, db profile + migration smoke, teardown. Any manual step not written in the runbook is a
     runbook defect: fix the runbook and repeat. Delete the clone afterwards.
1.14 Receipt docs/gates/G0/P0.4_receipt.md from the template. It records:
     - origin SYNTHETIC/N/A;
     - the pins with digests and the commands with exit codes;
     - the negative controls (secret, wal_level, bad migration);
     - the lab footprint;
     - the clean-checkout evidence;
     - limitations: GitHub CI NOT RUN until an owner push; no CDC connector, slot or Flink job exercised; the
       object-store status.
     Also add RISK_REGISTER updates for RISK-0001..0004, with the measured values, and RISK-0008 (LICENSE added).
1.15 Commits with explicit paths, in up to four logical commits, for example:
       chore(p0.4): Apache-2.0 license
       docs(p0.4): ADR-006 toolchain pins and pin manifest
       build(p0.4): uv project, lint/type/secret-scan config, CI workflow
       feat(p0.4): compose profiles, Alembic baseline, lab and migration smoke, bootstrap runbook, receipt
     After tests, every commit that contains code runs refresh_repo_map.py --stage. Never use --no-verify.
ACCEPTANCE P0.4 (each needs an evidence path in the receipt):
  [ ] Build/inspect: Python/Java/Flink/Debezium/dbt/PostgreSQL/Kafka pinned after validation; isolated Docker profiles;
      lint/types/secret scan/schema migration smoke/fixture validation -> TOOLCHAIN_PINS.md, ADR-006, compose.yaml,
      infra/db, CI
  [ ] Artifacts: dev bootstrap runbook, CI, pin manifest, offline smoke receipts -> paths
  [ ] Verification (agent part): a new clean checkout executes the baseline offline without a paid service -> 1.13
      evidence. Leave the P0.md box UNTICKED and write next to it: "clean-checkout evidence: <path>; G0 human signature
      pending". The card item includes the human signature.
  [ ] Evidence receipt -> docs/gates/G0/P0.4_receipt.md
CHECKPOINT 1: continue to Step 2 only if Build/inspect, Artifacts and the receipt have evidence AND the clean checkout
passed. Otherwise stop the wave and report.

=== STEP 2 — G0 gate packet (draft only; the owner signs) ===
Skills: repo-hygiene-team + $meterproof-evidence (read now).
2.1 Write docs/gates/G0/G0_GATE_RECEIPT.md from the template. Status: "IN_PROGRESS — gate packet drafted; advisor gate
    review and owner signoff pending". Never write PASS. It contains:
    - one row per subphase P0.1–P0.4: receipt path, commit SHA(s) and advisor review path/verdict (P0.4: pending);
    - the four P0 release-gate items, each with an evidence path or "OWNER" where only the owner can satisfy it;
    - the ADRs awaiting owner acceptance: ADR-001…006, all Proposed;
    - open items: GitHub CI run (owner push), OPEN-Q-1 deferred to G1/P1.2, the object-store status and every
      limitation from the four receipts;
    - an empty owner signoff block (name/date/decision/notes), left blank.
2.2 Repo hygiene sweep over the whole wave diff:
    - no secrets, raw provider data, real invoices or personal data;
    - no generated caches or lab volumes tracked;
    - .gitignore covers .venv, the compose .env and caches;
    - the claims-audit pattern of WAVE-01 2.7 run over the files this wave changed, with a hit table in the G0 receipt.
2.3 Commit: "docs(g0): draft G0 gate packet (unsigned)".

=== CLOSE THE WAVE ===
- P0.md:
  * tick only boxes whose evidence path exists; the P0.4 Verification box stays unticked as stated above;
  * set the Evidence line to the receipt list plus G0_GATE_RECEIPT.md and update RESUME_POINT;
  * P0 stays IN_PROGRESS and milestones.json is unchanged.
- PROJECT_STATUS.md: session log lines; RESUME_POINT with both branches and all SHAs; known risks; cost "none"; next
  steps:
    1. /meterproof-advisor review WAVE-02
    2. /meterproof-advisor gate G0
- _agent_ops, per SESSION_PROTOCOL (this list never waives a triggered record):
  * IMPLEMENTATION_LOG: one entry per step.
  * CURRENT_TASK and SESSION_BRIEF.
  * PROJECT_CONTEXT_CARD: durable state, including the toolchain pins.
  * DECISION_LOG: only if a material decision arose; it should have been a STOP instead.
  * RISK_REGISTER: as stated in 1.14.
  * REPO_MAP: via the refresh tool.
  Then run python ai-agent-workspace-pack/_agent_ops/tools/closure_check.py --root . --compact and resolve every row.
- Final checks:
  * on p0/wave-02-p0.4-g0: uv run pytest tests/contracts tests/unit green, ruff, mypy, the validator, hygiene,
    check_adr_scores and git diff --check all 0, git status clean;
  * docker ps -a and docker volume ls show nothing left from project "meterproof".
- Final message: one EXECUTION REPORT block per step (Step 0, P0.4, G0 packet), in the format of
  ADVISOR_EXECUTOR_WORKFLOW.md. Then list the skill/template files read and give a 5-line wave summary.

IN SCOPE (create/edit):
  Step 0: contracts/jsonschema/*.v1.schema.json; contracts/jsonschema/CHANGELOG.md; docs/contracts/DOMAIN_SPEC_v1.md;
          tests/fixtures/contracts/** (new N21–N33, schema_examples.json; F1–F3 unchanged); tests/contracts/**;
          tests/unit/test_check_adr_scores.py; tools/meterproof/check_adr_scores.py; docs/adr/ADR_00{1..5}_*.md
          (score tables + DEC-0008 wording only); docs/architecture/LINEAGE_AND_TRACE.md;
          docs/gates/G0/P0.2_receipt.md, P0.3_receipt.md (append FIX1 sections)
  P0.4:   pyproject.toml; uv.lock; .python-version; .gitignore (additions only); LICENSE; README.md (one line);
          infra/compose/compose.yaml; infra/compose/.env.example; infra/db/**; tools/meterproof/lab_smoke.py;
          tests/integration/test_migration_smoke.py; tests/unit/**; .github/workflows/meterproof-ci.yml;
          docs/adr/ADR_006_TOOLCHAIN_AND_VERSION_PINS.md; docs/architecture/TOOLCHAIN_PINS.md; docs/ops/DEV_BOOTSTRAP.md;
          lint fixes in tests/ and tools/meterproof/ (1.5 rules); docs/gates/G0/P0.4_receipt.md
  Step 2: docs/gates/G0/G0_GATE_RECEIPT.md
  All steps: P0.md checkboxes/Evidence/RESUME_POINT (not the Reviewer note); PROJECT_STATUS.md;
          ai-agent-workspace-pack/_agent_ops/{IMPLEMENTATION_LOG,DECISION_LOG,RISK_REGISTER,PROJECT_CONTEXT_CARD,
          CURRENT_TASK,SESSION_BRIEF,REPO_MAP}.md
OUT OF SCOPE:
  - Any domain table, ingestion/API code, Debezium connector registration, replication slot, Kafka topic contract,
    Flink job, dbt project, oracle code: P1+.
  - services/, core/, pipelines/, independent_oracle/, products/, infra/cloud/.
  - Everything in ai-agent-workspace-pack/ except the _agent_ops records above; .agents/ .claude/ .codex/.
  - .github/workflows/meterproof-overlay-contracts.yml; .drawio/.dot/.svg; milestones.json; other milestone cards;
    tests/fixtures/MP004_F1_SYNTHETIC.json; F1–F3 fixture files; replay_manifest field set.
  - Docker Desktop settings, host software installation, host JDK/PATH changes.
STOP AND ASK IF:
  - session_start is not OWNED, or the start state differs from "Expected start".
  - A W2 decision conflicts with a frozen contract/protocol statement, or would change F1–F3 facts, or an ADR's chosen
    option stops ranking first.
  - A W2-D8 rule cannot be satisfied by any released version.
  - gitleaks finds anything in this repository.
  - A task needs a package or image beyond AUTHORIZATION, an out-of-scope path, or a host/Docker Desktop change.
  - A change would alter Core v3.1–v3.3 meaning (an invariant weakened, logic shared between SQL and Flink, the oracle
    importing production code), or you would have to invent a business rule.
  - A checkpoint fails.
AUTHORIZATION
  Git:
    - Commit A2/C/D on p0/wave-01-p0.2-p0.3; create p0/wave-02-p0.4-g0 and commit there.
    - Stage explicit paths only (never `git add .`); never use --no-verify.
    - NO push, merge, rebase, tag, amend or history rewrite.
  Network (free downloads only):
    - uv: the Python packages named in W2-D8 and their dependencies, from PyPI.
    - Docker pulls of the W2-D8 images: postgres, apache/kafka, quay.io/debezium/connect, flink, a
      maven/eclipse-temurin 17 image, ghcr.io/gitleaks/gitleaks, and the object store only if official.
    - HTTP GET of official release, compatibility and registry pages, and of the Apache-2.0 text; git ls-remote for
      action SHAs.
    - Nothing else. No registry push, no cloud, no public ports.
  Docker (DEC-0010): local containers only, 127.0.0.1 ports, one full-lab measurement, mandatory down -v after every
    run.
  Cost: none. No paid API, no provider call, no cloud.
Do not claim anything you did not run. Then stop; the advisor reviews with `/meterproof-advisor review WAVE-02`.
```

## After Codex finishes

1. In Claude Code, run `/meterproof-advisor review WAVE-02`. It re-reviews P0.2 and P0.3 (Step 0) and reviews P0.4 and the G0 packet.
2. After APPROVE, the owner:
   - merges `p0/wave-01-p0.2-p0.3` first (this freezes contract v1), then `p0/wave-02-p0.4-g0`;
   - pushes, so that GitHub CI runs;
   - links the green CI run in the G0 receipt.
3. Run `/meterproof-advisor gate G0` → READY_FOR_OWNER_SIGNOFF or NOT_READY. The owner then accepts ADR-001…006 and signs G0.
4. Next is WAVE-03 = P1.1–P1.4 (the G1 spike). It stops before P1.5 HUMAN_GO and needs a decision on the provider/sandbox budget.
