# Risk Register / Danh sach rui ro

| Risk ID | Severity | Likelihood | Area | Description | Mitigation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| RISK-0001 | High | High | Toolchain | Host JDK 23 is not a supported Flink runtime (Flink 2.x: Java 17 recommended, 21 experimental). Building jobs with the host JDK will fail or behave inconsistently. | P0.4: JDK 17 toolchain (Maven/Gradle toolchains or build inside the Flink image); pin in technology ADR. | Open |
| RISK-0002 | Medium | High | Toolchain | `flink-connector-kafka` trails Flink core releases; newest Flink may lack a released Kafka connector. | P0.4: choose Flink version by connector availability; record both versions. | Open |
| RISK-0003 | Medium | Medium | Toolchain | Host Python 3.14; dbt-postgres support for 3.14 unconfirmed. | P0.4: pin project Python 3.12/3.13 with a lockfile (uv). | Open |
| RISK-0004 | Medium | Medium | Local lab | Full stack (Postgres, Kafka, Connect, Flink JM/TM, MinIO) on Docker Desktop/Windows may exceed memory; WAL slot growth can fill disk. | Measure in P0.4/P4.1; compose profiles; slot/WAL monitoring and teardown. | Open |
| RISK-0005 | High | Medium | G1 evidence | Provider generation correlation may be insufficient (true timeouts lack IDs) → G1 NO-GO. | Pivot path already defined (owner-export verification); no invented sources. | Open |
| RISK-0006 | High | Medium | Scope | 21 milestones / 82 subphases for one person; risk of stalling mid-Core. | One subphase per work order; Core first; Lite/Atlas only after their gates; replan via `/meterproof-advisor replan`. | Open |
| RISK-0007 | High | Low | Public repo | Repository is public: provider keys, raw provider records, prompts or personal data could leak through receipts/logs. | `.gitignore` for raw evidence; sanitized receipts only; hygiene check before every push. | Open |
| RISK-0008 | Medium | High | Licensing | No LICENSE file on a public repo (all rights reserved by default); AGPL/ELv2 references must not be copied. | Owner decides license in P0; study-only rule in OSS register. | Open |
| RISK-0009 | Medium | Medium | Process | Agents may claim PASS from scaffolding or mocks. | Validator requires gate receipt for passing statuses; advisor re-runs checks; owner signs gates. | Mitigated (partially) |
