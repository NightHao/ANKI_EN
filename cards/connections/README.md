# Connection Patterns Deck

This directory is the source of truth for the two-field Anki deck
`EN::Connection Patterns`. Its learning target, scope boundary, nine-subdeck
taxonomy, and card-format rules are defined in
[`../CONNECTION_DECK_PLAN.md`](../CONNECTION_DECK_PLAN.md).

## Learner-facing sources

The nine numbered Markdown files contain the actual Fronts and Backs:

1. `01-prepositions.md`
2. `02-verb-patterns.md`
3. `03-adjective-participle-patterns.md`
4. `04-noun-patterns.md`
5. `05-conjunction-clause-linkers.md`
6. `06-relative-noun-modifying-clauses.md`
7. `07-nonfinite-reduced-clauses.md`
8. `08-coordination-parallelism.md`
9. `09-comparison-degree-result.md`

`anki-import.tsv` is generated. Never edit it directly.

## Inventory and status model

- `inventory-slices/*.tsv` contains the editable coverage inventory.
- `coverage.tsv` is the mechanically merged inventory.
- A new viable inventory row begins as `proposed` with an empty `card_id`.
- Its matching Markdown card also begins as `proposed`.
- `excluded` means the item was reviewed and intentionally omitted.
- `deferred` is temporary and is forbidden in a final build.
- After independent content review, the promotion tool assigns the existing
  Markdown card ID to the inventory row and changes both statuses to
  `validated`.

Record review reasoning in the commit message or the conversation; it is not
part of the Anki fields.

## Edit and validation workflow

After changing inventory rows, rebuild and check the merged inventory:

```bash
python3 cards/tools/build_connection_coverage.py
python3 cards/tools/build_connection_coverage.py --check
```

After changing one Markdown source, run its strict lint:

```bash
python3 cards/tools/build_connection_import.py \
  --lint-source 03-adjective-participle-patterns.md
```

Before promotion, independently review every proposed card for:

- one useful connection decision;
- natural contemporary American English;
- a genuinely closed Front under the exact printed sentence;
- explicit accepted alternatives rather than false exclusivity;
- accurate complement shapes and meaning distinctions; and
- overlap with existing cards or another module's one-home responsibility.

Promote only after those checks and fixes:

```bash
python3 cards/tools/promote_connection_cards.py --apply
python3 cards/tools/promote_connection_cards.py --check
```

Then build and verify the import file:

```bash
python3 cards/tools/build_connection_import.py --final
python3 cards/tools/build_connection_import.py --final --check
```

The TSV has three columns: Deck, Front, and Back. It deliberately has no tag
column. Import it with Anki's Basic note type and honor the first column as the
Deck directive.

## Adding a card after a learner question

1. Search all nine sources and `coverage.tsv` for the same decision.
2. Prefer improving the nearest existing card when it already owns the
   pattern.
3. If a real gap remains, add one inventory row to the correct module with
   `status=proposed` and an empty `card_id`.
4. Add one sequentially numbered proposed card in that module's Markdown
   source.
5. Rebuild coverage, run strict lint, and independently review the exact
   Front/Back.
6. Promote, rebuild the final TSV, and rerun both final checks.

Changing an existing Front changes the note's identity; record it in
`cards/anki_changes.json` (see `AGENTS.md`) so Anki renames the note in place.

Do not add tags, activation batches, duplicate practice cards, or scheduling
metadata. Anki owns review frequency; this directory owns the knowledge.
