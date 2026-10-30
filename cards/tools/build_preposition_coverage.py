#!/usr/bin/env python3
"""Validate and merge Phase 1 preposition inventory slices."""

from __future__ import annotations

import argparse
import csv
import io
import sys
from collections import Counter
from pathlib import Path


CARDS_DIR = Path(__file__).resolve().parents[1]
PREPOSITIONS_DIR = CARDS_DIR / "prepositions"
SLICES_DIR = PREPOSITIONS_DIR / "inventory-slices"
OUTPUT_PATH = PREPOSITIONS_DIR / "coverage.tsv"

HEADER = [
    "item_id",
    "subdeck",
    "topic",
    "target_form",
    "meaning_or_distinction",
    "construction",
    "confusables",
    "card_type",
    "register",
    "source_file",
    "card_id",
    "status",
    "notes",
]

SLICE_CONTRACTS = {
    "01-03.tsv": {
        "01 Time": "01-time.md",
        "02 Place": "02-place.md",
        "03 Movement": "03-movement.md",
    },
    "04-05.tsv": {
        "04 Abstract Relationships": "04-abstract-relationships.md",
        "05 Verb + Preposition": "05-verb-preposition.md",
    },
    "06-07.tsv": {
        "06 Adjective and Participle + Preposition": (
            "06-adjective-participle-preposition.md"
        ),
        "07 Noun + Preposition": "07-noun-preposition.md",
    },
    "08-09.tsv": {
        "08 Fixed and Multiword Expressions": (
            "08-fixed-multiword-expressions.md"
        ),
        "09 No Preposition and Grammar Traps": (
            "09-no-preposition-grammar-traps.md"
        ),
    },
}

CARD_TYPES = {"chunk", "context", "contrast", "repair"}
STATUSES = {"proposed", "excluded"}
REGISTER_NORMALIZATION = {
    "neutral-formal": "neutral/formal",
}


class InventoryError(ValueError):
    """Raised when an inventory slice violates the merge contract."""


def read_slice(path: Path, contract: dict[str, str]) -> list[list[str]]:
    text = path.read_text(encoding="utf-8")
    if "\r" in text:
        raise InventoryError(f"{path.name}: carriage returns are not allowed")

    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if not rows or rows[0] != HEADER:
        raise InventoryError(f"{path.name}: header does not match the contract")

    output: list[list[str]] = []
    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(HEADER):
            raise InventoryError(
                f"{path.name}:{line_number}: expected {len(HEADER)} fields, "
                f"found {len(row)}"
            )
        if any("\n" in field or "\t" in field for field in row):
            raise InventoryError(
                f"{path.name}:{line_number}: embedded tabs/newlines are forbidden"
            )

        item_id, subdeck = row[0].strip(), row[1].strip()
        if not item_id:
            raise InventoryError(f"{path.name}:{line_number}: empty item_id")
        if subdeck not in contract:
            raise InventoryError(
                f"{path.name}:{line_number}: unexpected subdeck {subdeck!r}"
            )
        if row[9] != contract[subdeck]:
            raise InventoryError(
                f"{path.name}:{line_number}: source_file {row[9]!r} does not "
                f"match {subdeck!r}"
            )
        if row[7] not in CARD_TYPES:
            raise InventoryError(
                f"{path.name}:{line_number}: invalid card_type {row[7]!r}"
            )
        if row[10]:
            raise InventoryError(
                f"{path.name}:{line_number}: card_id must be empty in Phase 1"
            )
        if row[11] not in STATUSES:
            raise InventoryError(
                f"{path.name}:{line_number}: invalid status {row[11]!r}"
            )
        if any(not row[index].strip() for index in (2, 3, 4, 5, 7, 8, 9, 11)):
            raise InventoryError(
                f"{path.name}:{line_number}: required inventory field is empty"
            )

        normalized = [field.strip() for field in row]
        normalized[0] = normalized[0].upper()
        normalized[8] = REGISTER_NORMALIZATION.get(
            normalized[8], normalized[8]
        )
        output.append(normalized)

    return output


def build_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    seen_ids: dict[str, str] = {}

    for slice_name, contract in SLICE_CONTRACTS.items():
        path = SLICES_DIR / slice_name
        if not path.is_file():
            raise InventoryError(f"missing inventory slice: {path}")
        for row in read_slice(path, contract):
            item_id = row[0]
            if item_id in seen_ids:
                raise InventoryError(
                    f"duplicate item_id {item_id!r} in {slice_name} and "
                    f"{seen_ids[item_id]}"
                )
            seen_ids[item_id] = slice_name
            rows.append(row)

    return rows


def render(rows: list[list[str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(
        buffer,
        delimiter="\t",
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buffer.getvalue()


def print_counts(rows: list[list[str]]) -> None:
    deck_counts = Counter(row[1] for row in rows)
    type_counts = Counter(row[7] for row in rows)
    status_counts = Counter(row[11] for row in rows)

    print(f"rows: {len(rows)}")
    for subdeck in sorted(deck_counts):
        print(f"  {subdeck}: {deck_counts[subdeck]}")
    print("card types:")
    for card_type in sorted(type_counts):
        print(f"  {card_type}: {type_counts[card_type]}")
    print("statuses:")
    for status in sorted(status_counts):
        print(f"  {status}: {status_counts[status]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate slices and require coverage.tsv to be current",
    )
    args = parser.parse_args()

    try:
        rows = build_rows()
        expected = render(rows)
    except (InventoryError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.check:
        try:
            actual = OUTPUT_PATH.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"error: missing generated file {OUTPUT_PATH}", file=sys.stderr)
            return 1
        if actual != expected:
            print(
                f"error: {OUTPUT_PATH} is stale; rebuild without --check",
                file=sys.stderr,
            )
            return 1
        print("coverage inventory is valid and current")
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="")
        print(f"wrote {OUTPUT_PATH}")

    print_counts(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
