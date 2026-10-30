# AmE Preposition Deck — Inventory Audit

**Audit date:** 2026-07-30

**Scope:** Phase 1 coverage inventory and Phase 2 linguistic/classification
audit. This report does not approve the full card deck. Card authoring remains
behind the Phase 3 pilot gate.

## Result

The inventory is structurally valid and family-complete for the scope defined
in `PREPOSITION_DECK_PLAN.md`: a practical, C1-oriented American English
preposition resource, not a dictionary of every expression containing a
preposition.

The integrated manifest contains 599 reviewed rows:

| Subdeck | Proposed candidates | Excluded or rerouted | Total reviewed |
|---|---:|---:|---:|
| 01 Time | 56 | 0 | 56 |
| 02 Place | 51 | 3 | 54 |
| 03 Movement | 39 | 3 | 42 |
| 04 Abstract Relationships | 43 | 7 | 50 |
| 05 Verb + Preposition | 98 | 10 | 108 |
| 06 Adjective and Participle + Preposition | 63 | 4 | 67 |
| 07 Noun + Preposition | 63 | 4 | 67 |
| 08 Fixed and Multiword Expressions | 76 | 18 | 94 |
| 09 No Preposition and Grammar Traps | 58 | 3 | 61 |
| **Total** | **547** | **52** | **599** |

The 547 proposed candidates currently break down as:

| Card type | Candidate decisions |
|---|---:|
| Chunk | 197 |
| Context | 81 |
| Contrast | 206 |
| Repair | 63 |

These are inventory decisions, not a promised final card count. A candidate
can still be revised or excluded during card-level review, and no proposed row
is exported.

## Audit method

1. Four independently owned inventory slices covered all nine subdecks.
2. Each slice was reviewed by someone other than its author.
3. The primary integration pass applied the review findings to the slice
   sources rather than merely recording suggestions.
4. `build_preposition_coverage.py` validated the schema, IDs, routing values,
   statuses, and deterministic merged output.
5. A cross-manifest duplicate scan found no duplicate proposed item IDs or
   target forms. The only repeated construction is the intentional pair
   `relate to + noun`, split into connection and identification senses.

Detailed review reports:

- `inventory-reviews/01-03.md`
- `inventory-reviews/04-05.md`
- `inventory-reviews/06-07.md`
- `inventory-reviews/08-09.md`

## Material corrections applied

### Duplicate and false-contrast cleanup

- Combined paired decisions such as `for + V-ing` versus infinitival `to`,
  `made of` versus `made from`, `under control` versus `in control of`, and
  `result in` versus `result from`.
- Removed separate cards that would have treated accepted AmE alternatives as
  wrong, including `different than`, `based off`, `disappointed in/with`,
  `angry with/at`, and overlapping `protect from/against` uses.
- Merged or rerouted duplicate direct-object traps such as `enter`, `reach`,
  and `approach`.

### Classification repairs

- Routed time, direct-object, and infinitival-`to` decisions to their single
  designated homes.
- Moved `answer for` and exchange patterns to Verb + Preposition.
- Split overloaded lexical rows such as `provide for`, `account for`,
  `relate to`, and `withdraw from` into independently testable senses.

### Scope control

- Excluded broad labels that cannot yield a fair retrieval card, such as a
  generic `preposition + noun phrase` item and an unrestricted
  `in + condition/state` item.
- Pruned a low-value formal-expression tail where neutral, more reusable
  alternatives already cover the practical decision.
- Kept useful formal patterns only when they contribute a distinct,
  reusable construction.

### Missing coverage added

- `by + means of transport`
- `reimburse + person for + expense`
- `answer for + action/behavior`
- passive-cause and relationship patterns `caused by` and `related to`
- source-side noun patterns `effect of + cause` and `impact of + cause`
- concrete infinitival-`to` traps after `opportunity` and `ability`

## Open constraints for card authoring

There are no blocking inventory-level questions. Card authors must still
resolve the following at the individual Front/Back level:

- provide enough context when more than one preposition could otherwise fit;
- state `Also OK:` when the actual Front permits a normal alternative;
- do not convert register preferences into grammar rules;
- do not make sentence-final prepositions look ungrammatical;
- use source-versus-target context for `effect/impact on` and `of`;
- use variable-versus-amount context for `increase/decrease in` and `of`; and
- retain the lexical anchor when varying examples for transfer.

If a card cannot meet those constraints, its manifest item remains proposed or
is excluded. Uncertainty must never be exported as a forced single answer.

## Validation

Commands:

```bash
python3 EN/cards/tools/build_preposition_coverage.py
python3 EN/cards/tools/build_preposition_coverage.py --check
```

Latest result:

```text
coverage inventory is valid and current
rows: 599
statuses:
  excluded: 52
  proposed: 547
```

The deterministic merged artifact is `coverage.tsv`. The four slice files in
`inventory-slices/` remain the editable sources.

## Current gate

Phase 1 and Phase 2 are complete. The learner accepted `PILOT.md` on
2026-07-30, so the module-level style gate is complete. The later scope
expansion supersedes standalone production: do not build a preposition-only
TSV while `CONNECTION_DECK_PLAN.md` awaits approval.

## Phase 3 pilot review

The 24-card pilot was independently reviewed in three read-only passes:

1. natural contemporary AmE, meaning, register, and alternative answers;
2. one-decision card design, manifest mapping, and answer leakage; and
3. vocabulary level, formatting, explanation depth, and gate coverage.

The review found no blocking issue. Before learner delivery, the pilot was
revised to:

- make `in/at the office` an explicit viewpoint decision while acknowledging
  overlap;
- remove ambiguous `above/over` and `across/through` contexts;
- replace answer-revealing chunk Fronts;
- make the agent-versus-instrument contrast explicit;
- label `different from` as the neutral default while accepting common AmE
  `different than`; and
- broaden the documented `from ... perspective` construction without
  revealing the answer on the Front.

A targeted re-review confirmed that the first correction pass resolved the
original findings and identified one remaining numerical alternative,
`over the target`.

The learner's subsequent review established a stricter requirement:
acknowledging several alternatives on the Back is not enough when the Front
still makes self-grading subjective. The plan now requires a closed-answer
test that includes competing vocabulary and constructions, not only competing
prepositions. The overlapping `at/in the office` and
`above/over/higher than the target` pilot prompts were removed and replaced
with closed place contexts, so the numerical alternative no longer appears in
the pilot.

Structural pilot validation:

```text
cards: 24
subdecks: 9 of 9
card types: chunk 6, context 3, contrast 12, repair 3
duplicate item IDs: 0
manifest mapping errors: 0
```

## Learner acceptance

The learner confirmed that the original retrieval-oriented card forms are
appropriate and specifically favored well-constructed contrast cards such as
`despite + complement` versus `although + clause`. The accepted behavior is:

- compare genuinely confusable structures on one coherent card;
- put normal secondary answers such as `in spite of` under `Also OK:`;
- preserve objective self-grading by closing the answer space;
- retain `chunk` for lexical combinations and `context` for productive
  situational rules; and
- select card types from the knowledge, not from a target ratio.

The accepted concession pilot was tightened from `Although receiving ...`,
which could also form a reduced clause, to the closed noun-phrase contrast
`Despite strong objections ...` versus
`Although several residents objected ...`.

## Scope expansion after pilot acceptance

On 2026-07-30 the learner clarified that the ultimate target is not
prepositions alone. The desired resource teaches how words, phrases, and
clauses connect, including the marker and complement shape that follows an
anchor. `Although + V-ing`, verb complement choices, relative reductions, and
other connection systems therefore belong in the larger resource.

The preposition inventory and pilot remain valid reviewed inputs, but
standalone bulk generation is permanently superseded. The learner accepted
`CONNECTION_DECK_PLAN.md` on 2026-07-30; it defines one parent deck with nine
broader subdecks and how these rows migrate without duplication.
