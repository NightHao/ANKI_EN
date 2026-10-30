#!/usr/bin/env python3
"""Promote reviewed Connection Patterns cards from proposed to validated.

This is deliberately a mechanical finalization step. It does not decide
whether a card is linguistically ready; that decision must be completed in the
review reports before ``--apply`` is run.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

import build_connection_coverage as coverage
import build_connection_import as card_build


STATUS_INDEX = coverage.HEADER.index("status")
CARD_ID_INDEX = coverage.HEADER.index("card_id")
ITEM_ID_INDEX = coverage.HEADER.index("item_id")
SOURCE_INDEX = coverage.HEADER.index("source_file")
COMPLEMENT_SHAPE_INDEX = coverage.HEADER.index("complement_shape")


class PromotionError(ValueError):
    """Raised when the deck cannot be promoted safely."""


def _read_slice(path: Path) -> tuple[list[str], list[list[str]]]:
    text = path.read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if not rows or rows[0] != coverage.HEADER:
        raise PromotionError(f"{path}: invalid inventory header")
    normalized_rows: list[list[str]] = []
    for raw_row in rows[1:]:
        row = [field.strip() for field in raw_row]
        row[COMPLEMENT_SHAPE_INDEX] = ";".join(
            shape.strip()
            for shape in row[COMPLEMENT_SHAPE_INDEX].split(";")
        )
        normalized_rows.append(row)
    return rows[0], normalized_rows


def _render_rows(header: list[str], rows: list[list[str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(
        buffer,
        delimiter="\t",
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue()


def _load_cards() -> list[card_build.Card]:
    manifest = card_build._read_manifest()
    cards = card_build._load_all_cards()
    card_build._validate_cards(cards, manifest, final=False)
    for source_name in card_build.SOURCE_DECKS:
        source_cards = [
            card for card in cards if card.source_file == source_name
        ]
        card_build._validate_source_completeness(
            source_cards, manifest, source_name
        )
    return cards


def _require_current_coverage() -> None:
    expected = coverage.render(coverage.build_rows())
    try:
        actual = coverage.OUTPUT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise PromotionError(
            "coverage.tsv is missing; rebuild the inventory first"
        ) from error
    if actual != expected:
        raise PromotionError(
            "coverage.tsv is stale; rebuild the inventory before promotion"
        )


def _prepare_promotion() -> tuple[
    dict[Path, str], dict[Path, str], str, int
]:
    _require_current_coverage()
    cards = _load_cards()
    card_by_item = {card.item_id: card for card in cards}

    source_outputs: dict[Path, str] = {}
    for source_name in card_build.SOURCE_DECKS:
        path = card_build.CONNECTIONS_DIR / source_name
        text = path.read_text(encoding="utf-8")
        source_cards = [
            card for card in cards if card.source_file == source_name
        ]
        proposed_count = sum(card.status == "proposed" for card in source_cards)
        if proposed_count:
            expected_marker_count = text.count("status: proposed")
            if expected_marker_count != proposed_count:
                raise PromotionError(
                    f"{source_name}: source status marker count does not "
                    "match parsed cards"
                )
            text = text.replace("status: proposed", "status: validated")
        source_outputs[path] = text

    slice_outputs: dict[Path, str] = {}
    merged_rows: list[list[str]] = []
    promoted = 0
    seen_viable: set[str] = set()
    for slice_name in coverage.SLICE_SUBDECKS:
        path = coverage.SLICES_DIR / slice_name
        header, rows = _read_slice(path)
        updated_rows: list[list[str]] = []
        for row in rows:
            updated = list(row)
            item_id = updated[ITEM_ID_INDEX].strip()
            status = updated[STATUS_INDEX].strip()
            if status == "deferred":
                raise PromotionError(
                    f"{slice_name}: unresolved deferred item {item_id}"
                )
            if status in {"proposed", "validated"}:
                card = card_by_item.get(item_id)
                if not card:
                    raise PromotionError(
                        f"{slice_name}: viable item {item_id} has no card"
                    )
                if card.source_file != updated[SOURCE_INDEX].strip():
                    raise PromotionError(
                        f"{slice_name}: source mismatch for {item_id}"
                    )
                if status == "proposed":
                    updated[CARD_ID_INDEX] = card.card_id
                    updated[STATUS_INDEX] = "validated"
                    promoted += 1
                elif updated[CARD_ID_INDEX].strip() != card.card_id:
                    raise PromotionError(
                        f"{slice_name}: validated card ID mismatch for "
                        f"{item_id}"
                    )
                seen_viable.add(item_id)
            updated_rows.append(updated)
            merged_rows.append(updated)
        slice_outputs[path] = _render_rows(header, updated_rows)

    missing = sorted(set(card_by_item) - seen_viable)
    if missing:
        raise PromotionError(
            "source cards without viable inventory items: "
            + ", ".join(missing[:12])
        )

    coverage_output = coverage.render(merged_rows)
    return source_outputs, slice_outputs, coverage_output, promoted


def _check_final_state() -> int:
    _require_current_coverage()
    manifest = card_build._read_manifest()
    cards = card_build._load_all_cards()
    for source_name in card_build.SOURCE_DECKS:
        source_cards = [
            card for card in cards if card.source_file == source_name
        ]
        card_build._validate_source_completeness(
            source_cards, manifest, source_name
        )
    card_build._validate_cards(cards, manifest, final=True)
    print(f"promotion state is complete: {len(cards)} validated cards")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--apply",
        action="store_true",
        help="promote every reviewed viable card and update coverage.tsv",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="require a complete, internally consistent promoted state",
    )
    args = parser.parse_args()

    try:
        if args.check:
            return _check_final_state()

        source_outputs, slice_outputs, coverage_output, promoted = (
            _prepare_promotion()
        )
        for path, text in source_outputs.items():
            path.write_text(text, encoding="utf-8", newline="")
        for path, text in slice_outputs.items():
            path.write_text(text, encoding="utf-8", newline="")
        coverage.OUTPUT_PATH.write_text(
            coverage_output, encoding="utf-8", newline=""
        )
        print(f"promoted {promoted} cards")
        print(f"updated {len(source_outputs)} sources and "
              f"{len(slice_outputs)} inventory slices")
        return _check_final_state()
    except (
        PromotionError,
        coverage.InventoryError,
        card_build.BuildError,
        OSError,
        UnicodeError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
