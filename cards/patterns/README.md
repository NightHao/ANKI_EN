# `EN::Patterns`

This directory is the source of truth for the two-field Anki deck
`EN::Patterns`.

- [`cards.md`](cards.md) contains the learner-facing Fronts and Backs.
- [`PATTERN_FRAME_SELECTION.md`](PATTERN_FRAME_SELECTION.md) defines the
  reviewed high-value production-frame layer.
- [`OMISSION_GRAMMAR_CARD_SPEC.md`](OMISSION_GRAMMAR_CARD_SPEC.md) governs the
  operation-based omission and shortening cards.
- `anki-import.tsv` is generated and must not be edited directly.

The shared authoring rules are in
[`../CARD_AUTHORING.md`](../CARD_AUTHORING.md).

After changing a card, run from the repository root:

```bash
python3 cards/tools/build_import.py --self-test
python3 cards/tools/build_import.py
python3 scripts/check_cards.py
```

Changing a Front changes the note's identity; record it in
`cards/anki_changes.json` (see `AGENTS.md`).
