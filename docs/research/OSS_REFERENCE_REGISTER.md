# Open-source reference register (just-in-time study, not a reading sprint)

Source: an external research pass proposing 12+ repositories to study. Advisor disposition: keep the list, but study each repository **only when the milestone that needs the decision starts**, as a bounded review that feeds one ADR or one design choice. Nothing here changes Core v3.4 scope, and no repository is forked or renamed into METERPROOF.

## Rules
1. A review is bounded: one repository, the named components only, roughly one hour of reading or one runnable lab.
2. Every review writes `docs/research/<repo>-review.md` (template below) and pins the exact version/commit studied.
3. **Study-only** entries are never copied into this repository: AGPL, Elastic License, archived/unmaintained code. Patterns may be re-implemented from understanding, with attribution in the review.
4. A repository becomes a **dependency** only through an ADR that records license, pinned version, maintenance status, and why it beats writing the piece ourselves.
5. METERPROOF's own contribution is never outsourced: source-consistent manifest, cross-engine comparison, coverage-aware verdicts, independent oracle, report versioning and CAS publication.

## Register

License and maintenance columns are as reported by the research pass; **confirm both on the repository at review time** before relying on them.

| # | Repository | Study when | What to extract | Usage class | License / status to confirm | Review |
|---|---|---|---|---|---|---|
| 1 | [openmeterio/openmeter](https://github.com/openmeterio/openmeter) | P0.2–P0.3 | ingestion boundary, event identity and dedup scope (dedup may be off by default; memory vs Redis), split of usage events vs transactional state | study | Apache-2.0 | Reviewed: [`openmeter-review.md`](openmeter-review.md) @ `55759ef876f6326d57550ca982f8ac131a9d13ff` |
| 2 | [debezium/debezium-examples `outbox/`](https://github.com/debezium/debezium-examples/tree/main/outbox) | P0.3 (design), P2.2 + P4.1 (lab) | atomic intent+outbox write, event ID vs delivery ID, idempotent consumer, connector restart | study + runnable lab | Apache-2.0 | NOT_STARTED |
| 3 | [getlago/lago](https://github.com/getlago/lago) | P0.2 | billing event identity, idempotency keys, correction semantics, worker split; skip invoices/payments/subscriptions | **study-only** | AGPL-3.0 (no code copy) | Reviewed: [`lago-review.md`](lago-review.md) @ `lago` `1a30b73b951cc14e329605b1329207ffbb93fc8c`, `lago-api` `91c5d29b75faf6527bd1202dac7881cabad512bb` |
| 4 | [apache/flink-playgrounds `operations-playground`](https://github.com/apache/flink-playgrounds/tree/master/operations-playground) | P4.3–P4.4 | JobManager/TaskManager compose layout, checkpoint/savepoint, restart and recovery observation | study + runnable lab | Apache-2.0 | NOT_STARTED |
| 5 | [janbjorge/pgqueuer](https://github.com/janbjorge/pgqueuer) | P2.2 | transactional enqueue, `FOR UPDATE SKIP LOCKED`, LISTEN/NOTIFY; must be compared with an own `job_leases` table that carries fencing tokens | candidate dependency (ADR) | MIT | NOT_STARTED |
| 6 | [apache/iceberg](https://github.com/apache/iceberg) | P3.2–P3.4 | snapshot/branch and write-audit-publish pattern as inspiration for immutable manifests + CAS pointer; do **not** add a lakehouse stack | study | Apache-2.0 | NOT_STARTED |
| 7 | [DataRecce/recce](https://github.com/DataRecce/recce) | P5.1, P6.1, L1 | before/after diff presentation, impact assessment, review checklist UX | study (UX) | Apache-2.0 (some features cloud-only) | NOT_STARTED |
| 8 | [Shopify/toxiproxy](https://github.com/Shopify/toxiproxy) | P4.4, P5.3 | latency/timeout/reset injection on app→provider, Connect→Kafka, Flink→sink paths; complements, never replaces, real process kill for T03 | candidate test tool (ADR) | MIT | NOT_STARTED |
| 9 | [datafold/data-diff](https://github.com/datafold/data-diff) | P5.1 | checksum/bisection row-diff algorithm only | **study-only** | archived / unmaintained since 2024 | NOT_STARTED |
| 10 | [elementary-data/elementary](https://github.com/elementary-data/elementary) | P6.2 | dbt test result reporting and data-health surfaces | study | Apache-2.0 | NOT_STARTED |
| 11 | [MarquezProject/marquez](https://github.com/MarquezProject/marquez) / OpenLineage | P6.2, P7.1 | lineage/provenance model for manifest→run→report | study | Apache-2.0 | NOT_STARTED |
| 12 | [duckdb/duckdb](https://github.com/duckdb/duckdb) | L0.3 | embedded local engine for Lite | candidate dependency (ADR) | MIT | NOT_STARTED |
| 13 | [evidence-dev/evidence](https://github.com/evidence-dev/evidence) | L1, A1 | static report generation from SQL | study | MIT | NOT_STARTED |
| 14 | [langfuse/langfuse](https://github.com/langfuse/langfuse) | A0.4, A4 | trace model, OLTP/OLAP split; do not replicate its full stack | study | MIT core, separate `ee/` | NOT_STARTED |
| 15 | [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | A4 | tool-call tracing, groundedness/citation evals | **study-only** | Elastic License 2.0 | NOT_STARTED |

## Advisor notes on the research pass
- The three "new ideas" it proposes are already in v3.4 and need no new scope: *Verification Evidence Capsule* = P5.4 MP-004 capsule; *Coverage-Aware Release Gate* = the publication gate (P3.4, SOURCE_CUT_PROTOCOL §9–12); *Failure Reproducer as a developer tool* = a Lite candidate to validate in L0.1 interviews, not a commitment.
- Agreed with the research: do not replace SQL/dbt + Flink with a single analytical engine; the point is two independent engines plus an oracle.
- Do not let P0 become a 12-repository reading phase. P0 needs entries 1–3 only, each feeding P0.2/P0.3 decisions.

## Review file template (`docs/research/<repo>-review.md`)
```text
# <repo> review
Studied: <url> @ <tag or commit>, <date>; license confirmed: <license>; maintenance: <active/archived>
Feeds: <milestone/subphase> → <ADR or design decision>
| Component studied | Lesson | Decision for METERPROOF | Trade-off | Test that proves it |
|---|---|---|---|---|
Not adopted and why:
Attribution / license obligations:
```
