#!/usr/bin/env python3
"""Find existing cards that cover an expression, across all three decks.

    python3 scripts/find_cards.py regard "with respect to" concerning

Each query matches whole words and their inflections (regard -> regards,
regarded, regarding). Hits on a card's Term/Front are listed first, then cards
whose Back merely mentions the expression. Use --exact to disable inflections.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/anki'))
from exports import load_config, read_export  # noqa: E402

TAG = re.compile(r'<[^>]+>')


def plain(text: str) -> str:
    return re.sub(r'\s+', ' ', html.unescape(TAG.sub(' ', text))).strip()


def snippet(text: str, match: re.Match, width: int = 70) -> str:
    start, end = max(0, match.start() - width), min(len(text), match.end() + width)
    return ('…' if start else '') + text[start:end] + ('…' if end < len(text) else '')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('queries', nargs='+')
    parser.add_argument('--exact', action='store_true', help='match the exact words only')
    args = parser.parse_args()

    cards = []
    for family in load_config()['families']:
        _headers, rows = read_export(ROOT / family['export'])
        first, rest = family['fields'][0], family['fields'][1:]
        for row in rows:
            cards.append((family['name'], plain(row[first]), plain(' '.join(row[f] for f in rest))))

    for query in args.queries:
        words = r'\s+'.join(re.escape(w) for w in query.split())
        pattern = re.compile(r'\b' + words + (r'\b' if args.exact else r'\w*'), re.IGNORECASE)
        front_hits = [(fam, key) for fam, key, _back in cards if pattern.search(key)]
        back_hits = [(fam, key, snippet(back, m)) for fam, key, back in cards
                     if not pattern.search(key) and (m := pattern.search(back))]
        print(f'\n=== {query}: {len(front_hits)} card(s) named, {len(back_hits)} mention(s)')
        for fam, key in front_hits:
            print(f'  {fam:<12} {key}')
        for fam, key, text in back_hits:
            print(f'  {fam:<12} (mentioned) {key[:90]}\n               {text}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
