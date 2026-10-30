# `EN::Vocabulary`

This directory owns the repository's American-English vocabulary-learning
system.

- [`CARD_AUTHORING.md`](CARD_AUTHORING.md) is the complete source of truth for
  classification, card content, master data, Anki templates, export, and
  validation.
- `data/vocabulary_master.csv` is the canonical vocabulary data source.
- `exports/anki_import.csv` is generated from the master data and is never
  edited manually.
- `anki/` contains the note templates and styling; the add-on copies them into
  the `EN_Vocabulary` note type.
- `scripts/update_vocabulary.py` owns updates and export generation.

The repository-level `AGENTS.md` routes every vocabulary-maintenance request to
the authoring specification. General pattern-card and connection-card rules do
not govern this card family.

## Update workflow

Write a JSON update file to `tmp/` (ignored by git; the commit records the
result), using the structure in `CARD_AUTHORING.md` section 21 and the
fields read by `row_from_record` in the updater, then run:

```bash
python3 cards/vocabulary/scripts/update_vocabulary.py upsert \
  --input tmp/vocabulary-update.json
```

The command normalizes and merges headwords, increments existing encounters,
rewrites the master CSV, rebuilds the complete Anki export, and validates both
files and the note templates. It stops without reporting success if validation
fails.

To rebuild or validate without recording a new encounter:

```bash
python3 cards/vocabulary/scripts/update_vocabulary.py rebuild
python3 cards/vocabulary/scripts/update_vocabulary.py validate
```

The update JSON stores structured senses, examples, optional semantic
relations, classification metadata, and the observed form. Use
`"replace_senses": true` only for an intentional correction that should replace
the existing sense data; otherwise genuinely new senses are merged into the
existing headword.

For an editorial correction that is not a new personal encounter, add
`--no-encounter` to the `upsert` command.

## Grouped contrast notes

Each grouped sense block has `entry_term` identifying the member word and
`part_of_speech` identifying its role. Put `common_patterns` on the first
block for that member. Put one `comparison` object on the first block of the
note: `situations` is a list of objects with `situation`, `examples`, and
`guidance`; `note` explains the overlap and useful boundaries. The renderer
escapes this content and generates the approved comparison table. CSS stacks
its rows on narrow screens. Ordinary notes retain their existing rendering.

For an explicitly approved consolidation, an update may list exact existing
headwords in `merge_from`. Prepare the grouped sense data with every retained
source sense under its correct `entry_term` before running the update. The
command refuses merges that would lose an old definition, combines source
metadata, and removes the superseded master rows.

A merge changes card identities in Anki. In the same commit, record in
`cards/anki_changes.json` a rename from the member whose review history should
carry over (usually the most-studied one) to the new grouped Term, and a
removal for each other merged member. The add-on then edits and deletes the
Anki notes accordingly; see `AGENTS.md`.
