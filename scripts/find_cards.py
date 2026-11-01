#!/usr/bin/env python3
"""Find explicit card matches and candidate semantic owners across EN decks.

Examples:
  python3 scripts/find_cards.py "look up to" "the flip side"
  python3 scripts/find_cards.py --meaning "express respect and admiration"
Semantic similarity yields candidates, not claims of equivalent meaning.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts/anki"))
from exports import load_config, read_export  # noqa: E402
INDEX=ROOT/"cards/semantic/index.json"
TAG=re.compile(r"<[^>]+>")
STOP={"the","and","that","this","with","from","into","about","what","when",
      "where","have","has","does","for","some","someone","thing","things","also",
      "would","should","could","then","than","how","which","are","was","were",
      "you","your","him","her","them","they","our","one"}

def plain(text):
    return re.sub(r"\s+"," ",html.unescape(TAG.sub(" ",text))).strip()

def norm(text):
    return " ".join(text.casefold().replace("’","'").split())

def semantic_matches(query,index):
    return [(g,e) for g in index["groups"] for e in g["expressions"]
            if norm(e["text"])==norm(query)]

def tokens(value):
    return {w for w in re.findall(r"[a-z]{3,}",norm(value)) if w not in STOP}

def meaning_candidates(query,index,limit=8):
    """Rank overlapping human-authored meaning descriptors; do not equate synonyms."""
    query_words=tokens(query)
    if not query_words:
        return []
    results=[]
    for card in index["cards"]:
        fields=(
            (4,"key"),(3,"related_terms"),(2,"function"),(1,"meaning"),
            (2,"anchor"),(2,"construction"),(1,"confusables")
        )
        score=0
        for weight,field in fields:
            value=card.get(field,"")
            if isinstance(value,list):
                value=" ".join(value)
            score+=weight*len(query_words & tokens(value))
        if score:
            results.append((score,card))
    results.sort(key=lambda item:(-item[0],item[1]["family"],item[1]["key"]))
    return results[:limit]

def snippet(value,match,width=70):
    start,end=max(0,match.start()-width),min(len(value),match.end()+width)
    return ("…" if start else "")+value[start:end]+("…" if end<len(value) else "")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries",nargs="+")
    parser.add_argument("--exact",action="store_true",help="Disable inflection matching")
    parser.add_argument("--meaning",action="store_true",help="Search semantic descriptions; candidate results only")
    parser.add_argument("--limit",type=int,default=8)
    args=parser.parse_args()
    if args.limit<1:
        parser.error("--limit must be positive")
    index=json.loads(INDEX.read_text(encoding="utf-8"))
    cards=None
    if not args.meaning:
        cards=[]
        for family in load_config()["families"]:
            _,rows=read_export(ROOT/family["export"])
            first,rest=family["fields"][0],family["fields"][1:]
            for row in rows:
                cards.append((family["name"],plain(row[first]),
                              plain(" ".join(row[field] for field in rest))))
    for query in args.queries:
        print(f"\n=== {query}")
        exact=semantic_matches(query,index)
        for group,exp in exact:
            owner=group["owner"]
            note=f" ({exp['note']})" if exp.get("note") else ""
            print(f"  CURATED {group['id']} — {group['function']}")
            print(f"    {exp['relationship']}: {exp['text']}{note}")
            print(f"    owner: [{owner['family']}] {owner['key']}")
        if args.meaning:
            results=meaning_candidates(query,index,args.limit)
            print(f"  MEANING CANDIDATES ({len(results)}; inspect before treating as covered)")
            for score,card in results:
                print(f"    [{card['family']}] score={score} {plain(card['key'])[:120]}")
                print(f"      {card.get('function','')}: {card.get('meaning','')[:170]}")
            continue
        words=r"\s+".join(re.escape(w) for w in query.split())
        pattern=re.compile(r"\b"+words+(r"\b" if args.exact else r"\w*"),re.IGNORECASE)
        fronts=[(fam,key) for fam,key,_ in cards if pattern.search(key)]
        backs=[(fam,key,snippet(back,match)) for fam,key,back in cards
               if not pattern.search(key) and (match:=pattern.search(back))]
        print(f"  LITERAL {len(fronts)} Front match(es), {len(backs)} Back match(es)")
        for fam,key in fronts:
            print(f"    [{fam}] {key}")
        for fam,key,excerpt in backs:
            print(f"    [{fam}] mentioned: {key[:95]}\n      {excerpt}")
        if not exact and not fronts and not backs:
            print("  No exact/curated result. Try --meaning or related expressions.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
