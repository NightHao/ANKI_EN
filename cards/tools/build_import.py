#!/usr/bin/env python3
"""Build a directly importable Anki TSV from English pattern cards.

Source: cards/patterns/cards.md
Output: cards/patterns/anki-import.tsv

The TSV contains a special Deck column followed by the two Basic-note fields:
Front and Back.
"""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path


CARDS_DIR = Path(__file__).resolve().parents[1]
PATTERNS_DIR = CARDS_DIR / "patterns"
SOURCE = PATTERNS_DIR / "cards.md"
OUTPUT = PATTERNS_DIR / "anki-import.tsv"
PATTERN_SELECTION = PATTERNS_DIR / "PATTERN_FRAME_SELECTION.md"
CONNECTIONS_DIR = CARDS_DIR / "connections"
DECK = "EN::Patterns"
CARD_HEADING_RE = re.compile(r"^## `([^`\n]+)`\s*$")
BULLET_RE = re.compile(r"^- (.+)$")
GRAMMAR_CARD_MARKER = "<!-- grammar-card -->"
OVERVIEW_CARD_MARKER = "<!-- overview-card -->"
DIAGRAM_MARKER_RE = re.compile(r"^<!-- diagram: (en-prepositions-[a-z0-9-]+\.svg) -->$")
INLINE_MARKUP_RE = re.compile(r"(`[^`\n]+`|\*\*[^*\n]+\*\*)")
SELECTION_ROW_RE = re.compile(r"^\| [^|]+ \| `([^`\n]+)` \| [^|]*\|$")
SELECTION_COUNT_RE = re.compile(
    r"^The current selection contains (\d+) production frames\.",
    re.MULTILINE,
)
REVIEW_EXEMPT_ORDINARY_FRONTS = frozenset(
    {
        "Is/Are + subject + V-ing? / Has/Have + subject + past participle?",
    }
)


@dataclass(frozen=True)
class Card:
    front: str
    explanation: str | None = None
    examples: tuple[str, ...] = ()
    grammar_lines: tuple[str, ...] = ()
    is_overview: bool = False
    diagrams: tuple[str, ...] = ()


def render_inline(text: str) -> str:
    """Render the small inline-markup subset used by grammar-card Backs."""

    parts: list[str] = []
    cursor = 0
    for match in INLINE_MARKUP_RE.finditer(text):
        parts.append(html.escape(text[cursor : match.start()], quote=False))
        token = match.group(0)
        if token.startswith("`"):
            parts.append(f"<code>{html.escape(token[1:-1], quote=False)}</code>")
        else:
            parts.append(f"<strong>{html.escape(token[2:-2], quote=False)}</strong>")
        cursor = match.end()
    parts.append(html.escape(text[cursor:], quote=False))
    return "".join(parts)


def render_grammar_back(lines: tuple[str, ...]) -> str:
    """Preserve the reviewed line-and-section layout of a grammar card."""

    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(render_inline(line.strip()))
        elif current:
            paragraphs.append("<br>".join(current))
            current = []
    if current:
        paragraphs.append("<br>".join(current))
    return "<br><br>".join(paragraphs)


def parse_cards(text: str, source: Path = SOURCE) -> list[Card]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()
    starts: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        match = CARD_HEADING_RE.fullmatch(line)
        if not match:
            raise ValueError(
                f"{source}:{index + 1}: card headings must be "
                "'## `pattern shown on the Front`'"
            )
        starts.append((index, match.group(1).strip()))

    cards: list[Card] = []
    seen: dict[str, int] = {}

    for card_index, (start, front) in enumerate(starts):
        if not front:
            raise ValueError(f"{source}:{start + 1}: Front cannot be empty")
        if "\t" in front:
            raise ValueError(f"{source}:{start + 1}: Front cannot contain a tab")

        key = front.casefold()
        if key in seen:
            raise ValueError(
                f"{source}:{start + 1}: duplicate Front; first seen on "
                f"line {seen[key]}"
            )
        seen[key] = start + 1

        end = starts[card_index + 1][0] if card_index + 1 < len(starts) else len(lines)
        body = lines[start + 1 : end]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()

        if body and body[0].strip() == GRAMMAR_CARD_MARKER:
            grammar_lines = body[1:]
            while grammar_lines and not grammar_lines[0].strip():
                grammar_lines.pop(0)
            while grammar_lines and not grammar_lines[-1].strip():
                grammar_lines.pop()
            if not grammar_lines or not any(line.strip() for line in grammar_lines):
                raise ValueError(
                    f"{source}:{start + 1}: grammar-card Back cannot be empty"
                )
            if any("\t" in line for line in grammar_lines):
                raise ValueError(
                    f"{source}:{start + 1}: grammar-card Back cannot contain tabs"
                )
            if any(line.startswith("## ") for line in grammar_lines):
                raise ValueError(
                    f"{source}:{start + 1}: grammar-card Back cannot contain "
                    "level-two headings"
                )
            if any(
                re.search(r"\bcard\s+\d+\b", line, re.IGNORECASE)
                for line in grammar_lines
            ):
                raise ValueError(
                    f"{source}:{start + 1}: grammar-card Back cannot refer "
                    "to learner-facing card numbers"
                )
            cards.append(Card(front=front, grammar_lines=tuple(grammar_lines)))
            continue

        is_overview = bool(body and body[0].strip() == OVERVIEW_CARD_MARKER)
        if is_overview:
            body = body[1:]
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()

        diagrams: list[str] = []
        remaining: list[str] = []
        for line in body:
            match = DIAGRAM_MARKER_RE.fullmatch(line.strip())
            if match:
                if not is_overview:
                    raise ValueError(f"{source}:{start + 1}: diagrams require an overview card")
                filename = match.group(1)
                if not (PATTERNS_DIR / "media" / filename).is_file():
                    raise ValueError(f"{source}:{start + 1}: missing diagram {filename}")
                if filename in diagrams:
                    raise ValueError(f"{source}:{start + 1}: duplicate diagram {filename}")
                diagrams.append(filename)
            else:
                remaining.append(line)
        body = remaining

        first_bullet = next(
            (i for i, line in enumerate(body) if BULLET_RE.fullmatch(line)),
            None,
        )
        if first_bullet is None:
            raise ValueError(f"{source}:{start + 1}: Back has no example bullets")

        explanation_lines = body[:first_bullet]
        while explanation_lines and not explanation_lines[-1].strip():
            explanation_lines.pop()
        if not explanation_lines or not any(line.strip() for line in explanation_lines):
            raise ValueError(f"{source}:{start + 1}: Back needs an explanation")

        explanation_paragraphs: list[str] = []
        current_paragraph: list[str] = []
        for line in explanation_lines:
            if line.strip():
                current_paragraph.append(line.strip())
            elif current_paragraph:
                explanation_paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
        if current_paragraph:
            explanation_paragraphs.append(" ".join(current_paragraph))
        explanation = "\n\n".join(explanation_paragraphs)

        examples: list[str] = []
        for offset, line in enumerate(body[first_bullet:], start=first_bullet):
            if not line.strip():
                continue
            match = BULLET_RE.fullmatch(line)
            if not match:
                raise ValueError(
                    f"{source}:{start + offset + 2}: examples must use '- ' bullets"
                )
            examples.append(match.group(1).strip())

        if is_overview and len(examples) < 2:
            raise ValueError(
                f"{source}:{start + 1}: overview-card Back needs at least "
                f"2 examples; found {len(examples)}"
            )
        if not is_overview and len(examples) not in (2, 3):
            raise ValueError(
                f"{source}:{start + 1}: Back needs exactly 2 or 3 examples; "
                f"found {len(examples)}"
            )
        if any(not example for example in examples):
            raise ValueError(f"{source}:{start + 1}: examples cannot be empty")

        cards.append(
            Card(
                front=front,
                explanation=explanation,
                examples=tuple(examples),
                is_overview=is_overview,
                diagrams=tuple(diagrams),
            )
        )

    return cards


def render_back(card: Card) -> str:
    if card.grammar_lines:
        return render_grammar_back(card.grammar_lines)
    if card.explanation is None:
        raise ValueError(f"ordinary card has no explanation: {card.front}")
    explanation = "<br><br>".join(
        html.escape(paragraph, quote=False)
        for paragraph in card.explanation.split("\n\n")
    )
    examples = "<br>".join(
        f"• {html.escape(example, quote=False)}" for example in card.examples
    )
    body = f"{explanation}<br><br>{examples}"
    if card.is_overview:
        repeated_front = html.escape(card.front, quote=False)
        images = "".join(
            '<img src="' + html.escape(name, quote=True) +
            '" alt="Visual preposition guide" style="max-width:100%;height:auto;display:block;margin:8px auto">'
            for name in card.diagrams
        )
        visual = f"{images}<br><br>" if images else ""
        return (
            "<strong>Patterns on this card:</strong><br>"
            f"{repeated_front}<br><br>{visual}{body}"
        )
    return body


def build_tsv(cards: list[Card]) -> str:
    rows = [
        "#separator:tab",
        "#html:true",
        "#deck column:1",
    ]
    for card in cards:
        fields = [
            DECK,
            html.escape(card.front, quote=False),
            render_back(card),
        ]
        if any("\t" in field or "\n" in field for field in fields):
            raise ValueError(f"TSV field contains a raw tab or newline: {card.front}")
        rows.append("\t".join(fields))
    return "\n".join(rows) + "\n"


def parse_pattern_selection(
    text: str,
    source: Path = PATTERN_SELECTION,
) -> tuple[str, ...]:
    count_match = SELECTION_COUNT_RE.search(text)
    if count_match is None:
        raise ValueError(f"{source}: reviewed production-frame count is missing")
    declared_count = int(count_match.group(1))

    selected: list[str] = []
    seen: dict[str, int] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = SELECTION_ROW_RE.fullmatch(line)
        if not match:
            continue
        front = match.group(1).strip()
        key = front.casefold()
        if key in seen:
            raise ValueError(
                f"{source}:{line_number}: duplicate selected Front; first seen "
                f"on line {seen[key]}"
            )
        seen[key] = line_number
        selected.append(front)
    if not selected:
        raise ValueError(f"{source}: no selected production Fronts found")
    if len(selected) != declared_count:
        raise ValueError(
            f"{source}: declares {declared_count} reviewed production frames "
            f"but lists {len(selected)}"
        )
    return tuple(selected)


def validate_pattern_selection(cards: list[Card], selected: tuple[str, ...]) -> None:
    selected_keys = {front.casefold() for front in selected}
    live_fronts = {card.front.casefold() for card in cards}
    missing = [front for front in selected if front.casefold() not in live_fronts]
    if missing:
        formatted = "\n".join(f"- {front}" for front in missing)
        raise ValueError(
            "reviewed production Fronts are missing from cards.md:\n" + formatted
        )

    exempt_keys = {front.casefold() for front in REVIEW_EXEMPT_ORDINARY_FRONTS}
    unreviewed = [
        card.front
        for card in cards
        if not card.grammar_lines
        and not card.is_overview
        and card.front.casefold() not in selected_keys
        and card.front.casefold() not in exempt_keys
    ]
    if unreviewed:
        formatted = "\n".join(f"- {front}" for front in unreviewed)
        raise ValueError(
            "ordinary production Fronts are missing from "
            "PATTERN_FRAME_SELECTION.md:\n" + formatted
        )


def _normalize_example(text: str) -> str:
    without_inline_markdown = re.sub(r"[*_`]", "", text)
    return " ".join(without_inline_markdown.casefold().split())


def validate_example_uniqueness(
    cards: list[Card],
    connection_source_text: str,
) -> None:
    seen: dict[str, str] = {}
    normalized_connection_sources = _normalize_example(connection_source_text)

    for card in cards:
        for example in card.examples:
            normalized = _normalize_example(example)
            if normalized in seen:
                raise ValueError(
                    f"duplicate ordinary example in {card.front!r}; first used "
                    f"in {seen[normalized]!r}: {example}"
                )
            seen[normalized] = card.front
            if normalized in normalized_connection_sources:
                raise ValueError(
                    f"ordinary example in {card.front!r} duplicates a "
                    f"Connection Patterns source example: {example}"
                )


def self_test() -> None:
    sample = """# English Pattern Cards

## `the first/next/last/only + noun + to-infinitive`

Used to identify someone or something by its order or uniqueness in performing an action.

- Amy was the first person to arrive.
- This is the last train to leave tonight.
- He was the only applicant to meet every requirement.
"""
    cards = parse_cards(sample, Path("<self-test>"))
    assert len(cards) == 1
    assert len(cards[0].examples) == 3
    output = build_tsv(cards)
    data_row = output.splitlines()[-1]
    assert len(data_row.split("\t")) == 3
    assert data_row.startswith(f"{DECK}\t")

    spaced_sample = sample.replace(
        "Used to identify someone or something by its order or uniqueness in "
        "performing an action.",
        "Used to identify someone or something by its order or uniqueness in "
        "performing an action.\n\n"
        "Common words include first, next, last, and only.\n\n"
        "Examples:",
    )
    spaced_cards = parse_cards(spaced_sample, Path("<spaced-self-test>"))
    assert spaced_cards[0].explanation is not None
    assert "\n\nCommon words" in spaced_cards[0].explanation
    spaced_output = build_tsv(spaced_cards)
    spaced_row = spaced_output.splitlines()[-1]
    assert "<br><br>Common words" in spaced_row
    assert "<br><br>Examples:<br><br>" in spaced_row

    grammar_sample = """# English Pattern Cards

## `ONE-WORD DELETION — When can one small word disappear?`

<!-- grammar-card -->

This card tests one operation:

`delete one word → keep every other word unchanged`

**1**

The book that Maya recommended explains the issue clearly.
→ The book Maya recommended explains the issue clearly.
"""
    grammar_cards = parse_cards(grammar_sample, Path("<grammar-self-test>"))
    assert len(grammar_cards) == 1
    grammar_output = build_tsv(grammar_cards)
    grammar_row = grammar_output.splitlines()[-1]
    assert "<strong>1</strong>" in grammar_row
    assert "<code>delete one word → keep every other word unchanged</code>" in grammar_row
    assert len(grammar_row.split("\t")) == 3

    numbered_reference = grammar_sample.replace(
        "This card tests one operation:",
        "See Card 2 for the rest.",
    )
    try:
        parse_cards(numbered_reference, Path("<grammar-number-reference-test>"))
    except ValueError as error:
        assert "cannot refer to learner-facing card numbers" in str(error)
    else:
        raise AssertionError("grammar cards must reject learner-facing card numbers")

    overview_sample = """# English Pattern Cards

## `on the left/right · at the top/bottom · in the middle/center`

<!-- overview-card -->

Use these expressions to describe general positions on a map.

Examples:

- The entrance is on the left, and the exit is on the right.
- The title is at the top, and the scale is at the bottom.
- The garden is in the middle, with a fountain in the center.
- The information desk is on the right.
"""
    overview_cards = parse_cards(overview_sample, Path("<overview-self-test>"))
    assert len(overview_cards) == 1
    assert overview_cards[0].is_overview
    assert len(overview_cards[0].examples) == 4
    overview_row = build_tsv(overview_cards).splitlines()[-1]
    assert len(overview_row.split("\t")) == 3
    overview_back = overview_row.split("\t")[2]
    assert "<strong>Patterns on this card:</strong>" in overview_back
    assert overview_cards[0].front in overview_back

    diagram_card = Card(front="in/on/at", explanation="Spatial guide.",
                        examples=("The map is on the wall.", "We met at the entrance."),
                        is_overview=True, diagrams=("en-prepositions-location-v1.svg",))
    assert '<img src="en-prepositions-location-v1.svg"' in render_back(diagram_card)

    ordinary_with_four_examples = sample + "- A fourth example is not allowed.\n"
    try:
        parse_cards(
            ordinary_with_four_examples,
            Path("<ordinary-example-limit-self-test>"),
        )
    except ValueError as error:
        assert "exactly 2 or 3 examples" in str(error)
    else:
        raise AssertionError("ordinary cards must retain the 2-or-3-example limit")

    selection_sample = """The current selection contains 1 production frames.

| Function | Production Front | Evidence |
| --- | --- | --- |
| Reason | `The main reason + clause + is that + clause` | `NOUN-001` |
"""
    selected = parse_pattern_selection(
        selection_sample,
        Path("<pattern-selection-self-test>"),
    )
    assert selected == ("The main reason + clause + is that + clause",)
    validate_pattern_selection(
        [
            Card(
                front="The main reason + clause + is that + clause",
                explanation="Used to give a reason.",
                examples=("Example one.", "Example two."),
            ),
            overview_cards[0],
        ],
        selected,
    )

    mismatched_selection = selection_sample.replace(
        "contains 1 production frames",
        "contains 2 production frames",
    )
    try:
        parse_pattern_selection(
            mismatched_selection,
            Path("<pattern-selection-count-test>"),
        )
    except ValueError as error:
        assert "declares 2" in str(error)
    else:
        raise AssertionError("selection count must match the reviewed table")

    try:
        validate_pattern_selection(
            [
                Card(
                    front="The main reason + clause + is that + clause",
                    explanation="Used to give a reason.",
                    examples=("Example one.", "Example two."),
                ),
                Card(
                    front="An unreviewed production frame",
                    explanation="This must be reviewed.",
                    examples=("Example one.", "Example two."),
                ),
            ],
            selected,
        )
    except ValueError as error:
        assert "missing from PATTERN_FRAME_SELECTION.md" in str(error)
    else:
        raise AssertionError("unreviewed ordinary cards must be rejected")

    duplicate_examples = [
        cards[0],
        Card(
            front="Another reviewed frame",
            explanation="Used for a different job.",
            examples=(cards[0].examples[0], "A different example."),
        ),
    ]
    try:
        validate_example_uniqueness(duplicate_examples, "")
    except ValueError as error:
        assert "duplicate ordinary example" in str(error)
    else:
        raise AssertionError("duplicate ordinary examples must be rejected")

    try:
        validate_example_uniqueness(
            cards,
            f"Source prompt: {cards[0].examples[0]}",
        )
    except ValueError as error:
        assert "duplicates a Connection Patterns source example" in str(error)
    else:
        raise AssertionError("cross-deck example duplication must be rejected")
    print("self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run parser and TSV-contract checks without changing files",
    )
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    cards = parse_cards(SOURCE.read_text(encoding="utf-8"))
    selected = parse_pattern_selection(PATTERN_SELECTION.read_text(encoding="utf-8"))
    validate_pattern_selection(cards, selected)
    connection_source_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(CONNECTIONS_DIR.glob("[0-9][0-9]-*.md"))
    )
    validate_example_uniqueness(cards, connection_source_text)
    OUTPUT.write_text(build_tsv(cards), encoding="utf-8", newline="\n")
    print(
        f"wrote {len(cards)} cards, including {len(selected)} reviewed "
        f"production frames and {sum(card.is_overview for card in cards)} "
        f"overview cards, to {OUTPUT}"
    )


if __name__ == "__main__":
    main()
