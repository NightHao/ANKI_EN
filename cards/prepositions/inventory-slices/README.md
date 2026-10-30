# Preposition Inventory Slice Contract

These files are temporary Phase 1 inputs to the canonical
`../coverage.tsv`. They let several agents propose knowledge items without
editing the same file.

## Required columns

Every slice uses this exact tab-separated header:

```text
item_id	subdeck	topic	target_form	meaning_or_distinction	construction	confusables	card_type	register	source_file	card_id	status	notes
```

## Row rules

- One row represents one reusable retrieval decision.
- Use the routing precedence in `../../PREPOSITION_DECK_PLAN.md`.
- Use only the assigned numeric subdecks and source filenames.
- Use a stable item ID with the subdeck prefix.
- Keep `card_id` empty during inventory work.
- Use `proposed` for a candidate that should proceed to primary review.
- Use `excluded` only when the row records a deliberate scope exclusion.
- Do not mark slice rows `validated`; validation belongs to the integrated
  audit.
- Choose exactly one card type: `chunk`, `context`, `contrast`, or `repair`.
- Write the reusable form in `target_form`, not a complete teaching card.
- State the actual meaning or distinction in plain English.
- Put the syntactic frame or complement requirement in `construction`.
- List plausible alternatives or learner errors in `confusables`; do not
  invent a competing form merely to fill the field.
- Use `notes` for an AmE caveat, unresolved ambiguity, or concise reference
  note. Do not add frequency scores.
- Do not copy example sentences or explanatory prose from a reference.
- Do not create duplicate rows merely to increase exposure.
- Keep every physical TSV record on one line and do not place tabs inside a
  field.

## Assigned files

| Slice | Subdecks | Required source files |
|---|---|---|
| `01-03.tsv` | `01 Time`, `02 Place`, `03 Movement` | `01-time.md`, `02-place.md`, `03-movement.md` |
| `04-05.tsv` | `04 Abstract Relationships`, `05 Verb + Preposition` | `04-abstract-relationships.md`, `05-verb-preposition.md` |
| `06-07.tsv` | `06 Adjective and Participle + Preposition`, `07 Noun + Preposition` | `06-adjective-participle-preposition.md`, `07-noun-preposition.md` |
| `08-09.tsv` | `08 Fixed and Multiword Expressions`, `09 No Preposition and Grammar Traps` | `08-fixed-multiword-expressions.md`, `09-no-preposition-grammar-traps.md` |

The primary agent owns final normalization, cross-slice deduplication,
validation status, and `coverage.tsv`.
