#!/usr/bin/env python3
"""Search literal Front/Back matches and curated semantic aliases for Anki cards."""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/anki"))
from exports import load_config, read_export  # noqa: E402
INDEX = ROOT / "cards/semantic/index.json"
TAG = re.compile(r"<[^>]+>")

def plain(text):
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", text))).strip()

def norm(text):
    return " ".join(text.casefold().replace("’", "'").split())

def semantic_matches(query, index):
    return [(g, e) for g in index["groups"] for e in g["expressions"]
            if norm(e["text"]) == norm(query)]

def snippet(text, match, width=70):
    start, end = max(0, match.start()-width), min(len(text), match.end()+width)
    return ("…" if start else "")+text[start:end]+("…" if end < len(text) else "")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", nargs="+")
    parser.add_argument("--exact", action="store_true")
    args = parser.parse_args()
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    cards = []
    for family in load_config()["families"]:
        _, rows = read_export(ROOT / family["export"])
        first, rest = family["fields"][0], family["fields"][1:]
        for row in rows:
            cards.append((family["name"], plain(row[first]),
                          plain(" ".join(row[field] for field in rest))))
    for query in args.queries:
        print(f"\n=== {query}")
        semantic = semantic_matches(query, index)
        for group, exp in semantic:
            owner = group["owner"]
            note = f" ({exp['note']})" if exp.get("note") else ""
            print(f"  SEMANTIC {group['id']}: {group['function']}")
            print(f"    {exp['relationship']}: {exp['text']}{note}")
            print(f"    owner: [{owner['family']}] {owner['key']}")
        words = r"\s+".join(re.escape(w) for w in query.split())
        pattern = re.compile(r"\b"+words+(r"\b" if args.exact else r"\w*"), re.IGNORECASE)
        fronts = [(fam,key) for fam,key,_ in cards if pattern.search(key)]
        backs = [(fam,key,snippet(back,hit)) for fam,key,back in cards
                 if not pattern.search(key) and (hit := pattern.search(back))]
        print(f"  LITERAL {len(fronts)} Front match(es), {len(backs)} Back match(es)")
        for fam,key in fronts:
            print(f"    [{fam}] {key}")
        for fam,key,part in backs:
            print(f"    [{fam}] mentioned: {key[:95]}\n      {part}")
        if not semantic and not fronts and not backs:
            print("  No indexed match. Search related meanings manually.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
