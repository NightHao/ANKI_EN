# EN Anki cards

Source of truth for three English Anki decks, and the rules agents follow when
teaching and correcting the learner's English. **Agents: read
[AGENTS.md](AGENTS.md) first** (`CLAUDE.md` simply loads it).

| Deck | Notes | What it teaches |
| --- | ---: | --- |
| `EN::Vocabulary` | 336 | Words and expressions, with meanings, examples, patterns, and contrast groups |
| `EN::Patterns` | 330 | Reusable sentence frames for speaking and writing |
| `EN::Connection Patterns` | 603 | Prepositions, complements, and linkers, in nine subdecks |

Counts as of 2026-10-30; `python3 scripts/check_cards.py` prints the current ones.

## How it works

1. **Ask an agent to add or change cards.** It explains the items, checks
   existing cards with `scripts/find_cards.py`, proposes merges or new cards,
   and writes only after you approve. Then it rebuilds the imports, runs
   `scripts/check_cards.py`, commits, and pushes. GitHub Actions repeats the
   checks.
2. **In Anki, choose Tools > Update EN cards from GitHub.** The add-on syncs
   with AnkiWeb, pulls this repo, shows a summary, applies it as one undoable
   step (Edit > Undo), and syncs again. Phones get the changes on their next
   sync.

Edited cards keep their review history. Renames, merges, and removals that you
approved are recorded in `cards/anki_changes.json` and applied by the add-on,
so old cards never need deleting by hand.

## Layout

```text
AGENTS.md                 instructions for agents (teaching rules + card workflow)
cards/
  vocabulary/             EN::Vocabulary: master CSV, updater, templates, export
  patterns/               EN::Patterns: cards.md source and export
  connections/            EN::Connection Patterns: nine sources, inventory, export
  corrections/            tracked English mistakes (not a deck)
  tools/                  pattern and connection builders
  anki_sync.json          note type, fields, and deck for each family
  anki_changes.json       this commit's renames and removals
anki_addon/en_cards_sync/ the Anki add-on
scripts/
  check_cards.py          all card checks (run before every push)
  find_cards.py           search existing cards across all decks
  anki/                   planner used by the add-on, and its tests
```

## Setting up a computer

Requires Python 3.10+ and git. The card tools use only the standard library.

```bash
git clone https://github.com/NightHao/ANKI_EN.git && cd ANKI_EN
python3 scripts/check_cards.py
```

To update Anki from this computer, link the add-on and restart Anki:

```bash
# macOS (Windows: %APPDATA%\Anki2\addons21)
ln -s "$PWD/anki_addon/en_cards_sync" ~/Library/Application\ Support/Anki2/addons21/en_cards_sync
```

Sync Anki with AnkiWeb before the first update on a new computer, and choose
**Download from AnkiWeb** if Anki asks which side to keep.

To run the planner tests locally: `pip install anki==26.9.3`, then
`python3 scripts/anki/test_anki_sync.py`.
