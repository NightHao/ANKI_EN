#!/usr/bin/env python3
"""Validate Connection Patterns Markdown and build one Anki TSV.

Canonical inputs:
  EN/cards/connections/01-prepositions.md
  ...
  EN/cards/connections/09-comparison-degree-result.md
  EN/cards/connections/coverage.tsv

Output:
  EN/cards/connections/anki-import.tsv
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


CARDS_DIR = Path(__file__).resolve().parents[1]
CONNECTIONS_DIR = CARDS_DIR / "connections"
COVERAGE_PATH = CONNECTIONS_DIR / "coverage.tsv"
OUTPUT_PATH = CONNECTIONS_DIR / "anki-import.tsv"
PARENT_DECK = "EN::Connection Patterns"

SOURCE_DECKS = {
    "01-prepositions.md": "01 Prepositions and Prepositional Phrases",
    "02-verb-patterns.md": "02 Verb Patterns",
    "03-adjective-participle-patterns.md": (
        "03 Adjective and Participle Patterns"
    ),
    "04-noun-patterns.md": "04 Noun Patterns",
    "05-conjunction-clause-linkers.md": (
        "05 Conjunctions and Clause Linkers"
    ),
    "06-relative-noun-modifying-clauses.md": (
        "06 Relative and Noun-Modifying Clauses"
    ),
    "07-nonfinite-reduced-clauses.md": (
        "07 Non-finite and Reduced Clauses"
    ),
    "08-coordination-parallelism.md": "08 Coordination and Parallelism",
    "09-comparison-degree-result.md": (
        "09 Comparison, Degree, and Result Patterns"
    ),
}

COVERAGE_HEADER = [
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

CARD_TYPES = {"chunk", "context", "contrast", "repair"}
SOURCE_STATUSES = {"proposed", "validated"}
MANIFEST_STATUSES = {"proposed", "validated", "excluded", "deferred"}
CARD_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$")
CARD_HEADING_RE = re.compile(r"(?m)^## ([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\s*$")
META_RE = re.compile(r"\A\s*<!-- card\n(.*?)\n-->\s*", re.DOTALL)
FIELD_HEADING_RE = re.compile(r"(?m)^### (Front|Back)\s*$")
META_LINE_RE = re.compile(r"^([a-z_]+):[ \t]*(.*?)$")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")
NUMBERED_PROMPT_RE = re.compile(r"(?m)^\d+\.\s+")
EXAMPLE_BULLET_RE = re.compile(r"(?m)^-\s+\S")
FORBIDDEN_SCAFFOLD = (
    "complete the connection for this meaning",
    "complete the frame for this meaning",
    "complete the construction for this meaning",
    "complete the linker pattern for this meaning",
    "choose the pattern for this distinction",
    "choose the frame that matches this meaning",
    "choose the construction for this meaning",
    "choose the construction for this precise distinction",
    "use the completed frame in a natural sentence",
    "use a context that fixes the intended reference",
    "keep the complement shape",
    "context cue:",
    "decision:",
)


@dataclass(frozen=True)
class ManifestItem:
    item_id: str
    subdeck: str
    card_type: str
    source_file: str
    card_id: str
    status: str


@dataclass(frozen=True)
class Card:
    card_id: str
    item_id: str
    card_type: str
    status: str
    source_file: str
    subdeck: str
    front: str
    back: str
    line_number: int


class BuildError(ValueError):
    """Raised when canonical card sources violate the build contract."""


def _normalize_visible(value: str) -> str:
    return " ".join(value.casefold().split())


def _read_manifest(path: Path = COVERAGE_PATH) -> dict[str, ManifestItem]:
    text = path.read_text(encoding="utf-8")
    if "\r" in text:
        raise BuildError(f"{path}: carriage returns are not allowed")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t"))
    if not rows or rows[0] != COVERAGE_HEADER:
        raise BuildError(f"{path}: header does not match the master contract")

    items: dict[str, ManifestItem] = {}
    seen_card_ids: dict[str, str] = {}
    for line_number, row in enumerate(rows[1:], start=2):
        if len(row) != len(COVERAGE_HEADER):
            raise BuildError(
                f"{path}:{line_number}: expected {len(COVERAGE_HEADER)} fields, "
                f"found {len(row)}"
            )
        record = dict(zip(COVERAGE_HEADER, (field.strip() for field in row)))
        item_id = record["item_id"]
        if not item_id:
            raise BuildError(f"{path}:{line_number}: empty item_id")
        if item_id in items:
            raise BuildError(f"{path}:{line_number}: duplicate item_id {item_id}")
        if record["status"] not in MANIFEST_STATUSES:
            raise BuildError(
                f"{path}:{line_number}: invalid status {record['status']!r}"
            )
        if record["card_type"] not in CARD_TYPES:
            raise BuildError(
                f"{path}:{line_number}: invalid card_type "
                f"{record['card_type']!r}"
            )
        if record["source_file"] not in SOURCE_DECKS:
            raise BuildError(
                f"{path}:{line_number}: unknown source_file "
                f"{record['source_file']!r}"
            )
        expected_subdeck = SOURCE_DECKS[record["source_file"]]
        if record["subdeck"] != expected_subdeck:
            raise BuildError(
                f"{path}:{line_number}: wrong source routing for {item_id}"
            )

        card_id = record["card_id"]
        if record["status"] == "validated":
            if not card_id or not CARD_ID_RE.fullmatch(card_id):
                raise BuildError(
                    f"{path}:{line_number}: validated item {item_id} needs a "
                    "well-formed card_id"
                )
        elif card_id:
            raise BuildError(
                f"{path}:{line_number}: only validated items may have card_id"
            )
        if card_id:
            if card_id in seen_card_ids:
                raise BuildError(
                    f"{path}:{line_number}: duplicate card_id {card_id}; first "
                    f"used by {seen_card_ids[card_id]}"
                )
            seen_card_ids[card_id] = item_id

        items[item_id] = ManifestItem(
            item_id=item_id,
            subdeck=record["subdeck"],
            card_type=record["card_type"],
            source_file=record["source_file"],
            card_id=card_id,
            status=record["status"],
        )

    return items


def _parse_metadata(
    block: str, source: Path, line_number: int
) -> tuple[dict[str, str], str]:
    match = META_RE.match(block)
    if not match:
        raise BuildError(
            f"{source}:{line_number}: card must begin with the exact "
            "`<!-- card ... -->` metadata block"
        )

    metadata: dict[str, str] = {}
    for offset, line in enumerate(match.group(1).splitlines(), start=1):
        field_match = META_LINE_RE.fullmatch(line)
        if not field_match:
            raise BuildError(
                f"{source}:{line_number + offset}: malformed metadata line"
            )
        key, value = field_match.groups()
        if key in metadata:
            raise BuildError(
                f"{source}:{line_number + offset}: duplicate metadata key {key}"
            )
        metadata[key] = value.strip()

    expected = {"item", "type", "status"}
    if set(metadata) != expected:
        missing = expected - set(metadata)
        extra = set(metadata) - expected
        raise BuildError(
            f"{source}:{line_number}: metadata mismatch; "
            f"missing={sorted(missing)}, extra={sorted(extra)}"
        )
    return metadata, block[match.end() :]


def _parse_sections(
    remainder: str, source: Path, line_number: int
) -> tuple[str, str]:
    headings = list(FIELD_HEADING_RE.finditer(remainder))
    if [match.group(1) for match in headings] != ["Front", "Back"]:
        raise BuildError(
            f"{source}:{line_number}: card needs exactly `### Front` followed "
            "by `### Back`"
        )

    prefix = remainder[: headings[0].start()]
    if prefix.strip():
        raise BuildError(
            f"{source}:{line_number}: unexpected text before `### Front`"
        )
    front = remainder[headings[0].end() : headings[1].start()].strip()
    back = remainder[headings[1].end() :].strip()
    if not front:
        raise BuildError(f"{source}:{line_number}: Front cannot be empty")
    if not back:
        raise BuildError(f"{source}:{line_number}: Back cannot be empty")
    if re.search(r"(?m)^#{1,6}\s", front) or re.search(
        r"(?m)^#{1,6}\s", back
    ):
        raise BuildError(
            f"{source}:{line_number}: nested Markdown headings are forbidden"
        )
    return front, back


def parse_source(path: Path, subdeck: str) -> list[Card]:
    text = path.read_text(encoding="utf-8")
    if "\r" in text:
        raise BuildError(f"{path}: carriage returns are not allowed")
    first_line = text.splitlines()[0].strip() if text.splitlines() else ""
    expected_title = f"# {subdeck}"
    if first_line != expected_title:
        raise BuildError(
            f"{path}: first line must be the exact title {expected_title!r}"
        )
    headings = list(CARD_HEADING_RE.finditer(text))
    cards: list[Card] = []

    for index, heading in enumerate(headings):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        block = text[start:end]
        line_number = text.count("\n", 0, heading.start()) + 1
        card_id = heading.group(1)
        metadata, remainder = _parse_metadata(block, path, line_number + 1)
        front, back = _parse_sections(remainder, path, line_number)

        if metadata["type"] not in CARD_TYPES:
            raise BuildError(
                f"{path}:{line_number}: invalid card type {metadata['type']!r}"
            )
        if metadata["status"] not in SOURCE_STATUSES:
            raise BuildError(
                f"{path}:{line_number}: invalid source status "
                f"{metadata['status']!r}"
            )
        if not CARD_ID_RE.fullmatch(card_id):
            raise BuildError(f"{path}:{line_number}: malformed card ID")
        if "\t" in front or "\t" in back:
            raise BuildError(f"{path}:{line_number}: raw tabs are forbidden")
        if any(
            marker in front.casefold()
            for marker in ("<!-- card", "item:", "status:", "### back")
        ):
            raise BuildError(
                f"{path}:{line_number}: Front exposes authoring metadata"
            )
        combined_visible = f"{front}\n{back}".casefold()
        scaffold = next(
            (
                phrase
                for phrase in FORBIDDEN_SCAFFOLD
                if phrase in combined_visible
            ),
            None,
        )
        if scaffold:
            raise BuildError(
                f"{path}:{line_number}: uninstantiated authoring scaffold "
                f"{scaffold!r} is forbidden"
            )
        numbered_prompts = len(NUMBERED_PROMPT_RE.findall(front))
        if numbered_prompts > 3 or front.count("?") > 3:
            raise BuildError(
                f"{path}:{line_number}: Front appears to contain several "
                "unrelated questions"
            )
        plain_back = re.sub(r"[*_`#>-]", " ", back)
        if len(plain_back.split()) < 6:
            raise BuildError(
                f"{path}:{line_number}: Back is too short to contain a "
                "complete answer and explanation"
            )
        if metadata["type"] == "repair" and not front.startswith("Fix if wrong:"):
            raise BuildError(
                f"{path}:{line_number}: repair Front must start with "
                "`Fix if wrong:`"
            )
        if metadata["type"] == "chunk":
            example_count = len(EXAMPLE_BULLET_RE.findall(back))
            if example_count not in {2, 3}:
                raise BuildError(
                    f"{path}:{line_number}: chunk Back needs exactly 2 or 3 "
                    f"complete example bullets; found {example_count}"
                )

        cards.append(
            Card(
                card_id=card_id,
                item_id=metadata["item"],
                card_type=metadata["type"],
                status=metadata["status"],
                source_file=path.name,
                subdeck=subdeck,
                front=front,
                back=back,
                line_number=line_number,
            )
        )

    return cards


def _validate_source_completeness(
    cards: list[Card],
    manifest: dict[str, ManifestItem],
    source_name: str,
) -> None:
    expected_items = [
        item.item_id
        for item in manifest.values()
        if item.source_file == source_name
        and item.status in {"proposed", "validated"}
    ]
    actual_items = [card.item_id for card in cards]
    if actual_items != expected_items:
        missing = [item for item in expected_items if item not in actual_items]
        extra = [item for item in actual_items if item not in expected_items]
        out_of_order = not missing and not extra
        raise BuildError(
            f"{source_name}: source coverage/order mismatch; "
            f"missing={missing[:12]}, extra={extra[:12]}, "
            f"out_of_order={out_of_order}"
        )

    module_number = source_name[:2]
    expected_card_ids = [
        f"C{module_number}-{index:03d}"
        for index in range(1, len(cards) + 1)
    ]
    actual_card_ids = [card.card_id for card in cards]
    if actual_card_ids != expected_card_ids:
        raise BuildError(
            f"{source_name}: card IDs must be sequential "
            f"C{module_number}-001... in manifest order"
        )


def _validate_cards(
    cards: list[Card],
    manifest: dict[str, ManifestItem],
    *,
    final: bool,
    require_complete_manifest: bool = True,
) -> None:
    seen_card_ids: dict[str, Card] = {}
    seen_item_ids: dict[str, Card] = {}
    seen_fronts: dict[str, Card] = {}

    for card in cards:
        previous = seen_card_ids.get(card.card_id)
        if previous:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: duplicate card ID "
                f"{card.card_id}; first in {previous.source_file}:"
                f"{previous.line_number}"
            )
        seen_card_ids[card.card_id] = card

        previous = seen_item_ids.get(card.item_id)
        if previous:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: item {card.item_id} "
                f"already has card {previous.card_id}"
            )
        seen_item_ids[card.item_id] = card

        front_key = _normalize_visible(card.front)
        previous = seen_fronts.get(front_key)
        if previous:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: duplicate visible "
                f"Front; first in {previous.source_file}:{previous.line_number}"
            )
        seen_fronts[front_key] = card

        item = manifest.get(card.item_id)
        if not item:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: card maps to missing "
                f"manifest item {card.item_id}"
            )
        if item.status in {"excluded", "deferred"}:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: card maps to "
                f"{item.status} item {card.item_id}"
            )
        if card.source_file != item.source_file or card.subdeck != item.subdeck:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: wrong subdeck routing "
                f"for {card.item_id}"
            )
        if card.card_type != item.card_type:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: source type "
                f"{card.card_type!r} does not match manifest "
                f"{item.card_type!r}"
            )
        if card.status != item.status:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: source status "
                f"{card.status!r} does not match manifest {item.status!r}"
            )
        if item.status == "validated" and card.card_id != item.card_id:
            raise BuildError(
                f"{card.source_file}:{card.line_number}: card ID "
                f"{card.card_id!r} does not match manifest {item.card_id!r}"
            )

    if require_complete_manifest:
        missing_validated = [
            item.item_id
            for item in manifest.values()
            if item.status == "validated" and item.item_id not in seen_item_ids
        ]
        if missing_validated:
            preview = ", ".join(missing_validated[:12])
            raise BuildError(
                "validated manifest items without cards: "
                f"{preview}{' ...' if len(missing_validated) > 12 else ''}"
            )

    if final:
        unresolved = [
            item.item_id
            for item in manifest.values()
            if item.status in {"proposed", "deferred"}
        ]
        if unresolved:
            preview = ", ".join(unresolved[:12])
            raise BuildError(
                "final build has unresolved manifest items: "
                f"{preview}{' ...' if len(unresolved) > 12 else ''}"
            )
        proposed_cards = [card.card_id for card in cards if card.status != "validated"]
        if proposed_cards:
            raise BuildError(
                "final build has proposed source cards: "
                + ", ".join(proposed_cards[:12])
            )

        repairs = [card for card in cards if card.card_type == "repair"]
        correct_repairs = [
            card for card in repairs if "Correct as written." in card.back
        ]
        incorrect_repairs = [
            card for card in repairs if "Correct as written." not in card.back
        ]
        if not correct_repairs or not incorrect_repairs:
            raise BuildError(
                "final resource needs both already-correct and incorrect "
                "repair cards"
            )


def _inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = BOLD_RE.sub(r"<b>\1</b>", escaped)
    return escaped


def markdown_to_html(value: str) -> str:
    lines = value.splitlines()
    output: list[str] = []
    blank_pending = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            blank_pending = True
            continue
        if blank_pending and output:
            output.append("<br>")
        blank_pending = False
        output.append(_inline_markdown(line))
    return "<br>".join(output)


def build_tsv(cards: list[Card]) -> str:
    rows = ["#separator:tab", "#html:true", "#deck column:1"]
    for card in cards:
        if card.status != "validated":
            continue
        fields = [
            f"{PARENT_DECK}::{card.subdeck}",
            markdown_to_html(card.front),
            markdown_to_html(card.back),
        ]
        if any("\t" in field or "\n" in field for field in fields):
            raise BuildError(
                f"{card.source_file}:{card.line_number}: rendered TSV field "
                "contains a raw tab or newline"
            )
        rows.append("\t".join(fields))
    return "\n".join(rows) + "\n"


def _load_all_cards() -> list[Card]:
    cards: list[Card] = []
    for source_file, subdeck in SOURCE_DECKS.items():
        path = CONNECTIONS_DIR / source_file
        if not path.is_file():
            raise BuildError(f"missing canonical source: {path}")
        cards.extend(parse_source(path, subdeck))
    return cards


def _print_counts(cards: list[Card], manifest: dict[str, ManifestItem]) -> None:
    validated = [card for card in cards if card.status == "validated"]
    subdeck_counts = Counter(card.subdeck for card in validated)
    type_counts = Counter(card.card_type for card in validated)
    manifest_counts = Counter(item.status for item in manifest.values())
    proposed_with_cards = sum(card.status == "proposed" for card in cards)
    proposed_without_cards = sum(
        item.status == "proposed"
        and not any(card.item_id == item.item_id for card in cards)
        for item in manifest.values()
    )

    print(f"source cards: {len(cards)}")
    print(f"exported validated cards: {len(validated)}")
    for subdeck in SOURCE_DECKS.values():
        print(f"  {subdeck}: {subdeck_counts[subdeck]}")
    print("validated card types:")
    for card_type in sorted(type_counts):
        print(f"  {card_type}: {type_counts[card_type]}")
    print("manifest statuses:")
    for status in sorted(manifest_counts):
        print(f"  {status}: {manifest_counts[status]}")
    print(f"proposed items with source cards: {proposed_with_cards}")
    print(f"proposed items without source cards: {proposed_without_cards}")


def self_test() -> None:
    sample = """# 05 Conjunctions and Clause Linkers

## LINK-001

<!-- card
item: LINK-CAUSE-BECAUSE
type: contrast
status: validated
-->

### Front

1. The event was canceled ___ heavy rain.
2. The event was canceled ___ the venue flooded.

### Back

1. The event was canceled **because of heavy rain**.
2. The event was canceled **because the venue flooded**.

Use `because of + NP` and `because + finite clause`.
"""
    path = Path("05-conjunction-clause-linkers.md")
    cards = parse_source(path, SOURCE_DECKS[path.name]) if path.exists() else []
    if not cards:
        temporary = Path("/tmp/connection-builder-self-test.md")
        temporary.write_text(sample, encoding="utf-8")
        try:
            cards = parse_source(
                temporary, "05 Conjunctions and Clause Linkers"
            )
        finally:
            temporary.unlink(missing_ok=True)
    assert len(cards) == 1
    assert cards[0].item_id == "LINK-CAUSE-BECAUSE"
    assert "<b>because of heavy rain</b>" in markdown_to_html(cards[0].back)
    cards = [
        Card(
            **{
                **cards[0].__dict__,
                "source_file": "05-conjunction-clause-linkers.md",
            }
        )
    ]
    assert len(build_tsv(cards).splitlines()[-1].split("\t")) == 3
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate all inputs and require the generated TSV to be current",
    )
    parser.add_argument(
        "--final",
        action="store_true",
        help="require every viable item and source card to be validated",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run parser and renderer tests without reading project sources",
    )
    parser.add_argument(
        "--lint-source",
        metavar="FILENAME",
        help="validate one canonical Markdown source without writing the TSV",
    )
    args = parser.parse_args()

    if args.self_test:
        try:
            self_test()
        except (AssertionError, BuildError, OSError, UnicodeError) as error:
            print(f"self-test failed: {error}", file=sys.stderr)
            return 1
        return 0

    if args.lint_source:
        source_name = Path(args.lint_source).name
        if source_name not in SOURCE_DECKS:
            print(
                f"error: unknown canonical source {source_name!r}",
                file=sys.stderr,
            )
            return 1
        try:
            manifest = _read_manifest()
            cards = parse_source(
                CONNECTIONS_DIR / source_name, SOURCE_DECKS[source_name]
            )
            _validate_cards(
                cards,
                manifest,
                final=False,
                require_complete_manifest=False,
            )
            _validate_source_completeness(cards, manifest, source_name)
        except (BuildError, OSError, UnicodeError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"{source_name}: {len(cards)} source cards valid")
        return 0

    try:
        manifest = _read_manifest()
        cards = _load_all_cards()
        _validate_cards(cards, manifest, final=args.final)
        expected = build_tsv(cards)
    except (BuildError, OSError, UnicodeError) as error:
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
        print("connection import is valid and current")
    else:
        OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
        print(f"wrote {OUTPUT_PATH}")

    _print_counts(cards, manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
