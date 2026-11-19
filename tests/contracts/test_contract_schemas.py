from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "contracts" / "jsonschema"
FIXTURES = ROOT / "tests" / "fixtures" / "contracts"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_for(name: str):
    return load_json(SCHEMAS / name)


def flatten(errors):
    for error in errors:
        yield error
        yield from flatten(error.context)


def positive_receipts():
    for name in (
        "F1_two_billed_attempts_one_request.json",
        "F2_unlinked_timeout.json",
    ):
        yield from load_json(FIXTURES / name)["receipts"]
    f3 = load_json(FIXTURES / "F3_invoice_late_duplicate_wrong.json")
    for case in f3["cases"]:
        yield from case["receipts"]


def test_every_schema_is_valid_draft_2020_12():
    for path in sorted(SCHEMAS.glob("*.v1.schema.json")):
        Draft202012Validator.check_schema(load_json(path))


def test_every_positive_contract_record_validates():
    receipt_validator = Draft202012Validator(
        schema_for("source_receipt.v1.schema.json"),
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    for receipt in positive_receipts():
        receipt_validator.validate(receipt)

    examples = load_json(FIXTURES / "schema_examples.json")
    receipt_validator.validate(examples["unlinked_billed_provider_receipt"])
    for receipt in examples["additional_source_receipts"]:
        receipt_validator.validate(receipt)
    for key, schema_name in (
        ("verification_decision", "verification_decision.v1.schema.json"),
        ("published_read_report", "published_read_report.v1.schema.json"),
        ("replay_manifest", "replay_manifest.v1.schema.json"),
    ):
        validator = Draft202012Validator(
            schema_for(schema_name),
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
        validator.validate(examples[key])


def test_every_negative_fixture_fails_for_its_declared_reason():
    for fixture_path in sorted((FIXTURES / "negative").glob("N*.json")):
        fixture = load_json(fixture_path)
        validator = Draft202012Validator(
            schema_for(fixture["target_schema"]),
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
        errors = list(validator.iter_errors(fixture["instance"]))
        expected = fixture["expected_error"]
        assert errors, fixture_path.name
        matching = [
            error
            for error in flatten(errors)
            if error.validator == expected["validator"]
            and list(error.absolute_path) == expected["path"]
            and ("property" not in expected or expected["property"] in error.message)
        ]
        assert matching, f"{fixture_path.name}: expected {expected}; got {[e.message for e in flatten(errors)]}"


def test_every_usd_schema_field_uses_the_frozen_pattern_and_transport_is_not_a_receipt_field():
    expected = r"^(0|[1-9][0-9]{0,11})(\.[0-9]{1,12})?$"

    def walk(node, path=()):
        if isinstance(node, dict):
            properties = node.get("properties", {})
            for name, child in properties.items():
                child_path = path + (name,)
                if name.endswith("_usd"):
                    assert child.get("pattern") == expected, child_path
                yield from walk(child, child_path)
            for key, value in node.items():
                if key != "properties":
                    yield from walk(value, path + (key,))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                yield from walk(value, path + (str(index),))

    for schema_path in sorted(SCHEMAS.glob("*.v1.schema.json")):
        list(walk(load_json(schema_path)))
    receipt_schema = schema_for("source_receipt.v1.schema.json")
    assert "transport_delivery_id" not in receipt_schema["properties"]
