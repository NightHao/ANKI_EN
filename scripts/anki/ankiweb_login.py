#!/usr/bin/env python3
"""Exchange an AnkiWeb email/password for a sync key and store only the key.

Run this yourself in a terminal; the password is read with getpass and is never
written anywhere. The stored key is what the Anki app itself keeps after login.
"""
from __future__ import annotations

import getpass
import json
import os
import sys
import tempfile
from pathlib import Path

from anki.collection import Collection

AUTH_PATH = Path(os.environ.get('EN_ANKI_AUTH', Path.home() / '.config/en-anki/ankiweb_auth.json'))


def main() -> int:
    username = input('AnkiWeb email: ').strip()
    password = getpass.getpass('AnkiWeb password (hidden): ')
    with tempfile.TemporaryDirectory() as scratch:
        col = Collection(str(Path(scratch) / 'login.anki2'))
        try:
            auth = col.sync_login(username=username, password=password, endpoint=None)
        except Exception as error:  # noqa: BLE001 - report the backend message as-is
            print(f'Login failed: {error}', file=sys.stderr)
            return 1
        finally:
            col.close()
    AUTH_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUTH_PATH.parent.chmod(0o700)
    descriptor = os.open(AUTH_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
        json.dump({'hkey': auth.hkey, 'endpoint': auth.endpoint}, handle)
    print(f'Login OK. Sync key saved to {AUTH_PATH} (owner-only permissions).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
