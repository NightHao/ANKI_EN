#!/usr/bin/env python3
"""Maintain the vocabulary master file and rebuild the Anki export."""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import sys
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MASTER_PATH = ROOT / "data" / "vocabulary_master.csv"
EXPORT_PATH = ROOT / "exports" / "anki_import.csv"
FRONT_PATH = ROOT / "anki" / "front.html"
BACK_PATH = ROOT / "anki" / "back.html"
STYLE_PATH = ROOT / "anki" / "styling.css"

MASTER_FIELDS = [
    "Term",
    "NormalizedTerm",
    "ObservedForms",
    "Priority",
    "PartsOfSpeech",
    "PronunciationHTML",
    "TTS_Text",
    "SensesJSON",
    "FrequencySource",
    "FrequencyValue",
    "FrequencyBand",
    "DailyConversationRelevance",
    "IELTSRelevance",
    "ProfessionalRelevance",
    "FantasyLiteraryRelevance",
    "EncounterCount",
    "FirstSeen",
    "LastSeen",
    "Sources",
    "IncludeInAnki",
    "ClassificationReason",
]

EXPORT_FIELDS = [
    "Term",
    "Priority",
    "PartsOfSpeech",
    "PronunciationHTML",
    "TTS_Text",
    "BackHTML",
    "Tags",
]

PRIORITIES = {"ACTIVE", "RECEPTIVE", "SKIP"}
RELATIONSHIPS = {
    "INTERCHANGEABLE",
    "NEAR-INTERCHANGEABLE",
    "RELATED",
    "DIRECT OPPOSITE",
    "CONTEXTUAL OPPOSITE",
}


def normalized_key(value: str) -> str:
    """Return a stable comparison key, including the documented normalizations."""
    text = value.strip().casefold().replace("’", "'")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    aliases = {
        "pretence": "pretense",
        "stave sth off": "stave off",
        "stave something off": "stave off",
    }
    return aliases.get(text, text)


def json_cell(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def parse_json_cell(value: str, expected_type: type, field: str) -> Any:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {field}: {exc}") from exc
    if not isinstance(parsed, expected_type):
        raise ValueError(f"{field} must contain a JSON {expected_type.__name__}")
    return parsed


def unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = re.sub(r"\s+", " ", value.strip())
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def merge_senses(existing: list[dict[str, Any]], incoming: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge genuinely new senses without duplicating a part-of-speech block."""
    merged = json.loads(json.dumps(existing))
    by_pos = {
        (block.get("entry_term", "").casefold(), block["part_of_speech"].casefold()): block
        for block in merged
    }
    for incoming_block in incoming:
        pos = incoming_block["part_of_speech"]
        key = (incoming_block.get("entry_term", "").casefold(), pos.casefold())
        if key not in by_pos:
            copied = json.loads(json.dumps(incoming_block))
            merged.append(copied)
            by_pos[key] = copied
            continue
        target = by_pos[key]
        for field in ("common_patterns", "comparison"):
            if field in incoming_block:
                target[field] = json.loads(json.dumps(incoming_block[field]))
        known_definitions = {
            sense.get("definition", "").strip().casefold()
            for sense in target.get("senses", [])
        }
        for sense in incoming_block.get("senses", []):
            definition = sense.get("definition", "").strip().casefold()
            if definition and definition not in known_definitions:
                target.setdefault("senses", []).append(json.loads(json.dumps(sense)))
                known_definitions.add(definition)
    return merged


def load_master() -> list[dict[str, str]]:
    if not MASTER_PATH.exists():
        return []
    with MASTER_PATH.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != MASTER_FIELDS:
            raise ValueError("The master CSV columns do not match the vocabulary schema")
        return list(reader)


def write_master(rows: list[dict[str, str]]) -> None:
    MASTER_PATH.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(rows, key=lambda row: row["NormalizedTerm"])
    with MASTER_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MASTER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ordered)


def row_from_record(record: dict[str, Any]) -> dict[str, str]:
    term = record["term"].strip()
    priority = record["priority"].upper()
    if priority not in PRIORITIES:
        raise ValueError(f"Unsupported priority for {term}: {priority}")
    parts = unique_strings(record.get("parts_of_speech", []))
    if not parts:
        raise ValueError(f"{term} has no part of speech")
    observed = unique_strings(record.get("observed_forms", [term]))
    sources = unique_strings(record.get("sources", ["direct user submission"]))
    seen = record.get("seen_date", date.today().isoformat())
    normalized = normalized_key(record.get("normalized_term", term))
    senses = record.get("senses", [])
    if not senses:
        raise ValueError(f"{term} has no sense data")
    return {
        "Term": term,
        "NormalizedTerm": normalized,
        "ObservedForms": json_cell(observed),
        "Priority": priority,
        "PartsOfSpeech": " · ".join(parts),
        "PronunciationHTML": record.get("pronunciation", "").strip(),
        "TTS_Text": record.get("tts_text", term).strip(),
        "SensesJSON": json_cell(senses),
        "FrequencySource": record.get("frequency_source", "qualitative estimate"),
        "FrequencyValue": str(record.get("frequency_value", "")),
        "FrequencyBand": record.get("frequency_band", "UNCOMMON"),
        "DailyConversationRelevance": record.get("daily_relevance", "LOW"),
        "IELTSRelevance": record.get("ielts_relevance", "LOW"),
        "ProfessionalRelevance": record.get("professional_relevance", "LOW"),
        "FantasyLiteraryRelevance": record.get("fantasy_literary_relevance", "LOW"),
        "EncounterCount": str(record.get("encounter_count", 1)),
        "FirstSeen": seen,
        "LastSeen": seen,
        "Sources": json_cell(sources),
        "IncludeInAnki": "true" if priority != "SKIP" else "false",
        "ClassificationReason": record.get("classification_reason", "").strip(),
    }


def merge_record(existing: dict[str, str], record: dict[str, Any]) -> dict[str, str]:
    incoming = row_from_record(record)
    merged = dict(existing)
    old_forms = parse_json_cell(existing["ObservedForms"], list, "ObservedForms")
    new_forms = parse_json_cell(incoming["ObservedForms"], list, "ObservedForms")
    old_sources = parse_json_cell(existing["Sources"], list, "Sources")
    new_sources = parse_json_cell(incoming["Sources"], list, "Sources")
    old_senses = parse_json_cell(existing["SensesJSON"], list, "SensesJSON")
    new_senses = parse_json_cell(incoming["SensesJSON"], list, "SensesJSON")

    for field in MASTER_FIELDS:
        if field not in {"ObservedForms", "Sources", "SensesJSON", "EncounterCount", "FirstSeen"}:
            merged[field] = incoming[field]
    merged["ObservedForms"] = json_cell(unique_strings(old_forms + new_forms))
    merged["Sources"] = json_cell(unique_strings(old_sources + new_sources))
    if record.get("replace_senses", False):
        merged["SensesJSON"] = incoming["SensesJSON"]
    else:
        merged["SensesJSON"] = json_cell(merge_senses(old_senses, new_senses))
    merged["EncounterCount"] = str(int(existing["EncounterCount"]) + int(record.get("encounter_increment", 1)))
    merged["FirstSeen"] = existing["FirstSeen"]
    return merged


def upsert(input_path: Path, increment_encounters: bool = True) -> dict[str, list[str]]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("The update file must contain a JSON list")
    rows = load_master()
    by_key = {row["NormalizedTerm"]: row for row in rows}
    added: list[str] = []
    updated: list[str] = []
    merged_members: list[str] = []
    for source_record in payload:
        if not isinstance(source_record, dict):
            raise ValueError("Every update item must be a JSON object")
        record = dict(source_record)
        if not increment_encounters:
            record["encounter_increment"] = 0
        incoming = row_from_record(record)
        key = incoming["NormalizedTerm"]
        # Explicitly approved consolidation: retain source metadata and require
        # every old sense to survive under the correct member of the new note.
        for member in record.get("merge_from", []):
            member_key = normalized_key(member)
            if member_key == key:
                raise ValueError("A merge source cannot be the target note")
            if member_key not in by_key:
                raise ValueError(f"Merge source does not exist: {member}")
            source = by_key[member_key]
            target_senses = record["senses"]
            old_senses = parse_json_cell(source["SensesJSON"], list, "SensesJSON")
            for block in old_senses:
                target_definitions = {
                    sense["definition"].strip().casefold()
                    for target in target_senses
                    if normalized_key(target.get("entry_term", "")) == member_key
                    and target["part_of_speech"].casefold() == block["part_of_speech"].casefold()
                    for sense in target["senses"]
                }
                if any(sense["definition"].strip().casefold() not in target_definitions for sense in block["senses"]):
                    raise ValueError(f"Merge would lose a sense of {member}")
            record["observed_forms"] = unique_strings(
                record.get("observed_forms", [record["term"]])
                + parse_json_cell(source["ObservedForms"], list, "ObservedForms")
            )
            record["sources"] = unique_strings(
                record.get("sources", []) + parse_json_cell(source["Sources"], list, "Sources")
            )
            record["encounter_count"] = int(record.get("encounter_count", 1)) + int(source["EncounterCount"])
            record["first_seen"] = min(record.get("first_seen", record.get("seen_date", date.today().isoformat())), source["FirstSeen"])
            rows.remove(source)
            del by_key[member_key]
            merged_members.append(source["Term"])
        incoming = row_from_record(record)
        if record.get("first_seen"):
            incoming["FirstSeen"] = record["first_seen"]
        if key in by_key:
            merged = merge_record(by_key[key], record)
            rows[rows.index(by_key[key])] = merged
            by_key[key] = merged
            updated.append(merged["Term"])
        else:
            rows.append(incoming)
            by_key[key] = incoming
            added.append(incoming["Term"])
    write_master(rows)
    rebuild_export(rows)
    validate()
    return {"added": added, "updated": updated, "merged": merged_members}


def render_relation_items(items: list[dict[str, Any]]) -> str:
    output: list[str] = []
    for fallback_rank, item in enumerate(items, start=1):
        rank = item.get("rank", fallback_rank)
        relationship = item.get("relationship", "")
        note = item.get("note", "").strip()
        suffix = f"; {html.escape(note)}" if note else ""
        output.append(
            '<div class="semantic-item">'
            f"<strong>{rank}. {html.escape(item['term'])}</strong> "
            f'— <span class="relation">{html.escape(relationship)}</span>{suffix}.'
            "</div>"
        )
    return "".join(output)


def render_grouped_back_html(senses: list[dict[str, Any]]) -> str:
    """Render the approved situation-based layout from escaped structured data."""
    entries: dict[str, list[dict[str, Any]]] = {}
    for block in senses:
        entries.setdefault(block["entry_term"], []).append(block)
    comparison = next((b["comparison"] for b in senses if "comparison" in b), None)
    output: list[str] = []
    for term, blocks in entries.items():
        output.append(f'<section class="lexical-entry"><h3>{html.escape(term)}</h3>')
        for block in blocks:
            output.append(f'<div class="pos-heading">{html.escape(block["part_of_speech"].upper())}</div>')
            for number, sense in enumerate(block["senses"], 1):
                output.append('<div class="sense"><div class="definition">'
                              f'<strong>{number}.</strong> {html.escape(sense["definition"])}</div>'
                              f'<div class="example">{html.escape(sense["example"])}</div></div>')
        output.append('</section>')
    if comparison:
        output.append('<section class="comparison"><h3>Everyday situations: what you can say</h3>'
                      '<table class="contrast-table"><thead><tr><th>Situation</th>'
                      '<th>Natural sentences</th><th>What to notice</th></tr></thead><tbody>')
        for situation in comparison["situations"]:
            output.append('<tr>' + ''.join(
                f'<td>{html.escape(situation[field])}</td>'
                for field in ("situation", "examples", "guidance")
            ) + '</tr>')
        output.append('</tbody></table><h3>Difference / overlap</h3>'
                      f'<p>{html.escape(comparison["note"])}</p></section>')
    output.append('<h3>Common patterns</h3>')
    for term, blocks in entries.items():
        for block in blocks:
            if block.get("common_patterns"):
                output.append(f'<div class="usage-note"><strong>{html.escape(term)}:</strong> '
                              f'{html.escape(block["common_patterns"])}</div>')
    for field, heading in (("synonyms", "Synonyms"), ("antonyms", "Antonyms")):
        output.append(f'<div class="semantic-heading">{heading}</div>')
        for term, blocks in entries.items():
            relations = [r for block in blocks for sense in block["senses"] for r in sense.get(field, [])]
            output.append(f'<div class="semantic-heading">{html.escape(term)}</div>')
            if relations:
                output.append(render_relation_items(relations))
            else:
                label = "synonym" if field == "synonyms" else "antonym"
                output.append(f'<div class="semantic-item">No useful {label} for this word.</div>')
    return ''.join(output)


def render_back_html(senses: list[dict[str, Any]]) -> str:
    if any(block.get("entry_term") for block in senses):
        return render_grouped_back_html(senses)
    has_synonyms = any(
        sense.get("synonyms")
        for block in senses
        for sense in block.get("senses", [])
    )
    has_antonyms = any(
        sense.get("antonyms")
        for block in senses
        for sense in block.get("senses", [])
    )
    blocks: list[str] = []
    for block in senses:
        blocks.append('<div class="pos-block">')
        blocks.append(f'<div class="pos-heading">{html.escape(block["part_of_speech"].upper())}</div>')
        for number, sense in enumerate(block.get("senses", []), start=1):
            blocks.append('<div class="sense">')
            blocks.append(
                '<div class="definition">'
                f"<strong>{number}.</strong> {html.escape(sense['definition'])}"
                "</div>"
            )
            example = sense.get("example", "").strip()
            if example:
                blocks.append(f'<div class="example">{html.escape(example)}</div>')
            usage_note = sense.get("usage_note", "").strip()
            if usage_note:
                blocks.append(f'<div class="usage-note">{html.escape(usage_note)}</div>')
            synonyms = sorted(sense.get("synonyms", []), key=lambda item: item.get("rank", 999))
            antonyms = sorted(sense.get("antonyms", []), key=lambda item: item.get("rank", 999))
            if synonyms:
                heading = "Synonym" if len(synonyms) == 1 else "Synonyms"
                blocks.append(f'<div class="semantic-heading">{heading}</div>')
                blocks.append(render_relation_items(synonyms))
            if antonyms:
                heading = "Antonym" if len(antonyms) == 1 else "Antonyms"
                blocks.append(f'<div class="semantic-heading">{heading}</div>')
                blocks.append(render_relation_items(antonyms))
            blocks.append("</div>")
        blocks.append("</div>")
    if not has_synonyms:
        blocks.append(
            '<div class="semantic-fallback">'
            '<div class="semantic-heading">Synonyms</div>'
            '<div class="semantic-item">No useful synonym for this word.</div>'
            "</div>"
        )
    if not has_antonyms:
        blocks.append(
            '<div class="semantic-fallback">'
            '<div class="semantic-heading">Antonyms</div>'
            '<div class="semantic-item">No useful antonym for this word.</div>'
            "</div>"
        )
    return "".join(blocks)


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def tags_for(row: dict[str, str]) -> str:
    tags = [f"priority::{row['Priority'].casefold()}"]
    tags.extend(f"pos::{slug(pos)}" for pos in row["PartsOfSpeech"].split(" · "))
    tags.append("domain::general")
    if row["IELTSRelevance"] == "HIGH":
        tags.append("domain::ielts")
    if row["ProfessionalRelevance"] == "HIGH":
        tags.append("domain::professional")
    if row["FantasyLiteraryRelevance"] == "HIGH":
        tags.append("domain::fantasy-literary")
    return " ".join(unique_strings(tags))


def rebuild_export(rows: list[dict[str, str]] | None = None) -> None:
    rows = load_master() if rows is None else rows
    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    included = sorted(
        (row for row in rows if row["Priority"] in {"ACTIVE", "RECEPTIVE"}),
        key=lambda row: row["NormalizedTerm"],
    )
    with EXPORT_PATH.open("w", encoding="utf-8", newline="") as handle:
        handle.write("#separator:Comma\n")
        handle.write("#html:true\n")
        handle.write("#notetype:EN_Vocabulary\n")
        handle.write("#deck:EN::Vocabulary\n")
        handle.write("#columns:" + ",".join(EXPORT_FIELDS) + "\n")
        writer = csv.writer(handle, lineterminator="\n")
        for row in included:
            senses = parse_json_cell(row["SensesJSON"], list, "SensesJSON")
            writer.writerow(
                [
                    row["Term"],
                    row["Priority"],
                    row["PartsOfSpeech"],
                    row["PronunciationHTML"],
                    row["TTS_Text"],
                    render_back_html(senses),
                    tags_for(row),
                ]
            )


class BalancedHTMLParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack.pop() != tag:
            raise ValueError(f"Malformed HTML near closing tag </{tag}>")

    def close(self) -> None:
        super().close()
        if self.stack:
            raise ValueError(f"Unclosed HTML tag <{self.stack[-1]}>")


def parse_export_rows() -> list[list[str]]:
    content = EXPORT_PATH.read_text(encoding="utf-8")
    data = "\n".join(line for line in content.splitlines() if not line.startswith("#"))
    return list(csv.reader(io.StringIO(data))) if data else []


def validate_senses(row: dict[str, str], require_examples: bool) -> list[dict[str, Any]]:
    senses = parse_json_cell(row["SensesJSON"], list, "SensesJSON")
    if not senses:
        raise ValueError(f"{row['Term']} has no sense blocks")
    grouped_terms = {block.get("entry_term", "") for block in senses if block.get("entry_term")}
    if grouped_terms:
        comparisons = [block for block in senses if "comparison" in block]
        if len(grouped_terms) < 2 or len(comparisons) != 1:
            raise ValueError(f"{row['Term']} needs multiple labelled terms and exactly one comparison")
    for block in senses:
        if not block.get("part_of_speech") or not block.get("senses"):
            raise ValueError(f"{row['Term']} has an incomplete part-of-speech block")
        if any(b.get("entry_term") for b in senses) and not block.get("entry_term", "").strip():
            raise ValueError(f"{row['Term']} mixes grouped and unlabelled sense blocks")
        if "comparison" in block:
            comparison = block["comparison"]
            if not comparison.get("note", "").strip() or not comparison.get("situations"):
                raise ValueError(f"{row['Term']} has an incomplete comparison")
            for situation in comparison["situations"]:
                if any(not situation.get(field, "").strip() for field in ("situation", "examples", "guidance")):
                    raise ValueError(f"{row['Term']} has an incomplete comparison situation")
        for sense in block["senses"]:
            if not sense.get("definition", "").strip():
                raise ValueError(f"{row['Term']} has an empty definition")
            if require_examples and not sense.get("example", "").strip():
                raise ValueError(f"{row['Term']} has an exported sense without an example")
            for relation_type in ("synonyms", "antonyms"):
                for relation in sense.get(relation_type, []):
                    if relation.get("relationship") not in RELATIONSHIPS:
                        raise ValueError(f"{row['Term']} has an invalid semantic relationship")
    return senses


def validate() -> dict[str, int]:
    if not MASTER_PATH.exists() or not EXPORT_PATH.exists():
        raise ValueError("Master data or Anki export is missing")
    rows = load_master()
    keys: set[str] = set()
    included: list[dict[str, str]] = []
    for row in rows:
        key = row["NormalizedTerm"]
        if key != normalized_key(key):
            raise ValueError(f"NormalizedTerm is not normalized: {key}")
        if key in keys:
            raise ValueError(f"Duplicate normalized headword: {key}")
        keys.add(key)
        if row["Priority"] not in PRIORITIES:
            raise ValueError(f"Invalid priority for {row['Term']}")
        parse_json_cell(row["ObservedForms"], list, "ObservedForms")
        parse_json_cell(row["Sources"], list, "Sources")
        require_examples = row["Priority"] != "SKIP"
        senses = validate_senses(row, require_examples)
        expected_include = row["Priority"] != "SKIP"
        if (row["IncludeInAnki"] == "true") != expected_include:
            raise ValueError(f"IncludeInAnki disagrees with priority for {row['Term']}")
        if expected_include:
            required = ["Term", "PartsOfSpeech", "PronunciationHTML", "TTS_Text"]
            if any(not row[field].strip() for field in required):
                raise ValueError(f"{row['Term']} is missing an exported field")
            if "/" not in row["PronunciationHTML"]:
                raise ValueError(f"{row['Term']} pronunciation does not look like IPA")
            back_html = render_back_html(senses)
            if not re.search(r'<div class="semantic-heading">Synonyms?</div>', back_html):
                raise ValueError(f"{row['Term']} is missing a visible Synonyms section")
            if not re.search(r'<div class="semantic-heading">Antonyms?</div>', back_html):
                raise ValueError(f"{row['Term']} is missing a visible Antonyms section")
            parser = BalancedHTMLParser()
            parser.feed(back_html)
            parser.close()
            included.append(row)

    export_rows = parse_export_rows()
    export_text = EXPORT_PATH.read_text(encoding="utf-8")
    if "#deck:EN::Vocabulary\n" not in export_text:
        raise ValueError("Anki export is not routed to the EN::Vocabulary subdeck")
    if any(len(export_row) != len(EXPORT_FIELDS) for export_row in export_rows):
        raise ValueError("Anki export contains a malformed CSV row")
    expected_export_rows: list[list[str]] = []
    for row in sorted(included, key=lambda item: item["NormalizedTerm"]):
        senses = parse_json_cell(row["SensesJSON"], list, "SensesJSON")
        expected_export_rows.append(
            [
                row["Term"],
                row["Priority"],
                row["PartsOfSpeech"],
                row["PronunciationHTML"],
                row["TTS_Text"],
                render_back_html(senses),
                tags_for(row),
            ]
        )
    if export_rows != expected_export_rows:
        raise ValueError("Anki export is stale or does not match the master data")
    export_terms = [export_row[0] for export_row in export_rows]
    skipped_terms = {row["Term"] for row in rows if row["Priority"] == "SKIP"}
    if skipped_terms.intersection(export_terms):
        raise ValueError("A SKIP item leaked into the Anki export")

    for template_path in (FRONT_PATH, BACK_PATH):
        template = template_path.read_text(encoding="utf-8")
        for field in ("{{Term}}", "{{PartsOfSpeech}}", "{{PronunciationHTML}}", "{{Priority}}", "{{tts en_US:TTS_Text}}"):
            if field not in template:
                raise ValueError(f"{template_path.name} is missing {field}")
    if "{{BackHTML}}" not in BACK_PATH.read_text(encoding="utf-8"):
        raise ValueError("back.html is missing BackHTML")
    style = STYLE_PATH.read_text(encoding="utf-8")
    for selector in (".term", ".pos", ".ipa", ".priority.ACTIVE", ".priority.RECEPTIVE", ".nightMode"):
        if selector not in style:
            raise ValueError(f"styling.css is missing {selector}")
    return {
        "master": len(rows),
        "active": sum(row["Priority"] == "ACTIVE" for row in rows),
        "receptive": sum(row["Priority"] == "RECEPTIVE" for row in rows),
        "skip": sum(row["Priority"] == "SKIP" for row in rows),
        "exported": len(export_rows),
    }


def print_summary(summary: dict[str, int]) -> None:
    print(
        "Validation passed: "
        f"{summary['master']} master entries; "
        f"{summary['active']} ACTIVE, {summary['receptive']} RECEPTIVE, "
        f"{summary['skip']} SKIP; {summary['exported']} exported."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    upsert_parser = subparsers.add_parser("upsert", help="upsert records from a JSON update file")
    upsert_parser.add_argument("--input", required=True, type=Path)
    upsert_parser.add_argument(
        "--no-encounter",
        action="store_true",
        help="apply an editorial correction without incrementing EncounterCount",
    )
    subparsers.add_parser("rebuild", help="regenerate the Anki export from the master CSV")
    subparsers.add_parser("validate", help="validate master data, export, templates, and styling")
    args = parser.parse_args()

    if args.command == "upsert":
        changes = upsert(args.input, increment_encounters=not args.no_encounter)
        print(f"Added: {', '.join(changes['added']) or 'none'}")
        print(f"Updated: {', '.join(changes['updated']) or 'none'}")
        print(f"Merged: {', '.join(changes['merged']) or 'none'}")
        print_summary(validate())
    elif args.command == "rebuild":
        rebuild_export()
        print_summary(validate())
    else:
        print_summary(validate())
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
