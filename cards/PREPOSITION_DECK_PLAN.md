# AmE Preposition Knowledge Deck — Execution Specification

**Status:** Module inventory, audit, and card-style pilot completed. On
2026-07-30 the learner expanded the target to a unified connection-pattern
deck. This document is now a module-level migration input governed by
the accepted `CONNECTION_DECK_PLAN.md`. Do not bulk-generate a standalone
preposition deck; migrate its reviewed work into the master resource.

**Version:** 0.4 — 2026-07-30

**Authority:** This document preserves detailed preposition coverage and audit
rules for migration into Subdeck 01 and the lexical-anchor subdecks defined by
`CONNECTION_DECK_PLAN.md`. The master plan owns final routing, source layout,
and export.

## 1. Learning goal

Build a broad, well-organized American English preposition resource that
supports the learner's overall English development through a C1-oriented
level.

The resource should make the learner able to:

1. choose common prepositions for time, place, movement, and abstract
   relationships;
2. distinguish choices that change meaning, such as `by` versus `until`,
   `in` versus `into`, and `on time` versus `in time`;
3. retrieve useful verb, adjective, participle, and noun combinations such as
   `contribute to`, `responsible for`, and `impact on`;
4. use common fixed and multiword prepositional expressions such as
   `because of`, `in terms of`, and `from my perspective`;
5. recognize when English requires no preposition, as in
   `discuss the issue`;
6. understand the complement controlled by a preposition, including
   preposition + noun/pronoun/`V-ing`; and
7. apply the same knowledge in unfamiliar sentences instead of memorizing one
   example.

This is one knowledge module in a larger English-learning system. Examples
should not be more elementary than material suitable for an IELTS 7 learner,
but that is only a vocabulary-and-complexity benchmark. The deck is not an
IELTS course and does not train or predict an IELTS score.

### 1.1 What the deck does not train

Do not add:

- speaking drills, recording loops, or timed answers;
- pronunciation or prosody training;
- fluency, delivery, or discourse-organization exercises;
- unrelated tense, article, clause, or vocabulary lessons; or
- artificial “advanced English” included only to look difficult.

The deck teaches and reviews preposition knowledge. The learner practices
speaking, writing, reading, and listening elsewhere.

### 1.2 Division of responsibility

The content system is responsible for:

- selecting enough useful knowledge;
- organizing it into understandable subdecks;
- writing correct and natural AmE;
- making each card test one clear decision;
- explaining genuine distinctions and alternatives; and
- exporting only validated cards.

Anki is responsible for:

- spaced repetition;
- review intervals;
- daily new-card limits;
- forgetting and relearning schedules; and
- mixing due cards during ordinary review.

Do not create duplicate cards merely to increase review frequency. Anki
already repeats a card according to the learner's performance.

## 2. What “complete” means

The deck is not a dictionary of every preposition-related expression in
English. It aims to be complete for a practical, C1-oriented general-English
knowledge resource.

| Area | Coverage promise |
|---|---|
| Time, place, and movement systems | Cover the major productive AmE distinctions and their important exceptions. |
| Abstract preposition meanings | Cover common relationships needed in general, academic, and professional English. |
| Dependent prepositions | Cover a curated productive core of useful verb, adjective, participle, and noun combinations. |
| Fixed and multiword expressions | Cover common reusable expressions, including neutral and broadly useful formal forms. |
| No-preposition and grammar traps | Cover common extra-preposition, missing-preposition, complement, and placement errors. |
| Rare idioms and specialist formulas | Exclude unless the learner later has a real need for them. |

The resource is:

- **family-complete**: every subdeck and coverage family in Sections 3 and 4
  must be audited;
- **item-selective**: individual lexical combinations enter only when they are
  useful in contemporary AmE;
- **organized**: every item has exactly one home subdeck; and
- **extendable**: future learner questions can add missing items without
  changing the overall structure.

The final claim is:

> Complete for the defined C1-oriented AmE preposition resource.

Never claim:

> Every possible use of every English preposition.

## 3. Subdeck architecture

Use one parent deck with numerically ordered subdecks:

```text
EN::Prepositions
├── 01 Time
├── 02 Place
├── 03 Movement
├── 04 Abstract Relationships
├── 05 Verb + Preposition
├── 06 Adjective and Participle + Preposition
├── 07 Noun + Preposition
├── 08 Fixed and Multiword Expressions
└── 09 No Preposition and Grammar Traps
```

The numeric prefixes are part of the deck names. They keep filesystem order and
Anki subdeck order stable.

### 3.1 No batch or tag system

Do not add:

- curriculum batches;
- batch activation;
- `intro_order`;
- `SEQUENCE.md`;
- filtered-deck instructions;
- sequence tags;
- family tags; or
- a tag-based scheduling workflow.

All validated cards are included in one import TSV. The learner can:

- study one subdeck directly;
- study the parent deck to review across subdecks; and
- choose the daily new-card limit in Anki.

The TSV Deck column routes each card to its subdeck. Tags are not required.

### 3.2 One item, one home

Some expressions could be described by several grammar labels. Do not create
duplicates. Assign one home by this routing order:

1. A time meaning goes to `01 Time`.
2. A static place meaning goes to `02 Place`.
3. A movement, direction, or path meaning goes to `03 Movement`.
4. A zero-preposition or grammar-form problem goes to
   `09 No Preposition and Grammar Traps`.
5. A combination selected by a verb goes to `05 Verb + Preposition`.
6. A combination selected by an adjective or participle goes to
   `06 Adjective and Participle + Preposition`.
7. A combination selected by a noun goes to `07 Noun + Preposition`.
8. A fixed or multiword expression goes to
   `08 Fixed and Multiword Expressions`.
9. Any remaining semantic relationship goes to
   `04 Abstract Relationships`.

Examples:

| Item | Home |
|---|---|
| `by` versus `until` | `01 Time` |
| `across` versus `through` | `03 Movement` |
| `result in` / `result from` | `05 Verb + Preposition` |
| `responsible for` | `06 Adjective and Participle + Preposition` |
| `impact on` | `07 Noun + Preposition` |
| `because of` | `08 Fixed and Multiword Expressions` |
| `from my perspective` | `08 Fixed and Multiword Expressions` |
| `discuss the issue` | `09 No Preposition and Grammar Traps` |

The classification is a filing decision, not a claim that the expression has
only one grammatical property.

### 3.3 Source and output layout

Create:

```text
EN/cards/prepositions/
├── 01-time.md
├── 02-place.md
├── 03-movement.md
├── 04-abstract-relationships.md
├── 05-verb-preposition.md
├── 06-adjective-participle-preposition.md
├── 07-noun-preposition.md
├── 08-fixed-multiword-expressions.md
├── 09-no-preposition-grammar-traps.md
├── coverage.tsv
├── AUDIT.md
└── anki-import.tsv

EN/cards/tools/build_preposition_import.py
```

Use one Markdown source per subdeck and one final import TSV for the entire
preposition resource.

## 4. Coverage taxonomy

The following list defines what must be investigated. It does not dictate a
card count. The inventory determines how many atomic knowledge items exist.

### 4.1 `01 Time`

Cover:

1. **Clock and reference points**
   - clock times, noon, midnight, night, moments, ages, and stages;
   - fixed chunks such as `at night`, `at the moment`, and `at the time`.
2. **Days, dates, and named occasions**
   - days, dates, holidays, birthdays, and day-linked periods;
   - forms such as `on Monday morning`.
3. **Periods**
   - months, years, seasons, decades, centuries, and parts of the day;
   - future time expressed with `in`.
4. **No-preposition time phrases**
   - `last`, `next`, `this`, `every`, `each`, and `all`.
5. **Duration**
   - `for`, `during`, `over`, and `throughout`.
6. **Starting points**
   - `since` and `from`.
7. **Deadlines and continuation**
   - `by`, `until`, `through`, and `up to`.
8. **Ranges**
   - `from ... to/through` and `between ... and`.
9. **Sequence and temporal distance**
   - `before`, `after`, `within`, `ago`, `later`, `prior to`, and
     `following`.
10. **Timing contrasts and fixed chunks**
    - `on time`, `in time`, `by the time`, `over time`, `at times`, and
      `from time to time`.

The inventory must distinguish different constructions involving the same
word. For example, `at night`, `on Friday night`, `during the night`, and
`last night` are separate decisions.

### 4.2 `02 Place`

Cover:

1. point, activity, enclosed-area, larger-area, and surface viewpoints;
2. `at/in/on` with homes, work, schools, hospitals, prisons, beds, offices,
   meetings, and events;
3. addresses, streets, intersections, floors, entrances, exits, stops, and
   routes;
4. cities, countries, regions, islands, coasts, borders, and parts of an area;
5. `above/over`, `below/under`, `between/among`, `beside/next to`,
   `near/by`, `opposite/across from`, `in front of/behind`,
   `inside/outside`, and `beyond`;
6. edges, centers, tops, bottoms, fronts, and backs;
7. static location in different kinds of transport; and
8. websites, documents, files, platforms, calls, chats, and online meetings.

Cards must provide enough context to establish the intended viewpoint. Do not
pretend that one abstract slogan such as “at = point” explains every normal
expression.

### 4.3 `03 Movement`

Cover:

1. destination and orientation: `to`, `toward`, and common no-`to` patterns;
2. source and separation: `from`, `out of`, `off`, and `away from`;
3. boundary change: `in/into`, `on/onto`, `out/out of`, and `off`;
4. path: `across`, `through`, `along`, `past`, and `around`;
5. vertical and obstacle movement: `over`, `under`, `up`, and `down`;
6. arrival, departure, return, entry, approach, and reach patterns; and
7. getting into, out of, on, and off different kinds of transport.

Meaning contrasts belong here when movement is the deciding meaning.

### 4.4 `04 Abstract Relationships`

Cover common productive meanings involving:

1. **Agent, instrument, method, and channel**
   - `by`, `with`, `through`, and `via`.
2. **Cause, source, and result**
   - ordinary semantic uses of `from`, `through`, `for`, and related forms;
   - combinations in which a particular verb, adjective, participle, or noun
     requires the preposition route to Subdecks 05–07.
3. **Purpose, beneficiary, exchange, and intended use**
   - central uses of `for` and `to`.
4. **Topic, reference, and scope**
   - `about`, `on`, and `regarding`.
5. **Comparison, resemblance, role, concession, exception, addition, and
   replacement**
   - `like/as`, `unlike`, `despite`, `except`, and related single-word forms.
6. **Association, composition, possession, and material**
   - productive contrasts involving `of`, `from`, `with`, and `by`.
7. **Measurement, rate, price, age, and numerical change**
   - `at`, `by`, `to`, `from ... to`, `of`, and `per`.
8. **State and circumstance**
   - broadly productive uses expressing risk, pressure, control, condition,
     and responsibility when they are not better treated as fixed chunks.

### 4.5 `05 Verb + Preposition`

Build a curated productive core covering high-value verbs for:

- dependence and reliance;
- cause, result, contribution, and influence;
- participation and engagement;
- focus and concentration;
- application, payment, and investment;
- communication, apology, agreement, and disagreement;
- provision, supply, prevention, and protection;
- coping, dealing, benefiting, and suffering;
- reference, response, and attention; and
- verb + object + preposition patterns.

Examples include:

- `depend/rely on`;
- `contribute/lead to`;
- `result in/from`;
- `focus/concentrate on`;
- `participate/engage in`;
- `apply for/to`;
- `apologize to someone for something`;
- `provide someone with something`;
- `prevent someone from V-ing`;
- `cope/deal with`; and
- `benefit/suffer from`.

This is not permission to include every verb found in a dictionary.

### 4.6 `06 Adjective and Participle + Preposition`

Cover useful combinations expressing:

- interest and concern;
- awareness and knowledge;
- responsibility and capability;
- relevance and relationship;
- similarity and difference;
- dependence and independence;
- satisfaction and dissatisfaction;
- benefit, harm, suitability, and availability;
- cause and association in participial/passive forms; and
- emotional or evaluative reactions.

Examples include:

- `interested in`;
- `concerned about`;
- `aware of`;
- `responsible for`;
- `capable of`;
- `relevant to`;
- `similar to`;
- `different from`;
- `dependent on`;
- `satisfied with`;
- `beneficial/harmful to`;
- `based on`; and
- `associated with`.

### 4.7 `07 Noun + Preposition`

Cover useful combinations involving:

- reasons, causes, effects, and impacts;
- solutions, approaches, answers, and responses;
- increases, decreases, changes, and differences;
- demand, need, access, and opportunity;
- attitudes, opinions, confidence, and concern;
- relationships, connections, and comparisons;
- advantages, disadvantages, benefits, and costs;
- responsibility, control, and influence; and
- common nouns whose countability or article choice affects the expression.

Examples include:

- `reason for`;
- `impact/effect on`;
- `solution/approach to`;
- `increase/decrease in`;
- `demand/need for`;
- `access to`;
- `attitude toward`;
- `confidence in`;
- `relationship between`;
- `advantage/disadvantage of`; and
- `response to`.

### 4.8 `08 Fixed and Multiword Expressions`

Cover common reusable expressions for:

- cause and result;
- concession;
- addition and exception;
- substitution and preference;
- reference and scope;
- response and relationship;
- representation and agency;
- conformity and basis;
- stance and qualification;
- practical versus theoretical framing;
- conditions and time horizons; and
- broadly useful formal or academic communication.

Candidates include:

- `because of`, `due to`, and `as a result of`;
- `in spite of` and `regardless of`;
- `in addition to`, `apart from`, and `except for`;
- `instead of`;
- `according to`;
- `in terms of`, `with regard to`, and `with respect to`;
- `in response to` and `in relation to`;
- `on behalf of`;
- `on the basis of` and `in line with`;
- `from my perspective` and `in my view`;
- `on the one hand` / `on the other hand`;
- `to some extent`;
- `in practice` / `in theory`;
- `in the short/long term`; and
- `under certain circumstances`.

Include a broadly useful formal expression when it improves general academic
or professional English. Exclude archaic, legalistic, or domain-locked
formulas.

### 4.9 `09 No Preposition and Grammar Traps`

Cover:

1. verbs that commonly take a direct object without the learner's expected
   preposition, including `discuss`, `enter`, `reach`, `mention`, and
   `approach`;
2. constructions where a preposition is required but often omitted;
3. preposition + noun, pronoun, or `V-ing`;
4. prepositional `to` versus infinitival `to`;
5. natural preposition placement in questions and relative clauses;
6. formal fronted placement for recognition and broadly useful writing;
7. pronoun form after a preposition;
8. article or determiner choices inseparable from a fixed prepositional
   expression;
9. preposition versus verb-particle boundaries needed to route a card; and
10. common Mandarin-transfer errors not already housed in Subdecks 01–08.

Do not turn this subdeck into a general grammar-error deck. The preposition
decision must remain central.

## 5. Inclusion and evidence policy

### 5.1 Include an item when

The item must satisfy both:

1. the central learning decision is a preposition, no preposition, a fixed
   prepositional expression, or the complement controlled by a preposition;
2. it is useful in contemporary general, academic, or professional AmE.

Prioritize items that are:

- broadly useful across topics;
- difficult to infer from a simple rule;
- easily confused with another normal form;
- likely to change meaning when the form changes;
- common learner errors; or
- reusable as a complete chunk.

### 5.2 Exclude or route elsewhere

Exclude:

- pure discourse markers with no preposition decision, such as `however`;
- particle-only phrasal verbs such as `give up`;
- rare idioms;
- literary, archaic, legalistic, or specialist formulas;
- vocabulary whose only purpose is to make a card look advanced; and
- grammar whose central decision belongs to another English module.

### 5.3 Evidence standard

Use:

- contemporary AmE dictionaries for accepted form, meaning, and register;
- corpus evidence when naturalness, register, or alternatives are unclear;
- reputable learner references to discover contrasts and common errors; and
- the learner's real questions to identify omissions and priorities.

Do not:

- require a `frequency_band`;
- rank every item through COCA;
- store corpus-frequency numbers in the card;
- use frequency to control Anki intervals; or
- use *English Grammar in Use* units as the scope, order, or authority.

Language frequency may be consulted informally to reject an obscure candidate.
It is not part of the manifest or scheduling system.

### 5.4 Validation rule

Only validated cards enter `anki-import.tsv`.

If a candidate remains uncertain:

- keep it as `proposed` in `coverage.tsv`;
- record the unresolved question in `AUDIT.md`;
- do not export it; and
- do not create a “suspended” row in the final TSV.

The resource must prefer a visible gap over teaching an uncertain answer.

## 6. Coverage manifest

Create:

```text
EN/cards/prepositions/coverage.tsv
```

Use these columns:

| Column | Meaning |
|---|---|
| `item_id` | Stable identifier for the knowledge item inside the source repository. |
| `subdeck` | One of the nine numeric subdeck names. |
| `topic` | Short human-readable topic within the subdeck. |
| `target_form` | The pattern, choice, or correction being learned. |
| `meaning_or_distinction` | Precise meaning or contrast. |
| `construction` | Reusable syntactic shape. |
| `confusables` | Plausible competing forms or common wrong forms. |
| `card_type` | `chunk`, `context`, `contrast`, or `repair`. |
| `register` | `neutral`, `conversational`, `formal`, `academic`, or a concise combination. |
| `source_file` | Numeric Markdown source filename. |
| `card_id` | Card heading that covers the item. |
| `status` | `proposed`, `validated`, or `excluded`. Only `validated` items may be exported. |
| `notes` | Clarification, evidence note, or exclusion reason. |

Do not add:

- frequency fields;
- exposure quotas;
- lexical-host fields;
- batch or sequence fields;
- tag fields; or
- suspension state.

### 6.1 Atomicity

One manifest row represents one reusable retrieval decision.

Split rows when:

- one form has materially different meanings;
- different alternatives must be chosen in different contexts;
- one row would require two unrelated answers; or
- a learner could know one part while not knowing the other.

Examples:

- `by + deadline` differs from `by + agent`;
- `on time` differs from `in time to + verb`;
- `at night` differs from `on Friday night`;
- `impact on + noun` differs from the surface meaning of `on`;
- `by` versus `until` may be one contrast item when the retrieval decision is
  precisely that comparison.

### 6.2 Card count

Do not choose a card count in advance.

Default to one card per atomic item. Use Anki repetition to reinforce it.

Create an additional card only when it tests a genuinely different decision,
for example:

- a meaning contrast not captured by the original card;
- a zero-preposition repair problem;
- a newly discovered learner error that the existing card cannot test; or
- a separate construction that should have been a separate manifest item.

Do not generate a `chunk` card and a `context` card for every item merely to
increase exposure.

The final card count is the number required to represent all validated items
clearly and without duplication.

## 7. Card model

### 7.1 Governing rule

Each card tests exactly one retrieval decision.

Anki schedules one interval per card. A card containing several unrelated
questions cannot be graded fairly. Therefore:

- do not place unrelated items on one Front;
- do not group several answers merely because they share a category;
- do not reveal the answer family in the Front title; and
- let Anki mix due cards during review.

A `contrast` card may contain two minimal-pair lines because distinguishing the
pair is one decision.

### 7.2 Visible fields

Every imported note has exactly:

- Front
- Back

The special Deck column routes the note and is not a visible note field.

Do not use the LeetCode field schema.

### 7.3 Card types

#### `chunk`

Use for a fixed lexical combination or reusable pattern.

Front:

```text
confidence ___ + noun
(trust in a person, institution, or ability)
```

Back:

```text
confidence in + noun

Used for the person, institution, or ability that is trusted.

• Public confidence in local government has declined.
• She has complete confidence in her ability to lead the project.
```

#### `context`

Use when the surrounding situation is necessary to choose the form.

Front:

```text
The research team must submit its revised proposal ___ Friday.
```

Back:

```text
The research team must submit its revised proposal by Friday.

by Friday = no later than Friday. Use until for an action or state that
continues up to that time.
```

#### `contrast`

Use when the comparison itself is the knowledge.

Front:

```text
1. We have to submit the revised proposal ___ Friday. (completion)
2. The registration desk will stay open ___ Friday. (continuation)
```

Back:

```text
1. by Friday
2. until Friday

by = no later than the endpoint.
until = continuing up to the endpoint.
```

#### `repair`

Use when the learner must notice an extra, missing, or incorrect preposition.
The Front has no blank.

Front:

```text
Fix if wrong:
The panel discussed about several alternatives before reaching a decision.
```

Back:

```text
The panel discussed several alternatives before reaching a decision.

discuss takes a direct object. Compare talk about, which requires about.
```

Some repair cards must already be correct:

```text
Front:
Fix if wrong:
The committee agreed on a revised timeline.

Back:
Correct as written.

agree on = reach a shared decision about something.
Also OK: agree to a timeline = accept a timeline that was proposed.
```

This prevents “every repair card is wrong” from becoming a shortcut.

### 7.4 Front rules

- Give enough context to identify the intended meaning.
- Do not print `Ø` on the Front.
- Do not use a broad grammar label as the question.
- Do not include several unrelated blanks.
- Keep vocabulary natural and useful.
- Keep the preposition decision more salient than the surrounding vocabulary.
- A learner may answer mentally, in writing, or aloud; the deck does not
  prescribe speaking practice.

### 7.5 Back rules

The Back must:

- show the complete chunk, sentence, or correction;
- explain a real distinction when the answer is not self-evident;
- give two or three examples on a `chunk` card;
- name another normal answer with `Also OK:` when that particular Front
  genuinely permits it; and
- distinguish alternatives rather than marking a natural answer wrong.

Do not add:

- a generic `GENERALIZATION` section;
- unrelated example paragraphs;
- a chapter-length explanation;
- a bare preposition without the word or expression it belongs with, or
  without a completed sentence; or
- an alternative that is grammatical only after changing the intended
  meaning, unless that meaning difference is explained.

### 7.6 Context variation

When an item appears in more than one example:

- keep the word that selects the preposition when it is part of the pattern;
- vary the subject, complement, situation, and topic;
- for semantic choices such as `by + deadline`, vary the surrounding verb and
  endpoint;
- describe the relationship in plain learner-facing language; and
- do not claim transfer by replacing the anchor word with a different pattern.

For example, vary:

- `confidence in local government`;
- `confidence in the education system`;
- `confidence in her ability to lead`.

The anchor remains `confidence`; the context changes.

### 7.7 Ambiguity

- A card must have one normal answer in its intended context or explicitly
  accept alternatives.
- Add context when several forms would otherwise fit.
- Put `Also OK:` on the Back only when the actual Front permits the
  alternative.
- Avoid prompts such as `___ the rain` when `because of`, `due to`, and
  `despite` would all create different grammatical meanings.
- It is acceptable to supply part of a frame, such as
  `because ___ severe weather`, to isolate the target.

#### Closed-answer test

The learner must be able to grade an answer without deciding between several
equally natural words or constructions.

Before validating a Front, list the common completions that fit the exact
sentence without changing any printed words. Include:

- another preposition with the same intended meaning;
- a multiword construction that fits the same blank, such as `higher than`
  where `above` was intended;
- an accepted AmE variant; and
- a different construction that the wording itself makes salient.

Then apply this rule:

1. If one completion is clearly selected by the syntax and intended meaning,
   keep the Front.
2. If a limited secondary variant is normal, use `Also OK:` only when the
   learner can still grade the main decision easily.
3. If several common completions compete, rewrite the surrounding sentence so
   the answer space becomes closed.
4. If the distinction inherently overlaps and cannot be made objective in a
   natural sentence, do not use it as a free-answer cloze. Exclude it or teach
   it through another independently approved card design.

`Also OK:` is not a cleanup mechanism for an open-ended Front. A card that
requires the learner to judge a subtle stylistic preference has failed this
test.

Examples of failed Fronts:

- `Inflation remains ___ the target.` admits `above`, `over`, and
  `higher than`.
- `She is ___ the office today.` commonly admits both `at` and `in` in AmE.

The problem in those examples is the prompt, not the learner's answer.

### 7.8 Learner-approved style baseline

The learner accepted the revised 24-card `PILOT.md` on 2026-07-30. Future
authors and reviewers must preserve the following decisions:

- Keep the four demonstrated card forms: `chunk`, `context`, `contrast`, and
  `repair`.
- Preserve retrieval on the Front. Do not respond to ambiguity by turning
  every card into an answer-revealing explanation card.
- The learner particularly values `contrast` cards when the comparison is a
  genuine, reusable distinction. A strong contrast card uses two related
  lines, explains the boundary on the Back, and records a normal secondary
  form with `Also OK:` when applicable.
- Do not manufacture a contrast merely because two prepositions occur in the
  same topic. Highly overlapping choices with no objective boundary must be
  rewritten or excluded.
- `Also OK:` is valuable because it makes self-grading explicit. It must name
  the normal alternative that the actual Front permits; it must not conceal an
  uncontrolled answer space.
- Keep examples natural and useful at an IELTS-7/C1-oriented vocabulary
  benchmark, while making the preposition decision easier to notice than the
  surrounding vocabulary.
- A learner must be able to mark an answer correct or incorrect from the Back
  without making an unsupported judgment about subtle stylistic preference.

Select the card type by the knowledge being retrieved, not by a quota:

1. Use `repair` when the central skill is detecting an extra, missing, or
   incorrect preposition. Include some already-correct Fronts.
2. Use `contrast` when knowing one form requires distinguishing it from a
   coherent competing form, meaning, or complement structure.
3. Use `chunk` when a lexical anchor or fixed expression selects the
   preposition and should be learned as a unit, such as `confidence in` or
   `account for`.
4. Use `context` when a productive semantic rule must be applied to a new
   situation, such as `at + complete address`, and no explicit paired contrast
   is the main lesson.

Surface format alone does not determine the type. The difference between
`chunk` and `context` is the source of the answer: lexical selection versus a
productive situational rule.

## 8. Production workflow

### Phase 0 — Review this plan

Deliverable:

- reviewed and corrected `PREPOSITION_DECK_PLAN.md`.

Gate:

- the user accepts the learning target, subdeck structure, coverage taxonomy,
  card types, and validation standard.

Do not generate the full resource while the plan remains disputed.

### Phase 1 — Build the inventory

For each of the nine subdecks:

1. inspect every required category in Section 4;
2. propose atomic manifest items;
3. remove duplicates and split overloaded items;
4. assign exactly one home subdeck;
5. mark register and important confusables;
6. select the most suitable card type; and
7. mark unresolved questions visibly.

Deliverables:

- `coverage.tsv`;
- counts by subdeck and card type;
- an excluded/deferred summary; and
- a list of unresolved AmE or scope questions.

Gate:

- every Section 4 category has been reviewed;
- no item appears in two subdecks;
- no unresolved item is treated as validated; and
- the user can inspect the exact planned knowledge scope before bulk cards are
  written.

### Phase 2 — Audit the inventory

Review for:

- a missing major preposition distinction;
- lexical lists expanding without practical value;
- category duplicates;
- items too broad to test;
- items so narrow that they only memorize one sentence;
- AmE and register problems;
- missing Mandarin-transfer traps; and
- items that belong in another English module.

Correct the manifest before writing the pilot.

### Phase 3 — Produce the pilot

Create a small pilot that demonstrates:

- all four card types;
- several subdecks;
- a true meaning contrast;
- a zero-preposition repair card;
- an already-correct repair card;
- a Front with `Also OK:` on the Back;
- neutral, conversational, and formal contexts; and
- the intended explanation depth.

Gate:

- the user approves the card shape, vocabulary level, ambiguity handling, and
  subdeck organization.

Do not bulk-generate before this approval.

**Gate status:** Satisfied on 2026-07-30. The accepted baseline is recorded in
Section 7.8 and `PILOT.md`.

### Phase 4 — Implement source files and builder

Create the file layout in Section 3.3 and implement the builder contract in
Section 9.

### Phase 5 — Generate one subdeck at a time

For each numeric source file:

1. write cards only for validated manifest items;
2. keep source order from core decisions to finer distinctions;
3. run the builder validation;
4. run a linguistic review;
5. update the manifest `card_id`; and
6. finish the subdeck before moving to the next.

The source-file order is the initial learning order within that subdeck.
There is no batch layer.

### Phase 6 — Integrated review

After all subdecks exist, run separate passes for:

- coverage;
- semantic correctness;
- natural AmE;
- register;
- alternative answers;
- duplicate cards;
- classification;
- card clarity;
- source/build consistency; and
- a transfer audit using new sentences and contexts.

### Phase 7 — Final build

Generate:

```text
EN/cards/prepositions/anki-import.tsv
```

The file contains every validated card, routed to its numeric subdeck.
Unvalidated candidates are not included.

## 9. Source and builder contract

### 9.1 Canonical source syntax

Each numeric Markdown source uses:

```markdown
## TIME-001

<!-- card
item: TIME-DEADLINE-BY
type: context
status: validated
-->

### Front

The research team must submit its revised proposal ___ Friday.

### Back

The research team must submit its revised proposal by Friday.

by Friday = no later than Friday. Use until for continuation.
```

Rules:

- the heading is a stable repository card ID;
- `item` matches exactly one manifest row;
- `type` is `chunk`, `context`, `contrast`, or `repair`;
- `status` is `validated` before export;
- the source filename determines the Anki subdeck;
- metadata is not displayed on the card; and
- a `contrast` item remains one manifest decision even when its Front has two
  minimal-pair lines.

Stable update-in-place behavior after changing an already imported Front is
not part of version 0.4. If repeated post-import Front rewrites become common,
add and test Anki GUID support in a later version. Do not claim that the
current TSV updates renamed Fronts automatically.

### 9.2 TSV contract

The final TSV contains:

1. special Deck column;
2. Front;
3. Back.

Use Anki headers equivalent to:

```text
#separator:tab
#html:true
#deck column:1
```

There is:

- one final TSV;
- no Tags column;
- no batch or sequence field;
- no suspension state; and
- no frequency field.

### 9.3 Required builder behavior

`build_preposition_import.py` must:

1. discover the nine numeric source files in numeric order;
2. preserve card order within each source file;
3. derive the exact `EN::Prepositions::<numeric subdeck>` Deck value from the
   filename;
4. parse exactly one Front and one Back per card;
5. parse card ID, item ID, type, and status;
6. reject duplicate card IDs and duplicate visible Fronts;
7. reject missing or duplicated manifest mappings;
8. reject any exported card whose status is not `validated`;
9. reject a card placed in a subdeck different from its manifest row;
10. reject raw tabs or raw newlines in final TSV fields;
11. convert Markdown line breaks and lists to safe Anki HTML;
12. reject `Ø` on a Front;
13. reject a bare-preposition Back;
14. reject a non-contrast card containing several independent questions;
15. confirm that repair cards include both wrong and already-correct examples
    across the relevant subdeck or full resource;
16. report manifest items that are validated but have no card;
17. report cards whose manifest item is excluded, proposed, or missing;
18. emit deterministic output with exactly Deck, Front, and Back;
19. support a non-writing validation or self-test mode; and
20. print counts by subdeck and card type.

The builder verifies structure. It cannot prove that English is natural or
that an alternative answer is impossible; those require linguistic review.

## 10. Quality gates

### 10.1 Coverage

- Every Section 4 category has been investigated.
- Every validated manifest item has exactly one home subdeck.
- Every exported card maps to a validated item.
- Exclusions and unresolved candidates are visible.
- No card is counted as coverage merely because its answer appears in a note
  on another card.

### 10.2 Semantic and AmE review

Use the strongest model capability available when it materially improves
quality. Model cost or capability must not be reduced at the expense of
teaching incorrect English.

Reviewers must verify:

- every answer is grammatical and natural in the supplied AmE context;
- no normal answer is silently marked wrong;
- meaning-changing alternatives are explained;
- dependent combinations use the correct anchor word and complement;
- fixed expressions contain the correct article, determiner, number, and
  complement form;
- formal expressions are broadly useful rather than legalistic or inflated;
  and
- original examples do not copy a reference source.

Use dictionaries or corpus evidence to resolve uncertainty. If uncertainty
remains, do not export the card.

### 10.3 Card quality

- One retrieval decision per card.
- No Front reveals a category answer.
- Vocabulary supports rather than obscures the target.
- `chunk` cards give the pattern, a useful explanation, and two or three
  natural examples.
- `context` cards contain enough information for a fair answer.
- `contrast` cards compare one coherent distinction.
- `repair` cards do not all contain errors.
- `Also OK:` appears whenever that particular Front has another normal answer.
- Notes are detailed when needed and absent when they add nothing.

### 10.4 Classification and ordering

- Every item follows the routing rule in Section 3.2.
- No duplicate item exists in multiple subdecks.
- Numeric filenames and Deck paths agree.
- Within each file, core and broadly useful knowledge appears before finer or
  more formal distinctions.
- No hidden batch or tag dependency exists.

### 10.5 Build integrity

- A fresh validation succeeds.
- A fresh build produces the same output.
- TSV rows have exactly three columns.
- Deck, Front, and Back contain no raw tabs or line breaks.
- Card and manifest counts agree.
- `AUDIT.md` records counts, findings, corrections, and the final result.

### 10.6 Transfer audit

Create unseen test sentences that:

- use situations and complements not copied from the cards;
- cover every subdeck;
- emphasize meaning contrasts and common learner traps;
- include both neutral and broadly useful formal contexts; and
- test whether the same knowledge applies outside the memorized example.

For dependent combinations, retain the anchor word and vary its subject,
complement, or context. Do not replace the anchor with a different pattern and
call that transfer.

The artifact is not final merely because the TSV builds. It is final when the
coverage, language, classification, and transfer audits pass.

## 11. Multi-agent execution

If work is delegated:

- give each worker ownership of one or more numeric source files;
- do not let several workers edit `coverage.tsv` or the same source file
  concurrently;
- workers may return proposed manifest slices for primary integration;
- the primary agent owns deduplication, routing, wording consistency, builder
  integration, and final output;
- use a high-capability model for semantic and AmE review when it improves
  confidence;
- uncertainty must remain visible and must not become a forced single answer;
- reviewers inspect the integrated resource, not only one worker's slice; and
- all agents preserve unrelated workspace edits.

A reasonable split is:

1. time, place, and movement;
2. abstract relationships plus verb combinations;
3. adjective, participle, and noun combinations;
4. fixed expressions, grammar traps, integration, and independent review.

The learner-facing result remains one parent deck with nine subdecks and one
import TSV.

## 12. Maintenance and future card requests

When the learner asks a preposition question and explicitly requests a card:

1. answer the language question first;
2. read this plan, `coverage.tsv`, and the nearest numeric source file;
3. search for the same decision and close patterns;
4. identify the one correct home subdeck;
5. improve the nearest existing card when it already covers the item;
6. otherwise add a proposed manifest row and validate it before writing the
   card;
7. avoid adding a second card solely for extra repetition;
8. update the manifest and source file;
9. run validation and rebuild the single import TSV; and
10. show the user the complete resulting card and identify the regenerated
    TSV.

If a new issue reveals that one item is overloaded, split the manifest item
and repair the affected card rather than adding an unclear exception.

### 12.1 Repeatedly failed cards

Repeated failure triggers diagnosis; it does not automatically prove that the
card or the learner is defective.

Check:

1. Does the Front admit another normal answer?
2. Is the surrounding vocabulary harder than the preposition?
3. Does the card accidentally contain two decisions?
4. Is the explanation missing the real meaning distinction?
5. Is another similar card causing interference?
6. Does the learner need a prerequisite explanation before retrieval?

Then:

- clarify or reformulate the card when it is defective;
- add `Also OK:` when the answer was unfairly narrow;
- split an overloaded item;
- temporarily stop studying a confusing card if interference is the problem;
  or
- add a genuinely different repair/contrast card only when it teaches a
  missing decision.

Record material reformulations in `AUDIT.md`.

## 13. Definition of done

This legacy definition is retained as module-level quality evidence. It no
longer authorizes a standalone final deck; master completion and export follow
`CONNECTION_DECK_PLAN.md`.

The resource is complete only when:

- the user has accepted this plan and the pilot;
- all nine subdecks exist;
- every Section 4 category has been inventoried and audited;
- all exported cards are validated;
- every item has exactly one home subdeck;
- all cards pass semantic, AmE, ambiguity, register, and card-quality review;
- no uncertain item enters the final TSV;
- the transfer audit reveals no systematic gap;
- the source files, manifest, audit, builder, and TSV agree;
- a fresh deterministic build succeeds; and
- the final claim remains limited to the defined C1-oriented AmE preposition
  resource.

Anki review frequency is not part of content completion. Anki schedules the
validated knowledge after import.

## 14. Instructions for the next external reviewer

Review this plan without generating the deck. Report:

1. **Blocking** — cannot be executed or can teach incorrect English.
2. **Major** — substantial scope, classification, card-design, or validation
   weakness.
3. **Minor** — wording or implementation detail that does not change the
   learning contract.

For every finding:

- cite the section;
- explain the learner or implementation consequence;
- propose a concrete revision; and
- distinguish a defect from a reasonable design choice.

Explicitly test:

- whether the goal is clearly a general-English knowledge resource rather than
  a speaking course;
- whether the nine subdecks cover the productive domain without becoming an
  unbounded dictionary;
- whether the one-home routing rule prevents category duplication;
- whether the four card types cover the knowledge decisions fairly;
- whether one card per atomic item plus Anki repetition is sufficient;
- whether ambiguity and natural alternatives are handled fairly;
- whether the builder can produce one directly importable TSV with numeric
  subdecks;
- whether unvalidated content is reliably excluded;
- whether another session can execute the plan without this conversation; and
- whether any removed batch, tag, frequency, exposure, or suspension mechanism
  has accidentally returned.

Do not generate cards during this review.

## 15. References

- [American English — Teacher's Corner: Prepositions](https://americanenglish.state.gov/resources/teachers-corner-prepositions)
- [CEFR global scale](https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale)
- [Anki manual — Text Files](https://docs.ankiweb.net/importing/text-files.html)
- [Anki manual — Deck Options](https://docs.ankiweb.net/deck-options.html)

These references support the language variety, broad proficiency orientation,
and import behavior. None is treated as an exhaustive preposition syllabus.

## 16. Review record

### 0.1 → 0.2

External review introduced:

- one retrieval decision per card;
- `chunk`, `context`, `contrast`, and `repair` card types;
- repair cards that may already be correct;
- no `Ø` cue on the Front;
- `Also OK:` for genuine alternatives;
- corpus/frequency fields;
- batch sequencing and tags;
- suspended-card handling; and
- a C1 speech-and-writing target.

### 0.2 → 0.3

User clarification retained:

- the broad C1-oriented general-English knowledge goal;
- no speaking drills inside the deck;
- one retrieval decision per card;
- the four useful card types;
- high-capability semantic review; and
- only validated content in the final resource.

User clarification changed:

- numeric topic subdecks replace batches and tags;
- one Markdown source per subdeck and one final TSV replace `SEQUENCE.md`;
- one card per atomic item is the default; Anki handles repetition;
- `frequency_band` and ranked corpus evidence are removed;
- `lexical_hosts` is replaced by plain context-variation guidance;
- every item receives exactly one home subdeck instead of overlapping family
  metadata;
- uncertain content is excluded from the import instead of shipped
  suspended;
- stable Anki GUID update behavior is deferred; and
- no model ceiling is imposed when a stronger reviewer improves accuracy.

### 0.3 → 0.4

- Recorded completion of the inventory and independent audit.
- Added the learner-approved four-type pilot as the authoring baseline.
- Added the closed-answer test for competing vocabulary, constructions, and
  overlapping AmE forms.
- Clarified that the learner especially values genuine contrast cards with
  explicit `Also OK:` alternatives.
- Defined `chunk` as lexical or fixed-pattern retrieval and `context` as
  applying a productive semantic rule.
- Recorded Phase 3 acceptance and authorized Phases 4–7.
