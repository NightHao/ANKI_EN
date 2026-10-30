#!/usr/bin/env python3
"""Compare a downloaded Anki collection with the repo's generated imports (read-only).

Reports every note type, the note types actually used inside each EN deck tree,
and, per card family, which repo notes are identical, changed, missing in Anki,
or present only in Anki. Matching uses the first field, as Anki's importer does.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from anki.collection import Collection

ROOT = Path(__file__).resolve().parents[2]


def read_export(path: Path) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Parse an Anki text-import file into its header directives and rows."""
    headers: dict[str, str] = {}
    body: list[str] = []
    for line in path.read_text(encoding='utf-8').splitlines(keepends=True):
        if not body and line.startswith('#') and ':' in line:
            key, value = line[1:].rstrip('\r\n').split(':', 1)
            headers[key] = value
        else:
            body.append(line)
    delimiter = '\t' if headers.get('separator', '').lower() == 'tab' else ','
    rows = list(csv.reader(body, delimiter=delimiter))
    if 'columns' in headers:
        columns = headers['columns'].split(delimiter)
    else:
        # Pattern/connection TSVs: deck column, then the two Basic fields.
        columns = ['Deck', 'Front', 'Back']
    return headers, [dict(zip(columns, row, strict=True)) for row in rows if row]


FAMILIES = {
    'vocabulary': ('cards/vocabulary/exports/anki_import.csv', 'EN::Vocabulary'),
    'patterns': ('cards/patterns/anki-import.tsv', 'EN::Patterns'),
    'connections': ('cards/connections/anki-import.tsv', 'EN::Connection Patterns'),
}


def note_decks(col: Collection, note) -> set[str]:
    return {col.decks.name(card.did) for card in note.cards()}


def inspect_family(col: Collection, first_field_index: dict[str, list[int]], name: str,
                   export: str, deck_root: str) -> dict:
    headers, rows = read_export(ROOT / export)
    field_columns = [c for c in rows[0] if c not in ('Deck', 'Tags')]
    match_field = field_columns[0]
    repo = {row[match_field]: row for row in rows}

    in_tree = col.find_notes(f'"deck:{deck_root}"')
    by_key: dict[str, list] = defaultdict(list)
    notetypes = Counter()
    for nid in in_tree:
        note = col.get_note(nid)
        notetypes[note.note_type()['name']] += 1
        by_key[note.fields[0]].append(note)

    report = {
        'export': export, 'deck_root': deck_root, 'header_notetype': headers.get('notetype'),
        'repo_notes': len(repo), 'anki_notes_in_tree': len(in_tree),
        'notetypes_in_tree': dict(notetypes), 'identical': 0,
        'changed': [], 'repo_only': [], 'anki_only': [], 'duplicates_in_anki': [],
        'outside_tree_matches': [], 'deck_mismatch': [],
    }
    for key, row in repo.items():
        notes = by_key.get(key, [])
        if not notes:
            # A missing note might still exist outside the deck tree.
            elsewhere = first_field_index.get(key, [])
            entry = {'key': key[:120]}
            if elsewhere:
                n = col.get_note(elsewhere[0])
                entry.update(notetype=n.note_type()['name'], decks=sorted(note_decks(col, n)))
                report['outside_tree_matches'].append(entry)
            else:
                report['repo_only'].append(key[:120])
            continue
        if len(notes) > 1:
            report['duplicates_in_anki'].append(key[:120])
        note = notes[0]
        names = [f['name'] for f in note.note_type()['flds']]
        diffs = []
        for column in field_columns:
            actual = note[column] if column in names else None
            if actual != row[column]:
                diffs.append({'field': column, 'anki': (actual or '')[:300], 'repo': row[column][:300],
                              'anki_len': len(actual or ''), 'repo_len': len(row[column])})
        if 'Tags' in row and set(row['Tags'].split()) != set(note.tags):
            diffs.append({'field': 'Tags', 'anki': ' '.join(note.tags), 'repo': row['Tags']})
        if 'Deck' in row and row['Deck'] not in note_decks(col, note):
            report['deck_mismatch'].append({'key': key[:120], 'repo': row['Deck'],
                                            'anki': sorted(note_decks(col, note))})
        if diffs:
            report['changed'].append({'key': key[:120], 'notetype': note.note_type()['name'], 'diffs': diffs})
        else:
            report['identical'] += 1
    report['anki_only'] = [k[:120] for k in by_key if k not in repo]
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('collection', type=Path, help='downloaded .anki2 file (opened from a temp copy)')
    parser.add_argument('--json', type=Path, help='write the full report here')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / 'inspect.anki2'
        shutil.copy2(args.collection, copy)
        col = Collection(str(copy))
        try:
            notetypes = []
            for entry in col.models.all_names_and_ids():
                model = col.models.get(entry.id)
                notetypes.append({
                    'name': model['name'], 'id': model['id'], 'cloze': model['type'] == 1,
                    'fields': [f['name'] for f in model['flds']],
                    'templates': [t['name'] for t in model['tmpls']],
                    'notes': col.models.use_count(model),
                })
            decks = sorted(d.name for d in col.decks.all_names_and_ids() if d.name.startswith('EN'))
            first_field_index: dict[str, list[int]] = defaultdict(list)
            for nid, flds in col.db.all('select id, flds from notes'):
                first_field_index[flds.split('\x1f', 1)[0]].append(nid)
            families = {name: inspect_family(col, first_field_index, name, *spec)
                        for name, spec in FAMILIES.items()}
            totals = {'notes': col.note_count(), 'cards': col.card_count()}
        finally:
            col.close()

    report = {'collection': totals, 'notetypes': notetypes, 'en_decks': decks, 'families': families}
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Collection: {totals['notes']} notes, {totals['cards']} cards")
    print('\nNote types:')
    for nt in notetypes:
        kind = 'cloze' if nt['cloze'] else 'standard'
        print(f"  {nt['name']!r} ({kind}, {nt['notes']} notes) fields={nt['fields']} templates={nt['templates']}")
    print('\nEN decks:\n  ' + '\n  '.join(decks))
    for name, fam in families.items():
        print(f"\n[{name}] {fam['deck_root']}  repo={fam['repo_notes']}  anki_in_tree={fam['anki_notes_in_tree']}")
        print(f"  note types in tree: {fam['notetypes_in_tree']}  (export header: {fam['header_notetype']})")
        print(f"  identical={fam['identical']}  changed={len(fam['changed'])}  repo_only={len(fam['repo_only'])}"
              f"  anki_only={len(fam['anki_only'])}  dupes={len(fam['duplicates_in_anki'])}"
              f"  outside_tree={len(fam['outside_tree_matches'])}  deck_mismatch={len(fam['deck_mismatch'])}")
        changed_fields = Counter(d['field'] for c in fam['changed'] for d in c['diffs'])
        if changed_fields:
            print(f'  changed fields: {dict(changed_fields)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
