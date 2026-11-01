#!/usr/bin/env python3
"""Generate the semantic lookup from every canonical EN Anki card.

Every card receives human-authored meaning/function metadata from its own source.
Cross-card equivalences remain separately curated in groups.json.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts/anki"))
from exports import load_config, read_export  # noqa: E402
GROUPS=ROOT/"cards/semantic/groups.json"
OUTPUT=ROOT/"cards/semantic/index.json"
RELATIONS={"core","variant","near_synonym","related","contrast"}

def vocab_meta():
    result={}
    with (ROOT/"cards/vocabulary/data/vocabulary_master.csv").open(encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f):
            blocks=json.loads(row["SensesJSON"])
            senses=[s for b in blocks for s in b.get("senses",[])]
            definitions=[s["definition"] for s in senses][:4]
            synonyms=list(dict.fromkeys(r["term"] for s in senses for r in s.get("synonyms",[])))[:8]
            result[row["Term"]]={"function":"vocabulary",
                                 "meaning":"; ".join(definitions),
                                 "related_terms":synonyms}
    return result

def pattern_meta():
    functions={}
    selection=(ROOT/"cards/patterns/PATTERN_FRAME_SELECTION.md").read_text(encoding="utf-8")
    for line in selection.splitlines():
        m=re.fullmatch(r"\| ([^|]+) \| \x60([^\x60]+)\x60 \| [^|]*\|",line)
        if m:
            functions[m.group(2)]=m.group(1)
    descriptions={}
    lines=(ROOT/"cards/patterns/cards.md").read_text(encoding="utf-8").splitlines()
    for i,line in enumerate(lines):
        m=re.fullmatch(r"## \x60([^\x60]+)\x60",line)
        if not m:
            continue
        buf=[]
        for item in lines[i+1:]:
            val=item.strip()
            if val.startswith("<!--"):
                continue
            if not val:
                if buf:
                    break
                continue
            if val.startswith("## ") or val=="Examples:" or val.startswith("- "):
                break
            buf.append(val)
        descriptions[m.group(1)]=" ".join(buf)
    return functions,descriptions

def connection_meta():
    directory=ROOT/"cards/connections"
    with (directory/"coverage.tsv").open(encoding="utf-8",newline="") as f:
        validated={r["card_id"]:r for r in csv.DictReader(f,delimiter="\t")
                   if r["status"]=="validated" and r["card_id"]}
    ordered=[]
    for p in sorted(directory.glob("[0-9][0-9]-*.md")):
        ordered.extend(re.findall(r"^## (C\d\d-\d\d\d)\s*$",
                       p.read_text(encoding="utf-8"),re.MULTILINE))
    if len(ordered)!=len(validated) or set(ordered)!=set(validated):
        raise ValueError("Connection source IDs disagree with coverage")
    return [validated[k] for k in ordered]

def build():
    vocab=vocab_meta()
    functions,descriptions=pattern_meta()
    connection=connection_meta()
    cards=[]
    identities=set()
    connection_pos=0
    for family in load_config()["families"]:
        _,rows=read_export(ROOT/family["export"])
        for row in rows:
            key=row[family["fields"][0]]
            identity=(family["name"],key)
            if identity in identities:
                raise ValueError(f"Duplicate card identity: {identity}")
            identities.add(identity)
            card={"family":family["name"],"key":key,
                  "deck":row.get("Deck") or family["deck_root"]}
            if family["name"]=="vocabulary":
                card.update(vocab[key])
            elif family["name"]=="patterns":
                card.update({"function":functions.get(key,"Grammar operations"),
                             "meaning":descriptions.get(key,"")})
            elif family["name"]=="connections":
                if connection_pos>=len(connection):
                    raise ValueError("Too many connection exports")
                r=connection[connection_pos]
                connection_pos+=1
                card.update({"function":r["topic"],
                             "meaning":r["meaning_or_distinction"],
                             "anchor":r["anchor"],
                             "construction":r["target_pattern"],
                             "confusables":r["confusables"]})
            cards.append(card)
    if connection_pos!=len(connection):
        raise ValueError("Not all connection cards exported")
    groups=json.loads(GROUPS.read_text(encoding="utf-8"))
    if groups.get("schema_version")!=1:
        raise ValueError("Unsupported semantic schema version")
    seen_groups=set()
    for g in groups["groups"]:
        if not g.get("id") or g["id"] in seen_groups:
            raise ValueError(f"Empty/duplicate group ID: {g.get('id')}")
        seen_groups.add(g["id"])
        owner=(g["owner"]["family"],g["owner"]["key"])
        if owner not in identities:
            raise ValueError(f"Invalid semantic owner: {g['id']}")
        exps=set()
        for exp in g["expressions"]:
            name=" ".join(exp["text"].replace("’","'").casefold().split())
            if not name or name in exps:
                raise ValueError(f"Duplicate expression: {name}")
            exps.add(name)
            if exp["relationship"] not in RELATIONS:
                raise ValueError(f"Bad relation in {g['id']}")
    return {"schema_version":1,"cards":cards,"groups":groups["groups"]}

def render():
    return json.dumps(build(),ensure_ascii=False,indent=2)+"\n"

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    expected=render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8")!=expected:
            raise ValueError("Semantic index stale; rebuild with scripts/build_semantic_index.py")
        print("Semantic index valid.")
    else:
        OUTPUT.write_text(expected,encoding="utf-8")
        print(f"Semantic index built: {len(build()['cards'])} cards.")
    return 0

if __name__=="__main__":
    try:
        raise SystemExit(main())
    except (OSError,ValueError,KeyError) as e:
        print(f"error: {e}",file=sys.stderr)
        raise SystemExit(1)
