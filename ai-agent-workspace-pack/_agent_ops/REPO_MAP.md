# Repo Map / Ban do ma nguon

Generated file. Do not hand-edit; regenerate with
`python ai-agent-workspace-pack/_agent_ops/tools/generate_repo_map.py --root . --output ai-agent-workspace-pack/_agent_ops/REPO_MAP.md --force`.

Read this BEFORE grepping the repository. It answers "where does the code
live" and "what breaks if I touch this" in one Tier-1 read.

## Last Verified Commit

`231d9d7`

## Indexed Source Fingerprint

`sha256:3:a267675849c914a560a63e440f1bcedd0459c51fce2b955184cf06290d484041`

## Snapshot

- Branch: `p0/wave-01-p0.2-p0.3`
- Generated: `2026-11-20`
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

28 symbols, 39 edges (exact 33, heuristic 0, ambiguous 6, weak 0).

### Most-called symbols

| Symbol | Called by | Where |
| --- | --- | --- |
| `load_json` | 7 | `tests/contracts/test_contract_schemas.py:13` |
| `compute_case` | 4 | `tests/contracts/test_expected_facts.py:128` |
| `schema_for` | 3 | `tests/contracts/test_contract_schemas.py:17` |
| `test_every_usd_schema_field_uses_the_frozen_pattern_and_transport_is_not_a_receipt_field.walk` | 3 | `tests/contracts/test_contract_schemas.py:96` |
| `test_unformatted_strings_and_string_array_items_are_nonempty.walk` | 3 | `tests/contracts/test_contract_schemas.py:118` |
| `compute_verdicts` | 3 | `tests/contracts/test_expected_facts.py:142` |
| `money_text` | 3 | `tests/contracts/test_expected_facts.py:23` |
| `all_cases` | 2 | `tests/contracts/test_expected_facts.py:187` |
| `load_json` | 2 | `tests/contracts/test_expected_facts.py:15` |
| `flatten` | 1 | `tests/contracts/test_contract_schemas.py:21` |
| `positive_receipts` | 1 | `tests/contracts/test_contract_schemas.py:27` |
| `apply_source_cut` | 1 | `tests/contracts/test_expected_facts.py:27` |

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
