# Semantic owner index for EN Anki

The index is a retrieval aid, **not** an Anki deck or alternate canonical source.

- `groups.json` contains manually reviewed communicative functions,
  expression aliases, relation types, and current owning cards.
- `index.json` is generated from all three canonical Anki exports plus
  curated groups. It indexes **every exported card**, but only curated
  groups have reviewed semantic aliases.
- `scripts/find_cards.py` searches the groups and literal Front/Back text.
- `scripts/build_semantic_index.py` rebuilds/checks the index.

```
python3 scripts/find_cards.py "look up to" "the flip side"
python3 scripts/find_cards.py --meaning "respect admiration"
python3 scripts/build_semantic_index.py --check
python3 scripts/test_semantic_index.py
```

`variant` is an alternative form of the same basic expression.
`near_synonym` overlaps but may differ in register/meaning.
`related` shares a domain without claiming interchangeability.
`contrast` is a decision that matters; `core` is the group's anchor.

Meaning-search results are **candidates** ranked by lexical overlap with
semantic descriptors. They are not embedding similarity, proof of coverage,
or permission to merge cards. A semantic group is **not** a requirement to merge every member into one
card. Read actual cards before deciding whether a new expression is covered,
needs a Back addition, needs a grouped Front, or a new card. Editing a card
requires user approval, and changing first fields requires the Anki change
record. No vector database or new Anki note fields are required.
