# `EN::Patterns` Omission and Shortening Grammar Cards

This specification governs the nine operation-based grammar cards stored in
`cards.md` and exported to `EN::Patterns`. Read it in full before reviewing,
editing, or adding any card in this suite.

The ordinary tense/aspect pattern card in `cards.md` is outside this suite.

## Non-negotiable design rule

Correctness and completeness come before compression.

Never simplify only by rearranging the content already present in a card. The
existing card may already contain omissions, false generalizations, or content
owned by another card.

For every revision:

1. reconstruct the complete target rule independently of the current card;
2. check the whole nine-card suite for existing ownership;
3. classify every relevant form as valid, meaning-changing, invalid, or
   outside the practical target;
4. verify subject, time, aspect, voice, polarity, modality, clause
   environment, and register;
5. only then merge repeated explanations and examples.

Two cases may share one section only when all three are the same:

- the learner performs the same visible edit;
- the learner uses the same eligibility test;
- the edit preserves the same core meaning.

Inflectional variants such as `has/have/had` belong in one formula. Keep
separate examples only when they demonstrate different time relations or
meaning. If one shared explanation is not true for every form in a group,
rewrite the explanation or split the group.

## One knowledge point, one home

Every rule, warning, and contrast has one canonical home. Do not reteach it on
another card. Do not refer to learner-facing cards as “Card 1,” “Card 2,” and
so on: Anki does not present them in a fixed reading order.

Before adding a formula or example, search every grammar-card Back in
`cards.md`. A technically different sentence environment does not justify
duplicating the same learner decision.

## Canonical ownership

| Operation | Owns | Does not own |
| --- | --- | --- |
| One-word deletion | Optional `that` after common reporting/thinking verbs and common certainty/emotion adjectives; object `that/who/whom/which` before another subject; safe `day when`, `place where`, and `reason why` frames; a stranded preposition already at the end; direct-verb, comma, `whose`, and fronted-preposition boundaries | Removal of `be`; conversion to `V-ing`, `having`, or `to`; any edit that changes more than one word |
| Subject + finite `be` deletion | Removing a subject marker or understood subject together with `am/is/are/was/were`; noun modifiers with or without commas; `while/when/if/although`; what may remain after the noun; subject-identity boundary | `has/have/had been`; modal + `be`; ordinary active verb conversion |
| Active verb to `V-ing` | A noun performing a simple active action; the same edit after a comma; simple active verbs after `while/when`; loss of ability or requirement from `can/must + verb` | Object relatives; passive forms; perfect and perfect-progressive preservation |
| Earlier situation to a perfect participle | `has/have/had + past participle`; simple past whose earlier order is explicit; negative perfect; passive perfect; perfect progressive; same-subject requirement; formal-register warning | Simultaneous `while` clauses; ordinary current/general `V-ing`; arbitrary standalone or noun-relative clauses |
| Task, purpose, or possible action to `to + verb` | Understood actor; `for + actor + to`; passive `to be + past participle`; same/different-subject purpose; first/next/last/only; `who/what/where/when/how/whether + to`; the `why to` boundary; completed-fact boundary; required passive action | An existing `is to ...` shortened only by deleting subject + `be`; completed facts presented as purpose |
| Repeated action omission | `do/does/did`; modal, perfect, and `be` helpers; infinitival `to`; American-English possessive `have`; `too/either/so/neither`; comparisons; concise coordination; ambiguity boundary | Question-answer remnants; repeated nouns after quantities |
| Unknown-information remnant | Leaving only `who/what/where/when/why/how` after an established event; direct short answers; ambiguity boundary | Quantity-noun omission; `what/where/how + to + verb` |
| Repeated noun after a quantity | Numbers; common count-noun quantities such as `some/any/many/few/a few/several/more/most/fewer/enough/all/both/each/either/neither/none`; common mass-noun quantities such as `some/any/much/little/a little/more/most/less/enough/all/none`; `one/ones` boundary; ambiguity boundary | Repeated verb phrases; general short answers |
| Informal opening omission | Predictable opening subjects and helpers in casual American conversation, texts, and notes; register and clarity boundaries | Formal or academic writing; omission licensed by an earlier noun or clause |

## Coverage audit

For each card, build a private coverage matrix before editing:

| Axis | Questions |
| --- | --- |
| Source shape | Which full forms can legitimately produce this edit? |
| Output shape | Does the result need `V-ing`, a past participle, `being`, `having`, `to`, a helper, or no replacement? |
| Time and aspect | Is the action current, general, completed, earlier, ongoing, or simultaneous? What information disappears? |
| Voice | Does the subject perform or receive the action? |
| Polarity | Is the negative retained in the output? |
| Modality | Are ability, permission, prediction, or obligation preserved? |
| Subject identity | Who performs or receives every action after words are removed? |
| Environment | Is the form after a noun, after a comma, after a connector, or at the start of an informal utterance? |
| Meaning | Is the result truly equivalent, merely possible in some contexts, or different? |
| Naturalness | Is it normal American English at an IELTS 7 target, formal but useful, rare, or misleading? |

Do not claim completeness until every relevant axis has been checked against the
whole suite.

## Compression rules

- One card contains one visible editing operation.
- One numbered section contains one learner decision, not one tense or one
  example.
- Put alternative output shapes under the same section when their eligibility
  test and meaning are shared.
- Put a valid example and its nearest invalid lookalike under the decision they
  test.
- Keep one full sentence for every distinct output shape or meaning boundary.
- Remove examples that merely substitute a different topic, subject, or verb.
- Do not impose a fixed number of sections or examples.
- If a card exceeds five decisions, recheck whether similar decisions can be
  combined or whether ownership is wrong.

Compression must never remove a source form, output form, semantic distinction,
negative boundary, or register warning.

## Learner-facing style

- Use plain English and natural American-English examples.
- Prefer useful IELTS topics without making the vocabulary harder than the
  grammar.
- Use complete sentences.
- Use `→` for a valid transformation and `≠` for a changed or invalid result.
- Put only abstract formulas in inline code formatting. Full examples and
  explanations remain ordinary text.
- Avoid unexplained labels such as “linker,” “finite clause,” “sluicing,” or
  “predicative complement.”
- A Front shows the reusable transformation pattern directly. Parentheses may
  mark words that can disappear when the Back's conditions are satisfied. The
  Front must not claim to cover every use of a particular word.
- A Back must stand on its own and must not mention another card number.

## Required workflow

1. Read this file and `CARD_AUTHORING.md`.
2. Search the complete `cards.md` suite for the target forms.
3. Reconstruct and check the coverage matrix independently.
4. Resolve canonical ownership before writing examples.
5. Draft the complete card, then compress by learner decision.
6. Run `python3 cards/tools/build_import.py --self-test`.
7. Run `python3 cards/tools/build_import.py`.
8. Confirm every generated row has exactly Deck, Front, and Back fields.
9. Present the complete changed card or suite for learner review.
