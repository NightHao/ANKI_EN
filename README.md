# EN card authoring

Source of truth for the learner's EN Anki decks. Agents follow
[AGENTS.md](AGENTS.md) (and [CLAUDE.md](CLAUDE.md)); [design.md](design.md)
records the original Oct 27 handoff.

## Daily workflow

1. **Add or edit cards** from any computer: ask an agent, which edits the
   family's sources, runs its builder, and pushes to this private repo.
   GitHub Actions checks every push (it never contacts AnkiWeb).
2. **Deliver them to Anki** on a computer with Anki and this repo: choose
   **Tools > Update EN cards from GitHub**. The add-on syncs with AnkiWeb, runs
   `git pull`, previews the changes, applies them as one undoable step, and
   syncs again. Phones then receive them through a normal Anki sync.

Note types and deck trees per family are declared in
[cards/anki_sync.json](cards/anki_sync.json). Updates keep review history; the
add-on never deletes, renames, or moves notes.

### Installing the add-on on another computer

Clone this repo, then link the add-on into Anki's add-on folder and restart Anki:

```bash
# macOS; on Windows use %APPDATA%\Anki2\addons21
ln -s "$PWD/anki_addon/en_cards_sync" ~/Library/Application\ Support/Anki2/addons21/en_cards_sync
```

Sync Anki with AnkiWeb before the first update on that computer.

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
| EN::Vocabulary | 336 | [CSV](cards/vocabulary/exports/anki_import.csv) |
| EN::Patterns | 330 | [TSV](cards/patterns/anki-import.tsv) |
| EN::Connection Patterns | 603 | [TSV](cards/connections/anki-import.tsv) |

Counts as of 2026-10-30, after reconciling with AnkiWeb (all 1,269 notes
matched exactly). [The Oct 27 batch](handoff/last_card_update/updated_cards.html)
is kept as handoff evidence.

## What this transfers

Card sources, build scripts, templates, authoring rules, correction tracking,
lightweight text references, and recent implementation evidence are included.
Old backups, caches, machine configuration, credentials, PDF/audio/image media,
and the actual Anki collection/review history are excluded. Use AnkiWeb sync or
your own Anki collection backup for study progress.

The original broad grammar audit is known to fail on legacy chapter paths and
some reference-link handling. Card-specific checks are available separately.
Textbook media links may require original media that is not in this bundle.
