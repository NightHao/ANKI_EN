# Pattern Back organization

Learner-approved default, 2026-11-12. Applies to all general Patterns cards,
including ordinary production cards, grouped overviews, and the presentation
of existing grammar decisions. Keep exactly two Anki fields: Front and Back.

## Learning organization

- **Front:** keep related expressions together, in separate shaded blocks.
  Keep the complete text within each pattern at one font size, including
  placeholders such as clause, noun, and V-ing. Formatting must not rename it.
- **Grouped Back:** begin with one short shared idea, communicative purpose,
  or organizing comparison. Then use one block per complete Front group, in
  the same order: **pattern → its own usage/structure → its own examples**.
- **Single-pattern Back:** one pattern block with its explanation and examples;
  do not repeat the same explanation as a shared introduction.
- Do not put all usage explanations in one paragraph or all examples in a
  separate bank. Do not repeat the complete Front above the answer blocks.
- For genuine alternatives, prefer matched examples in the same situation so
  changes in wording/grammar are easy to compare. State shared valid choices
  explicitly. Do not manufacture sharp distinctions between near-equivalents.
- Preserve real differences in meaning, grammar, collocation, and register.
  Do not force different communicative jobs into an identical sentence.
- Keep useful Back-only variants in their owning block. An economical Front
  does not need to enumerate every inflection or equivalent grammatical form.
- Preserve necessary usage boundaries, negative examples, and useful original
  examples. Add context to short replies so their meaning is recoverable.
- Single-pattern cards normally have two or three examples. Grouped cards
  require an example for every group and at least two overall; use more only
  for another form or meaningful boundary. Do not pad for repetition.

## Canonical source and validation

Keep existing Front text and overview markers. Add `<!-- grouped-layout -->`
below the optional `<!-- overview-card -->`. The shared introduction is
followed by one `###` code-span heading for every complete Front item split
on ` · `, in exact order. Keep slash alternatives in their owning group.
Each section has its own non-empty usage paragraph and example bullets.
Do not create overview markers solely to obtain the layout.

```markdown
## `try to + verb · try + V-ing`

<!-- grouped-layout -->

Distinguish attempting an action from testing an action as a possible method.
The meanings can overlap; neither form guarantees success.

### `try to + verb`

Emphasize the attempt to perform the action.

- I tried to restart the laptop, but it would not respond.

### `try + V-ing`

Present the action as an experiment or possible solution.

- Try restarting the laptop; that may fix it.
```

The concession example illustrates the matched-situation principle:

- Although I was tired, I finished the review.
- Despite being tired, I finished the review.
- In spite of being tired, I finished the review.

These share a message after restructuring. Although takes a complete clause;
despite/in spite of take a noun or V-ing, or the fact that + clause. Neither
despite of nor despite I was tired is the model. Keep these explanations and
examples inside the owning pattern blocks on the actual card.

The inference comparison uses one compilation situation:

- Compiling successfully does not necessarily mean the program works correctly.
- Just because the program compiles does not mean it works correctly.
- Compiling successfully does not guarantee that the program works correctly.

All three work here; the first two question an inference and the third
emphasizes lack of certainty. Do not invent a rigid difference.

## Grammar and non-Basic notes

The nine operation-based grammar cards keep the original source and all full
valid/invalid transformations, timing, voice, polarity, actor, modality, and
register boundaries. Their existing numbered decisions become visual blocks;
do not rewrite them as ordinary two-example cards. Content revisions still
require `OMISSION_GRAMMAR_CARD_SPEC.md` and its independent coverage audit.
A visual reorganization is not a claim of a new semantic completeness audit.

The `EN_Vocabulary` comparison note intentionally placed in Patterns retains
its full vocabulary comparison layout and note type. This policy does not
rewrite Vocabulary or Connection Patterns templates/content.

## Delivery checks

Run the builder self-test, builder, semantic-index rebuild, and
`python3 scripts/check_cards.py`. Keep Fronts and note/card IDs stable during
this presentation migration; no rename/removal manifest is needed when only
Backs change. Validate desktop/phone, light/dark, and pattern-to-connection
transitions using the actual Anki reviewer lifecycle. Preserve the
`onUpdateHook` class reapplication after Anki resets its body classes.

On the Lewis.yeh work PC, apply approved edits locally in Anki and use the
official client's normal sync. Do not push or require personal GitHub login.
