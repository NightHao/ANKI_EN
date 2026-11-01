#!/usr/bin/env python3
"""Build/check a semantic owner lookup over all three EN Anki exports."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/anki"))
from exports import load_config, read_export  # noqa: E402
GROUPS = ROOT / "cards/semantic/groups.json"
OUTPUT = ROOT / "cards/semantic/index.json"
RELATIONS = {"core", "variant", "near_synonym", "related", "contrast"}

def build():
    cards, identities = [], set()
    for family in load_config()["families"]:
        _, rows = read_export(ROOT / family["export"])
        for row in rows:
            key = row[family["fields"][0]]
            identity = (family["name"], key)
            if identity in identities:
                raise ValueError(f"Duplicate Anki note: {identity}")
            identities.add(identity)
            cards.append({"family": family["name"], "key": key,
                          "deck": row.get("Deck") or family["deck_root"]})
    data = json.loads(GROUPS.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported semantic schema version")
    seen_groups = set()
    for group in data["groups"]:
        if not group.get("id") or group["id"] in seen_groups:
            raise ValueError(f"Duplicate/empty semantic group: {group.get('id')}")
        seen_groups.add(group["id"])
        owner = (group["owner"]["family"], group["owner"]["key"])
        if owner not in identities:
            raise ValueError(f"Missing semantic group owner {group['id']}: {owner}")
        seen_expressions = set()
        for exp in group["expressions"]:
            value = " ".join(exp["text"].casefold().replace("’", "'").split())
            if not value or value in seen_expressions:
                raise ValueError(f"Empty/duplicate expression: {group['id']} {value}")
            seen_expressions.add(value)
            if exp["relationship"] not in RELATIONS:
                raise ValueError(f"Invalid relationship: {exp['relationship']}")
    return {"schema_version": 1, "cards": cards, "groups": data["groups"]}

def render():
    return json.dumps(build(), ensure_ascii=False, indent=2) + "\n"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            raise ValueError("Semantic index stale: run python3 scripts/build_semantic_index.py")
        print("Semantic index valid.")
    else:
        OUTPUT.write_text(expected, encoding="utf-8")
        print(f"Semantic index generated: {len(build()['cards'])} cards.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        raise SystemExit(1)
