#!/usr/bin/env python3
"""Maintain the learner's persistent English-correction registry."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = ROOT / "data" / "correction_master.json"
SCHEMA_VERSION = 1
MAX_STORED_EXAMPLES = 3

CATEGORIES = ("CORRECT_ONLY", "TRACK", "CARD_CANDIDATE")
CATEGORY_RANK = {category: rank for rank, category in enumerate(CATEGORIES)}
ERROR_TYPES = {
    "ARTICLE",
    "COLLOCATION",
    "GRAMMAR",
    "MEANING",
    "PREPOSITION",
    "PUNCTUATION",
    "REGISTER",
    "SPELLING",
    "STRUCTURE",
    "VERB_FORM",
    "VOCABULARY",
    "WORD_FORM",
    "OTHER",
}
TARGETS = {"NONE", "UNDECIDED", "VOCABULARY", "PATTERN", "CONNECTION"}
CARD_STATUSES = ("NONE", "PREVIEWED", "APPROVED", "ADDED", "DECLINED")
CARD_TRANSITIONS = {
    "NONE": {"PREVIEWED"},
    "PREVIEWED": {"APPROVED", "DECLINED"},
    "APPROVED": {"ADDED"},
    "ADDED": set(),
    "DECLINED": {"PREVIEWED"},
}

ENTRY_FIELDS = {
    "pattern_key",
    "normalized_key",
    "category",
    "error_type",
    "target",
    "summary",
    "rule",
    "classification_reason",
    "encounter_count",
    "successful_use_count",
    "first_seen",
    "last_seen",
    "last_success",
    "sources",
    "examples",
    "successful_examples",
    "card_status",
    "card_ref",
}


def normalized_key(value: str) -> str:
    """Return a stable key for merging equivalent correction records."""

    text = value.strip().casefold().replace("’", "'")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([+/])\s*", r" \1 ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_text(value: Any, field: str, *, required: bool = True) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    cleaned = re.sub(r"\s+", " ", value.strip())
    if required and not cleaned:
        raise ValueError(f"{field} cannot be empty")
    return cleaned


def iso_date(value: Any, field: str, *, allow_empty: bool = False) -> str:
    if allow_empty and value == "":
        return ""
    cleaned = clean_text(value, field)
    try:
        date.fromisoformat(cleaned)
    except ValueError as exc:
        raise ValueError(f"{field} must use YYYY-MM-DD: {cleaned}") from exc
    return cleaned


def unique_strings(values: list[Any], field: str) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = clean_text(value, field)
        key = cleaned.casefold()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def empty_master() -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "entries": []}


def validate_example(example: Any, field: str) -> None:
    if not isinstance(example, dict):
        raise ValueError(f"{field} items must be objects")
    expected = {"date", "original", "corrected", "source"}
    if set(example) != expected:
        raise ValueError(f"{field} items must contain exactly {sorted(expected)}")
    iso_date(example["date"], f"{field}.date")
    clean_text(example["original"], f"{field}.original")
    clean_text(example["corrected"], f"{field}.corrected")
    clean_text(example["source"], f"{field}.source")


def validate_success_example(example: Any, field: str) -> None:
    if not isinstance(example, dict):
        raise ValueError(f"{field} items must be objects")
    expected = {"date", "example", "source"}
    if set(example) != expected:
        raise ValueError(f"{field} items must contain exactly {sorted(expected)}")
    iso_date(example["date"], f"{field}.date")
    clean_text(example["example"], f"{field}.example")
    clean_text(example["source"], f"{field}.source")


def validate_entry(entry: Any) -> None:
    if not isinstance(entry, dict):
        raise ValueError("Every correction entry must be an object")
    if set(entry) != ENTRY_FIELDS:
        missing = sorted(ENTRY_FIELDS - set(entry))
        extra = sorted(set(entry) - ENTRY_FIELDS)
        raise ValueError(f"Correction entry fields mismatch; missing={missing}, extra={extra}")

    key = clean_text(entry["pattern_key"], "pattern_key")
    normalized = clean_text(entry["normalized_key"], "normalized_key")
    if normalized != normalized_key(key):
        raise ValueError(f"normalized_key is stale for {key!r}")
    if entry["category"] not in CATEGORIES:
        raise ValueError(f"Invalid category for {key}: {entry['category']}")
    if entry["error_type"] not in ERROR_TYPES:
        raise ValueError(f"Invalid error_type for {key}: {entry['error_type']}")
    if entry["target"] not in TARGETS:
        raise ValueError(f"Invalid target for {key}: {entry['target']}")
    for field in ("summary", "rule", "classification_reason"):
        clean_text(entry[field], field)

    if not isinstance(entry["encounter_count"], int) or entry["encounter_count"] < 1:
        raise ValueError(f"encounter_count must be a positive integer for {key}")
    if not isinstance(entry["successful_use_count"], int) or entry["successful_use_count"] < 0:
        raise ValueError(f"successful_use_count must be a nonnegative integer for {key}")

    first_seen = iso_date(entry["first_seen"], "first_seen")
    last_seen = iso_date(entry["last_seen"], "last_seen")
    if first_seen > last_seen:
        raise ValueError(f"first_seen is after last_seen for {key}")
    last_success = iso_date(entry["last_success"], "last_success", allow_empty=True)
    if entry["successful_use_count"] and not last_success:
        raise ValueError(f"last_success is required when successes exist for {key}")
    if not entry["successful_use_count"] and last_success:
        raise ValueError(f"last_success requires a successful use for {key}")

    if not isinstance(entry["sources"], list) or not entry["sources"]:
        raise ValueError(f"sources must be a nonempty list for {key}")
    if entry["sources"] != unique_strings(entry["sources"], "sources"):
        raise ValueError(f"sources contain duplicates or unclean values for {key}")

    examples = entry["examples"]
    successful_examples = entry["successful_examples"]
    if not isinstance(examples, list) or not examples:
        raise ValueError(f"examples must be a nonempty list for {key}")
    if len(examples) > MAX_STORED_EXAMPLES:
        raise ValueError(f"too many stored correction examples for {key}")
    if not isinstance(successful_examples, list):
        raise ValueError(f"successful_examples must be a list for {key}")
    if len(successful_examples) > MAX_STORED_EXAMPLES:
        raise ValueError(f"too many stored successful examples for {key}")
    for example in examples:
        validate_example(example, "examples")
    for example in successful_examples:
        validate_success_example(example, "successful_examples")

    card_status = entry["card_status"]
    if card_status not in CARD_STATUSES:
        raise ValueError(f"Invalid card_status for {key}: {card_status}")
    if card_status != "NONE" and entry["category"] != "CARD_CANDIDATE":
        raise ValueError(f"Only CARD_CANDIDATE entries can have card workflow state: {key}")
    if card_status != "NONE" and entry["target"] not in {
        "VOCABULARY",
        "PATTERN",
        "CONNECTION",
    }:
        raise ValueError(f"Card workflow requires a resolved destination for {key}")
    card_ref = clean_text(entry["card_ref"], "card_ref", required=False)
    if card_status == "ADDED" and not card_ref:
        raise ValueError(f"ADDED requires card_ref for {key}")
    if card_status != "ADDED" and card_ref:
        raise ValueError(f"card_ref is only allowed for ADDED entries: {key}")


def validate_master(master: Any) -> dict[str, int]:
    if not isinstance(master, dict) or set(master) != {"schema_version", "entries"}:
        raise ValueError("Master JSON must contain exactly schema_version and entries")
    if master["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema_version: {master['schema_version']}")
    if not isinstance(master["entries"], list):
        raise ValueError("entries must be a list")

    seen: set[str] = set()
    for entry in master["entries"]:
        validate_entry(entry)
        key = entry["normalized_key"]
        if key in seen:
            raise ValueError(f"Duplicate normalized correction key: {key}")
        seen.add(key)

    return {
        "entries": len(master["entries"]),
        "correct_only": sum(e["category"] == "CORRECT_ONLY" for e in master["entries"]),
        "track": sum(e["category"] == "TRACK" for e in master["entries"]),
        "card_candidate": sum(e["category"] == "CARD_CANDIDATE" for e in master["entries"]),
        "added": sum(e["card_status"] == "ADDED" for e in master["entries"]),
    }


def load_master(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ValueError(f"Correction master is missing: {path}")
    try:
        master = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    validate_master(master)
    return master


def write_master(path: Path, master: dict[str, Any]) -> None:
    validate_master(master)
    master["entries"].sort(key=lambda entry: entry["normalized_key"])
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(master, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(serialized)
        temporary_path = Path(handle.name)
    try:
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def required_record_text(record: dict[str, Any], field: str) -> str:
    if field not in record:
        raise ValueError(f"Record is missing {field}")
    return clean_text(record[field], field)


def normalized_enum(
    record: dict[str, Any],
    field: str,
    allowed: set[str] | tuple[str, ...],
    default: str | None = None,
) -> str:
    value = record.get(field, default)
    if value is None:
        raise ValueError(f"Record is missing {field}")
    cleaned = clean_text(value, field).upper()
    if cleaned not in allowed:
        raise ValueError(f"Unsupported {field}: {cleaned}")
    return cleaned


def capped_append(
    items: list[dict[str, str]],
    item: dict[str, str],
    identity_fields: tuple[str, ...],
) -> list[dict[str, str]]:
    identity = tuple(item[field].casefold() for field in identity_fields)
    retained = [
        existing
        for existing in items
        if tuple(existing[field].casefold() for field in identity_fields) != identity
    ]
    retained.append(item)
    return retained[-MAX_STORED_EXAMPLES:]


def resolve_target(existing: str, incoming: str) -> str:
    if incoming == "UNDECIDED":
        return existing
    if existing in {"UNDECIDED", "NONE"}:
        return incoming
    if existing == incoming:
        return existing
    return "UNDECIDED"


def record_correction(master: dict[str, Any], record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if not isinstance(record, dict):
        raise ValueError("Every correction record must be an object")

    pattern_key = required_record_text(record, "pattern_key")
    key = normalized_key(pattern_key)
    category = normalized_enum(record, "category", CATEGORIES)
    error_type = normalized_enum(record, "error_type", ERROR_TYPES)
    target = normalized_enum(record, "target", TARGETS, "UNDECIDED")
    summary = required_record_text(record, "summary")
    rule = required_record_text(record, "rule")
    reason = required_record_text(record, "classification_reason")
    original = required_record_text(record, "original")
    corrected = required_record_text(record, "corrected")
    source = clean_text(record.get("source", "direct user conversation"), "source")
    seen_date = iso_date(record.get("seen_date", date.today().isoformat()), "seen_date")
    increment = record.get("encounter_increment", 1)
    if not isinstance(increment, int) or increment < 1:
        raise ValueError("encounter_increment must be a positive integer")

    example = {
        "date": seen_date,
        "original": original,
        "corrected": corrected,
        "source": source,
    }
    by_key = {entry["normalized_key"]: entry for entry in master["entries"]}
    if key not in by_key:
        entry = {
            "pattern_key": pattern_key,
            "normalized_key": key,
            "category": category,
            "error_type": error_type,
            "target": target,
            "summary": summary,
            "rule": rule,
            "classification_reason": reason,
            "encounter_count": increment,
            "successful_use_count": 0,
            "first_seen": seen_date,
            "last_seen": seen_date,
            "last_success": "",
            "sources": [source],
            "examples": [example],
            "successful_examples": [],
            "card_status": "NONE",
            "card_ref": "",
        }
        master["entries"].append(entry)
        validate_entry(entry)
        return "added", entry

    entry = by_key[key]
    if CATEGORY_RANK[category] > CATEGORY_RANK[entry["category"]]:
        entry["category"] = category
    if entry["error_type"] != error_type:
        entry["error_type"] = "OTHER"
    if entry["card_status"] != "ADDED":
        entry["target"] = resolve_target(entry["target"], target)
    entry["summary"] = summary
    entry["rule"] = rule
    entry["classification_reason"] = reason
    entry["encounter_count"] += increment
    entry["first_seen"] = min(entry["first_seen"], seen_date)
    entry["last_seen"] = max(entry["last_seen"], seen_date)
    entry["sources"] = unique_strings(entry["sources"] + [source], "sources")
    entry["examples"] = capped_append(
        entry["examples"], example, ("original", "corrected")
    )
    validate_entry(entry)
    return "updated", entry


def get_entry(master: dict[str, Any], key_value: str) -> dict[str, Any]:
    key = normalized_key(key_value)
    for entry in master["entries"]:
        if entry["normalized_key"] == key:
            return entry
    raise ValueError(f"Unknown correction key: {key_value}")


def record_success(
    master: dict[str, Any], key_value: str, seen_date: str, source: str, example_text: str
) -> dict[str, Any]:
    entry = get_entry(master, key_value)
    seen = iso_date(seen_date, "seen_date")
    source = clean_text(source, "source")
    example_text = clean_text(example_text, "example")
    success = {"date": seen, "example": example_text, "source": source}
    entry["successful_use_count"] += 1
    entry["last_success"] = max(entry["last_success"], seen)
    entry["sources"] = unique_strings(entry["sources"] + [source], "sources")
    entry["successful_examples"] = capped_append(
        entry["successful_examples"], success, ("example",)
    )
    validate_entry(entry)
    return entry


def classify_entry(
    master: dict[str, Any], key_value: str, category: str, target: str | None, reason: str
) -> dict[str, Any]:
    entry = get_entry(master, key_value)
    category = category.upper()
    if category not in CATEGORIES:
        raise ValueError(f"Unsupported category: {category}")
    if entry["card_status"] == "ADDED" and category != "CARD_CANDIDATE":
        raise ValueError("An ADDED entry cannot be moved out of CARD_CANDIDATE")
    entry["category"] = category
    if category != "CARD_CANDIDATE":
        entry["card_status"] = "NONE"
        entry["card_ref"] = ""
    if target is not None:
        target = target.upper()
        if target not in TARGETS:
            raise ValueError(f"Unsupported target: {target}")
        if entry["card_status"] == "ADDED" and target != entry["target"]:
            raise ValueError("An ADDED entry's target cannot be changed")
        entry["target"] = target
    entry["classification_reason"] = clean_text(reason, "classification_reason")
    validate_entry(entry)
    return entry


def update_card_status(
    master: dict[str, Any], key_value: str, new_status: str, card_ref: str
) -> dict[str, Any]:
    entry = get_entry(master, key_value)
    new_status = new_status.upper()
    if new_status not in CARD_STATUSES:
        raise ValueError(f"Unsupported card status: {new_status}")
    current = entry["card_status"]
    if new_status not in CARD_TRANSITIONS[current]:
        raise ValueError(f"Invalid card transition for {key_value}: {current} -> {new_status}")
    if entry["category"] != "CARD_CANDIDATE":
        raise ValueError("Only CARD_CANDIDATE entries can enter the card workflow")
    if entry["target"] not in {"VOCABULARY", "PATTERN", "CONNECTION"}:
        raise ValueError("Resolve the card target before entering the card workflow")
    cleaned_ref = clean_text(card_ref, "card_ref", required=False)
    if new_status == "ADDED" and not cleaned_ref:
        raise ValueError("ADDED requires --card-ref")
    if new_status != "ADDED" and cleaned_ref:
        raise ValueError("--card-ref is only valid with ADDED")
    entry["card_status"] = new_status
    entry["card_ref"] = cleaned_ref
    validate_entry(entry)
    return entry


def delete_entry(
    master: dict[str, Any], key_value: str, confirmed_key: str
) -> dict[str, Any]:
    """Delete one exact unlinked record after key confirmation."""

    entry = get_entry(master, key_value)
    if normalized_key(confirmed_key) != entry["normalized_key"]:
        raise ValueError("--confirm-key must match the exact correction key")
    if entry["card_status"] == "ADDED":
        raise ValueError(
            "Cannot delete an ADDED correction record; review the linked Anki card first"
        )
    master["entries"].remove(entry)
    validate_master(master)
    return entry


def load_records(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    records = payload if isinstance(payload, list) else [payload]
    if not records or any(not isinstance(record, dict) for record in records):
        raise ValueError("Input must be a correction object or a nonempty list of objects")
    return records


def print_summary(summary: dict[str, int]) -> None:
    print(
        "Validation passed: "
        f"{summary['entries']} entries; "
        f"{summary['correct_only']} CORRECT_ONLY, "
        f"{summary['track']} TRACK, "
        f"{summary['card_candidate']} CARD_CANDIDATE; "
        f"{summary['added']} cards added."
    )


def list_entries(
    master: dict[str, Any], category: str | None, card_status: str | None, output_format: str
) -> None:
    entries = [
        entry
        for entry in master["entries"]
        if (category is None or entry["category"] == category)
        and (card_status is None or entry["card_status"] == card_status)
    ]
    if output_format == "json":
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return
    print("Category\tErrors\tSuccesses\tTarget\tCard status\tLast seen\tPattern")
    for entry in entries:
        print(
            "\t".join(
                [
                    entry["category"],
                    str(entry["encounter_count"]),
                    str(entry["successful_use_count"]),
                    entry["target"],
                    entry["card_status"],
                    entry["last_seen"],
                    entry["pattern_key"],
                ]
            )
        )


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "correction_master.json"
        master = empty_master()
        write_master(path, master)
        base = {
            "pattern_key": "modal + base verb",
            "category": "CORRECT_ONLY",
            "error_type": "VERB_FORM",
            "target": "PATTERN",
            "summary": "Use the base form after a modal verb.",
            "rule": "modal + base verb",
            "classification_reason": "First observed production slip.",
            "original": "it might leads",
            "corrected": "it might lead",
            "source": "self-test",
            "seen_date": "2026-09-14",
        }
        change, entry = record_correction(master, base)
        assert change == "added" and entry["encounter_count"] == 1

        second = dict(base)
        second.update(
            {
                "category": "TRACK",
                "original": "it can causes delays",
                "corrected": "it can cause delays",
                "seen_date": "2026-09-15",
                "classification_reason": "The same root problem recurred.",
            }
        )
        change, entry = record_correction(master, second)
        assert change == "updated"
        assert entry["category"] == "TRACK" and entry["encounter_count"] == 2

        for day, original, corrected in (
            ("2026-09-16", "it should works", "it should work"),
            ("2026-09-17", "it may fails", "it may fail"),
        ):
            incoming = dict(second)
            incoming.update(
                {
                    "seen_date": day,
                    "original": original,
                    "corrected": corrected,
                }
            )
            record_correction(master, incoming)
        assert len(entry["examples"]) == MAX_STORED_EXAMPLES
        assert entry["encounter_count"] == 4

        record_success(master, "MODAL + BASE VERB", "2026-09-18", "self-test", "It might help.")
        assert entry["successful_use_count"] == 1
        classify_entry(
            master,
            "modal + base verb",
            "CARD_CANDIDATE",
            "UNDECIDED",
            "Repeated across independent encounters and broadly reusable.",
        )
        try:
            update_card_status(master, "modal + base verb", "PREVIEWED", "")
        except ValueError:
            pass
        else:
            raise AssertionError("The card workflow requires a resolved target")
        classify_entry(
            master,
            "modal + base verb",
            "CARD_CANDIDATE",
            "PATTERN",
            "Reviewed and routed to the production-pattern deck.",
        )
        try:
            update_card_status(master, "modal + base verb", "APPROVED", "")
        except ValueError:
            pass
        else:
            raise AssertionError("The card workflow must not skip PREVIEWED")
        update_card_status(master, "modal + base verb", "PREVIEWED", "")
        try:
            update_card_status(
                master,
                "modal + base verb",
                "ADDED",
                "cards/patterns/cards.md#modal-base-verb",
            )
        except ValueError:
            pass
        else:
            raise AssertionError("The card workflow must not skip APPROVED")
        update_card_status(master, "modal + base verb", "APPROVED", "")
        update_card_status(
            master,
            "modal + base verb",
            "ADDED",
            "cards/patterns/cards.md#modal-base-verb",
        )
        write_master(path, master)
        reloaded = load_master(path)
        summary = validate_master(reloaded)
        assert summary == {
            "entries": 1,
            "correct_only": 0,
            "track": 0,
            "card_candidate": 1,
            "added": 1,
        }

        try:
            update_card_status(reloaded, "modal + base verb", "PREVIEWED", "")
        except ValueError:
            pass
        else:
            raise AssertionError("ADDED entries must reject further transitions")

        try:
            delete_entry(reloaded, "modal + base verb", "modal + base verb")
        except ValueError:
            pass
        else:
            raise AssertionError("ADDED correction records must not be deleted")

        disposable = dict(base)
        disposable.update(
            {
                "pattern_key": "isolated capitalization slip",
                "category": "CORRECT_ONLY",
                "error_type": "PUNCTUATION",
                "target": "NONE",
                "summary": "Capitalize the first word of a written sentence.",
                "rule": "sentence start -> capital letter",
                "classification_reason": "Low-value isolated slip.",
                "original": "this starts in lowercase.",
                "corrected": "This starts with a capital letter.",
            }
        )
        record_correction(reloaded, disposable)
        try:
            delete_entry(reloaded, disposable["pattern_key"], "wrong key")
        except ValueError:
            pass
        else:
            raise AssertionError("Deletion must require the exact confirmation key")
        deleted = delete_entry(
            reloaded, disposable["pattern_key"], disposable["pattern_key"]
        )
        assert deleted["category"] == "CORRECT_ONLY"
        assert len(reloaded["entries"]) == 1
    print(
        "Self-test passed: merge, cap, success, classification, "
        "approval lifecycle, and guarded deletion."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master", type=Path, default=MASTER_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="record or merge correction JSON")
    record_parser.add_argument("--input", required=True, type=Path)

    success_parser = subparsers.add_parser("success", help="record a successful learner use")
    success_parser.add_argument("--key", required=True)
    success_parser.add_argument("--date", default=date.today().isoformat())
    success_parser.add_argument("--source", default="targeted practice")
    success_parser.add_argument("--example", required=True)

    classify_parser = subparsers.add_parser("classify", help="review a correction classification")
    classify_parser.add_argument("--key", required=True)
    classify_parser.add_argument("--category", required=True, choices=CATEGORIES)
    classify_parser.add_argument("--target", choices=sorted(TARGETS))
    classify_parser.add_argument("--reason", required=True)

    status_parser = subparsers.add_parser(
        "card-status", help="advance the approval-gated card lifecycle"
    )
    status_parser.add_argument("--key", required=True)
    status_parser.add_argument("--status", required=True, choices=CARD_STATUSES[1:])
    status_parser.add_argument("--card-ref", default="")

    delete_parser = subparsers.add_parser(
        "delete", help="delete one exact correction record"
    )
    delete_parser.add_argument("--key", required=True)
    delete_parser.add_argument(
        "--confirm-key",
        required=True,
        help="repeat the exact key to confirm the deletion",
    )

    list_parser = subparsers.add_parser("list", help="list correction records")
    list_parser.add_argument("--category", choices=CATEGORIES)
    list_parser.add_argument("--card-status", choices=CARD_STATUSES)
    list_parser.add_argument("--format", choices=("table", "json"), default="table")

    subparsers.add_parser("validate", help="validate the correction master")
    subparsers.add_parser("self-test", help="run isolated workflow tests")
    args = parser.parse_args()

    if args.command == "self-test":
        run_self_test()
        return 0

    master = load_master(args.master)
    if args.command == "record":
        added: list[str] = []
        updated: list[str] = []
        for record in load_records(args.input):
            change, entry = record_correction(master, record)
            (added if change == "added" else updated).append(entry["pattern_key"])
        write_master(args.master, master)
        print(f"Added: {', '.join(added) or 'none'}")
        print(f"Updated: {', '.join(updated) or 'none'}")
        print_summary(validate_master(master))
    elif args.command == "success":
        entry = record_success(master, args.key, args.date, args.source, args.example)
        write_master(args.master, master)
        print(f"Recorded success: {entry['pattern_key']}")
        print_summary(validate_master(master))
    elif args.command == "classify":
        entry = classify_entry(master, args.key, args.category, args.target, args.reason)
        write_master(args.master, master)
        print(f"Classified: {entry['pattern_key']} -> {entry['category']}")
        print_summary(validate_master(master))
    elif args.command == "card-status":
        entry = update_card_status(master, args.key, args.status, args.card_ref)
        write_master(args.master, master)
        print(f"Card status: {entry['pattern_key']} -> {entry['card_status']}")
        print_summary(validate_master(master))
    elif args.command == "delete":
        entry = delete_entry(master, args.key, args.confirm_key)
        write_master(args.master, master)
        print(f"Deleted: {entry['pattern_key']}")
        print_summary(validate_master(master))
    elif args.command == "list":
        list_entries(master, args.category, args.card_status, args.format)
    else:
        print_summary(validate_master(master))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, AssertionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
