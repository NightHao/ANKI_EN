#!/usr/bin/env python3
"""Plan and apply the repo's generated card imports to an Anki collection.

The EN Cards Sync add-on calls build_plan/apply_plan on the Anki app's open
collection; Anki itself then syncs. Run from the command line, this module only
previews the plan against a closed collection file. Nothing here contacts
AnkiWeb, whose terms allow only official Anki clients.

Notes are matched the way Anki's text importer matches them: same note type and
same first field, restricted to the family's deck tree (cards/anki_sync.json).
The planner adds missing notes, updates changed fields/tags (keeping review
history), and updates template text and CSS that the repo owns.

Card identity changes come only from the change records in
cards/anki_changes.json (one per commit, gathered from git history by the
add-on): a rename edits the existing note's first field in place, keeping its
review history; a removal deletes the named note. Nothing else is ever deleted,
and a note type's fields are never changed.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from anki.collection import Collection

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exports import CHANGES, ROOT, EMPTY_CHANGES, load_config, parse_changes, read_export  # noqa: E402


class SyncAbort(Exception):
    """A condition that must stop the run before anything is written."""


@dataclass
class Plan:
    additions: list[tuple[str, str, dict[str, str], list[str]]] = field(default_factory=list)
    updates: list[tuple[str, int, dict[str, str], list[str] | None, list[str]]] = field(default_factory=list)
    renames: list[tuple[str, int, str, dict[str, str], list[str] | None]] = field(default_factory=list)
    removals: list[tuple[str, int, str]] = field(default_factory=list)
    notetype_updates: list[tuple[str, list[str]]] = field(default_factory=list)
    anki_only: dict[str, list[str]] = field(default_factory=dict)
    deck_mismatches: list[str] = field(default_factory=list)
    unchanged: dict[str, int] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        return not (self.additions or self.updates or self.renames or self.removals or self.notetype_updates)


def merge_changes(records: list[dict]) -> dict:
    """Combine change records in commit order."""
    merged = {'renames': [], 'removals': []}
    for record in records:
        merged['renames'] += record.get('renames', [])
        merged['removals'] += record.get('removals', [])
    return merged


def resolve_notetype(col: Collection, family: dict) -> dict:
    notetype = col.models.by_name(family['notetype'])
    if notetype is None:
        raise SyncAbort(f"[{family['name']}] note type {family['notetype']!r} does not exist in Anki")
    actual = [f['name'] for f in notetype['flds']]
    if actual != family['fields']:
        raise SyncAbort(f"[{family['name']}] note type {family['notetype']!r} has fields {actual}, "
                        f"expected {family['fields']}; change the note type in the Anki app first")
    return notetype


def plan_family(col: Collection, family: dict, plan: Plan, root: Path, changes: dict) -> None:
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

    # Later records win; follow chains such as A -> B -> C back to a live note.
    renamed_from = {r['to']: r['from'] for r in changes['renames'] if r['family'] == name}
    consumed: set[str] = set()

    def rename_source(key: str) -> str | None:
        seen_keys = {key}
        while key in renamed_from:
            key = renamed_from[key]
            if key in seen_keys:
                raise SyncAbort(f'[{name}] rename records form a cycle at {key[:60]!r}')
            seen_keys.add(key)
            if key in in_tree:
                return key
        return None

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
            source = rename_source(key)
            if source is not None:
                if source in consumed:
                    raise SyncAbort(f'[{name}] two cards claim the rename source {source[:60]!r}')
                consumed.add(source)
                plan.renames.append((name, in_tree[source][0], source, fields,
                                     tags if family.get('sync_tags') else None))
                continue
            if key in outside:
                decks = sorted({col.decks.name(c.did) for c in col.get_note(outside[key]).cards()})
                raise SyncAbort(f'[{name}] {key[:60]!r} already exists outside {deck_root} in {decks}; '
                                'move it in the Anki app or resolve the conflict first')
            plan.additions.append((name, deck, fields, tags))
            continue
        if key in renamed_from and rename_source(key) is not None:
            raise SyncAbort(f'[{name}] both {key[:50]!r} and its rename source exist in Anki; '
                            'delete the one without review history in the Anki app')
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

    for removal in changes['removals']:
        if removal['family'] != name:
            continue
        key = removal['key']
        if key in seen:
            raise SyncAbort(f'[{name}] a change record removes {key[:60]!r}, but the repo still has it')
        if key in in_tree and key not in consumed and all(r[2] != in_tree[key][0] for r in plan.removals):
            plan.removals.append((name, in_tree[key][0], key))
    removed = {r[2] for r in plan.removals if r[0] == name}
    plan.unchanged[name] = unchanged
    plan.anki_only[name] = [k[:80] for k in in_tree if k not in seen and k not in consumed and k not in removed]

    template_changes = []
    for template_name, paths in family.get('templates', {}).items():
        template = next((t for t in notetype['tmpls'] if t['name'] == template_name), None)
        if template is None:
            raise SyncAbort(f'[{name}] template {template_name!r} is missing from {family["notetype"]!r}')
        for side, key in (('front', 'qfmt'), ('back', 'afmt')):
            if template[key].strip() != (root / paths[side]).read_text(encoding='utf-8').strip():
                template_changes.append(f'{template_name} {side}')
    if family.get('css') and notetype['css'].strip() != (root / family['css']).read_text(encoding='utf-8').strip():
        template_changes.append('css')
    if template_changes:
        plan.notetype_updates.append((name, template_changes))


def build_plan(col: Collection, config: dict, root: Path = ROOT, changes: dict | None = None) -> Plan:
    changes = changes or EMPTY_CHANGES
    plan = Plan()
    for family in config['families']:
        plan_family(col, family, plan, root, changes)
    limits = config.get('limits', {})
    for label, items in (('additions', plan.additions), ('updates', plan.updates + plan.renames),
                         ('removals', plan.removals)):
        if len(items) > limits.get(f'max_{label}', 10**9):
            raise SyncAbort(f'{len(items)} {label} exceed max_{label} in cards/anki_sync.json; '
                            'raise the limit there if this is intended')
    return plan


def schema_stamp(col: Collection) -> int:
    return col.db.scalar('select scm from col')


IMAGE_SOURCE_RE = re.compile(r'<img\\b[^>]*\\bsrc="([^"]+)"')


def install_pattern_media(col: Collection, plan: Plan, config: dict, root: Path) -> None:
    """Install versioned diagram assets before updating note HTML.

    Anki's regular post-update sync distributes media to mobile devices.
    """
    families = {f["name"]: f for f in config["families"]}
    pending = [(name, fields) for name, _deck, fields, _tags in plan.additions]
    pending += [(name, fields) for name, _id, fields, _tags, _changed in plan.updates]
    pending += [(name, fields) for name, _id, _old, fields, _tags in plan.renames]
    installed: set[str] = set()
    for family_name, fields in pending:
        media_dir = families[family_name].get("media_dir")
        if not media_dir:
            continue
        for value in fields.values():
            for filename in IMAGE_SOURCE_RE.findall(value):
                if filename in installed:
                    continue
                if not re.fullmatch(r"en-prepositions-[a-z0-9-]+\\.svg", filename):
                    raise SyncAbort(f"Unexpected diagram name: {filename}")
                path = root / media_dir / filename
                if not path.is_file():
                    raise SyncAbort(f"Missing diagram asset: {path}")
                actual = col.media.add_file(str(path))
                if actual != filename:
                    raise SyncAbort(
                        f"Anki media filename collision: {filename} became {actual}"
                    )
                installed.add(filename)


def apply_plan(col: Collection, plan: Plan, config: dict, root: Path = ROOT) -> None:
    families = {f['name']: f for f in config['families']}
    before = schema_stamp(col)
    install_pattern_media(col, plan, config, root)
    for name, deck, fields, tags in plan.additions:
        note = col.new_note(col.models.by_name(families[name]['notetype']))
        for key, value in fields.items():
            note[key] = value
        note.tags = tags
        col.add_note(note, col.decks.id(deck, create=True))
    edits = [(nid, fields, tags) for _n, nid, fields, tags, _c in plan.updates]
    edits += [(nid, fields, tags) for _n, nid, _old, fields, tags in plan.renames]
    for nid, fields, tags in edits:
        note = col.get_note(nid)
        for key, value in fields.items():
            note[key] = value
        if tags is not None:
            note.tags = tags
        col.update_note(note)
    if plan.removals:
        col.remove_notes([nid for _name, nid, _key in plan.removals])
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
        raise SyncAbort('changes would modify the collection schema (forcing a full sync)')


def render_report(plan: Plan, applied: bool) -> str:
    verb = 'Applied' if applied else 'Planned'
    lines = [f'## EN cards: {verb}', '',
             '| Family | Unchanged | Add | Update | Rename | Remove | Only in Anki |',
             '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for name, unchanged in plan.unchanged.items():
        counts = [sum(1 for item in items if item[0] == name)
                  for items in (plan.additions, plan.updates, plan.renames, plan.removals)]
        lines.append(f'| {name} | {unchanged} | ' + ' | '.join(map(str, counts))
                     + f' | {len(plan.anki_only.get(name, []))} |')
    lines.append('')
    for name, deck, fields, _tags in plan.additions:
        lines.append(f'- add [{name}] {next(iter(fields.values()))[:90]} → {deck}')
    for name, _nid, fields, _tags, changed in plan.updates:
        lines.append(f'- update [{name}] {", ".join(changed)}: {next(iter(fields.values()), "")[:60]}')
    for name, _nid, old, fields, _tags in plan.renames:
        lines.append(f'- rename [{name}] {old[:50]} → {next(iter(fields.values()))[:50]} (review history kept)')
    for name, _nid, key in plan.removals:
        lines.append(f'- remove [{name}] {key[:80]}')
    for name, changes in plan.notetype_updates:
        lines.append(f'- note type [{name}]: update {", ".join(changes)}')
    for name, keys in plan.anki_only.items():
        for key in keys:
            lines.append(f'- only in Anki, left untouched [{name}]: {key}')
    for mismatch in plan.deck_mismatches:
        lines.append(f'- deck differs, left untouched {mismatch}')
    if plan.empty:
        lines.append('Anki already matches the repo.')
    return '\n'.join(lines) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('collection', type=Path,
                        help='a closed .anki2 file to preview against (a temporary copy is opened)')
    args = parser.parse_args()

    changes = parse_changes(CHANGES.read_text(encoding='utf-8')) if CHANGES.exists() else EMPTY_CHANGES
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / 'collection.anki2'
        shutil.copy2(args.collection, copy)
        col = Collection(str(copy))
        try:
            plan = build_plan(col, load_config(), changes=changes)
        except SyncAbort as error:
            print(f'ABORTED: {error}', file=sys.stderr)
            return 1
        finally:
            col.close()
    print(render_report(plan, applied=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
