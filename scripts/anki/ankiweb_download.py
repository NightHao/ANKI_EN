#!/usr/bin/env python3
"""Download a read-only copy of the AnkiWeb collection into a fresh local file.

This performs a full download only. It never uploads, never runs an incremental
sync, and never touches the Anki app's own profile folder.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from anki.collection import Collection
from anki.sync import SyncAuth

AUTH_PATH = Path(os.environ.get('EN_ANKI_AUTH', Path.home() / '.config/en-anki/ankiweb_auth.json'))


def load_auth() -> SyncAuth:
    """Read the sync key from ANKIWEB_HKEY (CI secret) or the local key file."""
    if os.environ.get('ANKIWEB_HKEY'):
        stored = {'hkey': os.environ['ANKIWEB_HKEY'], 'endpoint': os.environ.get('ANKIWEB_ENDPOINT', '')}
    elif AUTH_PATH.is_file():
        stored = json.loads(AUTH_PATH.read_text(encoding='utf-8'))
    else:
        raise SystemExit(f'No sync key in ANKIWEB_HKEY or {AUTH_PATH}; run scripts/anki/ankiweb_login.py first.')
    auth = SyncAuth(hkey=stored['hkey'])
    if stored.get('endpoint'):
        auth.endpoint = stored['endpoint']
    return auth


def download(output: Path, auth: SyncAuth) -> Collection:
    """Full-download the AnkiWeb collection into a new file and return it open."""
    if output.exists():
        raise SystemExit(f'Refusing to overwrite existing file: {output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    col = Collection(str(output))
    # AnkiWeb shards accounts across hosts; the status check names the right one.
    status = col.sync_status(auth)
    if status.new_endpoint:
        auth.endpoint = status.new_endpoint
    col.close_for_full_sync()
    col.full_upload_or_download(auth=auth, server_usn=None, upload=False)
    col.reopen(after_full_sync=True)
    return col


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='new .anki2 path to create')
    args = parser.parse_args()
    col = download(args.output, load_auth())
    print(f'Downloaded {col.note_count()} notes, {col.card_count()} cards to {args.output}')
    col.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
