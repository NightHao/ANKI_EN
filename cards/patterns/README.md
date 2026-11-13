# `EN::01 Patterns`

This directory is the source of truth for the two-field Anki deck
`EN::01 Patterns`.

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

## Reviewed layout — 2026-11-12

`anki/front.html`, `anki/back.html`, and `anki/styling.css` implement the
learner-approved Vocabulary-style layout. Templates keep the Basic note type
and its existing Front/Back fields. Formatting is scoped to `EN::01 Patterns`
(and its legacy name `EN::Patterns`); other Basic cards keep their appearance.
Front text stays unchanged in the note; grouped patterns are separated only
when displayed. The original Basic appearance is retained outside this scope.

The learner-approved default Back organization is in
[`BACK_LAYOUT.md`](BACK_LAYOUT.md). Production and overview sources use
`<!-- grouped-layout -->`, with one section per complete Front group, in
order. Each section owns its usage and examples. Keep the shared introduction
short, use matched situations for actual alternatives, and do not repeat the
aggregate Front above the answer. Single-pattern cards use one block.
Grammar cards retain all existing lines, grouped visually by their existing
numbered decision. No Front, note identity, or review schedule changes.

### Approved visual revision — 2026-11-12

Display separate patterns in lightly shaded, rounded blocks with comfortable
spacing and balanced wrapping. Use a uniform font size, weight, and color
within each pattern; grammatical placeholders such as `clause`, `noun`,
and `V-ing` inherit the surrounding text style. Do not shrink placeholders
or reduce individual groups just because a card contains more patterns.
Fronts use 26px on desktop and 24px on phones; answer-block headings use
21px throughout. Keep this presentation scoped to Patterns, retain dark-mode
contrast, and preserve note content, identities, and review history.

### Reviewer lifecycle regression check

Anki resets the review page's body classes after executing template scripts.
The template applies its deck-specific class immediately and again through
Anki's `onUpdateHook`, after that reset. Keep both paths so standalone previews
and the actual reviewer behave consistently. Do not replace this check with
a static HTML screenshot: that does not exercise the reviewer's reset.

With Anki's Python environment, run:

```bash
python scripts/anki/test_pattern_presentation.py
```

This uses the installed Anki reviewer JavaScript in Qt and never opens an
Anki collection. It checks Fronts, Backs, repeated reviews, mobile widths,
dark mode, and isolation from Connection Patterns.
