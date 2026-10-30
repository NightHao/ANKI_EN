#!/usr/bin/env python3
"""Audit the generated English grammar guide."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


EN_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADINGS = ["## A", "## B", "## Exercises"]
OLD_TEMPLATE_HEADINGS = [
    "## Use it when",
    "## Core contrast",
    "## Natural examples",
    "## Common failure",
    "## Say it yourself",
    "## Check yourself",
]
BANNED_DRAFT_PHRASES = [
    "We use the grammar here to make the relationship clear",
    "Look at these examples from similar everyday situations",
    "Compare the choices carefully. The form can change",
    "In spontaneous speaking, begin with the complete pattern",
    "Write two sentences about the situation in section A",
    "Answers vary",
    "> undefined",
]
LOCAL_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
EXERCISE_RE = re.compile(r"^###\s+(\d+)\.(\d+)\s*$", re.M)


def unit_files() -> list[Path]:
    return sorted(EN_ROOT.glob("chapters/*/units/[0-9][0-9][0-9].md"))


def audit_units(errors: list[str]) -> None:
    files = unit_files()
    numbers = [int(path.stem) for path in files]
    counts = Counter(numbers)
    expected = set(range(1, 146))

    if set(numbers) != expected:
        errors.append(
            "unit set mismatch: "
            f"missing={sorted(expected - set(numbers))}, "
            f"extra={sorted(set(numbers) - expected)}"
        )
    duplicates = sorted(number for number, count in counts.items() if count > 1)
    if duplicates:
        errors.append(f"duplicate unit numbers: {duplicates}")

    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(EN_ROOT)
        words = len(re.findall(r"\b[\w'-]+\b", text))
        if not 280 <= words <= 650:
            errors.append(f"{relative}: {words} words (expected 280-650)")
        for heading in REQUIRED_HEADINGS:
            if text.count(heading) != 1:
                errors.append(
                    f"{relative}: expected one {heading!r}, found {text.count(heading)}"
                )
        for heading in OLD_TEMPLATE_HEADINGS:
            if heading in text:
                errors.append(f"{relative}: contains obsolete heading {heading!r}")
        lettered = re.findall(r"^## ([A-E])$", text, re.M)
        expected_letters = list("ABCDE")[: len(lettered)]
        if not 2 <= len(lettered) <= 5 or lettered != expected_letters:
            errors.append(
                f"{relative}: explanation sections must be consecutive A-E; "
                f"found {lettered}"
            )
        exercise_numbers = EXERCISE_RE.findall(text)
        if not 2 <= len(exercise_numbers) <= 5:
            errors.append(
                f"{relative}: expected 2-5 numbered exercise sets, "
                f"found {len(exercise_numbers)}"
            )
        elif any(int(unit) != int(path.stem) for unit, _ in exercise_numbers):
            errors.append(f"{relative}: exercise number does not match unit number")
        elif [int(item) for _, item in exercise_numbers] != list(
            range(1, len(exercise_numbers) + 1)
        ):
            errors.append(f"{relative}: exercise sets are not numbered consecutively")
        if not text.startswith(f"# Unit {int(path.stem)} — "):
            errors.append(f"{relative}: title does not match unit number")
        if CJK_RE.search(text):
            errors.append(f"{relative}: contains CJK text")
        if text.count("<details>") != 1 or text.count(
            "<summary>Answers</summary>"
        ) != 1:
            errors.append(f"{relative}: missing collapsible answer")
        if text.count("</details>") != 1:
            errors.append(f"{relative}: expected exactly one closing details tag")
        for phrase in BANNED_DRAFT_PHRASES:
            if phrase in text:
                errors.append(f"{relative}: contains draft placeholder {phrase!r}")
        positions = [
            text.find("## A"),
            text.find("## B"),
            text.find("## Exercises"),
            text.find("<details>"),
        ]
        if positions != sorted(positions):
            errors.append(f"{relative}: explanation, exercises, and answers are out of order")


def audit_structure(errors: list[str]) -> None:
    chapter_readmes = sorted(EN_ROOT.glob("chapters/*/README.md"))
    if len(chapter_readmes) != 12:
        errors.append(f"expected 12 chapter READMEs, found {len(chapter_readmes)}")

    required = [
        "README.md",
        "PLAN.md",
        "UNIT-MANIFEST.md",
        "grammar-map.md",
        "diagnostic.md",
        "cheat-sheet.md",
        "paths/ielts-speaking-7.md",
        "paths/natural-speaking.md",
        "practice/speaking-prompts.md",
    ]
    for relative in required:
        if not (EN_ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for path in EN_ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if CJK_RE.search(text):
            errors.append(f"{path.relative_to(EN_ROOT)}: contains CJK text")
        for raw_target in LOCAL_LINK_RE.findall(text):
            target = raw_target.split("#", 1)[0]
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if resolved.is_dir():
                resolved = resolved / "README.md"
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(EN_ROOT)}: broken link target {raw_target}"
                )


def audit_map(errors: list[str]) -> None:
    map_path = EN_ROOT / "grammar-map.md"
    if not map_path.is_file():
        return
    text = map_path.read_text(encoding="utf-8")
    mapped = [int(number) for number in re.findall(r"^\|\s*(\d+)\s*\|", text, re.M)]
    if sorted(mapped) != list(range(1, 146)):
        errors.append("grammar-map.md does not list Units 1-145 exactly once")


def main() -> int:
    errors: list[str] = []
    audit_units(errors)
    audit_structure(errors)
    audit_map(errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1
    print(
        "EN audit passed: 145 units, 12 chapters, source-style schema, "
        "English-only Markdown, and valid links."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
