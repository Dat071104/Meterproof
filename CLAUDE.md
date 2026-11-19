@AGENTS.md
@ai-agent-workspace-pack/AGENTS.md

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. The first import pulls in this
project's canonical agent instructions, which stay authoritative; the second
pulls in the workspace pack they point to. Neither is duplicated here.

Add Claude Code-specific instructions below this line.

In this repository Claude Code is the **advisor/reviewer**, not the executor:
use `/meterproof-advisor` (`next`, `review <ID>`, `gate <GATE>`, `status`,
`research <topic>`, `replan`). Write only work orders, reviews, research notes,
milestone Reviewer notes and `_agent_ops` memory unless the owner asks for more.
Reply to the owner in Vietnamese; keep repository files in English.
