#!/usr/bin/env python3
"""Plan and apply the repo's generated card imports to an Anki collection.

The EN Cards Sync add-on calls build_plan/apply_plan on the Anki app's open
collection; Anki itself then syncs. Run from the command line, this module only
previews the plan against a closed collection file. Nothing here contacts
AnkiWeb, whose terms allow only official Anki clients.

Notes are matched the way Anki's text importer matches them: same note type and
same first field, restricted to the family's deck tree (cards/anki_sync.json).
The tool adds missing notes, updates changed fields/tags of matched notes (which
keeps their review history), and updates template text and CSS that the repo
owns. It never deletes, renames, or moves notes, never changes a note type's
fields or templates list, and never performs a full upload.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from anki.collection import Collection

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_collection import read_export  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'cards/anki_sync.json'


class SyncAbort(Exception):
    """A condition that must stop the run before anything is written."""


@dataclass
class Plan:
    additions: list[tuple[str, str, dict[str, str], list[str]]] = field(default_factory=list)
    updates: list[tuple[str, int, dict[str, str], list[str] | None, list[str]]] = field(default_factory=list)
    notetype_updates: list[tuple[str, list[str]]] = field(default_factory=list)
    anki_only: dict[str, list[str]] = field(default_factory=dict)
    deck_mismatches: list[str] = field(default_factory=list)
    unchanged: dict[str, int] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        return not (self.additions or self.updates or self.notetype_updates)


def load_config(path: Path = CONFIG) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def resolve_notetype(col: Collection, family: dict) -> dict:
    notetype = col.models.by_name(family['notetype'])
    if notetype is None:
        raise SyncAbort(f"[{family['name']}] note type {family['notetype']!r} does not exist in Anki")
    actual = [f['name'] for f in notetype['flds']]
    if actual != family['fields']:
        raise SyncAbort(f"[{family['name']}] note type {family['notetype']!r} has fields {actual}, "
                        f"expected {family['fields']}; change the note type in the Anki app first")
    return notetype


def plan_family(col: Collection, family: dict, plan: Plan, root: Path) -> None:
    name, deck_root = family['name'], family['deck_root']
    notetype = resolve_notetype(col, family)
    headers, rows = read_export(root / family['export'])
    match_field = family['fields'][0]

    in_tree: dict[str, list[int]] = {}
    for nid in col.find_notes(f'"deck:{deck_root}" mid:{notetype["id"]}'):
        key = col.get_note(nid).fields[0]
        in_tree.setdefault(key, []).append(nid)
    duplicates = [k for k, ids in in_tree.items() if len(ids) > 1]
    if duplicates:
        raise SyncAbort(f'[{name}] duplicate notes in Anki for: {duplicates[:5]}')

    outside: dict[str, int] = {}
    for nid, flds in col.db.all('select id, flds from notes where mid = ?', notetype['id']):
        key = flds.split('\x1f', 1)[0]
        if key not in in_tree:
            outside[key] = nid

    seen: set[str] = set()
    unchanged = 0
    for row in rows:
        key = row[match_field]
        if key in seen:
            raise SyncAbort(f'[{name}] export has a duplicate first field: {key[:80]}')
        seen.add(key)
        deck = row.get('Deck') or headers.get('deck', '')
        if deck != deck_root and not deck.startswith(deck_root + '::'):
            raise SyncAbort(f'[{name}] export routes {key[:60]!r} to {deck!r}, outside {deck_root!r}')
        fields = {f: row[f] for f in family['fields']}
        tags = row.get('Tags', '').split() if family.get('sync_tags') else []
        if key not in in_tree:
            if key in outside:
                decks = sorted({col.decks.name(c.did) for c in col.get_note(outside[key]).cards()})
                raise SyncAbort(f'[{name}] {key[:60]!r} already exists outside {deck_root} in {decks}; '
                                'move it in the Anki app or resolve the conflict first')
            plan.additions.append((name, deck, fields, tags))
            continue
        note = col.get_note(in_tree[key][0])
        changed = [f for f in family['fields'] if note[f] != fields[f]]
        new_tags = None
        if family.get('sync_tags') and sorted(note.tags) != sorted(tags):
            new_tags = tags
            changed.append('tags')
        card_decks = {col.decks.name(c.did) for c in note.cards()}
        if deck not in card_decks:
            plan.deck_mismatches.append(f'[{name}] {key[:60]!r}: Anki {sorted(card_decks)}, repo {deck!r}')
        if changed:
            plan.updates.append((name, note.id, {f: fields[f] for f in changed if f != 'tags'}, new_tags, changed))
        else:
            unchanged += 1
    plan.unchanged[name] = unchanged
    plan.anki_only[name] = [k[:80] for k in in_tree if k not in seen]

    changes = []
    for template_name, paths in family.get('templates', {}).items():
        template = next((t for t in notetype['tmpls'] if t['name'] == template_name), None)
        if template is None:
            raise SyncAbort(f'[{name}] template {template_name!r} is missing from {family["notetype"]!r}')
        for side, key in (('front', 'qfmt'), ('back', 'afmt')):
            if template[key].strip() != (root / paths[side]).read_text(encoding='utf-8').strip():
                changes.append(f'{template_name} {side}')
    if family.get('css') and notetype['css'].strip() != (root / family['css']).read_text(encoding='utf-8').strip():
        changes.append('css')
    if changes:
        plan.notetype_updates.append((name, changes))


def build_plan(col: Collection, config: dict, root: Path = ROOT) -> Plan:
    plan = Plan()
    for family in config['families']:
        plan_family(col, family, plan, root)
    limits = config.get('limits', {})
    if len(plan.additions) > limits.get('max_additions', 10**9):
        raise SyncAbort(f'{len(plan.additions)} additions exceed max_additions; rerun with --allow-large if intended')
    if len(plan.updates) > limits.get('max_updates', 10**9):
        raise SyncAbort(f'{len(plan.updates)} updates exceed max_updates; rerun with --allow-large if intended')
    return plan


def schema_stamp(col: Collection) -> int:
    return col.db.scalar('select scm from col')


def apply_plan(col: Collection, plan: Plan, config: dict, root: Path = ROOT) -> None:
    families = {f['name']: f for f in config['families']}
    before = schema_stamp(col)
    for name, deck, fields, tags in plan.additions:
        note = col.new_note(col.models.by_name(families[name]['notetype']))
        for key, value in fields.items():
            note[key] = value
        note.tags = tags
        col.add_note(note, col.decks.id(deck, create=True))
    for _name, nid, fields, tags, _changed in plan.updates:
        note = col.get_note(nid)
        for key, value in fields.items():
            note[key] = value
        if tags is not None:
            note.tags = tags
        col.update_note(note)
    for name, _changes in plan.notetype_updates:
        family = families[name]
        notetype = col.models.by_name(family['notetype'])
        for template in notetype['tmpls']:
            paths = family.get('templates', {}).get(template['name'])
            if paths:
                template['qfmt'] = (root / paths['front']).read_text(encoding='utf-8')
                template['afmt'] = (root / paths['back']).read_text(encoding='utf-8')
        if family.get('css'):
            notetype['css'] = (root / family['css']).read_text(encoding='utf-8')
        col.models.update_dict(notetype)
    if schema_stamp(col) != before:
        raise SyncAbort('changes would modify the collection schema (forcing a full sync); nothing was synced')


def render_report(plan: Plan, applied: bool) -> str:
    verb = 'Applied' if applied else 'Planned (dry run)'
    lines = [f'## Anki sync: {verb}', '',
             '| Family | Unchanged | Add | Update | Only in Anki |', '| --- | ---: | ---: | ---: | ---: |']
    for name, unchanged in plan.unchanged.items():
        adds = sum(1 for a in plan.additions if a[0] == name)
        updates = sum(1 for u in plan.updates if u[0] == name)
        lines.append(f'| {name} | {unchanged} | {adds} | {updates} | {len(plan.anki_only.get(name, []))} |')
    for name, deck, fields, _tags in plan.additions:
        lines.append(f'- add [{name}] {next(iter(fields.values()))[:90]} → {deck}')
    for name, _nid, fields, _tags, changed in plan.updates:
        lines.append(f'- update [{name}] {", ".join(changed)}: {next(iter(fields.values()), "")[:60]}')
    for name, changes in plan.notetype_updates:
        lines.append(f'- note type [{name}]: update {", ".join(changes)}')
    for name, keys in plan.anki_only.items():
        for key in keys:
            lines.append(f'- only in Anki, left untouched [{name}]: {key}')
    for mismatch in plan.deck_mismatches:
        lines.append(f'- deck differs, left untouched {mismatch}')
    if plan.empty:
        lines.append('\nAnkiWeb already matches the repo.')
    return '\n'.join(lines) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('collection', type=Path,
                        help='a closed .anki2 file to preview against (a temporary copy is opened)')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / 'collection.anki2'
        shutil.copy2(args.collection, copy)
        col = Collection(str(copy))
        try:
            plan = build_plan(col, load_config())
        except SyncAbort as error:
            print(f'ABORTED: {error}', file=sys.stderr)
            return 1
        finally:
            col.close()
    print(render_report(plan, applied=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
