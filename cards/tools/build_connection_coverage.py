#!/usr/bin/env python3
"""Validate and merge Connection Patterns inventory slices."""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


CARDS_DIR = Path(__file__).resolve().parents[1]
CONNECTIONS_DIR = CARDS_DIR / "connections"
SLICES_DIR = CONNECTIONS_DIR / "inventory-slices"
OUTPUT_PATH = CONNECTIONS_DIR / "coverage.tsv"

HEADER = [
    "item_id",
    "subdeck",
    "topic",
    "anchor",
    "connector_or_marker",
    "complement_shape",
    "target_pattern",
    "meaning_or_distinction",
    "confusables",
    "card_type",
    "register",
    "source_file",
    "card_id",
    "status",
    "evidence_note",
    "notes",
]

SUBDECK_SOURCES = {
    "01 Prepositions and Prepositional Phrases": "01-prepositions.md",
    "02 Verb Patterns": "02-verb-patterns.md",
    "03 Adjective and Participle Patterns": (
        "03-adjective-participle-patterns.md"
    ),
    "04 Noun Patterns": "04-noun-patterns.md",
    "05 Conjunctions and Clause Linkers": (
        "05-conjunction-clause-linkers.md"
    ),
    "06 Relative and Noun-Modifying Clauses": (
        "06-relative-noun-modifying-clauses.md"
    ),
    "07 Non-finite and Reduced Clauses": (
        "07-nonfinite-reduced-clauses.md"
    ),
    "08 Coordination and Parallelism": "08-coordination-parallelism.md",
    "09 Comparison, Degree, and Result Patterns": (
        "09-comparison-degree-result.md"
    ),
}

SLICE_SUBDECKS = {
    "01-02.tsv": {
        "01 Prepositions and Prepositional Phrases",
        "02 Verb Patterns",
    },
    "03-04.tsv": {
        "03 Adjective and Participle Patterns",
        "04 Noun Patterns",
    },
    "05-07.tsv": {
        "05 Conjunctions and Clause Linkers",
        "06 Relative and Noun-Modifying Clauses",
        "07 Non-finite and Reduced Clauses",
    },
    "08-09.tsv": {
        "08 Coordination and Parallelism",
        "09 Comparison, Degree, and Result Patterns",
    },
}

ID_PREFIXES = {
    "01 Prepositions and Prepositional Phrases": "PREP-",
    "02 Verb Patterns": "VERB-",
    "03 Adjective and Participle Patterns": "ADJ-",
    "04 Noun Patterns": "NOUN-",
    "05 Conjunctions and Clause Linkers": "LINK-",
    "06 Relative and Noun-Modifying Clauses": "REL-",
    "07 Non-finite and Reduced Clauses": "NF-",
    "08 Coordination and Parallelism": "COORD-",
    "09 Comparison, Degree, and Result Patterns": "CMP-",
}

COMPLEMENT_SHAPES = {
    "NP",
    "finite-clause",
    "that-clause",
    "wh-clause",
    "to-inf",
    "bare-inf",
    "V-ing-clause",
    "past-participle-clause",
    "AdjP",
    "PP",
    "predicative-NP",
    "relative-clause",
    "reduced-relative",
    "parallel-unit",
    "zero",
}
CARD_TYPES = {"chunk", "context", "contrast", "repair"}
REGISTERS = {
    "conversational",
    "conversational/neutral",
    "neutral",
    "neutral/formal",
    "formal",
}
STATUSES = {"proposed", "validated", "excluded", "deferred"}
REQUIRED_NONEMPTY = {
    "item_id",
    "subdeck",
    "topic",
    "anchor",
    "connector_or_marker",
    "complement_shape",
    "target_pattern",
    "meaning_or_distinction",
    "card_type",
    "register",
    "source_file",
    "status",
}
ITEM_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")


class InventoryError(ValueError):
    """Raised when an inventory slice violates the merge contract."""


def _read_slice(path: Path, allowed_subdecks: set[str]) -> list[list[str]]:
    text = path.read_text(encoding="utf-8")
    if "\r" in text:
        raise InventoryError(f"{path.name}: carriage returns are not allowed")

    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if not rows or rows[0] != HEADER:
        raise InventoryError(f"{path.name}: header does not match the contract")

    output: list[list[str]] = []
    for line_number, raw_row in enumerate(rows[1:], start=2):
        if len(raw_row) != len(HEADER):
            raise InventoryError(
                f"{path.name}:{line_number}: expected {len(HEADER)} fields, "
                f"found {len(raw_row)}"
            )
        if any("\n" in field or "\t" in field for field in raw_row):
            raise InventoryError(
                f"{path.name}:{line_number}: embedded tabs/newlines are forbidden"
            )

        row = [field.strip() for field in raw_row]
        record = dict(zip(HEADER, row))
        for field in REQUIRED_NONEMPTY:
            if not record[field]:
                raise InventoryError(
                    f"{path.name}:{line_number}: required field {field!r} is empty"
                )

        item_id = record["item_id"]
        subdeck = record["subdeck"]
        if not ITEM_ID_RE.fullmatch(item_id):
            raise InventoryError(
                f"{path.name}:{line_number}: malformed item_id {item_id!r}"
            )
        if subdeck not in allowed_subdecks:
            raise InventoryError(
                f"{path.name}:{line_number}: unexpected subdeck {subdeck!r}"
            )
        if not item_id.startswith(ID_PREFIXES[subdeck]):
            raise InventoryError(
                f"{path.name}:{line_number}: {item_id!r} needs prefix "
                f"{ID_PREFIXES[subdeck]!r}"
            )
        if record["source_file"] != SUBDECK_SOURCES[subdeck]:
            raise InventoryError(
                f"{path.name}:{line_number}: source_file "
                f"{record['source_file']!r} does not match {subdeck!r}"
            )

        shapes = [
            shape.strip() for shape in record["complement_shape"].split(";")
        ]
        invalid_shapes = set(shapes) - COMPLEMENT_SHAPES
        if invalid_shapes or any(not shape for shape in shapes):
            raise InventoryError(
                f"{path.name}:{line_number}: invalid complement shape(s): "
                f"{sorted(invalid_shapes)!r}"
            )
        if len(shapes) != len(set(shapes)):
            raise InventoryError(
                f"{path.name}:{line_number}: duplicate complement shape"
            )
        record["complement_shape"] = ";".join(shapes)
        row[HEADER.index("complement_shape")] = record["complement_shape"]
        if record["card_type"] not in CARD_TYPES:
            raise InventoryError(
                f"{path.name}:{line_number}: invalid card_type "
                f"{record['card_type']!r}"
            )
        if record["register"] not in REGISTERS:
            raise InventoryError(
                f"{path.name}:{line_number}: invalid register "
                f"{record['register']!r}"
            )
        if record["status"] not in STATUSES:
            raise InventoryError(
                f"{path.name}:{line_number}: invalid status "
                f"{record['status']!r}"
            )
        if record["status"] == "validated" and not record["card_id"]:
            raise InventoryError(
                f"{path.name}:{line_number}: validated item needs card_id"
            )
        if record["status"] != "validated" and record["card_id"]:
            raise InventoryError(
                f"{path.name}:{line_number}: only validated items may have "
                "card_id"
            )

        output.append(row)

    return output


def build_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    seen_ids: dict[str, str] = {}

    for slice_name, allowed_subdecks in SLICE_SUBDECKS.items():
        path = SLICES_DIR / slice_name
        if not path.is_file():
            raise InventoryError(f"missing inventory slice: {path}")
        for row in _read_slice(path, allowed_subdecks):
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
    indexes = {name: HEADER.index(name) for name in HEADER}
    deck_counts = Counter(row[indexes["subdeck"]] for row in rows)
    type_counts = Counter(row[indexes["card_type"]] for row in rows)
    status_counts = Counter(row[indexes["status"]] for row in rows)
    shape_counts: Counter[str] = Counter()
    target_locations: dict[str, list[str]] = defaultdict(list)

    for row in rows:
        for shape in row[indexes["complement_shape"]].split(";"):
            shape_counts[shape] += 1
        if row[indexes["status"]] == "proposed":
            target_locations[row[indexes["target_pattern"]].casefold()].append(
                row[indexes["item_id"]]
            )

    print(f"rows: {len(rows)}")
    for subdeck in SUBDECK_SOURCES:
        print(f"  {subdeck}: {deck_counts[subdeck]}")
    print("card types:")
    for card_type in sorted(type_counts):
        print(f"  {card_type}: {type_counts[card_type]}")
    print("statuses:")
    for status in sorted(status_counts):
        print(f"  {status}: {status_counts[status]}")
    print("complement shapes:")
    for shape in sorted(shape_counts):
        print(f"  {shape}: {shape_counts[shape]}")

    duplicate_targets = {
        target: item_ids
        for target, item_ids in target_locations.items()
        if len(item_ids) > 1
    }
    if duplicate_targets:
        print("review repeated proposed target_pattern values:")
        for target, item_ids in sorted(duplicate_targets.items()):
            print(f"  {target}: {', '.join(item_ids)}")


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
        print("connection inventory is valid and current")
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="")
        print(f"wrote {OUTPUT_PATH}")

    print_counts(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
