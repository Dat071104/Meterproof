#!/usr/bin/env python3
"""Check weighted option scores in ADR Markdown tables using Decimal."""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from pathlib import Path


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def decimal_cell(value: str) -> Decimal:
    return Decimal(value.strip("* `"))


def weighted_tables(markdown: str) -> Iterator[tuple[list[str], list[list[str]]]]:
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        header = cells(line)
        if (
            len(header) < 5
            or header[0].strip("* ").lower() != "criterion"
            or header[1].strip("* ").lower() != "weight"
        ):
            continue
        rows = []
        for candidate in lines[index + 1 :]:
            if not candidate.lstrip().startswith("|"):
                break
            row = cells(candidate)
            if row and all(re.fullmatch(r":?-{3,}:?", cell) for cell in row):
                continue
            rows.append(row)
        yield header, rows


def inspect_markdown(markdown: str) -> tuple[list[str], list[str]]:
    errors = []
    details = []
    for number, (header, rows) in enumerate(weighted_tables(markdown), 1):
        options = header[3:]
        criteria = []
        stated = None
        for row in rows:
            if len(row) != len(header):
                errors.append(f"table {number}: row has {len(row)} cells; expected {len(header)}")
                continue
            label = row[0].strip("* ")
            if "weighted total" in label.lower():
                stated = row[3:]
                continue
            try:
                weight = decimal_cell(row[1])
                scores = [decimal_cell(value) for value in row[3:]]
            except InvalidOperation:
                errors.append(f"table {number}: {label!r} has a non-numeric weight or score")
                continue
            criteria.append((label, weight, scores))
        if not criteria:
            errors.append(f"table {number}: no criterion rows")
            continue
        weight_total = sum((weight for _, weight, _ in criteria), Decimal(0))
        if weight_total != Decimal(100):
            errors.append(f"table {number}: weights total {weight_total}, expected 100")
        if stated is None:
            errors.append(f"table {number}: missing weighted total row")
            continue
        if len(stated) != len(options):
            errors.append(
                f"table {number}: weighted total has {len(stated)} scores; expected {len(options)}"
            )
            continue
        computed = [
            sum((weight * scores[index] for _, weight, scores in criteria), Decimal(0))
            / Decimal(100)
            for index in range(len(options))
        ]
        for index, option in enumerate(options):
            try:
                stated_score = decimal_cell(stated[index])
            except InvalidOperation:
                errors.append(
                    f"table {number}: {option} has a non-numeric stated total {stated[index]!r}"
                )
                continue
            if stated_score != computed[index]:
                errors.append(
                    f"table {number}: {option} computed {computed[index]:.2f}, stated {stated_score:.2f}"
                )
        details.append(
            f"table {number}: weights={weight_total}; "
            + ", ".join(f"{option}={score:.2f}" for option, score in zip(options, computed))
        )
        if errors:
            for label, weight, scores in criteria:
                contributions = ", ".join(
                    f"{option}: {weight}x{score}={weight * score / Decimal(100):.2f}"
                    for option, score in zip(options, scores)
                )
                details.append(f"  {label}: {contributions}")
    return errors, details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    paths = sorted((args.root / "docs" / "adr").glob("ADR_*.md"))
    failed = False
    tables_found = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        tables_found += sum(1 for _ in weighted_tables(text))
        errors, details = inspect_markdown(text)
        if errors:
            failed = True
            print(f"FAIL {path.relative_to(args.root)}")
            for error in errors:
                print(f"  {error}")
            for detail in details:
                print(f"  {detail}")
        elif details:
            print(f"PASS {path.relative_to(args.root)}: {details[0]}")
    if tables_found == 0:
        print("No weighted ADR tables found.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
