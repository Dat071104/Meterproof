# METERPROOF v3.4 — Milestone registry

No phase duration estimates. Full target scope: all Core, Lite, Atlas and Adoption milestones. Gates sequence work and do not redefine mandatory parts as "advanced if time".

| ID | Focus | Gate | Prerequisites | State |
|---|---|---|---|---|
| [P0](core/P0.md) | Architecture, governance & honest business specification | G0 | preflight | NOT_STARTED |
| [P1](core/P1.md) | Real provider technical spike and honest evidence boundaries | G1 | G0 | NOT_STARTED |
| [P2](core/P2.md) | Durable vertical slice + SQL/dbt reconciliation | G2 | G1 | NOT_STARTED |
| [P3](core/P3.md) | Temporal correctness, immutable replay and safe publication | G3 | G2 | NOT_STARTED |
| [P4](core/P4.md) | Real WAL CDC → Kafka → Flink independently implemented shadow | G4 | G3 | NOT_STARTED |
| [P5](core/P5.md) | Differential verifier, mutations and MP-004 failure lab | G5 | G4 | NOT_STARTED |
| [P6](core/P6.md) | Production-style demo, operating metrics and security | G6 | G5 | NOT_STARTED |
| [P7](core/P7.md) | Technical case study, benchmark and defendable portfolio | G7 | G6 | NOT_STARTED |
| [L0](lite/L0.md) | User-facing specification and clean CLI boundary | LG0 | G2 | NOT_STARTED |
| [L1](lite/L1.md) | One-command local usage audit | LG1 | LG0 | NOT_STARTED |
| [L2](lite/L2.md) | SDK/adapters and GitHub Action | LG2 | LG1 | NOT_STARTED |
| [L3](lite/L3.md) | Open-source distribution and reliability | LG3 | LG2 | NOT_STARTED |
| [A0](atlas/A0.md) | Read-only AI/product architecture boundary | AG0 | G3 | NOT_STARTED |
| [A1](atlas/A1.md) | Governed analytics and dashboards | AG1 | AG0 | NOT_STARTED |
| [A2](atlas/A2.md) | Evidence retrieval & secured tools | AG2 | AG1 | NOT_STARTED |
| [A3](atlas/A3.md) | LangGraph AI Incident Analyst | AG3 | AG2 | NOT_STARTED |
| [A4](atlas/A4.md) | Evaluation, non-interference and AI security | AG4 | AG3 | NOT_STARTED |
| [A5](atlas/A5.md) | Capstone integration, demo and release | AG5 | AG4 | NOT_STARTED |
| [U0](adoption/U0.md) | Problem validation (not presumed market fit) | UG0 | G1 | NOT_STARTED |
| [U1](adoption/U1.md) | External user onboarding and activation | UG1 | LG1 | NOT_STARTED |
| [U2](adoption/U2.md) | Repeat usage and integration evidence | UG2 | LG3, UG1 | NOT_STARTED |

## Program-level acceptance
- **Core:** P0–P7/G0–G7: full science, real CDC/Flink, independent oracle, T01–T12, MP-004, reproducible evidence and safe publication.
- **Lite:** L0–L3/LG0–LG3: local-first CLI/SDK/adapters/CI and external installation; NOT a copy of Kafka/Flink or a weaker Core release.
- **Atlas:** A0–A5/AG0–AG5: verified read-only analytics/agent, security and non-interference; AI does not calculate or publish Core truth.
- **Adoption:** U0–U2/UG0–UG2: interviews, external users, repeat usage and verified integration evidence, with opt-in privacy.

## Gate transitions
1. **P1** approved after G0; P2–P7 remain intended scope but require human G1 GO/CONDITIONAL GO with mitigation and new reviewed gate.
2. **Lite L0** begins after G2 vertical slice; **Atlas A0** begins after G3 immutable read surface; branches can develop while other Core milestones proceed without replacing them.
3. **U0** can start after G1; U1 requires Lite LG1; U2 requires external onboarding and Lite release.
4. A missing real provider correlation can trigger a documented pivot to owner-export verification; it cannot be patched with invented sources.
5. Every signed gate requires actual executed command artifacts and negative controls. No PASS by checkboxes alone.
