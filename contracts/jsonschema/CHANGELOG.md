# JSON Schema Changelog — v1 pre-release drafts

The four v1 schemas remain pre-release drafts until P0.2 is approved. These changes are confined to the P0.2 work order; after approval, new contract changes require a new version file.

| Schema / contract | Change | Reason | Invariant | Negative fixture |
|---|---|---|---|---|
| `source_receipt.v1.schema.json` | Add source-kind/outcome conditional rules for APP, PROVIDER, and INVOICE; paired provider linkage; require billed provider cost/evidence; add invoice period/reference/amount and null provider fields. | Allow unlinked invoice/provider observations while preventing unsupported source/outcome combinations and incomplete billed/invoice receipts. | D2, D4 | N05–N11 and N16–N19 (N07/N08 were already rejected by the pre-change schema; N09/N10 and N16/N17 use legacy-shaped baseline instances). |
| `source_receipt.v1.schema.json` | Tighten `known_provider_cost_usd` to the 12+12 decimal string pattern; add `invoice_amount_usd` with the same pattern. | Preserve exact observed amounts within the declared numeric representation; reject over-scale values rather than round. | D5 / INV-05 | N12 and N20; N10 proves the old schema accepted an invoice with no invoice amount. |
| `verification_decision.v1.schema.json` | Require `origin`; require eligible publication to be VERIFIED and EQUAL; require VERIFIED decisions to be EQUAL with an explicit empty `unresolved_items`. | Encode source-origin and publication/decision implications that were previously unenforced. | D8 / INV-06 | N01–N04 (N01–N03 use legacy instances without the new origin property for old-schema controls). |
| `published_read_report.v1.schema.json` | Make `business_verdict` const `VERIFIED`; apply D5 to every `*_usd` property. | Only a covered VERIFIED candidate may be published; published money must keep exact declared precision. | D5, D8 / INV-05, INV-06 | N13–N14. |
| `replay_manifest.v1.schema.json` | No schema change: inspected v1 manifest contains no `*_usd` properties and no D4/D8 rule applies to its existing shape. | Avoid adding an unsupported field or changing the frozen source-cut contract. | D1, D5, SOURCE_CUT_PROTOCOL §§8, 12 | N/A — no changed rule. |

D9 also updates only the Gate state line in `docs/contracts/DOMAIN_AND_EVIDENCE_CONTRACT.md` to include the validator's `HUMAN_CONDITIONAL_GO` state; this contract-line change is not a JSON Schema change and has no JSON negative fixture.
