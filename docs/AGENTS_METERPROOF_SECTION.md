# METERPROOF — additive project governance (v3.4)

Canonical project entrypoint: `docs/METERPROOF_START_HERE.md`. Read `docs/ops/PROJECT_STATUS.md` and preinstalled `_agent_ops` handoff first. Never replace/modify generic `ai-agent-workspace-pack` skills, config, memory, or managed markers. Project domain skills live in `.agents/skills/meterproof-*` and `.agents/skills/atlas-ai-grounding`.

**Hard constraints:**
- Keep Core v3.1/v3.2/v3.3 meaning intact: source evidence + explicit coverage; independent SQL/dbt, real Debezium/Kafka/Flink, independent pure Python oracle; temporal replay, CAS safe publication, 12 real failure tests and incident MP-004. No shortcut with shared reducer.
- Work only on active milestone; G1 technical spike must produce human GO/NO-GO before the full system is authorized. The full intended scope remains P0–P7 + L0–L3 + A0–A5 + U0–U2; a gate controls sequencing, not deletion.
- `VERIFIED` applies to a declared scope, never global completeness. Timeout with no attributable provider generation means `UNDETERMINED`; a missing known segment can mean `INCOMPLETE`. Source cut must prove like-for-like inputs; not-comparable is not mismatch.
- **Core authoritative writers only.** Atlas uses read-only views/versioned APIs, least privilege and strict tool allowlist. Lite runs locally from user-supplied data and cannot claim full shadow-mode guarantees.
- Evidence: include commands, manifest SHA, code SHA, source cut/coverage, expected/observed, test tier, negative control, limitations. Installing docs, scaffolding or mock-only green tests cannot make Core gate PASS.
- Data origin: `PRODUCTION`, `PILOT`, `SANDBOX`, `SYNTHETIC` separate; no synthetic money-saved claims, provider management secrets, real prompts or personal data in public artifacts.
- Never create public infra, provision or run paid external AI/API calls, deploy, push, merge, or delete resources without explicit relevant authorization; record costs, limits and teardown.
- Stage only intended Git paths, do not `git add .`; on PAUSE finish atomic step and record exact RESUME_POINT; on RESUME re-verify live git/CI/resources and cap.
- If an architectural guarantee is not directly supported by tests + source evidence, downgrade the claim rather than hiding uncertainty.
