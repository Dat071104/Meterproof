---
name: meterproof-failure-drills
description: Use to run METERPROOF controlled CDC/Flink crashes, duplicate/out-of-order/late-event faults, mutation tests, the 12 acceptance tests and reproducible MP-004 incident.
---

# METERPROOF — Fault Injection & Evidence Receipts

## Trigger
Milestone G3/G4/G5, crash or retry investigation, fault injection, CDC connector restart, streaming recovery, mutation test, MP-004 demo.

## Required scenario matrix
T01 event redelivery => one business effect, raw duplicates retained.  
T02 2 provider attempts/request => 2 known costs, one billable success where policy applies.  
T03 crash after sink commit/before ack => no duplicate final effect.  
T04 out-of-order observations => same finalized state under equal cut.  
T05 late correction => immutable prior report, separate candidate.  
T06 bad SQL price rule => independent oracle detects + publish blocked.  
T07 bad Flink reducer => comparator identifies failing key + reproducer slice.  
T08 unavailable provider evidence => INCOMPLETE/UNDETERMINED.  
T09 concurrent publish => CAS blocks stale writer.  
T10 same manifest replay => same canonical digest on repeated runs.  
T11 bad oracle/comparator mutant => verifier tests catch it.  
T12 tenant spoofing => no cross-tenant reads or writes.

## Execution protocol
1. Freeze local manifests, test seed, code SHA, expected oracle and bounded Docker resource/teardown scope; check for unrelated live resources before injecting failure.
2. Run a healthy baseline and save test receipt.
3. Inject **one** deterministic fault at a precise point (e.g. sink commit completed; acknowledgement not emitted). Do not merely kill an arbitrary container and assume test covered that case.
4. Capture persisted DB/outbox/offset/checkpoint/sink states before and after restart, compare independent expected result and record recovery time if measured.
5. Run a negative/mutation case that SHOULD fail and ensure suite catches it.
6. Teardown only resources created for this test and preserve sanitized evidence.
7. Set each test `NOT_STARTED|IN_PROGRESS|PASS|FAILED|BLOCKED|NOT_APPLICABLE`; a unit pass does not cover an unrun real CDC fault drill.

## MP-004 distinction
Controlled fixture A is *known* billed despite dropped application response. Real network timeout without attributable provider evidence stays `UNDETERMINED`. Demonstrate the difference explicitly.

## STOP and output
Stop on unapproved cloud cost or API calls, uncertain teardown targets, unavailable independent oracle or inconsistent source cuts. Each test receipt includes scenario, exact command, seed, manifest/provenance, versions, observed result and assertion, evidence paths and limitations.
