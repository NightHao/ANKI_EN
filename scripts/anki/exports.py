"""Read the generated Anki imports, the family config, and the change record.

Standard library only, so scripts/check_cards.py can validate without Anki.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / 'cards/anki_sync.json'
CHANGES = ROOT / 'cards/anki_changes.json'
CHANGES_PATH_IN_REPO = 'cards/anki_changes.json'
EMPTY_CHANGES = {'renames': [], 'removals': []}


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
    if headers.get('separator', '').lower() == 'tab':
        # The pattern/connection builders write raw tab-separated fields.
        rows = list(csv.reader(body, delimiter='\t', quoting=csv.QUOTE_NONE))
        columns = headers['columns'].split('\t') if 'columns' in headers else ['Deck', 'Front', 'Back']
    else:
        rows = list(csv.reader(body))
        columns = headers['columns'].split(',')
    return headers, [dict(zip(columns, row, strict=True)) for row in rows if row]


def load_config(path: Path = CONFIG) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def parse_changes(text: str) -> dict:
    data = json.loads(text)
    for kind, fields in (('renames', ('family', 'from', 'to')), ('removals', ('family', 'key'))):
        for entry in data.get(kind, []):
            missing = [f for f in fields if not str(entry.get(f, '')).strip()]
            if missing:
                raise ValueError(f'{kind} entry is missing {missing}: {entry}')
    return {'renames': data.get('renames', []), 'removals': data.get('removals', [])}


def first_fields(config: dict, root: Path = ROOT) -> dict[str, set[str]]:
    """Current first-field values (note identities) per family."""
    keys = {}
    for family in config['families']:
        _headers, rows = read_export(root / family['export'])
        keys[family['name']] = {row[family['fields'][0]] for row in rows}
    return keys


def validate_changes(changes: dict, config: dict, root: Path = ROOT) -> list[str]:
    """Check the current change record against the current exports."""
    current = first_fields(config, root)
    errors = []
    renamed_to = {(r['family'], r['to']) for r in changes['renames']}
    for rename in changes['renames']:
        family = rename['family']
        if family not in current:
            errors.append(f'unknown family in rename: {family}')
            continue
        if rename['from'] == rename['to']:
            errors.append(f'[{family}] rename has identical from/to: {rename["from"][:60]}')
        if rename['from'] in current[family]:
            errors.append(f'[{family}] rename source is still a live card: {rename["from"][:60]}')
        if rename['to'] not in current[family] and not any(
                r['family'] == family and r['from'] == rename['to'] for r in changes['renames']):
            errors.append(f'[{family}] rename target is not in the export: {rename["to"][:60]}')
    for removal in changes['removals']:
        family = removal['family']
        if family not in current:
            errors.append(f'unknown family in removal: {family}')
        elif removal['key'] in current[family]:
            errors.append(f'[{family}] removal targets a card that is still in the export: {removal["key"][:60]}')
        elif (family, removal['key']) in renamed_to:
            errors.append(f'[{family}] removal targets a rename result: {removal["key"][:60]}')
    return errors


def change_records(git, last_commit: str | None, head: str) -> tuple[list[dict], str]:
    """Change records committed after last_commit up to head, oldest first.

    `git(*args, check=...)` runs git in the repo and returns a CompletedProcess.
    Without a known last commit (first run, or history rewritten), only the
    record at head is used.
    """
    known = bool(last_commit) and git('merge-base', '--is-ancestor', last_commit, head,
                                      check=False).returncode == 0
    if known:
        commits = git('log', '--reverse', '--format=%H', f'{last_commit}..{head}', '--',
                      CHANGES_PATH_IN_REPO).stdout.split()
        note = f'{len(commits)} change record(s) since {last_commit[:7]}'
    else:
        commits = [head]
        note = 'first run on this collection: using the current change record'
    records = []
    for commit in commits:
        shown = git('show', f'{commit}:{CHANGES_PATH_IN_REPO}', check=False)
        if shown.returncode == 0:
            records.append(parse_changes(shown.stdout))
    return records, note
