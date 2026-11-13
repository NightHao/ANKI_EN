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

**Minimize repeated Front variants.** Fronts contain the indispensable
retrieval pattern(s), not every grammatical or phrase variant. For example,
one `can't help` Front can teach `can't help + V-ing` and
`can't help but + base verb` on the Back. `The flip side is that` and
`On the flip side` can be demonstrated on one contrast card without adding
two separate Front entries. Keep the complement shapes explicit on the Back.
Group communicative jobs rather than merely similar spellings; avoid combining
different meaning boundaries solely to minimize card count. Search the
semantic index and read existing owner cards in full before editing.

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

Follow [`patterns/BACK_LAYOUT.md`](patterns/BACK_LAYOUT.md), the learner's
approved default organization for every general pattern card:

1. For a grouped card, one short shared meaning, purpose, or comparison.
2. One block for each complete Front group, in Front order.
3. In each block: the pattern, its own meaning/usage and useful complement
   structure, then its own natural examples. Keep these elements together.
4. Prefer examples in the same situation when the forms express comparable
   meanings. Say explicitly when more than one choice is valid. Do not force
   identical situations on forms with different communicative jobs.

Single-pattern cards use one block and normally two or three examples.
Grouped cards need at least one example per group and two overall; add only
examples that teach an additional form or boundary. Do not use an example
count to omit a Front group. A grouped layout does not change an ordinary
card into an overview or authorize new content, Front renames, or mergers.

Do not add Card Type, Quick Answer, Supplement, Common Trap, Notes, or practice
exercises. The note still has only Front and Back. The operation-based grammar
exception below retains complete transformations and conditions.

## Reviewed grouped overview cards

The user approved a second narrow exception on 2026-09-07 for compact overview
cards that organize an already reviewed semantic family, such as common ways
to describe position, distance, or movement. These cards provide a mental map
across related expressions; they do not replace the atomic retrieval decisions
in `EN::03 Connection Patterns`.

An overview card still has exactly two Anki fields. Its Front lists the distinct **core** retrieval expressions directly
(not each inflection or same-meaning variation), and its Back gives a concise organizing
explanation followed by enough natural examples to demonstrate every
expression on the Front at least once. Unlike an ordinary production card, an
overview card is not limited to two or three examples. Do not add examples
that merely repeat a form already demonstrated.

Each expression remains visible in its own answer-block heading. Do not
repeat the full Front above the Back or gather examples into a separate bank.
Use the grouped source format in `patterns/BACK_LAYOUT.md` for overview cards too.

Use this exception only after the user has reviewed the complete grouped card.
Mark it with `<!-- overview-card -->` immediately below the Front heading:

```markdown
## `on the left/right · at the top/bottom · in the middle/center`

<!-- overview-card -->

<!-- grouped-layout -->

Describe general positions on a map or diagram.

### `on the left/right`

Locate something horizontally within the map or space.

- The entrance is on the left, and the exit is on the right.

### `at the top/bottom`

Identify the upper or lower area.

- The title is at the top, and the scale is at the bottom.

### `in the middle/center`

Identify a central area.

- The garden is in the middle, with a fountain in the center.
```

Do not use overview cards to copy arbitrary sections of the connection deck,
create extra repetition, or combine unrelated language. The grouped Front
must express one coherent communicative domain, and every listed expression
must earn its place through a distinct usage or contrast.

## Reviewed operation-based grammar cards

The user explicitly approved a narrow exception for grammar cards grouped by
the visible editing operation a learner performs. These cards remain in
`EN::01 Patterns` and still have only Front and Back fields, but they are not
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
and `**bold text**`. It escapes other HTML. Production/overview cards use the per-pattern blocks described above.
Grammar cards retain their existing numbered decisions and full examples.

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
production/overview card using the `<!-- grouped-layout -->` marker and
`###` code-span headings matching the complete Front groups in order. Retain
`<!-- overview-card -->` when already applicable. See the complete source
examples and validation contract in `patterns/BACK_LAYOUT.md`. Legacy flat
cards remain readable by the builder for compatibility; they are not the
default for new or revised cards.

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
- every structured card has a non-empty shared explanation and section
  headings matching every complete Front group in order;
- each section has its own usage explanation and at least one example, with
  at least two examples overall;
- semantic review confirms examples belong to their sections, matched cases
  preserve meaning, and important variants/boundaries are retained;
- every marked grammar card has a non-empty Back and no raw tabs or nested
  level-two headings;
- no unexpected level-two headings are present;
- every output row has Deck, Front, and Back columns.

The EN Cards Sync add-on delivers the import to Anki (Basic note type). The
first TSV column is an Anki Deck directive column; the note itself has only
Front and Back.

## Optional visual diagrams on reviewed overview cards

A reviewed `<!-- overview-card -->` can reference original repository-owned SVG
assets stored under `cards/patterns/media/`. Insert each directive immediately
after the overview marker:

```markdown
<!-- overview-card -->
<!-- diagram: en-prepositions-location-v1.svg -->
```

The builder validates filenames and emits a responsive `<img>` tag on the
Back, preserving the two-field Basic note. On the next desktop Anki update, the
sync engine copies referenced diagrams into Anki's media collection before
changing notes. The ordinary Anki sync sends the media to other devices.
Use unique versioned filenames to avoid stale or conflicting graphics.
Diagrams complement, not replace, accurate usage rules and natural examples.

## Reviewed presentation — 2026-11-12

The learner approved a left-aligned Vocabulary-style presentation for
Patterns, with separated Front lines and responsive light/dark styling.
The final Back organization is specified in `patterns/BACK_LAYOUT.md`:
shared idea, then each pattern with its own usage/structure and examples.
Do not repeat the aggregate Front above those blocks. Front identities and
Basic's two fields stay unchanged. Scope the HTML/CSS under `patterns/anki/`
to Patterns; Connection Patterns and other Basic cards retain their appearance.

### Approved visual revision — 2026-11-12

Display separate patterns in lightly shaded, rounded blocks with comfortable
spacing and balanced wrapping. Use a uniform font size, weight, and color
within each pattern; grammatical placeholders such as `clause`, `noun`,
and `V-ing` inherit the surrounding text style. Do not shrink placeholders
or reduce individual groups just because a card contains more patterns.
Fronts use 26px on desktop and 24px on phones; answer-block headings use
21px throughout. Keep the complete pattern text at a uniform size. Keep this presentation scoped to Patterns, retain dark-mode
contrast, and preserve note content, identities, and review history.
