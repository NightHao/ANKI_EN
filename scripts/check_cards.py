#!/usr/bin/env python3
"""Check every card family: sources, generated imports, change record, and tests.

Run before every push: python3 scripts/check_cards.py  (add --rebuild to
regenerate all imports first). GitHub Actions runs the same checks.
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import subprocess
import re
from xml.etree import ElementTree
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def run(*arguments: str) -> None:
    print('\n> ' + ' '.join((Path(sys.executable).name, *arguments)), flush=True)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    subprocess.run([sys.executable, *arguments], cwd=ROOT, env=environment, check=True)


def check_patterns() -> None:
    path = ROOT / 'cards/tools/build_import.py'
    spec = importlib.util.spec_from_file_location('en_patterns_builder', path)
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


def check_pattern_diagrams() -> None:
    """Ensure each Anki image reference points to a valid owned SVG asset."""
    media = ROOT / 'cards/patterns/media'
    filenames = set()
    for path in media.glob('en-prepositions-*.svg'):
        if path.name in filenames:
            raise ValueError(f'duplicate preposition media name: {path.name}')
        filenames.add(path.name)
        root = ElementTree.parse(path).getroot()
        if root.tag != '{http://www.w3.org/2000/svg}svg':
            raise ValueError(f'not an SVG document: {path}')
    source = (ROOT / 'cards/patterns/cards.md').read_text(encoding='utf-8')
    import_text = (ROOT / 'cards/patterns/anki-import.tsv').read_text(encoding='utf-8')
    referenced = set(re.findall(r'<!-- diagram: (en-prepositions-[a-z0-9-]+\\.svg) -->', source))
    if referenced != filenames:
        raise ValueError(f'diagram inventory mismatch: referenced={referenced}, files={filenames}')
    for name in referenced:
        if f'<img src="{name}"' not in import_text:
            raise ValueError(f'Anki import does not reference diagram {name}')
    print(f'Pattern diagrams validated: {len(filenames)} SVG media files.', flush=True)


def check_change_record() -> None:
    sys.path.insert(0, str(ROOT / 'scripts/anki'))
    import exports
    changes = exports.parse_changes(exports.CHANGES.read_text(encoding='utf-8'))
    errors = exports.validate_changes(changes, exports.load_config())
    if errors:
        raise ValueError('cards/anki_changes.json is inconsistent with the exports:\n' + '\n'.join(errors))
    print(f"Change record is valid: {len(changes['renames'])} rename(s), {len(changes['removals'])} removal(s).",
          flush=True)


def export_count(relative: str, delimiter: str) -> int:
    with (ROOT / relative).open(encoding='utf-8', newline='') as stream:
        return sum(1 for row in csv.reader((line for line in stream if not line.startswith('#')), delimiter=delimiter) if row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild', action='store_true', help='Regenerate derived imports and coverage before validation.')
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        raise ValueError('Python 3.10 or newer is required.')
    if args.rebuild:
        run('cards/vocabulary/scripts/update_vocabulary.py', 'rebuild')
        run('cards/tools/build_import.py')
        run('cards/tools/build_connection_coverage.py')
        run('cards/tools/build_connection_import.py', '--final')
        run('scripts/build_semantic_index.py')
    run('cards/vocabulary/scripts/update_vocabulary.py', 'validate')
    run('scripts/build_semantic_index.py', '--check')
    run('scripts/test_semantic_index.py')
    check_patterns()
    check_pattern_diagrams()
    check_change_record()
    for arguments in [
        ('cards/tools/build_import.py', '--self-test'),
        ('cards/tools/build_connection_coverage.py', '--check'),
        ('cards/tools/promote_connection_cards.py', '--check'),
        ('cards/tools/build_connection_import.py', '--final', '--check'),
        ('cards/tools/build_connection_import.py', '--self-test'),
        ('cards/corrections/scripts/update_corrections.py', 'validate'),
        ('cards/corrections/scripts/update_corrections.py', 'self-test'),
        ('-m', 'unittest', 'discover', '-s', 'cards/vocabulary/scripts', '-p', 'test_grouped_vocabulary.py'),
        ('scripts/anki/test_change_records.py',),
    ]:
        run(*arguments)
    counts = {
        'vocabulary': export_count('cards/vocabulary/exports/anki_import.csv', ','),
        'patterns': export_count('cards/patterns/anki-import.tsv', '\t'),
        'connections': export_count('cards/connections/anki-import.tsv', '\t'),
    }
    print('\nAll card checks passed: ' + json.dumps(counts, sort_keys=True), flush=True)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'error: {error}', file=sys.stderr)
        raise SystemExit(1)
