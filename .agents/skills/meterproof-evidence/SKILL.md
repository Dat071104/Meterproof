---
name: meterproof-evidence
description: Use for METERPROOF event schemas, provider/app identities, pricing calculations, invoices, reconciliation and coverage-aware verification decisions. Do not infer a provider charge from a timeout.
---

# METERPROOF — Evidence & Billing Contracts

## Trigger
Changing receipts, provider generation links, business IDs, source coverage, pricing rules, invoice imports or verification states.

## Read order
Root `AGENTS.md` and current handoff -> phase/business contract -> affected code and fixtures. Use existing generic `build-team` or `tester-team` for generic implementation/test practice.

## Invariants
- Distinguish `logical_request_id`, `provider_attempt_id`, optional `provider_generation_id`, `source_event_id`, `source_receipt_id` and transport delivery IDs.
- One logical request can cause N real provider attempts; deduplicating all by logical ID can lose provider spend.
- `provider_spend` (confirmed billed attempts), `customer_billable_units` (versioned policy), `customer_charge`, `invoice_amount` are not equivalent.
- Genuine timeout without an attributable provider record remains `UNKNOWN_PROVIDER_OUTCOME`, not free and not definitely billed. Account aggregate matching never establishes per-request provenance.
- MVP policy: max one server-confirmed success billable per logical request. Never claim proven client delivery without separate client acknowledgement.
- Use Decimal/fixed-point with defined rounding, timezone, valid period and pricing version.
- Evidence decision: `VERIFIED` only within explicit covered scope; `MISMATCH` observed contradiction; `INCOMPLETE` known missing source segment; `UNDETERMINED` ineliminable uncertainty.
- Keep `PRODUCTION`, `PILOT`, `SANDBOX`, `SYNTHETIC` separated. Hashes attest bytes, not global evidence completeness.
- Never include provider management keys, prompts, responses or confidential identifiers in public artifacts.

## Workflow
1. State sources of authority and unknowns per field.
2. Build/update truth-table fixtures covering timeout, retry, duplicate, late record, unknown provider ID, invoice discrepancy.
3. Compute manually audited expected result before changing production code.
4. Implement the smallest contract change. Confirm tenant from credentials, not untrusted payload.
5. Test schemas, duplicate behavior, money precision, coverage state and negative cases.
6. Emit trace `claim -> source keys -> manifest -> policy version -> test command/result`.

## STOP and output
Stop on unagreed billing policy, guessed evidence, unapproved provider calls or change with no independent fixture. Report exact scope, affected invariants, tests actually run, unknowns and next action. Do not mark PASS based on a written test plan.
