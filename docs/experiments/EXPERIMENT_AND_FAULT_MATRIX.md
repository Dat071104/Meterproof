# Evidence-first scientific evaluation plan — no novelty/impact fabrication

## Falsifiable engineering hypotheses
- H1 **Retry/identity safety:** duplicates cause no double-applied business effect; legitimate provider attempts retain separate spend; verify against oracle and mutation.
- H2 **Source-aligned equivalence:** with same immutable scope, SQL/dbt and Flink finalized state agree on canonical business keys, including after crash/restart; mismatch is diagnostic, not normalized away.
- H3 **Evidence-aware publication:** missing and uncorrelatable records block inappropriate VERIFIED/global confidence and unsafe restatements; CAS prevents stale writers.
- H4 **AI non-interference:** Atlas enabled, disabled or down does not change canonical Core report digest/verdict/pointer; tool answers have citations/abstentions.
- H5 **Practical adoption:** a developer can audit a local exported dataset without deploying Kafka/Flink; repeat independent integrations and outcome reports, not just visits, substantiate value.

## Required fault matrix — every T01–T12 remains in full Core scope
| ID | Real scenario | Test source | Must prove |
|---|---|---|---|
| T01 | Debezium/outbox/Kafka event re-delivery | CDC integration | raw duplicate recorded; one canonical side effect |
| T02 | 2 confirmed billed provider attempts, 1 logical request | oracle + SQL + Flink | spend counts two; charge at most one, declared rule |
| T03 | process crash after sink commit before ACK | live Kafka/Flink + sink | restart idempotent; sink receipt + checkpoint + no double-apply |
| T04 | out-of-order app and provider events | integration+Flink | same finalized result with declared closure |
| T05 | late correction after immutable published report | temporal SQL/DB | original report remains addressable; corrected new version |
| T06 | SQL pricing mutation/regression | independent oracle | mutant detected; publication blocked |
| T07 | Flink state divergence vs batch | real Flink comparator | exact business key, input failure slice, root cause |
| T08 | missing provider ID/unknown outcome | provider fixture + oracle | INCOMPLETE/UNDETERMINED, no fake spend or VERIFIED |
| T09 | two concurrent publication candidates | DB transaction race | stale CAS writer blocked, no old version removed |
| T10 | N identical frozen-manifest replays | batch + stream | stable finalized canonical digest, exclude runtime metadata |
| T11 | intentionally broken comparator/oracle tests | negative/mutation | verifier itself fails rather than rubber-stamping |
| T12 | tenant spoofing, cross-tenant read | authenticated API + DB | tenant derived from auth, access denied |

## MP-004 flagship incident
- Controlled fixture where provider attempt A is **independently confirmed billed**, but app response is deliberately dropped. Separately include genuine timeout without generation ID → `UNKNOWN_PROVIDER_OUTCOME`/`UNDETERMINED`.
- Retry B succeeds; two provider attempts are preserved; only one eligible logical customer request billed under pinned policy.
- Inject duplicate delivery, late provider metadata and a wrong pricing/dedup rule. Preserve evidence for **why** SQL vs Flink vs oracle disagree.
- Replay pinned manifest, detect regression, block unsafe candidate, correct with verified new version and atomic CAS publication; export redacted evidence capsule.

## Baselines for scientific claims
- **B0:** SQL/dbt results and dbt tests alone, no differential replay.
- **B1:** SQL batch vs Flink parity on totals only, no source-consistency/coverage proof.
- **B2:** row-level SQL/Flink diff on aligned scope, no independent oracle or uncertain evidence semantics.
- **METERPROOF:** aligned scope + independent oracle + evidence state + safe publication + real faults.

Measure false-VERIFIED rate on labeled test population, false safe-publications blocked, correct abstention on unlinked timeout, mismatch localization accuracy, replay repeatability, recovery after fault, ingestion lag, p50/p95 query/diff latency, cost and footprint. **Do not invent numeric baselines; execute and report confidence/caveats.** Scenarios with incomparable input scope must count separately as `NOT_COMPARABLE`, not as failed parity.

## Evidence receipt schema
`gate_id`, `subphase`, `test_id`, `status`, `command`, `execution_environment`, `git_sha`, `input_manifest_sha256`, `origin`, `source_cut`, `provider_scope`, `kafka_offsets`, `flink_checkpoint`, `sink_commit_receipt`, `expected`, `observed`, `negative_control`, `sanitized_logs`, `limitations`, `reviewer`, `next_command`.

**Never mark PASS** because a markdown checklist was filled, a single unit mock passed, or an architecture exists.
