# EN Grammar Guide — Implementation Plan

## Goal

Build an original English grammar learning system that:

- uses the scope of *English Grammar in Use* Fifth Edition as a coverage map;
- prioritises grammar that transfers to natural conversation and IELTS Speaking 7;
- can be studied selectively instead of from Chapter 1 to Chapter 145;
- gives extra attention to relative clauses, reduced relative clauses, infinitive clauses,
  and other structures that were underexplained in the previous material;
- preserves the source book's example-led teaching rhythm while keeping each unit
  manageable as one learning session.

This is a companion and replacement study path, not a transcription of the copyrighted
book. It must not reproduce the book's explanations, exercises, or answer key.

## Learner experience

The entry point is `README.md`, which offers three routes:

1. **IELTS Speaking 7 core** — the smallest high-value path.
2. **Fix one problem** — jump from a symptom to the relevant sheet.
3. **Full grammar coverage** — follow the original 145-unit sequence inside 12 larger
   chapter groups.

The material has two levels:

- a **chapter overview** that gives the large mental model and navigation;
- **unit lessons** that preserve the book's unit number, grammar topic, and
  explanation-to-exercise learning sequence.

Every unit lesson follows the source book's broad teaching pattern:

1. **A concrete example situation** that makes the form meaningful.
2. **A–E explanation sections**, with the number of sections determined by the
   source unit's real distinctions.
3. **We use / We say / Compare** explanations and carefully chosen `(not ...)`
   contrasts where they are genuinely accurate.
4. **Exercises N.1, N.2, ...** that practise different decisions.
5. **A hidden answer section** for self-study.

Target length:

- chapter overview: normally 500–900 words;
- unit lesson: normally 280–650 words, including exercises and answers.

No long introductions, history, exhaustive exception lists, or generic filler. All
learner-facing material in `EN/` is written in English.

## Deliverables

```text
EN/
├── README.md
├── PLAN.md
├── grammar-map.md
├── diagnostic.md
├── cheat-sheet.md                 # preserve existing detailed clause reference
├── chapters/
│   ├── 01-time-and-tense/
│   │   ├── README.md
│   │   └── units/                 # Units 1–18
│   ├── 02-future-and-conditionals/
│   │   ├── README.md
│   │   └── units/                 # Units 19–25 and 38–41
│   ├── 03-modals-and-attitude/
│   │   ├── README.md
│   │   └── units/                 # Units 26–37
│   ├── 04-passive-and-reported-meaning/
│   │   ├── README.md
│   │   └── units/                 # Units 42–48
│   ├── 05-questions-and-conversation-control/
│   │   ├── README.md
│   │   └── units/                 # Units 49–52
│   ├── 06-verb-patterns-ing-and-to/
│   │   ├── README.md
│   │   └── units/                 # Units 53–68
│   ├── 07-nouns-articles-and-quantity/
│   │   ├── README.md
│   │   └── units/                 # Units 69–91
│   ├── 08-relative-and-reduced-clauses/
│   │   ├── README.md
│   │   └── units/                 # Units 92–97
│   ├── 09-adjectives-adverbs-and-comparison/
│   │   ├── README.md
│   │   └── units/                 # Units 98–112
│   ├── 10-linking-ideas/
│   │   ├── README.md
│   │   └── units/                 # Units 113–120
│   ├── 11-prepositions/
│   │   ├── README.md
│   │   └── units/                 # Units 121–136
│   └── 12-phrasal-verbs/
│       ├── README.md
│       └── units/                 # Units 137–145
├── paths/
│   ├── ielts-speaking-7.md
│   └── natural-speaking.md
└── practice/
    └── speaking-prompts.md
```

## Coverage model

The guide preserves all 145 unit numbers and topics, but does not give them equal study
priority.

- **Core production**: structures needed frequently in spontaneous conversation.
- **Contrast and repair**: common structures whose meaning changes through a small choice.
- **Recognition/reference**: lower-frequency details that should be findable but do not
  deserve a mandatory lesson.

`grammar-map.md` must account for every unit number from 1 through 145 and route it to
one chapter and one unit file. The grammar rules, distinctions, and common error
categories may follow the source because those are the knowledge being taught. The
wording, examples, exercises, and answers must be independently written.

## Special depth requirement

Chapter 08 and its Units 92–97 must clearly distinguish:

- subject and object relative clauses;
- when the relative word can be omitted;
- active `V-ing` and passive past-participle modifiers;
- ongoing passive `being + past participle`;
- infinitival relatives such as `the first person to arrive`;
- noun + infinitive patterns such as `something to eat`;
- meaning that reduction can remove;
- cases where a full relative clause is safer.

The chapter overview should link to `../../cheat-sheet.md` for optional detail rather
than repeating that file.

## IELTS Speaking 7 standard

The guide should train usable range and accuracy, not rare grammar display:

- frequent error-free simple and complex sentences;
- flexible tense control;
- conditionals, relative clauses, noun clauses, comparison, concession, and modals;
- natural discourse frames and paraphrasing;
- no recommendation to force inversions or memorised “advanced” structures.

The practice file must integrate grammar with the other speaking dimensions:
fluency/coherence, lexical resource, and pronunciation.

## Work split

- **Agent A — Units 1–48**: chapter groups 01–04.
- **Agent B — Units 49–97**: chapter groups 05–08, with extra care on Units 64–65
  and 92–97.
- **Agent C — Units 98–145**: chapter groups 09–12.
- **Primary agent — integration**: chapter overview placement, README, diagnostic,
  complete 145-unit map, learning paths, consistency edits, and final audit.

Agents may use `terra-medium` or `sol-medium`; no higher reasoning setting.

## Quality gates

Before completion:

- all planned files exist and internal links resolve;
- every book unit 1–145 has exactly one unit file and appears exactly once in
  `grammar-map.md`;
- chapter overviews and units follow the example-led teaching pattern and length
  targets;
- examples are original and conversational;
- no copied book exercises or extended wording;
- no contradictory rules across sheets;
- reduced relative clauses receive the required depth;
- the IELTS path can be completed without reading every sheet;
- Markdown structure passes a simple link and heading audit.
