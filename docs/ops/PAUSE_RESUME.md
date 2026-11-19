# Pause and resume without losing gate evidence

**PAUSE NOW:** Finish only current atomic step. Do not start any new cloud action/provider call/merge. Update `docs/ops/PROJECT_STATUS.md` for every touched milestone, last real command/exit, receipt and open blocker. Update preinstalled `_agent_ops` handoff with exact `RESUME_POINT`. Report cloud resources still running and cost/hour; do not assume free. Stop.

**RESUME:** Read root AGENTS, generic pack handoff, project status/current phase gate, contracts & source cut, then re-verify live Git/PR/CI and applicable Kafka/Flink/DB resources and cloud budget. Run bounded next command, preserve failed-test evidence, and write a new exact `RESUME_POINT` before ending. Never carry forward a claimed PASS merely because a former chat said so.
