# Repo Map / Ban do ma nguon

Generated file. Do not hand-edit; regenerate with
`python ai-agent-workspace-pack/_agent_ops/tools/generate_repo_map.py --root . --output ai-agent-workspace-pack/_agent_ops/REPO_MAP.md --force`.

Read this BEFORE grepping the repository. It answers "where does the code
live" and "what breaks if I touch this" in one Tier-1 read.

## Last Verified Commit

`f895e2d`

## Indexed Source Fingerprint

`sha256:3:a703927ffba10c52c19577b8c2121aea2468524fa7b2eda054e1d0ea62a0cc97`

## Snapshot

- Branch: `p0/wave-01-p0.2-p0.3`
- Generated: `2026-11-19`
- Code files indexed: 3
- Stack: Unknown

## Modules

`Inbound` counts imports coming from OUTSIDE the module: higher means more
code depends on it, so changes there travel further.

| Module | Files | Inbound | Entry points |
| --- | --- | --- | --- |
| `tests/contracts` | 2 | 0 | - |
| `tools/meterproof` | 1 | 0 | - |

## Hot Files (widest blast radius)

Ranked by fan-in. Treat an edit here as cross-module until proven otherwise.

| File | Imported by | Imports |
| --- | --- | --- |
| _no local import edges resolved_ | | |

## Symbol Graph

24 symbols, 30 edges (exact 30, heuristic 0, ambiguous 0, weak 0).

### Most-called symbols

| Symbol | Called by | Where |
| --- | --- | --- |
| `load_json` | 6 | `tests/contracts/test_contract_schemas.py:13` |
| `schema_for` | 3 | `tests/contracts/test_contract_schemas.py:17` |
| `compute_case` | 3 | `tests/contracts/test_expected_facts.py:121` |
| `compute_verdicts` | 3 | `tests/contracts/test_expected_facts.py:131` |
| `money_text` | 3 | `tests/contracts/test_expected_facts.py:23` |
| `all_cases` | 2 | `tests/contracts/test_expected_facts.py:176` |
| `flatten` | 1 | `tests/contracts/test_contract_schemas.py:21` |
| `positive_receipts` | 1 | `tests/contracts/test_contract_schemas.py:27` |
| `test_every_usd_schema_field_uses_the_frozen_pattern_and_transport_is_not_a_receipt_field.walk` | 1 | `tests/contracts/test_contract_schemas.py:90` |
| `canonical_digest` | 1 | `tests/contracts/test_expected_facts.py:157` |
| `compute_billable_facts` | 1 | `tests/contracts/test_expected_facts.py:27` |
| `compute_invoice_facts` | 1 | `tests/contracts/test_expected_facts.py:91` |

Query it instead of grepping:

```bash
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --symbol <name>    # callers, callees, flow
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --impact <name>    # blast radius + tests (ambiguous: use Cls.method)
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --path <a> <b>     # how a reaches b
```

## Entry Points

- None detected by filename convention. Confirm manually.

## Isolated Files

3 file(s) have no resolved local imports in either direction.
They are listed only on demand -- enumerating them here would recreate the
context bloat this map exists to prevent.

## Drill Down

This map is deliberately shallow. For the affected zone of a specific change:

```bash
python ai-agent-workspace-pack/_agent_ops/tools/scan_deps.py --root . --seed "<keyword>" --hops 2 --output markdown
```

## Limits

- Covers `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.java`, `.cs` only. Java and C#
  are regex-extracted (not parsed): their calls are always `weak`, and C#
  has no file import edges because `using` names namespaces, not files.
- Relative imports resolve exactly. Absolute Python imports and JS path
  aliases are inferred by probing parent directories, so they can be wrong;
  package imports (`react`, `numpy`) are not followed at all.
- Dynamic imports, DI wiring, and runtime registries are invisible here.
  Verify before claiming a file is unused.
