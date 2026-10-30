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
    if not AUTH_PATH.is_file():
        raise SystemExit(f'No sync key at {AUTH_PATH}; run scripts/anki/ankiweb_login.py first.')
    stored = json.loads(AUTH_PATH.read_text(encoding='utf-8'))
    auth = SyncAuth(hkey=stored['hkey'])
    if stored.get('endpoint'):
        auth.endpoint = stored['endpoint']
    return auth


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='new .anki2 path to create')
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit(f'Refusing to overwrite existing file: {args.output}')
    auth = load_auth()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    col = Collection(str(args.output))
    # AnkiWeb shards accounts across hosts; the status check names the right one.
    status = col.sync_status(auth)
    if status.new_endpoint:
        auth.endpoint = status.new_endpoint
    col.close_for_full_sync()
    col.full_upload_or_download(auth=auth, server_usn=None, upload=False)
    col.reopen(after_full_sync=True)
    print(f'Downloaded {col.note_count()} notes, {col.card_count()} cards to {args.output}')
    col.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
