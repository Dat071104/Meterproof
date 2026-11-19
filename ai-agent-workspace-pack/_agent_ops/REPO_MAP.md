# Repo Map / Ban do ma nguon

Generated file. Do not hand-edit; regenerate with
`python ai-agent-workspace-pack/_agent_ops/tools/generate_repo_map.py --root . --output ai-agent-workspace-pack/_agent_ops/REPO_MAP.md --force`.

Read this BEFORE grepping the repository. It answers "where does the code
live" and "what breaks if I touch this" in one Tier-1 read.

## Last Verified Commit

`ca46c11`

## Indexed Source Fingerprint

`sha256:1:7244fd576b5f7f029cce707509d76d8f2250040aaad87f343ebcc2d63f5a27cb`

## Snapshot

- Branch: `main`
- Generated: `2026-11-19`
- Code files indexed: 1
- Stack: Unknown

## Modules

`Inbound` counts imports coming from OUTSIDE the module: higher means more
code depends on it, so changes there travel further.

| Module | Files | Inbound | Entry points |
| --- | --- | --- | --- |
| `tools/meterproof` | 1 | 0 | - |

## Hot Files (widest blast radius)

Ranked by fan-in. Treat an edit here as cross-module until proven otherwise.

| File | Imported by | Imports |
| --- | --- | --- |
| _no local import edges resolved_ | | |

## Symbol Graph

1 symbols, 1 edges (exact 1, heuristic 0, ambiguous 0, weak 0).

### Most-called symbols

| Symbol | Called by | Where |
| --- | --- | --- |
| `main` | 1 | `tools/meterproof/validate_overlay.py:22` |

Query it instead of grepping:

```bash
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --symbol <name>    # callers, callees, flow
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --impact <name>    # blast radius + tests (ambiguous: use Cls.method)
python ai-agent-workspace-pack/_agent_ops/tools/explore.py --root . --path <a> <b>     # how a reaches b
```

## Entry Points

- None detected by filename convention. Confirm manually.

## Isolated Files

1 file(s) have no resolved local imports in either direction.
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
