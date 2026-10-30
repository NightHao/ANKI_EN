# English Pattern Card Authoring Guide

These are minimal production cards. Their purpose is to make a natural English
pattern immediately available while speaking or writing. They are not grammar
reference notes and must not copy the LeetCode card shape.

## Scope of this guide

This file governs the existing direct-pattern cards in `patterns/cards.md`.

High-value frames selected from the Connection Patterns resource are governed
additionally by
[`patterns/PATTERN_FRAME_SELECTION.md`](patterns/PATTERN_FRAME_SELECTION.md).
That file defines the production-layer purpose, inclusion criteria, exclusions,
and current reviewed selection. Do not copy the whole connection deck into
`patterns/cards.md`.

The Connection Patterns knowledge deck is a separate two-field card family
organized into nine numeric subdecks. It carries exactly one retrieval decision
per card across four defined card types (`chunk`, `context`, `contrast`,
`repair`), rather than a single visible pattern. Read
[`CONNECTION_DECK_PLAN.md`](CONNECTION_DECK_PLAN.md) before any connection-deck
review or implementation. Do not force the master deck into the source format or
2–3-example constraint below.

## The two-field card

### Front

Put the reusable pattern itself on the Front.

Good:

```text
gain experience in + noun / V-ing
```

```text
The main reason + clause + is that + clause
```

```text
the first/next/last/only + noun + to-infinitive
```

Bad:

```text
When should you use this expression?
```

```text
Reduced relative clauses
```

Do not turn the Front into a question, lesson title, grammar-unit number, or
broad grammar label. Choose the smallest useful pattern: it should be specific
enough to guide production and broad enough to reuse in several realistic
situations.

### Back

The Back contains only:

1. a brief plain-English explanation of the meaning or use;
2. when useful, a separate short paragraph naming the common words that use
   the pattern;
3. an optional `Examples:` label; and
4. two or three short, natural examples.

Keep a blank line between the usage explanation, the common-words paragraph,
the `Examples:` label, and the example bullets. Do not turn those paragraphs
into extra bullet lists: ordinary cards reserve bullets for examples.

Example:

```text
Used to identify someone or something as first, next, last, or unique in
performing an action.

Common words include first, next, last, and only.

Examples:

• Amy was the first person to arrive.
• This is the last train to leave tonight.
• He was the only applicant to meet every requirement.
```

Do not add Card Type, Quick Answer, Supplement, Common Trap, Notes, exercises,
or other standard sections unless the user explicitly changes this format.

## Reviewed grouped overview cards

The user approved a second narrow exception on 2026-09-07 for compact overview
cards that organize an already reviewed semantic family, such as common ways
to describe position, distance, or movement. These cards provide a mental map
across related expressions; they do not replace the atomic retrieval decisions
in `EN::Connection Patterns`.

An overview card still has exactly two Anki fields. Its Front lists the related
reusable expressions directly, and its Back gives a concise organizing
explanation followed by enough natural examples to demonstrate every
expression on the Front at least once. Unlike an ordinary production card, an
overview card is not limited to two or three examples. Do not add examples
that merely repeat a form already demonstrated.

The builder automatically begins the generated Back with **Patterns on this
card:** followed by the complete Front. This keeps the target expressions
visible while the learner examines the explanation and examples. Do not copy
the Front manually into the editable Back in `cards.md`.

Use this exception only after the user has reviewed the complete grouped card.
Mark it with `<!-- overview-card -->` immediately below the Front heading:

```markdown
## `on the left/right · at the top/bottom · in the middle/center`

<!-- overview-card -->

Use these expressions to describe general positions on a map or diagram.

Examples:

- The entrance is on the left, and the exit is on the right.
- The title is at the top, and the scale is at the bottom.
- The garden is in the middle, with a fountain in the center.
```

Do not use overview cards to copy arbitrary sections of the connection deck,
create extra repetition, or combine unrelated language. The grouped Front
must express one coherent communicative domain, and every listed expression
must earn its place through a distinct usage or contrast.

## Reviewed operation-based grammar cards

The user explicitly approved a narrow exception for grammar cards grouped by
the visible editing operation a learner performs. These cards remain in
`EN::Patterns` and still have only Front and Back fields, but they are not
forced into the ordinary 2–3-example production-card shape. Their Fronts show
the reusable transformation pattern directly rather than using a lesson-title
question.

For omission and shortening cards, read
[`patterns/OMISSION_GRAMMAR_CARD_SPEC.md`](patterns/OMISSION_GRAMMAR_CARD_SPEC.md)
in full before reviewing or editing content. That specification owns the
nine-card inventory, cross-card ownership, completeness audit, compression
rules, and required workflow.

Use this exception only after the user has reviewed the complete card. Mark the
Back with `<!-- grammar-card -->` immediately below the Front heading:

```markdown
## `... + (that/who/whom/which/when/where/why) + subject + verb`

<!-- grammar-card -->

This card tests one operation only:

`delete one word → keep every other word unchanged`

**1**

Full original sentence.
→ Full transformed sentence.
```

For these reviewed cards:

- group content by one visible edit, not by traditional grammar names;
- make the Front show the reusable transformation pattern directly without
  claiming to cover every environment in which a particular word can
  disappear;
- put the conditions on the Back;
- use full, natural American-English examples at roughly IELTS 7 level;
- include both valid transformations and similar-looking invalid ones;
- use `→` for a valid edit and `≠` for a non-equivalent result;
- say “do not remove only ...” when another card may shorten the same phrase
  through a different operation;
- use as many examples as the operation genuinely needs instead of forcing a
  fixed count.

The grammar-card renderer accepts plain lines, blank lines, inline code spans,
and `**bold text**`. It escapes other HTML. Ordinary cards continue to require
one explanation and exactly two or three bullet examples.

## Example level

The default target is IELTS Speaking 7. Examples should reinforce useful
vocabulary as well as the pattern:

- use natural, high-value topic vocabulary and common collocations;
- when suitable, draw from IELTS themes such as education, technology,
  employment, public policy, health, and the environment;
- avoid toy-like examples when an equally clear, more useful context is
  available;
- do not insert obscure, inflated, or unnaturally formal vocabulary merely to
  sound advanced;
- keep the grammar contrast obvious: vocabulary must support the pattern, not
  distract from it.

## What counts as a useful pattern

A pattern is a good card candidate when several of these are true:

- it works in at least five realistic situations;
- native speakers commonly use it as a chunk or frame;
- it addresses a repeated production problem;
- it performs a useful function such as giving a reason, comparing options,
  expressing uncertainty, describing a trade-off, or explaining a decision.

Prefer:

- collocations: `gain experience in`, `apply for a position`;
- verb patterns: `practice + V-ing`, `avoid + V-ing`;
- sentence frames: `The main reason + clause + is that + clause`;
- communication structures: `On the one hand, ...; on the other hand, ...`;
- productive grammar constructions, when the construction itself is a reusable
  pattern.

Do not create a card for a broad label alone, such as `gerund`, `adverb`, or
`reduced relative clause`.

## Source format

`patterns/cards.md` is the canonical human-readable card source. Write each
card as:

```markdown
## `pattern shown on the Front`

One brief meaning or usage explanation.

Optional common-words paragraph.

Examples:

- First natural example.
- Second natural example.
- Optional third natural example.
```

Everything inside the level-two heading's code span is the Front. Everything
below it, up to the next level-two heading, is the Back. Keep exactly two or
three example bullets on ordinary cards. Reviewed overview cards use the
marker and example-coverage rule defined above.

Before adding a card, search `patterns/cards.md` for the same idea under nearby
wording. If the same production pattern is already present, update it rather
than adding a duplicate. Changing a Front changes the note's identity; record
it in `cards/anki_changes.json` (see `AGENTS.md`) so Anki renames the existing
note in place.

## Build the Anki import

`patterns/cards.md` is the editable source.
`patterns/anki-import.tsv` is the final file delivered to the user for Anki
import.

After every card change, run from the repository root:

```bash
python3 cards/tools/build_import.py
```

The builder validates that:

- every Front is unique;
- every ordinary card has one non-empty explanation and exactly two or three
  examples;
- every reviewed overview card has a non-empty explanation and at least two
  examples, with semantic review confirming that every Front expression is
  demonstrated, and its generated Back repeats the complete Front;
- every marked grammar card has a non-empty Back and no raw tabs or nested
  level-two headings;
- no unexpected level-two headings are present;
- every output row has Deck, Front, and Back columns.

The EN Cards Sync add-on delivers the import to Anki (Basic note type). The
first TSV column is an Anki Deck directive column; the note itself has only
Front and Back.
