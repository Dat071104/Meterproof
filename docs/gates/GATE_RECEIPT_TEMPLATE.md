# Gate / test evidence receipt template (fill after actual command)

| Field | Observed value |
|---|---|
| Gate + subphase + tests | `G? / P?.? / T?` |
| Status | `NOT_STARTED / IN_PROGRESS / BLOCKED / FAILED / PASS` |
| Git branch & SHA | `UNOBSERVED` |
| Exact command & exit code | `NOT RUN` |
| Environment / tool versions | `UNOBSERVED` |
| Input manifest SHA + source cut | `UNOBSERVED` |
| Provider/invoice coverage and exclusions | `UNOBSERVED` |
| Kafka partition offset vector / Flink checkpoint / sink receipt (if relevant) | `N/A — justification` |
| Origin PRODUCTION/PILOT/SANDBOX/SYNTHETIC | `UNOBSERVED` |
| Expected output / invariant | `NOT REVIEWED` |
| Actual output / row-level diff | `NOT RUN` |
| Negative control / mutant | `NOT RUN` |
| Sanitized raw log references | `NONE` |
| Known limitations / reasons to withhold claim | `NOT REVIEWED` |
| Reviewer / authorization | `NOT APPROVED` |
| Exact next command / RESUME_POINT | `TBD` |

**Gate PASS rule:** gate-specific acceptance evidence must exist, command actually run, negative controls documented, reviewer record present. Filling the template does not by itself grant authorization to spend or proceed.
