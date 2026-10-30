# Vocabulary Card System Authoring Specification

This document is the source of truth for maintaining the repository's English
vocabulary-learning system and producing Anki-importable vocabulary cards.
Read it in full before every vocabulary-card update.

All relative paths in this document, such as `data/`, `exports/`, `anki/`, and
`scripts/`, are relative to `cards/vocabulary/`.

The job is not merely to create dictionary entries. The goal is to efficiently
build both:

- **active vocabulary**: words the learner should retrieve and use in speaking
  and writing;
- **receptive vocabulary**: words the learner mainly needs to recognize while
  reading and listening.

The learner is studying **modern American English**. Default to American
spelling, pronunciation, vocabulary, examples, and usage.

Prioritize learning efficiency. Do not put every unfamiliar word into Anki,
and do not overload cards with unnecessary information.

## 1. Core workflow

Use a mandatory two-stage workflow whenever the learner supplies one or more
English words, expressions, or phrases.

### Stage A: explain and propose

1. Normalize each item for analysis.
2. Check read-only whether it already exists in the master vocabulary file.
3. Explain its useful modern meanings, parts of speech, typical patterns, and
   important usage boundaries.
4. Propose `ACTIVE`, `RECEPTIVE`, or `SKIP` with a concise reason.
5. Do not update the master data or regenerate the Anki export.
6. Wait for the learner's explicit approval.

### Stage B: add after approval

After explicit approval such as `add them`, `add these`, or an equally clear
instruction:

1. Apply any classification or content adjustments the learner made.
2. Normalize each item and check for existing master entries.
3. Add or update the master vocabulary data.
4. Regenerate the Anki-importable CSV from all `ACTIVE` and `RECEPTIVE`
   entries.
5. Do not export `SKIP` entries to Anki.
6. Validate the master data, export, and templates.
7. Give the learner a short summary of what was added, updated, promoted, or
   skipped.

Do not ask routine clarification questions during either stage. Ask only when
the input is genuinely ambiguous and the intended word or expression cannot
reasonably be inferred. Once explicit approval is given, do not ask for an
additional confirmation.

## 2. Vocabulary classification

### ACTIVE

Use `ACTIVE` when the learner should eventually be able to produce the word
naturally in conversation, writing, IELTS, or professional communication.

Strong signals include:

- useful in everyday modern English;
- useful for IELTS Speaking or Writing;
- useful for professional or technical discussion;
- relatively common in educated speech or writing;
- broadly reusable across multiple contexts;
- worth being able to retrieve spontaneously.

Examples include `blatant`, `discreet`, `unilateral`, `condemn`, `apathy`,
`stave off`, and `sufficient`.

The learner's own review rule for an `ACTIVE` card is:

> Recall its meaning and make one original sentence using it.

Do not display this instruction on the card.

### RECEPTIVE

Use `RECEPTIVE` when the word is useful to understand but has lower productive
value.

Typical cases include:

- literary vocabulary;
- fantasy vocabulary;
- historical or religious vocabulary;
- relatively uncommon descriptive vocabulary;
- specialized words the learner may encounter while reading;
- concrete nouns worth recognizing;
- words native speakers commonly recognize but do not often produce
  themselves.

Examples may include `deity`, `writhe`, `filial`, `cardinal`, and `bloodlust`.
A `RECEPTIVE` card still goes into Anki, but recognition is sufficient.

### SKIP

Use `SKIP` when deliberate spaced review would probably not justify the review
cost.

Typical cases include:

- extremely rare vocabulary;
- archaic vocabulary;
- obsolete meanings;
- highly specialized terminology irrelevant to the learner's goals;
- one-off fantasy terminology;
- proper nouns unless educationally important;
- uncommon variants where learning the standard form is sufficient.

`SKIP` does not mean that an item is bad English. It means that the agent
explains it when encountered and records it, but Anki does not repeatedly
review it. Keep `SKIP` entries in the master file so repeated encounters can be
tracked.

## 3. Personal encounter frequency

General corpus frequency is only one signal. Track how often the learner
personally encounters an item.

Every time an existing item is submitted:

- increment `EncounterCount`;
- update `LastSeen`;
- merge any genuinely new sense or context;
- do not create a duplicate card.

Repeated encounters should influence classification. A repeatedly encountered
`SKIP` item may become `RECEPTIVE`; a `RECEPTIVE` item relevant to the
learner's speaking or professional life may become `ACTIVE`. Do not promote
mechanically at a fixed threshold. Treat encounter count as evidence alongside
usefulness.

An explicit instruction such as `make this ACTIVE` or `this only needs to be
RECEPTIVE` overrides automatic classification.

## 4. Frequency and usefulness

Never classify by raw frequency alone. Evaluate at least:

- general English frequency;
- daily-conversation relevance;
- IELTS relevance;
- professional-English relevance;
- fantasy or literary relevance;
- personal encounter count.

Use a trustworthy local frequency resource such as `wordfreq` when available.
If exact corpus frequency is unavailable, use qualitative labels, do not
invent numeric frequency values, and mark the source as an estimate.

Allowed qualitative bands are:

- `VERY_COMMON`
- `COMMON`
- `MODERATELY_COMMON`
- `UNCOMMON`
- `RARE`
- `SPECIALIZED`

Store these internally; do not display them on cards.

## 5. One headword equals one Anki card; explicit contrast-group exception

This is the default design rule. Do not create separate cards merely because a word
has several meanings, several parts of speech, or homographic meanings.
Organize all retained meanings inside one learner-dictionary-style card.

For example, `light` may contain noun, adjective, and verb meanings on one
card. `Cardinal` may contain the senior Catholic official, the bird, and the
adjective meaning fundamental or very important on one card.

### Learner-requested contrast cards

When the learner explicitly requests a group of terms as one contrast card
(including terms grouped in parentheses with that instruction), preserve the
group as one note. This is an exception to the single-headword rule, not a
reason to combine every set of similar words automatically.

Use the same layout as a normal vocabulary card:

- Front: the grouped terms, with clearly associated parts of speech and
  American pronunciations, audio, and priority. Do not use a comparison quiz,
  fill-in-the-blank task, or definition question instead of the normal header.
- Back: repeat the header and give each term its normal compact dictionary
  information: useful meanings grouped by part of speech, natural examples,
  useful Common patterns, and the required synonym/antonym sections or honest
  fallback messages.
- Add a concise **Difference** note after the individual entries. Explain the
  actual meaning, grammar, collocation, or register boundaries and when to
  choose each expression. Use a short matched example when helpful. State
  overlap or interchangeability where it exists; do not invent absolute
  distinctions.

When terms are near synonyms, lead with their overlap and show natural
alternatives together. Do not require the learner to distinguish them in
contexts where either works. Prioritize proper use in everyday American
English: practical patterns, suitable contexts, and genuine usage boundaries.
Explain a difference only when it helps the learner choose or construct a
sentence; avoid fine distinctions that add confusion without productive value.

Use this learner-approved Back order for contrast cards: normal header;
individual definitions and sense examples; everyday situations with matched
natural sentences; concise overlap/usage boundaries; Common patterns;
synonym/antonym information. A compact table may use Situation, Natural
sentences, and What to notice columns. Lead each comparison with a concrete
situation, show both alternatives when both work, and identify the practical
construction or meaning difference when it matters. Keep pronunciation and
the other normal vocabulary fields. Do not turn the Front into a quiz or hide
the useful comparison inside a long distinction paragraph.

Use canonical forms for each member of the grouped `Term`, with a stable
separator such as ` / `, and keep pronunciation labels unambiguous. Check both
the group and its members for existing coverage before proposing a write.
Reuse or merge existing material where appropriate; do not automatically add
duplicate standalone cards for all group members or delete existing cards.
The normal Stage A/Stage B approval boundary still applies.

## 6. Meaning selection

Do not reproduce every dictionary sense. Include:

1. current common meanings;
2. reasonably useful modern meanings;
3. any meaning the learner actually encountered.

Exclude archaic, obsolete, extremely technical, and extremely rare historical
senses by default unless the learner encountered the sense or it is necessary
to understand the word. A card should resemble a compact learner's dictionary,
not an exhaustive historical dictionary.

## 7. Organization by part of speech

On the Back:

1. group meanings by part of speech;
2. use uppercase section headings;
3. number meanings within each part of speech.

Use this structure:

```text
NOUN

1. definition
   example

2. definition
   example

ADJECTIVE

1. definition
   example

VERB

1. definition
   example
```

Do not mix meanings from different parts of speech.

## 8. Definitions

Definitions must be concise, understandable to an upper-intermediate or
advanced learner, written in English, based on modern American usage, and
specific enough to distinguish the sense from similar words.

Do not write unnecessarily academic dictionary definitions. Do not include
Chinese translations unless explicitly requested.

## 9. Example sentences

Each included sense should normally have one high-quality example sentence.
The sentence must:

- sound natural in modern American English;
- demonstrate the exact sense;
- demonstrate a typical context or collocation when possible;
- be short enough to scan quickly;
- avoid unnecessarily difficult vocabulary.

The example should teach common usage. For `conspicuous`, for example:

> There was a conspicuous absence of security.

Do not create artificial textbook sentences merely to contain the target word.

### Useful common patterns

Include short, visible **Common patterns** notes on the Back whenever they
help the learner produce everyday American English or useful professional
English. This applies from initial authoring to later revisions, for both
normal and contrast cards. Do not rely on examples alone when the complement
shape or collocation is important and easy to miss.

Choose only practical, reusable guidance: `deprive someone of something`,
`be accountable for something / to someone`, or `end up + V-ing`. Associate
patterns with the relevant sense, and demonstrate them in natural examples.
Explain a usage restriction briefly when needed. Use the existing sense
`usage_note` field for visible notes where supported; do not store useful
patterns only in internal metadata.

Do not force a pattern section for every word, list every possible combination,
or pad the card with generic grammar. A short useful collocation belongs here;
an exhaustive collocation list does not. Pattern notes remain part of the
vocabulary card and do not automatically authorize separate pattern cards.

## 10. Synonyms

Synonyms are a required visible study field on every polished `ACTIVE` and
`RECEPTIVE` card. Include one to three useful, sense-specific synonyms when a
linguistically defensible candidate exists. Rank them from closest or most
useful to less directly equivalent, and label interchangeability explicitly.
Do not treat a related word as interchangeable merely to satisfy this rule.

Allowed relationship labels are:

### INTERCHANGEABLE

The synonym can replace the target in most normal contexts for this sense
without materially changing meaning. Use this label cautiously.

### NEAR-INTERCHANGEABLE

The synonym is often replaceable but differs in nuance, register, collocation,
emphasis, or grammatical behavior.

### RELATED

The synonym expresses a similar idea but is not normally a direct substitute.

Example for `blatant`:

1. `flagrant` — `NEAR-INTERCHANGEABLE`; similarly strongly negative and often
   used for violations or offenses.
2. `obvious` — `RELATED`; easy to notice but lacking the shameless or offensive
   implication of `blatant`.

The first synonym should normally be the closest useful alternative. A
multi-sense card does not need synonyms under every sense, but the card as a
whole must display a Synonyms section. If no retained sense has a genuine
synonym, display `No useful synonym for this word.` rather than omitting the
section or inventing a false synonym.

## 11. Antonyms

Antonyms are a required visible study field on every polished `ACTIVE` and
`RECEPTIVE` card. Include one or two sense-specific antonyms when a
linguistically defensible direct or contextual opposite exists. Antonyms may
differ by sense: `heavy` is an antonym of `light` meaning not heavy, whereas
`dark` is an antonym of `light` meaning pale in color.

Allowed labels include `DIRECT OPPOSITE` and `CONTEXTUAL OPPOSITE`. A
multi-sense card does not need antonyms under every sense, but the card as a
whole must display an Antonyms section. If no retained sense has a genuine
antonym, display `No useful antonym for this word.` Never manufacture antonyms
for concrete nouns such as `sparrow`, `pope`, or `Colosseum`.

## 12. No pictures

Do not add images, create an image field, or download images. Images are
outside the current design.

## 13. American English

Default to modern American spelling, IPA, examples, vocabulary, and register
judgments.

When the learner encounters a British spelling such as `pretence`, normalize
the primary learning form to `pretense` and record the encountered form in
master metadata. When useful, add a short Back note such as `BrE: pretence`.
Do not make British English the default.

## 14. Pronunciation and IPA

IPA belongs on both Front and Back. Use American pronunciation. When all major
meanings and parts of speech share a pronunciation, show one IPA line.

When pronunciation changes by part of speech, show the relevant pronunciations
separately. For example:

```text
record

noun: /ˈrɛkərd/
verb: /rɪˈkɔrd/
```

Do not imply that a heteronym has only one pronunciation.

## 15. Audio

Use Anki's built-in text-to-speech. Do not generate MP3 files or add audio file
paths to the CSV. Use American-English TTS with `en_US`, available on both
sides of the card:

```html
{{tts en_US:TTS_Text}}
```

For ordinary words, `TTS_Text` normally equals `Term`. When pronunciation
changes by grammatical role, create a minimal disambiguating string, such as
`a record. to record.` Keep TTS text minimal; its purpose is pronunciation,
not listening-comprehension training.

## 16. Front card design

The Front must display only:

1. `Term`
2. part or parts of speech
3. IPA
4. audio
5. the `ACTIVE` or `RECEPTIVE` label

Do not display definitions, examples, synonyms, antonyms, frequency, IELTS
relevance, source, encounter count, or review instructions.

Conceptual example:

```text
conspicuous

adjective

/kənˈspɪkjuəs/ [audio]

ACTIVE
```

## 17. Front visual hierarchy

Each element must have a distinct font size, visual weight, and color role.

### Term

- 44px;
- bold;
- strongest visual element;
- dark neutral in light mode;
- near-white in dark mode.

### Part of speech

- 15px;
- italic;
- muted purple.

### IPA

- 19px;
- medium weight;
- blue.

### Audio

- positioned next to the pronunciation;
- visually associated with IPA;
- use the same blue color family when practical.

### ACTIVE badge

- 12px;
- uppercase;
- bold;
- letter-spaced;
- warm orange or amber;
- visually stronger than `RECEPTIVE`.

### RECEPTIVE badge

- 12px;
- uppercase;
- bold;
- letter-spaced;
- cool slate or blue-gray;
- less visually demanding than `ACTIVE`.

Use typography and shape as well as color so the distinction does not depend
only on color.

## 18. Back card design

Repeat the same compact header: term, parts of speech, IPA, audio, and priority
badge. Then display the compact dictionary information.

Example:

```text
CARDINAL

noun · adjective

/ˈkɑrdənəl/ [audio]

RECEPTIVE

NOUN

1. A senior official in the Roman Catholic Church.

   The cardinals gathered to elect a new pope.

2. A small North American bird, whose male is usually bright red.

   A cardinal landed on the fence.

ADJECTIVE

1. Extremely important or fundamental.

   Trust is a cardinal principle of the profession.

   Synonyms:

   1. fundamental — NEAR-INTERCHANGEABLE
   2. essential — RELATED; emphasizes necessity
   3. major — RELATED; broader and less precise

   Antonyms:

   1. minor — CONTEXTUAL OPPOSITE
   2. secondary — CONTEXTUAL OPPOSITE
```

Include useful Common patterns notes as specified in section 9 and a
Difference note for learner-requested contrast cards as specified in section
5. Do not add unnecessary explanatory sections.

## 19. Information excluded from Anki cards

The following may be useful internally but must not clutter repeated reviews:

- raw corpus frequency;
- frequency source;
- daily-conversation relevance;
- IELTS relevance;
- professional relevance;
- fantasy or literary relevance;
- encounter count;
- first-seen and last-seen dates;
- source;
- classification reasoning;
- original context;
- exhaustive collocation lists beyond useful Common patterns notes;
- exhaustive grammar pattern lists beyond useful Common patterns notes;
- long usage-boundary essays.

Store the excluded information only in master data. This exclusion does not
apply to concise Common patterns or contrast-card Difference notes.

## 20. Master data architecture

Maintain `data/vocabulary_master.csv` as the source of truth with UTF-8
encoding.

Use these columns:

```text
Term
NormalizedTerm
ObservedForms
Priority
PartsOfSpeech
PronunciationHTML
TTS_Text
SensesJSON
FrequencySource
FrequencyValue
FrequencyBand
DailyConversationRelevance
IELTSRelevance
ProfessionalRelevance
FantasyLiteraryRelevance
EncounterCount
FirstSeen
LastSeen
Sources
IncludeInAnki
ClassificationReason
```

Use Python's standard CSV writer or another robust CSV library. Never manually
concatenate CSV rows. Correctly quote commas, quotation marks, line breaks, and
cells containing JSON.

## 21. `SensesJSON` structure

Store structured meaning information in `SensesJSON`:

```json
[
  {
    "part_of_speech": "adjective",
    "senses": [
      {
        "definition": "easy to notice because it clearly stands out",
        "example": "His bright red jacket made him conspicuous in the crowd.",
        "synonyms": [
          {
            "term": "noticeable",
            "rank": 1,
            "relationship": "NEAR-INTERCHANGEABLE",
            "note": "usually less emphatic"
          }
        ],
        "antonyms": [
          {
            "term": "inconspicuous",
            "rank": 1,
            "relationship": "DIRECT OPPOSITE",
            "note": ""
          }
        ]
      }
    ]
  }
]
```

Do not add fake placeholder objects to empty synonym or antonym arrays. Use
empty arrays when necessary internally; the Back renderer supplies the
required `No useful synonym for this word.` or `No useful antonym for this
word.` message.

## 22. Anki export architecture

For grouped contrast notes, sense blocks additionally use `entry_term` to
identify the member word. Use `common_patterns` on that member's first block
and one `comparison` object per note, containing a `note` and `situations`
list with `situation`, `examples`, and `guidance` strings. These are structured
fields rendered as escaped HTML, not raw HTML stored in a definition or an
example. See `README.md` for approved merge operations. Grouped blocks are
merged by member term plus part of speech so different members' senses cannot
be accidentally combined.

Regenerate `exports/anki_import.csv` after every vocabulary update. Never
append indefinitely. Rebuild from current master data so classification
changes are reflected, old values do not remain stale, promotions and
demotions are handled cleanly, and duplicate rows do not accumulate.

Export only `ACTIVE` and `RECEPTIVE`; never export `SKIP`.

## 23. Anki CSV fields

Use these visible or import fields:

```text
Term
Priority
PartsOfSpeech
PronunciationHTML
TTS_Text
BackHTML
Tags
```

`Term` must be the first field so an existing headword can be matched and
updated instead of duplicated. One headword normally corresponds to one Anki
note; an explicitly requested contrast group uses its stable grouped `Term`
as the note's identity (section 5).
Generate valid HTML in `BackHTML` and use Anki-compatible UTF-8 text import.

When useful, add Anki import headers such as:

```text
#separator:Comma
#html:true
#notetype:English Vocabulary
#deck:EN::Vocabulary
#columns:Term,Priority,PartsOfSpeech,PronunciationHTML,TTS_Text,BackHTML,Tags
```

Verify that the produced file remains valid for Anki import.

## 24. Normalization and duplicate handling

Before adding an entry:

- lowercase for comparison;
- trim whitespace;
- normalize repeated spaces;
- normalize obvious punctuation differences;
- identify the lemma or base form;
- normalize American spelling when appropriate.

The visible `Term` must always use the canonical dictionary form:

- verbs use the base form, not a past-tense, participle, or third-person form;
- countable nouns normally use the singular unless the lexical item is
  conventionally plural;
- adjectives use the uninflected base degree;
- fixed expressions use their canonical lexical form.

Example sentences may use any tense, number, comparison, or other inflected
form that is natural in context. Preserve the submitted form in
`ObservedForms`.

Examples:

```text
writhing
→ writhe

stave sth off
→ stave off

pretence
→ pretense
```

Keep every encountered form in `ObservedForms`. Do not merge different lexical
expressions incorrectly: `light` and `light up` are separate entries.

When the headword already exists:

- merge useful new senses;
- update observed forms;
- increment encounter count;
- update source metadata and `LastSeen`;
- reconsider priority when justified.

Never duplicate a headword merely because the learner encountered another
part of speech or meaning.

## 25. Tags

Generate useful, predictable, machine-friendly Anki tags without displaying
them on the card. Examples:

```text
priority::active
priority::receptive
pos::noun
pos::verb
domain::general
domain::fantasy
domain::professional
```

## 26. Front template

Create `anki/front.html` with this conceptual structure:

```html
<div class="vocab-header">
  <div class="term">{{Term}}</div>

  <div class="pos">
    {{PartsOfSpeech}}
  </div>

  <div class="pronunciation-row">
    <span class="ipa">{{PronunciationHTML}}</span>
    <span class="audio">{{tts en_US:TTS_Text}}</span>
  </div>

  <div class="priority {{Priority}}">
    {{Priority}}
  </div>
</div>
```

If Anki's template engine requires adjustments, preserve the intended visual
and behavioral design instead of blindly copying syntax that does not work.

## 27. Back template

Create `anki/back.html`. Repeat the header instead of relying on a layout that
removes or changes pronunciation audio:

```html
<div class="vocab-header">
  <div class="term">{{Term}}</div>

  <div class="pos">
    {{PartsOfSpeech}}
  </div>

  <div class="pronunciation-row">
    <span class="ipa">{{PronunciationHTML}}</span>
    <span class="audio">{{tts en_US:TTS_Text}}</span>
  </div>

  <div class="priority {{Priority}}">
    {{Priority}}
  </div>
</div>

<div class="answer">
  {{BackHTML}}
</div>
```

## 28. Styling

Create `anki/styling.css` using system fonts only. Do not require external font
files. Start with this styling:

```css
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  text-align: left;
  background: #ffffff;
  color: #1f2937;
  padding: 24px;
  line-height: 1.5;
}

.term {
  font-size: 44px;
  line-height: 1.1;
  font-weight: 750;
  color: #111827;
}

.pos {
  margin-top: 6px;
  font-size: 15px;
  font-style: italic;
  color: #7c3aed;
}

.pronunciation-row {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ipa {
  font-size: 19px;
  font-weight: 500;
  color: #2563eb;
}

.priority {
  display: inline-block;
  margin-top: 14px;
  padding: 4px 9px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.priority.ACTIVE {
  color: #ffffff;
  background: #d97706;
}

.priority.RECEPTIVE {
  color: #ffffff;
  background: #64748b;
}

.answer {
  margin-top: 28px;
}

.pos-heading {
  margin-top: 28px;
  margin-bottom: 12px;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #6b7280;
}

.sense {
  margin-bottom: 22px;
}

.definition {
  font-size: 18px;
  font-weight: 500;
}

.example {
  margin-top: 8px;
  margin-left: 12px;
  font-size: 16px;
  font-style: italic;
  color: #4b5563;
}

.semantic-heading {
  margin-top: 10px;
  font-size: 13px;
  font-weight: 700;
  color: #6b7280;
}

.semantic-item {
  margin-top: 4px;
  font-size: 15px;
}

.relation {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.nightMode.card {
  background: #111827;
  color: #e5e7eb;
}

.nightMode .term {
  color: #f8fafc;
}

.nightMode .pos {
  color: #c4b5fd;
}

.nightMode .ipa {
  color: #93c5fd;
}

.nightMode .pos-heading,
.nightMode .semantic-heading {
  color: #9ca3af;
}

.nightMode .example {
  color: #d1d5db;
}
```

Implementation details may improve, but preserve distinct colors and sizes for
term, part of speech, IPA, and priority; make `ACTIVE` visually stronger than
`RECEPTIVE`; support readable light and dark modes; keep the layout compact;
and avoid decorative clutter.

## 29. `BackHTML` generation

Generate semantic HTML. For each part of speech, use this structure:

```html
<div class="pos-block">
  <div class="pos-heading">ADJECTIVE</div>

  <div class="sense">
    <div class="definition">
      <strong>1.</strong>
      Easy to notice because it clearly stands out.
    </div>

    <div class="example">
      His bright red jacket made him conspicuous in the crowd.
    </div>

    <div class="semantic-heading">Synonyms</div>

    <div class="semantic-item">
      <strong>1. noticeable</strong>
      — <span class="relation">NEAR-INTERCHANGEABLE</span>;
      usually less emphatic.
    </div>

    <div class="semantic-heading">Antonyms</div>

    <div class="semantic-item">
      <strong>inconspicuous</strong>
      — <span class="relation">DIRECT OPPOSITE</span>
    </div>
  </div>
</div>
```

Every polished `ACTIVE` and `RECEPTIVE` Back must display both Synonyms and
Antonyms headings. Render sense-specific entries where they exist. If the
entire card has no genuine entry for one of the two fields, render the
corresponding explicit fallback message instead of an empty section:

```text
Synonyms
No useful synonym for this word.

Antonyms
No useful antonym for this word.
```

`SKIP` entries do not require these visible sections because they are not
exported to Anki.

## 30. Learning-efficiency rules

Always optimize for review efficiency. Do not turn cards into encyclopedia
entries. Avoid excessive definitions, long paragraphs, large synonym lists,
redundant examples, trivia, etymology unless requested, decorative
information, and repeated metadata.

A learner may see a card dozens of times. Every visible element must justify
repeated attention.

## 31. Priority does not change card structure

`ACTIVE` and `RECEPTIVE` cards use the same structural layout. The label
changes review behavior:

- `ACTIVE`: the learner should eventually produce the item;
- `RECEPTIVE`: recognition is sufficient.

Do not create separate note types unless explicitly requested later.

## 32. `SKIP` entries

Keep `SKIP` items in `data/vocabulary_master.csv` with enough information to
identify and reconsider them later:

- term;
- normalized term;
- observed form;
- short meaning;
- frequency and relevance metadata;
- encounter count;
- dates;
- sources;
- classification reason.

Do not generate polished Anki HTML for `SKIP` items unless they are later
promoted.

## 33. Source tracking

When the learner provides a sentence or source, save it internally. Sources
may include a fantasy comic, novel, YouTube video, conversation, or IELTS
article. Do not display source data on the current card design. Keep it for
encounter tracking, personal relevance, and future reclassification.

## 34. Initial project setup

On the first vocabulary update, create missing parts of this structure without
overwriting existing data:

```text
cards/vocabulary/
├── CARD_AUTHORING.md
├── README.md
├── data/
│   └── vocabulary_master.csv
├── exports/
│   └── anki_import.csv
├── anki/
│   ├── front.html
│   ├── back.html
│   └── styling.css
└── scripts/
    └── update_vocabulary.py
```

The repository-level `AGENTS.md` contains the durable trigger for this
specification. Do not duplicate the entire specification there. Never
overwrite existing vocabulary data during initialization.

## 35. Automation

Implement a maintainable workflow so vocabulary updates never require manual
CSV-cell editing. Prefer `scripts/update_vocabulary.py`, which can:

- read the master CSV;
- update or create entries;
- validate structured fields;
- merge duplicate headwords;
- increment encounters;
- regenerate `BackHTML`;
- regenerate `exports/anki_import.csv`;
- preserve UTF-8;
- escape CSV and HTML correctly.

Keep the repository understandable and editable by future agents.

## 36. Validation

Before reporting an update as complete, verify:

- the master CSV parses correctly;
- JSON in `SensesJSON` parses correctly;
- no duplicate normalized headwords exist;
- `ACTIVE` and `RECEPTIVE` rows appear in the Anki export;
- `SKIP` rows do not appear in the Anki export;
- every exported item has `Term`, `Priority`, part of speech, pronunciation, at
  least one definition, and at least one natural example;
- HTML is well formed;
- every exported card visibly includes both Synonyms and Antonyms sections;
- a field with no genuine candidate uses the required explicit fallback
  message rather than a fabricated entry;
- pronunciation is American English;
- `TTS_Text` is populated;
- Front and Back templates still match the required design.
- useful production patterns are visible where they add practical guidance;
- requested contrast groups retain the normal vocabulary layout and include
  individual term information plus a concise Difference note.

Do not say the system or an update is ready until these checks pass.

## 37. Reviewing and processing a submitted batch

The learner may submit a plain list such as:

```text
devoid
aberration
backwater
deity
conspicuous
```

or:

```text
stave sth off
filial
placate
pacify
discreet
unilateral
```

Treat a bare list as Stage A only:

1. analyze the items;
2. explain the useful meanings and usage;
3. propose `ACTIVE`, `RECEPTIVE`, or `SKIP` for each item;
4. explicitly state that no data or export was changed;
5. wait for approval.

After the learner explicitly approves the batch, perform Stage B and give a
concise result such as:

```text
Processed 6 items.

ACTIVE
- stave off
- discreet
- unilateral

RECEPTIVE
- filial
- placate
- pacify

SKIP
- none

Updated existing entries
- none

Anki export regenerated successfully.
```

Do not dump the complete CSV into chat unless requested.

## 38. Explanation, approval, and processing requests

A vocabulary list by itself requests explanation and proposed classification,
not a write. Never change master data or the export solely because a list was
submitted.

Only an explicit instruction to add, update, save, or process previously
reviewed items authorizes Stage B. The approval may be brief; `add them` is
sufficient when its referent is clear.

If the learner asks a question such as `What's the difference between placate
and pacify?`, answer the question first. Do not silently modify vocabulary data
without subsequent explicit approval.

## 39. Manual overrides and corrections

When the learner corrects a classification, definition, example,
pronunciation, synonym relationship, or other card content:

- treat the correction as intentional;
- update the master data;
- regenerate the Anki export;
- do not restore the old version later without a strong reason;
- preserve manual edits whenever possible.

## 40. Quality standard

Before saving an item, ask:

- Is this meaning current?
- Is this normal American English?
- Would a concise Common patterns note help the learner use this item?
- For a requested contrast group, does each term retain its normal card
  information, and does the Difference note explain real usage boundaries?
- Could a native speaker plausibly say or write the example?
- Does the card visibly include both Synonyms and Antonyms sections?
- Is a proposed synonym genuinely substitutable or merely related?
- Is the synonym relationship label accurate?
- Is an antonym meaningful for this particular sense?
- If no genuine synonym or antonym exists, did the card say so explicitly
  instead of omitting the field or fabricating an entry?
- Is an obscure dictionary sense consuming review time without justification?
- Is `ACTIVE` justified, or is `RECEPTIVE` enough?
- Is `RECEPTIVE` justified, or should this be `SKIP`?

Prefer fewer high-quality cards over a large, noisy deck.

## 41. Core philosophy

The system supports this learning loop:

```text
Encounter unfamiliar English
        ↓
Understand it in context
        ↓
Classify usefulness
        ↓
ACTIVE / RECEPTIVE / SKIP
        ↓
ACTIVE + RECEPTIVE → Anki
        ↓
Spaced retrieval
        ↓
ACTIVE → learner creates an original sentence and receives feedback
        ↓
Future natural encounters strengthen the word
```

Anki is for efficient spaced exposure and retrieval. It is not meant to
contain every piece of linguistic knowledge about a word. Keep cards compact,
useful, and pleasant to review.
