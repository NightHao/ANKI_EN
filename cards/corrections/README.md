# Persistent Correction Tracking

This directory is the shared staging system for English problems corrected in
conversation. It lets any AI working in `EN/` preserve evidence across chats
without turning every mistake into an Anki card.

The correction registry is **not an Anki deck**. It records and consolidates
production problems. A card can be added to an existing card family only after
the learner has seen the complete proposed card and explicitly approved it.

## Core guarantees

1. Answer the learner's actual question before discussing their English.
2. Follow the correction-selection rules in `AGENTS.md`; logging does not give
   permission to correct every minor issue.
3. Store one entry per reusable root problem, not one entry per sentence.
4. Record correction evidence automatically. Do not ask for approval merely to
   record or merge an entry in this registry.
5. Never create, edit, or export an Anki card automatically.
6. Preview the complete proposed card and wait for explicit approval before
   changing any card source or generated import file.
7. Route approved content into an existing card family. Do not build a separate
   correction deck.

Automatic correction tracking was approved by the learner on 2026-09-15.

## The three classifications

### `CORRECT_ONLY`

Use when the learner benefits from the immediate correction but spaced
repetition is unlikely to justify its cost.

Typical cases:

- an isolated typo or spelling slip;
- capitalization or punctuation that does not represent a broader weakness;
- a sentence-specific repair;
- an error the learner immediately understands and repairs; or
- a low-value distinction for the learner's goals.

`CORRECT_ONLY` entries remain in the registry so a later recurrence can be
merged and reclassified. They never enter the card workflow directly.

### `TRACK`

Use when the correction may reveal a productive knowledge gap, but there is not
yet enough evidence to justify a card.

Strong signals:

- the pattern is common and broadly reusable;
- the learner understood the explanation but has not demonstrated delayed
  recall;
- the same root problem may explain multiple surface errors; or
- another independent occurrence would materially strengthen the case for a
  card.

This is the normal default for a first meaningful grammar, collocation, or
vocabulary-usage problem.

### `CARD_CANDIDATE`

Use when the problem deserves a card preview. Several of these should normally
be true:

- it recurred in an independent context or after a delay;
- the learner failed a later retrieval attempt;
- it changes meaning or seriously affects clarity;
- it is useful in conversation, IELTS, or professional communication;
- it can be generalized across at least several realistic situations;
- one clear retrieval decision can test it; and
- no existing card already teaches the same decision.

Do not promote mechanically at a fixed encounter count. A repeated typo can
remain `CORRECT_ONLY`, while a high-value meaning reversal may become a
`CARD_CANDIDATE` after one encounter.

## What to record

Record genuine corrections of the learner's own English. In an ordinary
response, this normally means the same one to three high-impact corrections
selected for teaching.

For a deep writing review, correct every meaningful problem in the response but
record at most the three most reusable root problems. The registry is a
long-term activation layer, not a transcript of every edit.

Do not record:

- quoted or transcribed source language;
- standard British English preserved from a source;
- casual abbreviations such as `u`, `sth`, or `ppl` when they are acceptable in
  context;
- optional alternative wording;
- an incorrect exercise answer when the learner's English expression itself is
  natural;
- a word requested only for explanation or comparison, unless the learner also
  misused it; or
- every typo from a long text.

## Canonical root problems

The `pattern_key` is the durable identity used for merging. Make it the
smallest reusable pattern or contrast that explains the error.

Good keys:

- `modal + base verb`
- `before + V-ing / before + subject + verb`
- `the same + noun`
- `substitute A for B / replace B with A`
- `find out vs realize`

Bad keys:

- the learner's complete original sentence;
- `grammar mistake`;
- `wrong vocabulary`;
- a date or lesson number; or
- a new key for each modal, tense, or example sentence covered by the same
  underlying rule.

Before recording, inspect the registry for equivalent wording:

```bash
python3 cards/corrections/scripts/update_corrections.py list
```

The maintenance script also normalizes capitalization, whitespace, apostrophes,
and spacing around `+` and `/`, but semantic deduplication remains the AI's
responsibility.

## Master data

The canonical data file is:

```text
cards/corrections/data/correction_master.json
```

Each entry stores:

- a human-readable and normalized pattern key;
- classification, error type, and possible destination;
- a short summary, reusable rule, and classification reason;
- corrected-occurrence and successful-use counts;
- first-seen, last-seen, and last-success dates;
- sources;
- at most the three most recent distinct correction examples;
- at most the three most recent distinct successful examples; and
- the approval-gated card state and final card reference, if any.

Example lists are capped so the registry grows by reusable problems rather than
by an unlimited transcript of conversations. Counts continue increasing even
after older examples rotate out.

Do not edit the master JSON directly. Use the maintenance script so merging,
normalization, state transitions, and validation remain consistent.

## Recording a correction

Prepare a temporary JSON object or list of objects with this shape:

```json
{
  "pattern_key": "modal + base verb",
  "category": "TRACK",
  "error_type": "VERB_FORM",
  "target": "PATTERN",
  "summary": "Use the base form after a modal verb.",
  "rule": "can/could/may/might/will/would/should/must + base verb",
  "classification_reason": "Common productive pattern; first meaningful occurrence.",
  "original": "that might also leads to",
  "corrected": "that might also lead to",
  "source": "direct user conversation",
  "seen_date": "2026-09-15"
}
```

Then run:

```bash
python3 cards/corrections/scripts/update_corrections.py record --input /tmp/correction-record.json
```

Supported `error_type` values are:

```text
ARTICLE, COLLOCATION, GRAMMAR, MEANING, PREPOSITION, PUNCTUATION, REGISTER,
SPELLING, STRUCTURE, VERB_FORM, VOCABULARY, WORD_FORM, OTHER
```

Supported targets are:

```text
NONE, UNDECIDED, VOCABULARY, PATTERN, CONNECTION
```

Use `UNDECIDED` when the eventual destination needs content review. Conflicting
specific targets merge back to `UNDECIDED` rather than silently selecting one.
The script rejects a card preview until the target has been resolved to
`VOCABULARY`, `PATTERN`, or `CONNECTION`.

Recording the same normalized key increments `encounter_count`, preserves the
earliest date, updates the latest date, merges sources, and retains the three
most recent distinct examples. A new record may raise the classification from
`CORRECT_ONLY` to `TRACK` or `CARD_CANDIDATE`; routine recording never silently
demotes an entry.

## Recording successful use

When the learner correctly uses a tracked pattern in the requested follow-up
practice, record the evidence:

```bash
python3 cards/corrections/scripts/update_corrections.py success \
  --key "modal + base verb" \
  --example "The system might reduce unnecessary reviews." \
  --source "targeted practice"
```

Prefer delayed or spontaneous successful use as stronger evidence than copying
an example immediately after the explanation. Success evidence informs later
classification; it does not automatically delete or demote an entry.

## Reviewing classification

Classification requires judgment, so it is changed explicitly:

```bash
python3 cards/corrections/scripts/update_corrections.py classify \
  --key "modal + base verb" \
  --category CARD_CANDIDATE \
  --target PATTERN \
  --reason "The problem recurred across independent contexts and remains difficult."
```

Useful review commands:

```bash
python3 cards/corrections/scripts/update_corrections.py list --category TRACK
python3 cards/corrections/scripts/update_corrections.py list --category CARD_CANDIDATE
python3 cards/corrections/scripts/update_corrections.py list --format json
python3 cards/corrections/scripts/update_corrections.py validate
```

## Reclassifying or deleting a basic record

When the learner says a tracked problem is too basic, first distinguish two
intentions:

- **Stop considering it for a card:** reclassify it as `CORRECT_ONLY`. This is
  normally preferable because the compact record preserves recurrence evidence
  without creating Anki reviews.
- **Remove the tracking record entirely:** delete it only after the learner
  explicitly identifies the record to remove.

To reclassify:

```bash
python3 cards/corrections/scripts/update_corrections.py classify \
  --key "the exact pattern key" \
  --category CORRECT_ONLY \
  --target NONE \
  --reason "The learner said this item is too basic to track for a card."
```

To delete one exact record:

```bash
python3 cards/corrections/scripts/update_corrections.py delete \
  --key "the exact pattern key" \
  --confirm-key "the exact pattern key"
```

Resolve the exact key with `list` before deletion. The repeated confirmation
key prevents a broad or accidental delete. Never infer a target from an
ambiguous phrase such as “delete that one.”

Deletion removes the record and its recurrence evidence. If the same problem
appears later, automatic tracking may create it again as a new occurrence.

The script refuses to delete a record whose card status is `ADDED`. Deleting a
registry record does not delete an Anki card; review the linked card through its
own card-family workflow first.

## Approval-gated card lifecycle

Classification and card approval are separate. `CARD_CANDIDATE` means “prepare
a preview,” not “write a card.”

The enforced lifecycle is:

```text
NONE -> PREVIEWED -> APPROVED -> ADDED
          |
          +-> DECLINED -> PREVIEWED
```

The actual allowed transitions are:

- `NONE` → `PREVIEWED`
- `PREVIEWED` → `APPROVED` or `DECLINED`
- `DECLINED` → `PREVIEWED`
- `APPROVED` → `ADDED`

After authoring the complete card preview in the response, record:

```bash
python3 cards/corrections/scripts/update_corrections.py card-status \
  --key "modal + base verb" \
  --status PREVIEWED
```

Only after the learner explicitly approves that preview:

```bash
python3 cards/corrections/scripts/update_corrections.py card-status \
  --key "modal + base verb" \
  --status APPROVED
```

Then follow the destination card family's complete authoring, deduplication,
build, and validation workflow. After successful addition and validation:

```bash
python3 cards/corrections/scripts/update_corrections.py card-status \
  --key "modal + base verb" \
  --status ADDED \
  --card-ref "cards/patterns/cards.md#modal-base-verb"
```

`ADDED` requires a durable `card_ref`. The script rejects skipped lifecycle
steps, including `NONE` → `APPROVED` and `PREVIEWED` → `ADDED`.

## Routing approved candidates

### `VOCABULARY`

Read `cards/vocabulary/CARD_AUTHORING.md` in full. Check the canonical headword
and existing master entry. Preview the full vocabulary card, wait for explicit
approval, upsert the approved data, rebuild the export, and validate. A usage
mistake involving an existing word updates that one headword; it does not
create a second error-specific vocabulary card.

### `PATTERN`

Read `cards/CARD_AUTHORING.md`. Search `cards/patterns/cards.md` for the same or
an equivalent production pattern. Preview the complete two-field result, wait
for explicit approval, update or add the source, and run:

```bash
python3 cards/tools/build_import.py
```

### `CONNECTION`

Read `cards/CONNECTION_DECK_PLAN.md` and `cards/connections/README.md` before
reviewing or changing anything. Use this target only when the correction belongs
to that deck's defined connection knowledge; do not route unrelated grammar or
spontaneous-speech content there.

### `NONE` and `UNDECIDED`

`NONE` means no Anki destination is appropriate. `UNDECIDED` means routing must
be reviewed before a card preview.

## Validation and self-test

Run both commands after changing this system's code, schema, or master data:

```bash
python3 cards/corrections/scripts/update_corrections.py validate
python3 cards/corrections/scripts/update_corrections.py self-test
```

The isolated self-test covers normalization and merging, example caps,
successful-use evidence, classification, persistence, the card-approval
lifecycle, and guarded deletion. It never writes to the real master file.

## Initial state and backfilling

The registry begins empty on 2026-09-15. Do not retroactively mine prior chats
or populate historical corrections unless the learner explicitly requests a
backfill. Begin automatic recording with new genuine corrections after this
system is installed.
