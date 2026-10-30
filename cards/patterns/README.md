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

The source contains **329 complete cards**: the **2026-10-20 replacement for review** (280 cards) plus **12 conversation-glue cards**, **2 topic-framing cards**, and **29 published-material gap cards** added at the learner’s request on 2026-10-21; 25 existing cards were also extended. On 2026-10-27, the learner approved six personal production frames; three existing Backs were enriched while preserving their Front identities.
Its [coverage catalog](american_english_production_patterns_catalog.md) maps
all 145 old notes and all 361 catalog review units to the replacement or an
explicit lexical exclusion. The local-reference audit covers all 145 Grammar in Use explanations and the 12 Cambridge Writing/Speaking chapter transcriptions, with exclusions recorded in the catalog. The source and import are ready for review;
the desktop Anki collection has not been changed. Replacing the local source
does not automatically retire old notes in Anki.

After changing a card, run from the EN directory:

```bash
python3 cards/tools/build_import.py --self-test
python3 cards/tools/build_import.py
python3 scripts/audit.py
```
