#!/usr/bin/env python3
"""Check the portable EN sources and imports, optionally rebuilding derived files."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def run(*arguments: str) -> None:
    print('\n> ' + ' '.join((Path(sys.executable).name, *arguments)), flush=True)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    subprocess.run([sys.executable, *arguments], cwd=ROOT, env=environment, check=True)


def check_snapshot() -> None:
    manifest = json.loads((ROOT / 'handoff/package_manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest['files'].items():
        relative = Path(name)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError(f'Invalid manifest path: {name}')
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f'Missing or invalid snapshot file: {name}')
        content = path.read_bytes()
        if len(content) != expected['bytes'] or hashlib.sha256(content).hexdigest() != expected['sha256']:
            raise ValueError(f'Snapshot differs: {name}; omit --check-snapshot after intentional edits.')
    print(f'Snapshot hashes verified: {len(manifest["files"])} files.', flush=True)


def check_patterns() -> None:
    path = ROOT / 'cards/tools/build_import.py'
    spec = importlib.util.spec_from_file_location('en_handoff_patterns', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    cards = module.parse_cards(module.SOURCE.read_text(encoding='utf-8'))
    selected = module.parse_pattern_selection(module.PATTERN_SELECTION.read_text(encoding='utf-8'))
    module.validate_pattern_selection(cards, selected)
    connection_sources = '\n'.join(
        file.read_text(encoding='utf-8')
        for file in sorted(module.CONNECTIONS_DIR.glob('[0-9][0-9]-*.md'))
    )
    module.validate_example_uniqueness(cards, connection_sources)
    if module.OUTPUT.read_text(encoding='utf-8') != module.build_tsv(cards):
        raise ValueError('Pattern import is stale. Rebuild before reporting completion.')
    print(f'Pattern sources and import agree: {len(cards)} notes.', flush=True)


def export_count(relative: str, delimiter: str) -> int:
    with (ROOT / relative).open(encoding='utf-8', newline='') as stream:
        return sum(1 for row in csv.reader((line for line in stream if not line.startswith('#')), delimiter=delimiter) if row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-snapshot', action='store_true', help='Verify original bundle hashes before editing.')
    parser.add_argument('--rebuild', action='store_true', help='Regenerate derived imports and coverage before validation.')
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        raise ValueError('Python 3.10 or newer is required.')
    if args.check_snapshot:
        check_snapshot()
    if args.rebuild:
        run('cards/vocabulary/scripts/update_vocabulary.py', 'rebuild')
        run('cards/tools/build_import.py')
        run('cards/tools/build_connection_coverage.py')
        run('cards/tools/build_connection_import.py', '--final')
    run('cards/vocabulary/scripts/update_vocabulary.py', 'validate')
    check_patterns()
    for arguments in [
        ('cards/tools/build_import.py', '--self-test'),
        ('cards/tools/build_connection_coverage.py', '--check'),
        ('cards/tools/promote_connection_cards.py', '--check'),
        ('cards/tools/build_connection_import.py', '--final', '--check'),
        ('cards/tools/build_connection_import.py', '--self-test'),
        ('cards/corrections/scripts/update_corrections.py', 'validate'),
        ('cards/corrections/scripts/update_corrections.py', 'self-test'),
        ('-m', 'unittest', 'discover', '-s', 'cards/vocabulary/scripts', '-p', 'test_grouped_vocabulary.py'),
    ]:
        run(*arguments)
    counts = {
        'vocabulary': export_count('cards/vocabulary/exports/anki_import.csv', ','),
        'patterns': export_count('cards/patterns/anki-import.tsv', '\t'),
        'connections': export_count('cards/connections/anki-import.tsv', '\t'),
    }
    print('\nAll card checks passed: ' + json.dumps(counts, sort_keys=True), flush=True)
    print('Anki app import, review history, cloud connections, and the legacy grammar audit were not tested.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(1)
