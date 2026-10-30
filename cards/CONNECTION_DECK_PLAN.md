# English Connection Patterns Deck — Master Execution Specification

> **Note (2026-10-30):** the preposition plan, pilot, inventory, and audit this
> plan migrated from were retired after the migration; they remain in git
> history. References to them below are historical.

**Status:** Accepted by the learner on 2026-07-30. Inventory migration,
master inventory completion, source authoring, audit, builder, and final TSV
work may proceed. Do not generate the old standalone preposition deck.

**Version:** 0.1 — 2026-07-30

**Authority:** After learner approval, this document becomes the top-level
authority for the large connection-pattern deck under `cards/`. The
existing `PREPOSITION_DECK_PLAN.md`, preposition inventory, audit, and pilot
remain evidence and module-level inputs; they no longer define the whole
learning resource.

## 1. Learning objective

Build one large American English Anki deck that teaches how English words,
phrases, and clauses connect to the structures that follow them.

The learner should become able to answer:

1. Does this anchor require a connector or no connector?
2. If a connector is required, which preposition, conjunction, particle, or
   marker is natural?
3. What grammatical shape may follow: noun phrase, pronoun, finite clause,
   `V-ing` clause, to-infinitive, bare infinitive, past-participle clause,
   adjective phrase, prepositional phrase, or another coordinated unit?
4. When two connections are possible, how does the meaning change?
5. Which accepted alternatives are neutral, conversational, or formal AmE?
6. When can a full clause be reduced, and what controls its understood
   subject?
7. Can the same pattern be applied in an unfamiliar sentence rather than only
   reproduced from one memorized example?

Canonical learning statement:

> Given an anchor and an intended meaning, choose the connector and complement
> shape that natural contemporary AmE requires, and distinguish it from the
> nearest useful alternative.

This is broader than a preposition deck. Prepositions are one module inside
the larger system.

## 2. What “connection pattern” means

A connection pattern contains:

- an **anchor**: the word, phrase, or clause that controls or motivates the
  connection;
- a **connector or marker**, when present;
- a **complement shape**: the grammatical form that follows; and
- a **meaning or function** created by the construction.

Examples:

| Anchor | Connector or marker | Complement shape | Pattern |
|---|---|---|---|
| `depend` | `on` | noun phrase / wh-clause | `depend on + NP/wh-clause` |
| `avoid` | zero | `V-ing` clause | `avoid + V-ing` |
| `allow` | zero, then `to` | object + to-infinitive | `allow + object + to + verb` |
| `aware` | `of` | noun phrase / `V-ing` | `aware of + NP/V-ing` |
| `aware` | `that` | finite clause | `aware that + clause` |
| `reason` | `for` | noun phrase / `V-ing` | `reason for + NP/V-ing` |
| `reason` | `to` | infinitive | `reason to + verb` |
| `although` | subordinator | finite clause | `although + subject + finite verb` |
| `although` | subordinator | reduced clause | `although + V-ing/AdjP/PP/NP` |
| noun being modified | relative marker or zero | relative/reduced clause | `the first person to arrive` |
| comparative | `than` | phrase or clause | `higher than + NP/clause` |

The goal is not merely to memorize the labels in this table. Every validated
card must turn one of these relationships into a usable retrieval decision.

## 3. Scope boundary

### 3.1 Included

Include practical, reusable connection systems needed through a
C1-oriented general-English level:

- semantic preposition systems;
- dependent verb, adjective, participle, and noun patterns;
- verb complementation and valency;
- conjunctions and clause linkers;
- finite versus non-finite complement choices;
- relative clauses and reduced noun-modifying clauses;
- adverbial participle and reduced clauses;
- coordination and parallel structures;
- comparison, degree, purpose, and result frames;
- zero-marker and extra-marker traps;
- complement form and understood-subject restrictions;
- meaning-changing pattern contrasts;
- accepted contemporary AmE variants and relevant register differences; and
- broadly useful neutral, conversational, academic, and professional forms.

### 3.2 Excluded

Do not turn this deck into all of English grammar or vocabulary. Exclude unless
the construction directly affects a connection decision:

- tense and aspect as complete systems;
- article and determiner systems;
- subject–verb agreement;
- ordinary plural formation;
- general word order unrelated to complements or clause linking;
- pronunciation, stress, and prosody;
- speaking drills, recording, and timed production;
- paragraph organization and discourse strategy;
- every possible lexical collocation;
- arbitrary adverb–adjective intensity collocations such as `deeply worried`
  unless later justified as a separate vocabulary-pattern resource;
- rare literary, archaic, or specialist legal constructions; and
- terminology-only cards such as `gerund`, `subordinator`, or
  `non-finite clause`.

The vocabulary and sentence-complexity benchmark is suitable for an IELTS 7
learner, but this is not an IELTS course and does not predict a score.

### 3.3 Practical completeness claim

The deck aims to be:

- **system-complete** for the nine modules in Section 5;
- **item-selective** for lexical anchors;
- **family-audited** rather than dictionary-exhaustive;
- **American-English centered**;
- **organized by one-home routing**; and
- **extendable** when future learner questions reveal a genuine gap.

Permitted final claim:

> Complete for the defined C1-oriented AmE connection-pattern resource.

Forbidden final claim:

> Every possible way that every English word can connect to another word.

## 4. Complement-shape model

The inventory must record what follows the connector. Use these canonical
internal values:

| Internal value | Learner-facing interpretation | Example |
|---|---|---|
| `NP` | noun phrase or pronoun | `despite the delay`; `depend on it` |
| `finite-clause` | subject + tense-marked verb | `although residents objected` |
| `that-clause` | content clause introduced by `that` | `aware that costs increased` |
| `wh-clause` | clause beginning with `what/how/whether...` | `depends on whether it works` |
| `to-inf` | `to + base verb` | `decide to postpone` |
| `bare-inf` | base verb without `to` | `make them revise` |
| `V-ing-clause` | gerund-participial clause | `avoid making assumptions` |
| `past-participle-clause` | passive/reduced participial clause | `although criticized` |
| `AdjP` | adjective phrase | `although controversial` |
| `PP` | prepositional phrase | `although under pressure` |
| `predicative-NP` | noun phrase understood after omitted `be` | `although a newcomer` |
| `relative-clause` | finite noun modifier | `the policy that they approved` |
| `reduced-relative` | non-finite noun modifier | `the policy approved yesterday` |
| `parallel-unit` | same structural type as a coordinated neighbor | `collecting and analyzing data` |
| `zero` | no overt connector | `discuss the proposal`; `go home` |

On learner-facing Backs, give the pattern and plain-English explanation. Use
technical labels only when they help the learner choose the next form.

Do not call every `V-ing` form a noun. For example:

- `despite receiving objections` has a `V-ing` complement after a
  preposition;
- `although receiving objections` is a reduced non-finite concessive clause;
- `the committee receiving objections` may be part of another construction.

The visible word ending is not enough to determine the construction.

## 5. Parent deck and numeric subdecks

Use one parent deck:

```text
EN::Connection Patterns
├── 01 Prepositions and Prepositional Phrases
├── 02 Verb Patterns
├── 03 Adjective and Participle Patterns
├── 04 Noun Patterns
├── 05 Conjunctions and Clause Linkers
├── 06 Relative and Noun-Modifying Clauses
├── 07 Non-finite and Reduced Clauses
├── 08 Coordination and Parallelism
└── 09 Comparison, Degree, and Result Patterns
```

These nine entries are the only learner-facing subdeck layer. Do not reproduce
the old nine preposition categories as nested Anki subdecks. Their categories
remain internal topics inside Subdeck 01.

The numeric prefixes:

- stabilize filesystem order;
- stabilize Anki subdeck order;
- provide a readable taxonomy; and
- do not define a mandatory study sequence.

The learner may study one subdeck or the parent deck. Anki controls scheduling
and mixing.

### 5.1 Subdeck 01 — Prepositions and Prepositional Phrases

Teach productive preposition meaning and preposition-led constructions that
are not better owned by a lexical anchor or clause-relation contrast.

Required families:

- time: points, days, periods, duration, deadlines, continuation, sequence,
  `on time/in time`, and zero-preposition time expressions;
- place: point, enclosure, surface, institutional/site viewpoint, address,
  floor, geographic scale, boundary, relative position, and accepted overlap;
- movement: destination, source, boundary crossing, surface movement,
  vehicles, path, direction, and destination adverbs such as `home`;
- abstract roles: agent, instrument, method, source, cause, purpose,
  beneficiary, recipient, topic, scope, role, comparison, exception, addition,
  material, measurement, and rate;
- preposition complement shapes: `NP`, pronoun, and `V-ing` clause;
- standalone multiword prepositions and fixed prepositional frames, such as
  `in terms of`, `on behalf of`, and `from my perspective`;
- question-level preposition stranding and neutral/formal placement when it is
  not specifically a relative-clause decision;
- preposition versus directional adverb where the complement requirement is
  the lesson; and
- closed-answer treatment of accepted AmE variants.

Move lexical dependent patterns to Subdecks 02–04. Move clause-relation
contrasts such as `although` versus `despite` to Subdeck 05. Move relative
preposition placement to Subdeck 06.

### 5.2 Subdeck 02 — Verb Patterns

Teach the complement frame selected by a verb and the meaning change produced
by an alternative frame.

Required families:

- verb + direct object with no preposition: `discuss the issue`,
  `enter the building`, `approach the problem`;
- verb + preposition + complement: `depend on`, `contribute to`,
  `result in/from`;
- verb + to-infinitive: `decide to postpone`;
- verb + `V-ing`: `avoid making`, `consider changing`;
- verb + `that`-clause or wh-clause: `suggest that`, `explain why`;
- verb + object + to-infinitive: `allow someone to leave`;
- verb + object + bare infinitive: `make/let someone leave`;
- perception patterns: `see someone do/doing`;
- verb + object + past participle or adjective complement where broadly useful:
  `have the system checked`, `keep the door open`;
- ditransitive and recipient alternations:
  `give someone something / give something to someone`;
- reporting and recommendation frames, including standard AmE mandative forms;
- phrasal-verb particle placement and prepositional-verb non-separation;
- prepositional `to` versus infinitival `to` when controlled by a verb frame;
- meaning contrasts such as `remember/regret/try/stop/go on/mean +
  to-infinitive or V-ing`; and
- zero-marker traps caused by Mandarin transfer.

The anchor verb stays visible in transfer examples. Do not claim transfer by
switching to a different verb pattern.

### 5.3 Subdeck 03 — Adjective and Participle Patterns

Teach complements selected by adjectives and lexical participles.

Required families:

- adjective/participle + preposition: `interested in`, `responsible for`,
  `relevant to`, `caused by`;
- adjective + to-infinitive: `likely to`, `ready to`, `reluctant to`;
- adjective + `that`-clause: `aware that`, `concerned that`, `certain that`;
- adjective + wh-clause where useful: `unsure whether/how`;
- adjective + object/control patterns where natural;
- experiencer versus cause patterns: `interested in / interesting to`,
  `surprised at/by`;
- subject patterns such as `X is easy to use` versus
  `It is easy for someone to use X`;
- accepted overlapping AmE prepositions without false contrasts; and
- complement-form changes that materially change meaning or reference.

Do not add every emotion adjective. Select productive, frequent, and
confusion-prone anchors.

### 5.4 Subdeck 04 — Noun Patterns

Teach complements that complete the meaning of a noun.

Required families:

- noun + preposition: `reason for`, `solution to`, `confidence in`;
- noun + to-infinitive: `ability to`, `decision to`, `opportunity to`;
- noun + `that`-clause: `fact that`, `claim that`, `possibility that`;
- noun + wh-clause: `question of whether`, `decision about whether`;
- noun + `of + V-ing` and other productive nominal frames;
- one-anchor contrasts:
  `reason for + NP/V-ing / reason to + verb / reason why + clause`;
- source versus target:
  `effect of + cause / effect on + target`;
- variable versus amount:
  `increase in + variable / increase of + amount`;
- content `that`-clauses versus relative clauses:
  `the claim that prices fell` versus `the claim that they rejected`; and
- article/countability information only when it is necessary to use the
  connection pattern correctly.

Keep noun anchors together when their alternative complements form one useful
contrast. Do not split `reason for`, `reason to`, and `reason why` into
different modules merely because the connector changes.

### 5.5 Subdeck 05 — Conjunctions and Clause Linkers

Teach how clause relations are marked and what structural form each linker
introduces.

Required families:

- coordination boundary versus subordination;
- cause: `because`, `since`, `as`, and comparison with `because of`;
- concession: `although`, `though`, `even though`, `while`, and comparison
  with `despite/in spite of`;
- condition: `if`, `unless`, `even if`, `as long as`, `provided/providing`;
- time: `when`, `while`, `before`, `after`, `once`, `until`, `as soon as`;
- contrast: `whereas`, `while`, `but`;
- purpose: `so that`, `in order that`, and other practical purpose linkers;
- manner and hypothetical comparison: `as if/as though`;
- finite clauses versus permitted reduced clauses after a linker;
- `although/though + V-ing`, past participle, `AdjP`, `PP`, and
  predicative `NP`;
- understood-subject and dangling-modifier restrictions;
- `although + reduced clause` versus `despite + NP/V-ing`;
- neutral versus formal linker choices; and
- punctuation only where it affects interpretation or construction.

Approved model contrast:

```text
Despite strong objections, the council approved the plan.
Although several residents objected, the council approved the plan.
```

Approved extension:

```text
Although receiving strong objections, the council approved the plan.
Although controversial, the proposal gained support.
Although a newcomer, she handled the negotiations confidently.
```

The reduced forms are genuine learning items even though they were removed
from one preposition pilot Front to keep that particular answer space closed.

### 5.6 Subdeck 06 — Relative and Noun-Modifying Clauses

Teach how a clause or reduced clause connects to the noun it modifies.

Required families:

- defining versus non-defining relative clauses;
- `who`, `whom`, `which`, `that`, `whose`, `where`, and `when`;
- subject versus object relatives;
- omission of an object relative marker;
- preposition stranding versus formal fronting;
- prohibition of `preposition + that`;
- finite relative clauses versus reduced relatives;
- active `V-ing` modifiers: `students living abroad`;
- passive past-participle modifiers: `data collected last year`;
- to-infinitive modifiers: `the first person to arrive`,
  `the only option to remain`;
- ordinal, superlative, next/last/only licensing environments;
- reduced relative versus main-clause or adverbial-participle interpretation;
- content `that`-clause versus relative `that`-clause; and
- attachment and ambiguity when two nouns could be modified.

The explicit content-clause versus relative-clause contrast for a noun anchor
belongs to Subdeck 04. This module may cross-reference it but must not duplicate
that card.

This module directly covers the learner's original reduced-relative concern.

### 5.7 Subdeck 07 — Non-finite and Reduced Clauses

Teach non-finite clauses that supplement or modify a main clause rather than a
noun and are not selected by a conjunction.

Required families:

- present-participial clauses: `Working remotely, ...`;
- perfect participial clauses: `Having completed the audit, ...`;
- past-participial clauses: `Designed for small teams, ...`;
- infinitival purpose and comment clauses: `To reduce costs, ...`;
- negative forms: `Not knowing...`, `Having never seen...`;
- simultaneous, prior, causal, conditional, and result interpretations;
- understood-subject control;
- dangling and misplaced modifiers;
- explicit-subject `with + NP + V-ing/past participle` constructions when
  broadly useful;
- concise formal versus clearer finite-clause alternatives; and
- distinction from reduced relative clauses.

Reduced clauses introduced by `although/while/if/when` route to Subdeck 05.
Reduced clauses modifying a noun route to Subdeck 06.

### 5.8 Subdeck 08 — Coordination and Parallelism

Teach how equal grammatical units connect.

Required families:

- `and`, `but`, `or`, `nor`, `yet`, and coordinator `so`;
- word, phrase, and clause coordination;
- parallel complement shapes:
  `collecting and analyzing`, not `collecting and to analyze`;
- `both...and`, `either...or`, `neither...nor`,
  `not only...but also`;
- scope and attachment of coordinated units;
- shared complements and safe ellipsis;
- agreement with correlative subjects only where needed for the pattern;
- `rather than` when it coordinates parallel alternatives; and
- avoiding overloaded cards that test coordination plus unrelated grammar.

The lesson is the structural relationship, not memorizing the label
“coordinating conjunction.”

### 5.9 Subdeck 09 — Comparison, Degree, and Result Patterns

Teach connectors and complement shapes controlled by comparison and degree.

Required families:

- comparative + `than + NP/clause`;
- equality and inequality:
  `as...as`, `not as/so...as`;
- `the more..., the more...`;
- `too + adjective/adverb + to-infinitive`;
- `adjective/adverb + enough + to-infinitive`;
- `so + adjective/adverb + that-clause`;
- `such + (a/an) + adjective + noun + that-clause`;
- degree expressions followed by prepositional or clausal complements;
- `as opposed to` when the comparison frame is the lesson;
- cross-reference, but do not duplicate, `rather than` from Subdeck 08 or
  `as if/as though` from Subdeck 05;
- `higher than` versus `above/over` only with a closed answer space or explicit
  construction contrast; and
- parallel form inside comparisons.

This module covers structural adverb connections. Ordinary lexical
adverb–adjective collocations remain outside the deck.

## 6. One-home routing

Every atomic decision has exactly one learner-facing home. Route in this
order:

1. If the decision is selected by a verb, use Subdeck 02.
2. If selected by an adjective or lexical participle, use Subdeck 03.
3. If selected by a noun, use Subdeck 04.
4. If the decision compares or uses a clause linker, use Subdeck 05.
5. If the construction modifies a noun as a relative/reduced relative, use
   Subdeck 06.
6. If it is a free non-finite supplement modifying the main clause, use
   Subdeck 07.
7. If the central decision is coordination/parallelism, use Subdeck 08.
8. If the central decision is comparison, degree, or a degree-result frame,
   use Subdeck 09.
9. Otherwise, if a preposition or prepositional phrase itself supplies the
   semantic relation, use Subdeck 01.

This routing deliberately prevents “all forms containing a preposition” from
being dumped into Subdeck 01.

Examples:

| Decision | Home | Reason |
|---|---|---|
| `at 7:30` | 01 | time preposition supplies the relation |
| `depend on + NP` | 02 | selected by verb `depend` |
| `responsible for + NP/V-ing` | 03 | selected by adjective |
| `reason for/to/why` | 04 | one noun anchor with alternative complements |
| `although + clause/reduced clause` | 05 | subordinator controls clause relation |
| `although` versus `despite` | 05 | clause-relation and complement contrast |
| `the first person to arrive` | 06 | infinitive modifies a noun |
| `Having completed the audit, ...` | 07 | free adverbial non-finite clause |
| `both X and Y` | 08 | coordination and parallelism |
| `too expensive to maintain` | 09 | degree controls an infinitive result |

Cross-reference another module on the Back when useful, but do not create a
duplicate card.

## 7. Master coverage inventory

Create:

```text
cards/connections/coverage.tsv
```

Canonical fields:

```text
item_id
subdeck
topic
anchor
connector_or_marker
complement_shape
target_pattern
meaning_or_distinction
confusables
card_type
register
source_file
card_id
status
evidence_note
notes
```

### 7.1 Field meanings

- `item_id`: stable uppercase inventory identifier.
- `subdeck`: exact numeric learner-facing subdeck.
- `topic`: internal family, not an Anki tag.
- `anchor`: controlling lexical or grammatical expression.
- `connector_or_marker`: `on`, `although`, `to`, `that`, `zero`, etc.
- `complement_shape`: one or more canonical values from Section 4.
- `target_pattern`: complete reusable construction.
- `meaning_or_distinction`: the knowledge being retrieved.
- `confusables`: nearest normal or erroneous alternatives.
- `card_type`: `chunk`, `context`, `contrast`, or `repair`.
- `register`: contemporary AmE register information.
- `source_file`: exactly one numeric Markdown source.
- `card_id`: blank until canonical card authoring.
- `status`: `proposed`, `validated`, `excluded`, or `deferred`.
- `evidence_note`: concise pointer for a disputed form; not a frequency score.
- `notes`: routing, ambiguity, and authoring constraints.

No tags, frequency bands, batches, activation stages, or suspension fields.

### 7.2 Atomicity

One row represents one retrieval decision. Split when:

- one anchor accepts complements with materially different meanings;
- two senses require different contexts;
- one row would require unrelated answers; or
- a learner could know one side without knowing the other.

Keep one contrast row when distinguishing the alternatives is the decision:

- `remember to do / remember doing`;
- `despite + NP/V-ing / although + clause`;
- `reason for + NP/V-ing / reason to + verb`;
- `result in + outcome / result from + cause`.

### 7.3 Item inclusion

Include a lexical pattern when several are true:

- useful in at least five realistic situations;
- common enough for general, academic, or professional AmE;
- difficult to derive from a broad rule;
- commonly confused with a nearby frame;
- meaning changes when the complement changes;
- repeatedly relevant to the learner; or
- important for understanding or producing C1-oriented English.

Do not expand a list merely because a dictionary records another possible
complement.

## 8. Approved card system

The learner accepted the four-type style in
`prepositions/PILOT.md`. It becomes the visible style baseline for all nine
master subdecks.

Every Anki note has exactly:

- Front
- Back

The Deck column is import routing, not a visible field.

### 8.1 `chunk`

Use for a lexical or fixed connection:

```text
Front:
avoid ___ + action

Back:
avoid + V-ing

Use V-ing for the action that someone avoids.

• The report avoids making unsupported assumptions.
• Many applicants avoid discussing salary expectations.
```

### 8.2 `context`

Use for applying a productive semantic rule:

```text
Front:
The orientation will be held ___ 425 Lexington Avenue.

Back:
The orientation will be held at 425 Lexington Avenue.

Use at before a complete numbered address.
```

### 8.3 `contrast`

Use when comparison is the knowledge:

```text
Front:
1. ___ strong objections, the council approved the plan.
2. ___ several residents objected, the council approved the plan.

Back:
1. Despite strong objections, ...
2. Although several residents objected, ...

despite + NP/V-ing
although + finite clause

Also OK for 1: In spite of strong objections.
```

The learner particularly values this form when the contrast is genuine and the
Back makes accepted alternatives explicit.

### 8.4 `repair`

Use for extra, missing, or structurally wrong connectors:

```text
Front:
Fix if wrong:
The committee suggested to postpone the vote.

Back:
The committee suggested postponing the vote.

suggest + V-ing
Also OK: The committee suggested that the vote be postponed.
```

Some repair cards must already be correct.

### 8.5 Card-type selection

Use:

1. `repair` for error detection;
2. `contrast` for a coherent competing construction;
3. `chunk` for a lexical/fixed selection;
4. `context` for a productive rule applied to a situation.

Do not target a numerical ratio. The final ratio emerges from the inventory.

## 9. Closed-answer and self-grading standard

Every Front must let the learner grade the answer objectively.

Before validation, enumerate common forms that fit the exact printed sentence:

- other prepositions;
- other conjunctions;
- a multiword completion;
- a different complement construction;
- accepted AmE variants; and
- reductions that make an unexpected answer grammatical.

Examples:

- `Inflation remains ___ the target` is open because `above`, `over`, and
  `higher than` fit.
- `___ receiving objections` does not isolate `despite` because
  `although receiving` is also grammatical.
- `She is ___ the office` commonly permits both `at` and `in`.

If several common answers compete:

1. rewrite the context;
2. convert it to a genuine bounded contrast;
3. list a limited normal alternative under `Also OK:`; or
4. exclude the item if grading remains subjective.

`Also OK:` is not a substitute for a closed answer space. It is used when a
small, understandable accepted alternative remains after the main decision is
clear.

Do not fix ambiguity by putting the complete answer on every Front. Preserve
retrieval.

## 10. Example and explanation standard

- Write cards in English.
- Use contemporary natural AmE.
- Use IELTS-7/C1-oriented topic vocabulary without obscuring the connection.
- Prefer education, technology, employment, public policy, health,
  environment, daily life, and professional contexts.
- Do not inflate register merely to look advanced.
- A Back shows the completed pattern or sentence.
- A `chunk` Back gives two or three natural examples.
- A `contrast` Back states both structures and the meaning/complement boundary.
- Name a normal answer under `Also OK:` when that exact Front permits it.
- State the complement shape in a practical notation when it aids production.
- Explain understood subjects and reduction constraints when relevant.
- Do not add generic `GENERALIZATION` sections or unrelated mini-essays.
- Do not copy examples from reference works.

## 11. Source and build layout

After plan approval, create:

```text
cards/connections/
├── 01-prepositions.md
├── 02-verb-patterns.md
├── 03-adjective-participle-patterns.md
├── 04-noun-patterns.md
├── 05-conjunction-clause-linkers.md
├── 06-relative-noun-modifying-clauses.md
├── 07-nonfinite-reduced-clauses.md
├── 08-coordination-parallelism.md
├── 09-comparison-degree-result.md
├── coverage.tsv
├── AUDIT.md
└── anki-import.tsv

cards/tools/
└── build_connection_import.py
```

Use one Markdown source per learner-facing subdeck and one final import TSV.
Do not create per-subdeck TSVs.

### 11.1 Canonical card source

```markdown
## LINK-001

<!-- card
item: LINK-CONCESSION-DESPITE-ALTHOUGH
type: contrast
status: validated
-->

### Front

1. ___ strong objections, the council approved the plan.
2. ___ several residents objected, the council approved the plan.

### Back

1. Despite strong objections, the council approved the plan.
2. Although several residents objected, the council approved the plan.

despite + NP/V-ing
although + finite clause

Also OK for 1: In spite of strong objections.
```

### 11.2 TSV

The final TSV contains:

1. Deck
2. Front
3. Back

Use Anki headers equivalent to:

```text
#separator:tab
#html:true
#deck column:1
```

Deck values:

```text
EN::Connection Patterns::01 Prepositions and Prepositional Phrases
...
EN::Connection Patterns::09 Comparison, Degree, and Result Patterns
```

No Tags column, batch field, frequency field, or suspended output rows.

### 11.3 Builder requirements

`build_connection_import.py` must:

1. discover the nine numeric files in order;
2. derive exact Deck paths;
3. parse card ID, item ID, type, status, Front, and Back;
4. reject duplicate card IDs and visible Fronts;
5. validate every card against the master manifest;
6. reject wrong subdeck routing;
7. export only `validated` items and cards;
8. reject raw tabs/newlines in TSV fields;
9. convert safe Markdown formatting to Anki HTML;
10. reject answer-revealing metadata on the Front;
11. reject several unrelated questions on one card;
12. require complete answers, not a bare connector, on the Back;
13. confirm the full resource contains both wrong and already-correct repair
    cards;
14. report validated manifest items without cards;
15. report cards mapped to proposed, excluded, deferred, or missing items;
16. produce deterministic output;
17. support `--check` and self-test modes;
18. print counts by subdeck and card type; and
19. build the single final TSV.

The builder cannot prove linguistic naturalness or answer-space closure.
Those require semantic review.

## 12. Migration of existing preposition work

Do not discard the existing 599 reviewed rows or 24-card approved pilot.

Treat:

```text
cards/prepositions/coverage.tsv
```

as migration input, not the final master manifest.

### 12.1 Routing map

| Existing preposition category | Master destination |
|---|---|
| 01 Time | 01 Prepositions |
| 02 Place | 01 Prepositions |
| 03 Movement | 01 Prepositions |
| 04 Abstract Relationships | Usually 01; lexical anchors reroute |
| 05 Verb + Preposition | 02 Verb Patterns |
| 06 Adjective and Participle + Preposition | 03 Adjective and Participle Patterns |
| 07 Noun + Preposition | 04 Noun Patterns |
| 08 Fixed and Multiword Expressions | Split between 01 and 05 by lesson; cause/concession linkers route to 05 |
| 09 No Preposition and Grammar Traps | Split across 01, 02, 05, 06, and 07 |

Examples:

- `result in/from` → 02;
- `responsible for` → 03;
- `reason for` → 04 and later contrast with `reason to/why`;
- `because/because of`, including the `because of` chunk → 05;
- `despite/in spite of/although`, including the prepositional chunks → 05;
- relative preposition placement → 06;
- direct-object `discuss` → 02;
- free `go home` destination-adverb rule → 01.

### 12.2 Migration rules

1. Preserve evidence, exclusions, and review notes.
2. Add anchor, marker, and complement-shape fields.
3. Reassign exactly one master home.
4. Merge rows that become one cross-connector contrast.
5. Split rows that combine different complement meanings.
6. Do not preserve an old item merely to preserve its count.
7. Preserve stable old IDs when their decision remains unchanged; otherwise
   record old-to-new mapping.
8. Re-run the closed-answer audit.
9. Keep all migrated rows `proposed` until master-level review.
10. Do not generate a standalone preposition TSV.

The approved pilot governs style. It does not automatically validate every old
inventory row under the broader architecture.

## 13. Approximate resource size

Do not choose a final card count in advance. Initial planning ranges help
estimate workload only:

| Subdeck | Rough inventory range |
|---|---:|
| 01 Prepositions and Prepositional Phrases | 220–300 |
| 02 Verb Patterns | 130–180 |
| 03 Adjective and Participle Patterns | 70–100 |
| 04 Noun Patterns | 70–100 |
| 05 Conjunctions and Clause Linkers | 80–120 |
| 06 Relative and Noun-Modifying Clauses | 55–80 |
| 07 Non-finite and Reduced Clauses | 35–60 |
| 08 Coordination and Parallelism | 30–50 |
| 09 Comparison, Degree, and Result Patterns | 40–70 |
| **Provisional total** | **730–960** |

The ranges are not quotas. Genuine contrast cards can combine two sides of one
decision, exclusions can reduce the total, and inventory review may find a
missing family.

Default to one card per atomic validated decision. Anki supplies repetition.

## 14. Production workflow

### Phase 0 — Approve the master plan

The learner reviews:

- the broadened objective;
- nine-subdeck architecture;
- one-home routing;
- inclusion/exclusion boundary;
- migration strategy; and
- provisional workload.

Gate: no bulk card authoring until this master architecture is accepted.

### Phase 1 — Build migration map

- transform the preposition inventory into master schema;
- produce old-ID to new-ID and old-subdeck to new-subdeck mappings;
- preserve exclusions and evidence;
- report counts, merges, splits, and routing changes; and
- validate no old proposed row silently disappears.

### Phase 2 — Inventory missing modules

Inventory Subdecks 02–09 beyond the migrated material:

- inspect every family in Section 5;
- propose atomic patterns;
- mark complement shapes;
- select card types;
- record confusables and register;
- exclude lexical-list creep; and
- keep uncertainty visible.

Subagents may own disjoint module slices. The primary agent owns the integrated
manifest, routing, deduplication, and style consistency.

### Phase 3 — Master inventory audit

Run separate passes for:

- family coverage;
- duplicate decisions across modules;
- anchor families incorrectly split;
- false contrasts;
- complement-shape accuracy;
- AmE and register;
- Mandarin-transfer traps;
- closed answer space;
- missing accepted alternatives; and
- items outside the defined scope.

### Phase 4 — Implement sources and builder

- create nine numeric Markdown files;
- implement and self-test `build_connection_import.py`;
- validate source/manifest routing; and
- preserve the already approved card style.

### Phase 5 — Author one subdeck at a time

For each subdeck:

1. write only audited manifest items;
2. validate every Front's answer space;
3. run a linguistic review;
4. mark accepted cards and manifest rows `validated`;
5. build and inspect deterministic output; and
6. finish the module before moving to the next.

No new style pilot is required for the four accepted card types. New module
samplers may be shown for semantic review when a construction creates a new
ambiguity class.

### Phase 6 — Integrated transfer audit

Use unseen examples covering every subdeck:

- retain lexical anchors for dependent patterns;
- change topics, subjects, objects, and complements;
- test finite versus non-finite choices;
- include neutral and useful formal contexts;
- test accepted alternatives;
- include correct and incorrect repair prompts; and
- detect whether the learner could answer by a superficial shortcut.

### Phase 7 — Final build

Generate:

```text
cards/connections/anki-import.tsv
```

Then confirm:

- all exported cards are validated;
- every card maps to one inventory item and one subdeck;
- every validated item has one card;
- the TSV has exactly Deck, Front, and Back;
- the build is deterministic;
- no duplicate visible Front exists;
- all linguistic and transfer audits pass; and
- `AUDIT.md` records the final scope and counts.

## 15. Multi-agent execution rules

When delegated:

- assign one or more complete numeric source files per worker;
- never let multiple workers edit the master manifest concurrently;
- workers return inventory slices or own disjoint Markdown sources;
- all workers know that others share the workspace and must preserve their
  changes;
- independent reviewers do not author the same content they audit;
- use strong model capability when it materially improves linguistic
  correctness;
- the primary agent owns master routing, deduplication, integration, builder,
  and final output; and
- an uncertain answer remains proposed/deferred rather than becoming a forced
  rule.

Suggested inventory split:

1. Subdecks 01–02;
2. Subdecks 03–04;
3. Subdecks 05–07;
4. Subdecks 08–09 plus integration review.

## 16. Future learner questions and card requests

When the learner asks about a connection and requests a card:

1. answer the grammar question first;
2. read this master plan and the nearest source;
3. search the manifest and current cards for the same decision;
4. determine the anchor, marker, and complement shape;
5. route the item to one master subdeck;
6. improve an existing card when it already covers the decision;
7. otherwise add and audit a manifest item;
8. use a genuine contrast when the learner's confusion is a boundary between
   structures;
9. apply the closed-answer test;
10. update source and manifest;
11. rebuild the single final TSV; and
12. show the complete resulting card.

Do not create a near-duplicate merely to repeat the same form.

## 17. Definition of done

The large deck is complete only when:

- the learner has approved this master architecture;
- all nine subdecks exist;
- every required family in Section 5 has been inventoried and independently
  audited;
- the old preposition inventory has been migrated with no silent loss;
- every item has exactly one home;
- every exported card is validated;
- card Fronts pass the closed-answer standard;
- accepted alternatives are explicit;
- examples are natural contemporary AmE;
- technical complement labels are accurate and learner-useful;
- the transfer audit reveals no systematic gap;
- sources, manifest, builder, audit, and TSV agree;
- a clean deterministic rebuild succeeds; and
- the final claim stays within the practical C1-oriented scope.

## 18. Questions for the next external reviewer

Review this plan without generating cards. Report:

1. **Blocking:** architecture that cannot express the learner's goal or will
   create systematic duplication.
2. **Major:** missing high-value connection family, wrong routing order,
   unmanageable scope, or weak validation.
3. **Minor:** terminology, naming, ordering, or implementation detail.

Explicitly test:

- whether `although + V-ing/AdjP/PP/NP` has a clear home;
- whether `the first person to arrive` has a clear home;
- whether verb/adjective/noun prepositional patterns are kept with their
  anchors rather than duplicated under Prepositions;
- whether cross-category contrasts such as `although/despite` remain on one
  card;
- whether adverb-related scope is bounded;
- whether the migration preserves existing work; and
- whether one final TSV and numeric subdecks remain practical.
