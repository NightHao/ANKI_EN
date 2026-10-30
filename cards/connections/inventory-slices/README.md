# Connection Patterns Inventory Slice Contract

These TSV files are parallel authoring inputs for
`EN/cards/connections/coverage.tsv`.

## Files and ownership

- `01-02.tsv`: Prepositions and Verb Patterns
- `03-04.tsv`: Adjective/Participle and Noun Patterns
- `05-07.tsv`: Clause Linkers, Relative Clauses, and Non-finite Clauses
- `08-09.tsv`: Coordination/Parallelism and Comparison/Degree/Result

Only the assigned owner edits a slice during an authoring pass. The primary
agent owns integration and the master manifest.

## Exact TSV header

```text
item_id	subdeck	topic	anchor	connector_or_marker	complement_shape	target_pattern	meaning_or_distinction	confusables	card_type	register	source_file	card_id	status	evidence_note	notes
```

Every row has exactly 16 tab-separated fields.

## Allowed values

### `subdeck`

- `01 Prepositions and Prepositional Phrases`
- `02 Verb Patterns`
- `03 Adjective and Participle Patterns`
- `04 Noun Patterns`
- `05 Conjunctions and Clause Linkers`
- `06 Relative and Noun-Modifying Clauses`
- `07 Non-finite and Reduced Clauses`
- `08 Coordination and Parallelism`
- `09 Comparison, Degree, and Result Patterns`

### `complement_shape`

Use one or more semicolon-separated canonical values:

- `NP`
- `finite-clause`
- `that-clause`
- `wh-clause`
- `to-inf`
- `bare-inf`
- `V-ing-clause`
- `past-participle-clause`
- `AdjP`
- `PP`
- `predicative-NP`
- `relative-clause`
- `reduced-relative`
- `parallel-unit`
- `zero`

### `card_type`

- `chunk`
- `context`
- `contrast`
- `repair`

### `status`

- `proposed`
- `validated`
- `excluded`
- `deferred`

During initial inventory authoring, use `proposed`, `excluded`, or `deferred`
and leave `card_id` blank. A row changes to `validated` only after its canonical
card and independent linguistic audit exist; at that point `card_id` is
required. All other statuses keep `card_id` blank.

### `source_file`

- `01-prepositions.md`
- `02-verb-patterns.md`
- `03-adjective-participle-patterns.md`
- `04-noun-patterns.md`
- `05-conjunction-clause-linkers.md`
- `06-relative-noun-modifying-clauses.md`
- `07-nonfinite-reduced-clauses.md`
- `08-coordination-parallelism.md`
- `09-comparison-degree-result.md`

## Authoring requirements

1. Read `EN/cards/CONNECTION_DECK_PLAN.md` completely.
2. Read `EN/cards/prepositions/PILOT.md` as the visible style baseline.
3. Migrate relevant rows from `EN/cards/prepositions/coverage.tsv`; do not
   silently discard reviewed items.
4. Add missing families required by the master plan.
5. Give every atomic decision exactly one home.
6. Keep one coherent contrast in one row.
7. Record the anchor, marker, and exact complement shape.
8. Use contemporary natural AmE.
9. Preserve accepted alternatives in `confusables` or `notes`; do not create a
   false exclusive rule.
10. Leave `card_id` blank during inventory authoring.
11. Keep all viable rows `proposed` until their cards pass independent audit.
12. Exclude dictionary-like, rare, duplicated, or untestable rows visibly.
13. Do not add tags, batches, frequency fields, or suspension state.
14. You are not alone in the workspace. Do not revert or rewrite files owned
    by another agent.

## ID prefixes

- `PREP-`
- `VERB-`
- `ADJ-`
- `NOUN-`
- `LINK-`
- `REL-`
- `NF-`
- `COORD-`
- `CMP-`

Existing stable IDs may be preserved when the decision survives unchanged and
already follows an unambiguous prefix. Otherwise create a master ID and record
the old ID in `notes`.

## Closed-answer preparation

Inventory rows are not cards, but their notes must make future objective
self-grading possible. Record:

- the nearest common alternative;
- whether it is also correct;
- the context needed to distinguish meanings;
- any non-prepositional completion that could fit a blank;
- the understood subject of a reduced clause; and
- whether a contrast must use a noun phrase, finite clause, or another
  specific complement to remain closed.
