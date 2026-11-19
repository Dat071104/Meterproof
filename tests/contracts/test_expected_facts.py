from __future__ import annotations

import hashlib
import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "fixtures" / "contracts"
CENT = Decimal("0.01")
TWELVE_PLACES = Decimal("0.000000000001")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def money_text(value: Decimal) -> str:
    return format(value, "f")


def compute_billable_facts(policy, receipts):
    successful_requests = {
        receipt["logical_request_id"]
        for receipt in receipts
        if receipt["source_kind"] == "APP"
        and receipt["outcome"] == "APP_OBSERVED_SUCCESS"
    }
    billable_units = len(successful_requests)
    charge = (Decimal(policy["unit_price_usd"]) * billable_units).quantize(
        CENT, rounding=ROUND_HALF_EVEN
    )
    return {
        "billable_units": billable_units,
        "customer_charge_usd": money_text(charge),
    }


def compute_provider_facts(receipts):
    provider_receipts = [
        receipt for receipt in receipts if receipt["source_kind"] == "PROVIDER"
    ]
    provider_by_generation = {}
    for receipt in provider_receipts:
        if receipt["outcome"] != "PROVIDER_CONFIRMED_BILLED":
            continue
        provider_by_generation.setdefault(
            receipt["provider_generation_id"], Decimal(receipt["known_provider_cost_usd"])
        )
    known_spend = (
        sum(provider_by_generation.values(), Decimal("0"))
        if provider_receipts
        else None
    )
    unattributed_by_generation = {}
    for receipt in provider_receipts:
        if (
            receipt["outcome"] == "PROVIDER_CONFIRMED_BILLED"
            and receipt["provider_attempt_id"] is None
            and receipt["logical_request_id"] is None
        ):
            unattributed_by_generation.setdefault(
                receipt["provider_generation_id"], Decimal(receipt["known_provider_cost_usd"])
            )
    unattributed_spend = sum(unattributed_by_generation.values(), Decimal("0.0000"))
    linked_attempt_ids = {
        receipt["provider_attempt_id"]
        for receipt in provider_receipts
        if receipt["provider_attempt_id"] is not None
    }
    unresolved = sorted(
        f"{receipt['provider_attempt_id']}: UNKNOWN_PROVIDER_OUTCOME with no linked provider receipt"
        for receipt in receipts
        if receipt["source_kind"] == "APP"
        and receipt["outcome"] == "UNKNOWN_PROVIDER_OUTCOME"
        and receipt["provider_attempt_id"] not in linked_attempt_ids
    )
    return {
        "known_provider_spend_usd": money_text(known_spend) if known_spend is not None else None,
        "provider_generation_ids_counted": sorted(provider_by_generation),
        "unattributed_known_spend_usd": money_text(unattributed_spend),
        "unresolved_items": unresolved,
    }


def compute_invoice_facts(fixture, receipts, charge):
    cut = parse_time(fixture["source_cut"]["as_known_at"])
    excluded = []
    included_by_source_event = {}
    for receipt in receipts:
        if receipt["source_kind"] != "INVOICE":
            continue
        first_observed = parse_time(receipt["first_observed_at"])
        if first_observed > cut:
            excluded.append(
                f"{receipt['source_event_id']}: first_observed_at {receipt['first_observed_at']} is after source cut {fixture['source_cut']['as_known_at']}"
            )
            continue
        included_by_source_event.setdefault(
            receipt["source_event_id"], Decimal(receipt["invoice_amount_usd"])
        )
    invoice_amount = (
        sum(included_by_source_event.values(), Decimal("0"))
        if included_by_source_event
        else None
    )
    invoice_delta = invoice_amount - charge if invoice_amount is not None else None
    return {
        "invoice_amount_usd": money_text(invoice_amount) if invoice_amount is not None else None,
        "invoice_delta": money_text(invoice_delta) if invoice_delta is not None else None,
        "source_exclusions": sorted(excluded),
        "counted_invoice_source_event_ids": sorted(included_by_source_event),
    }


def compute_case(fixture, case=None):
    if case is None:
        case = fixture
    receipts = case["receipts"]
    policy = fixture["price_policy"]
    billable = compute_billable_facts(policy, receipts)
    facts = {**billable, **compute_provider_facts(receipts)}
    facts.update(compute_invoice_facts(fixture, receipts, Decimal(billable["customer_charge_usd"])))
    return facts

def compute_verdicts(fixture, facts, case=None):
    expected = {}
    if facts["invoice_amount_usd"] is not None:
        invoice_verdict = "VERIFIED" if Decimal(facts["invoice_delta"]) == 0 else "MISMATCH"
        invoice_scope = "invoice_reconciliation" if case is not None and "case_id" in case else "customer_charge_vs_invoice"
        expected[invoice_scope] = invoice_verdict
    provider_scope = fixture.get("provider_scope")
    if provider_scope is not None:
        provider_verdict = (
            "UNDETERMINED"
            if facts["unresolved_items"]
            or Decimal(facts["unattributed_known_spend_usd"]) > 0
            or not provider_scope["complete_within_fixture"]
            else "VERIFIED"
        )
        expected["provider_spend"] = provider_verdict
    if "customer_charge_vs_invoice" in expected and "provider_spend" in expected:
        if expected["customer_charge_vs_invoice"] == "MISMATCH":
            expected["overall_fixture_scope"] = "MISMATCH"
        elif expected["provider_spend"] == "UNDETERMINED":
            expected["overall_fixture_scope"] = "UNDETERMINED"
        else:
            expected["overall_fixture_scope"] = "VERIFIED"
    return expected


def canonical_digest(fixture, facts, verdicts):
    canonical = dict(facts)
    for name in ("known_provider_spend_usd", "unattributed_known_spend_usd", "invoice_amount_usd"):
        if canonical[name] is not None:
            canonical[name] = format(Decimal(canonical[name]).quantize(TWELVE_PLACES), ".12f")
    if canonical["customer_charge_usd"] is not None:
        canonical["customer_charge_usd"] = format(Decimal(canonical["customer_charge_usd"]).quantize(CENT), ".2f")
    if canonical["invoice_delta"] is not None:
        canonical["invoice_delta"] = format(Decimal(canonical["invoice_delta"]).quantize(TWELVE_PLACES), ".12f")
    payload = {
        "billing_period_id": fixture["billing_period"]["billing_period_id"],
        "price_policy_version": fixture["price_policy"]["price_policy_version"],
        "facts": canonical,
        "verdicts": verdicts,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def all_cases():
    for name in ("F1_two_billed_attempts_one_request.json", "F2_unlinked_timeout.json"):
        fixture = load_json(FIXTURES / name)
        yield fixture, fixture
    fixture = load_json(FIXTURES / "F3_invoice_late_duplicate_wrong.json")
    for case in fixture["cases"]:
        yield fixture, case


def test_hand_computed_facts_match_f1_f2_f3():
    for fixture, case in all_cases():
        facts = compute_case(fixture, case)
        assert facts == case["expected_facts"], case.get("case_id", fixture["fixture_id"])
        verdicts = compute_verdicts(fixture, facts, case)
        expected_verdicts = case["expected_verdicts"]
        for scope, verdict in verdicts.items():
            assert expected_verdicts[scope]["business_verdict"] == verdict
            assert expected_verdicts[scope]["reason"]


def test_decimal_and_rounding_controls():
    decimal_spend = Decimal("0.0120") + Decimal("0.0090")
    assert decimal_spend == Decimal("0.0210")
    assert 0.012 + 0.009 != float(decimal_spend)
    assert Decimal("0.125").quantize(CENT, rounding=ROUND_HALF_EVEN) == Decimal("0.12")
    assert Decimal("0.125").quantize(CENT, rounding=ROUND_HALF_UP) == Decimal("0.13")


def test_canonical_facts_digest_is_deterministic():
    for fixture, case in all_cases():
        facts = compute_case(fixture, case)
        verdicts = compute_verdicts(fixture, facts, case)
        assert canonical_digest(fixture, facts, verdicts) == canonical_digest(fixture, facts, verdicts)


def test_unlinked_billed_provider_spend_is_known_unattributed_and_undetermined():
    fixture = {
        "billing_period": {"billing_period_id": "2026-11-01_UTC"},
        "price_policy": {"price_policy_version": "demo-v1", "unit_price_usd": "0.05"},
        "source_cut": {"as_known_at": "2026-12-01T00:00:00Z"},
        "provider_scope": {"complete_within_fixture": True},
    }
    receipt = {
        "source_kind": "PROVIDER", "outcome": "PROVIDER_CONFIRMED_BILLED",
        "provider_attempt_id": None, "logical_request_id": None,
        "provider_generation_id": "generation-orphan", "known_provider_cost_usd": "0.0030",
        "provider_amount_evidence_id": "provider-evidence-orphan",
    }
    case = {"receipts": [receipt]}
    facts = compute_case(fixture, case)
    verdicts = compute_verdicts(fixture, facts, case)
    assert facts["known_provider_spend_usd"] == "0.0030"
    assert facts["unattributed_known_spend_usd"] == "0.0030"
    assert verdicts["provider_spend"] == "UNDETERMINED"
