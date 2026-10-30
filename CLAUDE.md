@AGENTS.md

## Repository workflow

This repo (private GitHub `NightHao/ANKI_EN`) is the source of truth for the EN
Anki decks. The learner's AnkiWeb collection receives changes only through the
**EN Cards Sync** add-on running inside the official Anki app.

- Run `git pull` before any card or correction work, and commit and push
  afterwards, so other computers and the add-on see the change.
- Edit only the sources each family's authoring guide names, then run that
  family's builder. Never hand-edit `anki_import.csv`, `anki-import.tsv`, or
  `coverage.tsv`. Before pushing, `python3 scripts/verify_handoff.py` must pass;
  GitHub Actions repeats it and fails if a generated import is stale.
- Note identity is note type + first field (`cards/anki_sync.json`). Editing a
  Back keeps review history. Renaming a Term or Front creates a new note and
  leaves the old one in Anki; do it only with the learner's explicit approval
  and tell them the old note must be deleted in Anki by hand.
- Never connect to AnkiWeb from a script, CI job, or agent. AnkiWeb's terms
  allow only official Anki clients; the add-on uses Anki's own sync.
- To deliver changes, tell the learner to choose **Tools > Update EN cards from
  GitHub** in Anki on a computer with this repo and the add-on installed.
