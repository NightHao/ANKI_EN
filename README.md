# EN card authoring: portable cloud handoff

Start with [design.md](design.md), then read [AGENTS.md](AGENTS.md).
This is a working source snapshot plus a proposed cloud architecture, not an
already deployed GitHub/Notion/Anki integration.

## Check the extracted package

From this `EN` directory, with Python 3.10 or newer:

```bash
python3 scripts/verify_handoff.py --check-snapshot
python3 scripts/verify_handoff.py --rebuild
```

On Windows, `py -3` may replace `python3`. No third-party Python packages are
needed for these card checks. After intentional edits, run the verifier without
`--check-snapshot`, which compares against the original archive contents.

## Current imports

| Deck | Notes | Import file |
| --- | ---: | --- |
| EN::Vocabulary | 319 | [CSV](cards/vocabulary/exports/anki_import.csv) |
| EN::Patterns | 329 | [TSV](cards/patterns/anki-import.tsv) |
| EN::Connection Patterns | 603 | [TSV](cards/connections/anki-import.tsv) |

See [the complete latest batch](handoff/last_card_update/updated_cards.html) for
the 63 additions and six revisions. The current canonical decks include all
earlier approved notes as well, not only that latest batch.

## What this transfers

Card sources, build scripts, templates, authoring rules, correction tracking,
lightweight text references, and recent implementation evidence are included.
Old backups, caches, machine configuration, credentials, PDF/audio/image media,
and the actual Anki collection/review history are excluded. Use AnkiWeb sync or
your own Anki collection backup for study progress.

The original broad grammar audit is known to fail on legacy chapter paths and
some reference-link handling. Card-specific checks are available separately.
Textbook media links may require original media that is not in this bundle.

## Continue with Codex

Ask Codex to read `AGENTS.md` and `design.md`, run the package verifier, and
help discuss or implement the next step. No repository, cloud environment,
maintenance skill, or account connection should be assumed to exist yet.
