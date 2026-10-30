#!/usr/bin/env python3
"""Build grammar-map.md from the checked-in unit manifest."""

from __future__ import annotations

import re
from pathlib import Path


EN_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = EN_ROOT / "UNIT-MANIFEST.md"
OUTPUT = EN_ROOT / "grammar-map.md"

CHAPTER_DIRS = {
    1: "01-time-and-tense",
    2: "02-future-and-conditionals",
    3: "03-modals-and-attitude",
    4: "04-passive-and-reported-meaning",
    5: "05-questions-and-conversation-control",
    6: "06-verb-patterns-ing-and-to",
    7: "07-nouns-articles-and-quantity",
    8: "08-relative-and-reduced-clauses",
    9: "09-adjectives-adverbs-and-comparison",
    10: "10-linking-ideas",
    11: "11-prepositions",
    12: "12-phrasal-verbs",
}

CHAPTER_RE = re.compile(r"^## Chapter (\d+) — (.+)$")
UNIT_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|$")


def parse_manifest() -> list[tuple[int, str, list[tuple[int, str]]]]:
    chapters: list[tuple[int, str, list[tuple[int, str]]]] = []
    current: tuple[int, str, list[tuple[int, str]]] | None = None

    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        chapter_match = CHAPTER_RE.match(line)
        if chapter_match:
            current = (int(chapter_match.group(1)), chapter_match.group(2), [])
            chapters.append(current)
            continue

        unit_match = UNIT_RE.match(line)
        if unit_match and current:
            current[2].append((int(unit_match.group(1)), unit_match.group(2)))

    units = [number for _, _, items in chapters for number, _ in items]
    expected = list(range(1, 146))
    if sorted(units) != expected:
        missing = sorted(set(expected) - set(units))
        duplicates = sorted({number for number in units if units.count(number) > 1})
        raise SystemExit(
            f"Invalid manifest: missing={missing}, duplicates={duplicates}, "
            f"count={len(units)}"
        )
    if sorted(number for number, _, _ in chapters) != list(range(1, 13)):
        raise SystemExit("Manifest must contain Chapters 1 through 12 exactly once")
    return chapters


def render(chapters: list[tuple[int, str, list[tuple[int, str]]]]) -> str:
    lines = [
        "# Grammar map",
        "",
        "Use this map to open one short lesson at a time. The numbering follows ",
        "*English Grammar in Use* Fifth Edition; the lesson content is original to ",
        "this guide.",
        "",
        "Priority depends on your errors and goals. Start with the ",
        "[diagnostic](diagnostic.md) or the ",
        "[IELTS Speaking 7 path](paths/ielts-speaking-7.md).",
        "",
    ]

    for chapter_number, chapter_title, units in chapters:
        chapter_dir = CHAPTER_DIRS[chapter_number]
        lines.extend(
            [
                f"## Chapter {chapter_number} — {chapter_title}",
                "",
                f"[Chapter overview](chapters/{chapter_dir}/)",
                "",
                "| Unit | Topic | Lesson |",
                "|---:|---|---|",
            ]
        )
        for unit_number, topic in units:
            path = f"chapters/{chapter_dir}/units/{unit_number:03d}.md"
            lines.append(f"| {unit_number} | {topic} | [Study]({path}) |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    OUTPUT.write_text(render(parse_manifest()), encoding="utf-8")


if __name__ == "__main__":
    main()

