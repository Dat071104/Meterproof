---
name: build-team
description: Use this when the user wants to implement a new feature, endpoint, module, or behavior change in an existing codebase. Plans the change, confirms placement and business rules, then writes the smallest complete change (ponytail rules) in one serialized lane with tests and a self-review. Not for bug fixes or cleanup.
---

<!-- AI_AGENT_WORKSPACE_PACK:ADAPTER v1 -- generated pointer into the pack folder; edit the pack, not this file. -->

# Build Team (adapter)

This is a Claude Code adapter. The source of truth is `ai-agent-workspace-pack/build-team/SKILL.md` at
the repo root. Read that file and follow it exactly. Open a reference below only
when the step you are on names it; do not preload them.

References: `ai-agent-workspace-pack/build-team/FEATURE_CONTRACT_TEMPLATE.md`,
`ai-agent-workspace-pack/build-team/SLICE_PLAN_TEMPLATE.md`, `ai-agent-workspace-pack/build-team/PONYTAIL_RULES.md`,
`ai-agent-workspace-pack/build-team/SELF_REVIEW_CHECKLIST.md`. Use `ai-agent-workspace-pack/_agent_ops/REPO_MAP.md` for placement
and blast radius, and the `tester` subagent (read-only) for verification. There
is no dedicated write subagent: the root agent is the single writer lane.
