# Monorepo topology — ownership and import rules

```text
<EXISTING-REPO>/
├── AGENTS.md                         # EXISTS from installed pack; only add an append block
├── ai-agent-workspace-pack/          # pack if embedded; leave ALL contents untouched
├── _agent_ops/                       # pack's session memory; do not reset
├── .agents/skills/                   # existing + additive project domain skills
├── .claude/skills/                   # existing + additive thin references
├── docs/
│   ├── METERPROOF_START_HERE.md
│   ├── architecture/                # topology, source-cut protocol, editable drawio, ADR links
│   ├── contracts/                   # contracts/invariants, traceability
│   ├── adr/                         # architectural choice records
│   ├── experiments/                 # fault matrix, baselines, claims
│   ├── milestones/{core,lite,atlas,adoption}/
│   ├── gates/                       # receipts created only after actual execution
│   └── ops/                         # project status + Codex start (pack still owns handoff)
├── contracts/jsonschema/           # versioned wire schemas
├── services/
│   ├── ingestion_api/               # authenticated receipts + transactional outbox
│   ├── durable_worker/              # idempotent leased work / DLQ
│   ├── verification_api/            # read-only published report scope
│   └── publication/                 # CAS pointer (Core-only writer)
├── core/
│   ├── evidence/                    # coverage state + provenance
│   ├── policy_spec/                 # immutable versioned human specification, NOT one shared reducer
│   ├── replay/                      # manifest orchestration, canonicalization
│   └── comparator/                  # separate execution output diff
├── pipelines/
│   ├── dbt/                         # independent SQL transformation
│   ├── debezium/                    # source WAL, snapshot configuration
│   └── flink_java/                  # independent Java DataStream transformation
├── independent_oracle/              # pure Python independently reviewed fixture reducer
├── products/
│   ├── lite/                         # uvx/PyPI CLI, SDK, DuckDB, HTML, GitHub Action
│   └── atlas/                        # read-only marts/tools/retrieval/agent/evals/UI
├── infra/{compose,cloud}/           # no automatic cloud provisioning
├── data/{manifests,samples}/             # local and untracked; synthetic fixtures live in tests/fixtures/
├── tests/{unit,contracts,integration,cdc,fault,security,mutations,e2e}/
└── tools/meterproof/                 # validate overlay, local developer commands
```

**This is a proposed target structure, not an assertion these code directories exist.** Installer creates only required planning/contracts/skill files; Codex must scaffold code paths within each approved milestone. Do not initialize blank directories simply for visual completeness.

## Mandatory import constraints
- Contracts schemas may be imported by Core, Lite, Atlas as applicable.
- SQL/dbt and Flink may share *human-readable business policy specification* and wire schemas but NEVER import the same executable transformation reducer.
- Independent oracle is test-only reference and must NOT import production transformation code.
- Lite can reuse business schemas, coverage helpers and local parsing; must explicitly state guarantees differ from full CDC pipeline.
- Atlas may import generated SDK for read API, never Core SQL writer/DB connection. Atlas data layer is published-version keyed.
- No product-specific package changes base `VERIFIED` decision semantics without ADR and full Core regression.

## Feature branches are temporary implementation isolation
`main` = Core authority and reviewed integration. `feature/lite` = CLI/SDK and end-user packaging once G2 vertical slice is usable. `feature/atlas-ai-analytics` = AI read-model extension once immutable verified read surface is available. `release/core-v1`, `release/lite-v1`, `release/atlas-v1` are example *tags or artifact names*, not a mandate to keep three permanent divergent branches.
