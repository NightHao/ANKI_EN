# EN Anki cards

Source of truth for three English Anki decks, and the rules agents follow when
teaching and correcting the learner's English. **Agents: read
[AGENTS.md](AGENTS.md) first** (`CLAUDE.md` simply loads it).

| Deck | Notes | What it teaches |
| --- | ---: | --- |
| `EN::01 Patterns` | 336 | Reusable sentence frames for speaking and writing |
| `EN::02 Vocabulary` | 402 | Words and expressions, with meanings, examples, patterns, and contrast groups |
| `EN::03 Connection Patterns` | 603 | Prepositions, complements, and linkers, in nine subdecks |

Counts as of 2026-11-10; `python3 scripts/check_cards.py` prints the current ones.


## Preferred Anki deck order and migration

```text
EN
├── 01 Patterns
├── 02 Vocabulary
└── 03 Connection Patterns
    ├── 01 Prepositions and Prepositional Phrases
    ├── 02 Verb Patterns
    └── ...seven remaining numbered subdecks (unchanged)
```

| Legacy root | Current root |
| --- | --- |
| `EN::Patterns` | `EN::01 Patterns` |
| `EN::Vocabulary` | `EN::02 Vocabulary` |
| `EN::Connection Patterns` | `EN::03 Connection Patterns` |

The numeric deck names, **not** the order of `families` in
`cards/anki_sync.json`, control their display order. All nine Connection
Patterns child names and IDs are preserved by Anki's parent-deck rename.

The work PC already uses the numbered deck names and has synced them. That
exception applies only to that machine: another computer may have received
the new names through ordinary Anki sync, or may still have the legacy names.
The add-on checks the actual collection: if only the old name exists, it
previews an in-place native deck rename; if only the new name exists, no rename
is needed; if both exist, it stops for manual resolution. New installations
create the new names. No review settings, card identities, or histories are
reset. Updates run only inside the official Anki client after approval.

The `EN_Vocabulary` note `lead to / result in / end up / turn out`
intentionally remains in `EN::01 Patterns`, rather than the Vocabulary deck.
Automatic correction tracking remains disabled.

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

Original preposition diagrams in Patterns are transferred as Anki media when you update the deck.

Edited cards keep their review history. Renames, merges, and removals that you
approved are recorded in `cards/anki_changes.json` and applied by the add-on,
so old cards never need deleting by hand.

## Layout

```text
AGENTS.md                 instructions for agents (teaching rules + card workflow)
cards/
  vocabulary/             EN::02 Vocabulary: master CSV, updater, templates, export
  patterns/               EN::01 Patterns: cards.md source and export
  connections/            EN::03 Connection Patterns: nine sources, inventory, export
  corrections/            tracked English mistakes (not a deck)
  tools/                  pattern and connection builders
  anki_sync.json          note type, fields, and deck for each family
  anki_changes.json       this commit's renames and removals
  semantic/               reviewed meaning groups and generated card lookup
anki_addon/en_cards_sync/ the Anki add-on
scripts/
  check_cards.py          all card checks (run before every push)
  find_cards.py           semantic owner lookup and literal search across decks
  build_semantic_index.py rebuild/check the generated semantic index
  anki/                   planner used by the add-on, and its tests
```

## Setting up a computer

Requires Python 3.10+ and git. The card tools use only the standard library.

```bash
git clone https://github.com/NightHao/ANKI_EN.git && cd ANKI_EN
python3 scripts/check_cards.py
python3 scripts/find_cards.py "look up to" "the flip side"
python3 scripts/find_cards.py --meaning "respect admiration"
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
