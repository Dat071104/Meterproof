# Phase Roadmap / Lo trinh giai doan

The authoritative roadmap, subphases and checklists are the milestone cards; this file only routes to them so nothing is duplicated.

- Registry: `docs/milestones/MILESTONE_INDEX.md` and `docs/milestones/milestones.json` (21 milestones, 82 subphases)
- Cards: `docs/milestones/{core,lite,atlas,adoption}/<ID>.md` (each subphase: Build/inspect, Artifacts, Verification, Evidence receipt; then Release gate)
- Gate policy: `docs/milestones/README_GATE_POLICY.md`; receipts: `docs/gates/<GATE>/`

## Parts

- Part 1 — Core P0–P7 (G0–G7): evidence model → provider spike + human GO/NO-GO → durable slice + dbt → temporal/replay/CAS → real CDC/Kafka/Flink shadow → verifier, mutations, T01–T12, MP-004 → demo/ops/security → case study/benchmark/release.
- Part 2 — Lite L0–L3 (after G2): local CLI/SDK/GitHub Action.
- Part 3 — Atlas A0–A5 (after G3): read-only analytics + grounded AI analyst.
- Part 4 — Adoption U0–U2 (U0 after G1): validation, onboarding, repeat usage.

## Phases

| Phase | Goal | Gate | Requires | Status |
| --- | --- | --- | --- | --- |
| P0 | Architecture, governance, honest business spec | G0 | — | NOT_STARTED (P0.1 work order issued) |
| P1 | Real provider spike, human GO/NO-GO | G1 | G0 | NOT_STARTED |
| P2 | Durable vertical slice + SQL/dbt | G2 | G1 | NOT_STARTED |
| P3 | Temporal correctness, replay, CAS publication | G3 | G2 | NOT_STARTED |
| P4 | WAL CDC → Kafka → Flink shadow | G4 | G3 | NOT_STARTED |
| P5 | Differential verifier, T01–T12, MP-004 | G5 | G4 | NOT_STARTED |
| P6 | Demo, metrics, security | G6 | G5 | NOT_STARTED |
| P7 | Case study, benchmark, release | G7 | G6 | NOT_STARTED |
| L0–L3 | Lite | LG0–LG3 | G2 | NOT_STARTED |
| A0–A5 | Atlas | AG0–AG5 | G3 | NOT_STARTED |
| U0–U2 | Adoption | UG0–UG2 | G1 / LG1 / LG3 | NOT_STARTED |

## Acceptance Gates

- Every gate needs executed receipts + negative controls + advisor review + owner signoff; G1 needs explicit `HUMAN_GO` / conditional GO / `NO_GO`.

## Suggested Consistency Audit Points

- After G0 (contracts frozen), after G2 (before Lite branches), after G3 (before Atlas branches), after G5 (before public demo), before each release tag.
