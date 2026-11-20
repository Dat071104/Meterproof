# JSON Schema Changelog — v1 pre-release drafts

The four v1 schemas remain pre-release drafts until P0.2 is approved. These changes are confined to the P0.2 work order; after approval, new contract changes require a new version file.

| Schema / contract | Change | Reason | Invariant | Negative fixture |
|---|---|---|---|---|
| `source_receipt.v1.schema.json` | Add source-kind/outcome conditional rules for APP, PROVIDER, and INVOICE; paired provider linkage; require billed provider cost/evidence; add invoice period/reference/amount and null provider fields. | Allow unlinked invoice/provider observations while preventing unsupported source/outcome combinations and incomplete billed/invoice receipts. | D2, D4 | N05–N11 and N16–N19 (N07/N08 were already rejected by the pre-change schema; N09/N10 and N16/N17 use legacy-shaped baseline instances). |
| `source_receipt.v1.schema.json` | Tighten `known_provider_cost_usd` to the 12+12 decimal string pattern; add `invoice_amount_usd` with the same pattern. | Preserve exact observed amounts within the declared numeric representation; reject over-scale values rather than round. | D5 / INV-05 | N12 and N20; N10 proves the old schema accepted an invoice with no invoice amount. |
| `verification_decision.v1.schema.json` | Require `origin`; require eligible publication to be VERIFIED and EQUAL; require VERIFIED decisions to be EQUAL with an explicit empty `unresolved_items`. | Encode source-origin and publication/decision implications that were previously unenforced. | D8 / INV-06 | N01–N04 (N01–N03 use legacy instances without the new origin property for old-schema controls). |
| `verification_decision.v1.schema.json` | For `business_verdict = VERIFIED`, require `policy_version` to be a non-empty string. | Missing policy means the calculation scope cannot be VERIFIED (DOMAIN_SPEC_v1.md §23; C6). | C6 | N34. |
| `published_read_report.v1.schema.json` | Make `business_verdict` const `VERIFIED`; apply D5 to every `*_usd` property. | Only a covered VERIFIED candidate may be published; published money must keep exact declared precision. | D5, D8 / INV-05, INV-06 | N13–N14. |
| `replay_manifest.v1.schema.json` | Keep the field set unchanged; require non-empty values for unformatted string fields and string-array items. | Reject empty source identities, references and exclusions without changing the frozen source-cut shape. | D2, D7, SOURCE_CUT_PROTOCOL §§8, 12 | Schema traversal control in `test_unformatted_strings_and_string_array_items_are_nonempty`. |

### WAVE-01 FIX1 — pre-release contract corrections

| Schema / contract | Change | Reason | Invariant | Negative fixture / control |
|---|---|---|---|---|
| `verification_decision.v1.schema.json` | Add the DEC-0008 two-axis rule: `DIFFERENT`, `NOT_COMPARABLE` and `ERROR` allow only `INCOMPLETE` or `UNDETERMINED`; retain the existing EQUAL requirements for `VERIFIED`. | Candidate disagreement or an incomparable cut cannot be reported as a business mismatch. | D8, SOURCE_CUT_PROTOCOL §9 | N21–N23; positive EQUAL+MISMATCH and DIFFERENT+UNDETERMINED decisions. |
| All four v1 schemas | Add `minLength: 1` to unformatted string and nullable-string schema nodes and to string-array items; leave every `required` list unchanged. | Prevent empty identities, references, scopes, coverage notes and array entries. | D2, INV-01, INV-04, INV-06 | N24–N28 and schema traversal control. |
| `source_receipt.v1.schema.json` | Restrict APP/PROVIDER field authority; APP provider generation is a correlation hint, not cost evidence; app cost/evidence fields are absent or null, invoice amount is absent; PROVIDER invoice amount is absent; NOT_BILLED cost is absent or null. | Prevent source-authority crossover while preserving the frozen D5 money pattern. | D2, D4, D5, INV-02, INV-05 | N29–N32. |
| `published_read_report.v1.schema.json` | Keep the frozen D5 pattern and add a nested two-fractional-digit constraint to `customer_charge_usd`. | Enforce the cent-rounded published customer charge representation. | D5, INV-05 | N33. |

D9 also updates only the Gate state line in `docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md` to include the validator's `HUMAN_CONDITIONAL_GO` state; this contract-line change is not a JSON Schema change and has no JSON negative fixture.
