# Connection Patterns Deck — Final Audit

**Audit date:** 2026-07-30  
**Result:** Complete for the defined C1-oriented contemporary AmE
connection-pattern resource.

This is a system-complete, item-selective learning resource. It does not claim
to contain every possible complement or collocation of every English word.

## Final result

The final inventory contains **685 reviewed decisions**:

| Status | Count |
|---|---:|
| Validated and exported | 600 |
| Excluded or rerouted with evidence | 85 |
| Proposed | 0 |
| Deferred | 0 |

The final import contains exactly **600 cards**:

| Subdeck | Cards |
|---|---:|
| 01 Prepositions and Prepositional Phrases | 85 |
| 02 Verb Patterns | 129 |
| 03 Adjective and Participle Patterns | 70 |
| 04 Noun Patterns | 59 |
| 05 Conjunctions and Clause Linkers | 76 |
| 06 Relative and Noun-Modifying Clauses | 41 |
| 07 Non-finite and Reduced Clauses | 29 |
| 08 Coordination and Parallelism | 42 |
| 09 Comparison, Degree, and Result Patterns | 69 |
| **Total** | **600** |

Validated card types:

| Type | Cards |
|---|---:|
| Chunk | 104 |
| Context | 198 |
| Contrast | 245 |
| Repair | 53 |

The type distribution is a consequence of the reviewed knowledge decisions,
not a target ratio.

## Audit method

Every viable inventory row was reconciled with exactly one source card and one
numeric subdeck. Module-level semantic audits are preserved in
[`card-reviews/`](card-reviews/), including final or targeted acceptance
evidence for Modules 01–09.

The integrated pass checked:

- practical family coverage against `CONNECTION_DECK_PLAN.md`;
- one-home routing across all nine modules;
- duplicate item IDs, card IDs, item-to-card mappings, and visible Fronts;
- repeated target patterns that might conceal semantic duplicates;
- complement-shape and card-type agreement;
- answer-space closure under each exact printed Front;
- accepted contemporary AmE alternatives and register labels;
- understood subjects in purpose, relative, and participial reductions;
- correct and incorrect repair prompts;
- unresolved proposed/deferred work;
- deterministic coverage and import generation; and
- final TSV structure and deck routing.

The four repeated viable `target_pattern` strings are intentional:

- causal `as` (`LINK-004`) versus temporal simultaneous `as` (`LINK-041`);
- polysemy recognition for finite **while** (`LINK-025`) versus the
  **when/while** point-versus-duration decision (`LINK-040`);
- same-agent accompanying V-ing (`NF-009`) versus a result entailed by the
  preceding clause (`NF-010`); and
- productive whole-clause **which** (`REL-041`) versus repair of
  non-defining **that** (`REL-042`).

## Integrated transfer audit

The transfer pass changed topics, subjects, objects, and complement content
while preserving the controlling decision. It covered all nine subdecks and
included:

- time, place, abstract-relation, and complement-shape preposition choices;
- verb-selected zero, prepositional, infinitive, V-ing, finite-clause,
  object-control, particle-placement, and reporting frames;
- adjective and noun anchors with alternative complement shapes;
- finite versus reduced linker clauses, including predicative NPs and the
  bounded formal `even though + AdjP` construction;
- defining/non-defining reference, object omission, preposition placement,
  noun-head reduction, and AdjP/PP noun postmodification;
- shared-subject, perfect, passive, explicit-subject, and dangling
  participial constructions;
- coordination scope, correlative placement, parallel units, and agreement
  boundaries; and
- comparison standards, ratios, count/mass quantity, degree-result
  infinitives, and accepted pragmatic overlap.

No transfer probe required a new family, reciprocal duplicate, or unresolved
exception after the final repair passes.

## Material corrections in the final integration

- Module 01 closed its three residual month-boundary, duration, and
  above/over alternatives.
- Module 03 replaced the spelling-memory cue for **likely to / liable to**
  with a semantic probability-versus-risk choice.
- Module 04 retired reciprocal noun-pattern cards and finished at 59 cards.
- Module 05 finished at 76 cards after merging reciprocal decisions, adding
  `while/if + predicative NP`, and retaining one evidence-bounded formal
  `even though + AdjP` card.
- Module 06 merged two exact duplicate decisions and added one AdjP and one PP
  noun-postmodifier card, leaving 41 cards.
- Modules 07 and 08 received new full card audits and bounded lexical or
  structural prompts where synonym guessing had remained possible.
- Module 09 isolated `too much`, `too many`, and `enough` decisions; closed
  the `compared with/to` item; and narrowed duplicate countability teaching.
- The promotion tool now canonicalizes multi-valued complement shapes before
  writing `coverage.tsv`; an idempotent second promotion completes with zero
  changes and a clean final-state check.
- Single-source lint now treats its card list as an intentional subset after
  global promotion, while full and final builds still require every validated
  inventory item. This prevents unrelated validated modules from being
  misreported as missing during `--lint-source`.

These revisions produce the final total of 600; no module was padded or
trimmed to reach a round number.

## Final artifacts

- [`coverage.tsv`](coverage.tsv) — merged reviewed inventory
- [`anki-import.tsv`](anki-import.tsv) — deterministic three-column Anki
  import with Deck, Front, and Back
- [`README.md`](README.md) — maintenance and import workflow
- [`card-reviews/`](card-reviews/) — module-level semantic review evidence

All 600 source cards and viable inventory rows are `validated`. Only validated
cards enter the import file.
