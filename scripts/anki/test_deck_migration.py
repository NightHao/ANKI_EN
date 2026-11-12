"""Deck-root migration integration tests using temporary Anki collections.

Run with: python3 scripts/anki/test_deck_migration.py
Requires the actual Anki Python package; no mock decks or network sync.
"""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anki_sync import SyncAbort, apply_plan, build_plan, render_report, schema_stamp  # noqa: E402

VOCAB_FIELDS = ['Term', 'Priority', 'PartsOfSpeech', 'PronunciationHTML', 'TTS_Text', 'BackHTML']
CHILDREN = [
    '01 Prepositions and Prepositional Phrases',
    '02 Verb Patterns',
    '03 Adjective and Participle Patterns',
    '04 Noun Patterns',
    '05 Conjunctions and Clause Linkers',
    '06 Relative and Noun-Modifying Clauses',
    '07 Non-finite and Reduced Clauses',
    '08 Coordination and Parallelism',
    '09 Comparison, Degree, and Result Patterns',
]
OLD = {'patterns': 'EN::Patterns', 'vocabulary': 'EN::Vocabulary',
       'connections': 'EN::Connection Patterns'}
NEW = {'patterns': 'EN::01 Patterns', 'vocabulary': 'EN::02 Vocabulary',
       'connections': 'EN::03 Connection Patterns'}


class DeckMigrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.col = Collection(str(self.root / 'test.anki2'))
        mm = self.col.models
        vocab = mm.new('EN_Vocabulary')
        for name in VOCAB_FIELDS:
            mm.add_field(vocab, mm.new_field(name))
        template = mm.new_template('Card 1')
        template['qfmt'], template['afmt'] = '{{Term}}', '{{BackHTML}}'
        mm.add_template(vocab, template)
        mm.add(vocab)
        self.config = {
            'families': [
                {'name': 'patterns', 'export': 'patterns.tsv', 'notetype': 'Basic',
                 'fields': ['Front', 'Back'], 'deck_root': NEW['patterns'], 'sync_tags': False},
                {'name': 'vocabulary', 'export': 'vocab.csv', 'notetype': 'EN_Vocabulary',
                 'fields': VOCAB_FIELDS, 'deck_root': NEW['vocabulary'], 'sync_tags': True},
                {'name': 'connections', 'export': 'connections.tsv', 'notetype': 'Basic',
                 'fields': ['Front', 'Back'], 'deck_root': NEW['connections'], 'sync_tags': False},
            ],
            'limits': {'max_additions': 10, 'max_updates': 10},
        }
        self.names = OLD.copy()
        self.note_ids: dict[str, int] = {}
        self.write_exports()

    def tearDown(self) -> None:
        self.col.close()
        self.tmp.cleanup()

    def write_exports(self) -> None:
        (self.root / 'patterns.tsv').write_text(
            '#separator:tab\n#html:true\n#deck column:1\n'
            + NEW['patterns'] + '\tReusable frame\tPattern explanation\n', encoding='utf-8')
        (self.root / 'connections.tsv').write_text(
            '#separator:tab\n#html:true\n#deck column:1\n'
            + NEW['connections'] + '::' + CHILDREN[0]
            + '\tA preposition frame\tConnection explanation\n', encoding='utf-8')
        with (self.root / 'vocab.csv').open('w', encoding='utf-8', newline='') as handle:
            handle.write('#separator:Comma\n#html:true\n#notetype:EN_Vocabulary\n'
                         + '#deck:' + NEW['vocabulary'] + '\n'
                         + '#columns:' + ','.join(VOCAB_FIELDS + ['Tags']) + '\n')
            csv.writer(handle, lineterminator='\n').writerow(
                ['orange', 'ACTIVE', 'noun', '/ˈɔrɪndʒ/', 'orange', '<div>fruit</div>', 'pos::noun'])

    def add(self, kind: str, deck: str, values: list[str], tags: list[str] | None = None) -> int:
        note = self.col.new_note(self.col.models.by_name(kind))
        for i, value in enumerate(values):
            note.fields[i] = value
        note.tags = tags or []
        self.col.add_note(note, self.col.decks.id(deck))
        return note.id

    def populate(self, legacy: bool) -> None:
        names = OLD if legacy else NEW
        self.names = names.copy()
        for name in names.values():
            self.col.decks.id(name)
        for child in CHILDREN:
            self.col.decks.id(names['connections'] + '::' + child)
        self.note_ids['patterns'] = self.add(
            'Basic', names['patterns'], ['Reusable frame', 'Pattern explanation'])
        self.note_ids['connections'] = self.add(
            'Basic', names['connections'] + '::' + CHILDREN[0],
            ['A preposition frame', 'Connection explanation'])
        self.note_ids['vocabulary'] = self.add(
            'EN_Vocabulary', names['vocabulary'],
            ['orange', 'ACTIVE', 'noun', '/ˈɔrɪndʒ/', 'orange', '<div>fruit</div>'],
            ['pos::noun'])
        # This EN_Vocabulary note deliberately belongs to Patterns, NOT Vocabulary.
        self.note_ids['cross_family'] = self.add(
            'EN_Vocabulary', names['patterns'],
            ['lead to / result in / end up / turn out', 'ACTIVE', 'verb',
             '/liːd/', 'lead to', '<div>Outcome expressions</div>'])
        for i, nid in enumerate(self.note_ids.values()):
            card = self.col.get_note(nid).cards()[0]
            card.ivl, card.due, card.type, card.queue = 35 + i, 500 + i, 2, 2
            self.col.update_card(card)
            self.col.db.execute(
                'insert into revlog (id, cid, usn, ease, ivl, lastIvl, factor, time, type) '
                'values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                1700000000000 + i, card.id, -1, 3, 35 + i, 21, 2500, 4000, 1)

    def snapshot(self):
        return {
            'decks': sorted((int(d.id), d.name) for d in self.col.decks.all_names_and_ids()),
            'notes': self.col.db.all('select id, mid, flds, tags from notes order by id'),
            'cards': self.col.db.all(
                'select id, nid, did, type, queue, due, ivl, factor, reps, lapses '
                'from cards order by id'),
            'revlog': self.col.db.all('select * from revlog order by id'),
            'schema': schema_stamp(self.col),
        }

    def plan(self, changes=None):
        return build_plan(self.col, self.config, self.root, changes)

    def test_old_install_plans_only_three_deck_renames_without_writes(self) -> None:
        self.populate(legacy=True)
        before = self.snapshot()
        plan = self.plan()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual({name for name, _id, _old, _new in plan.deck_renames},
                         set(OLD))
        self.assertFalse(plan.empty)
        self.assertEqual((plan.additions, plan.updates, plan.renames, plan.removals,
                          plan.deck_mismatches), ([], [], [], [], []))
        self.assertEqual(plan.unchanged, {'patterns': 1, 'vocabulary': 1, 'connections': 1})
        self.assertIn('rename deck [connections]', render_report(plan, applied=False))
        self.assertNotIn('Anki already matches the repo', render_report(plan, applied=False))

    def test_native_rename_preserves_all_child_ids_notes_cards_reviews_and_settings(self) -> None:
        self.populate(legacy=True)
        before = self.snapshot()
        plan = self.plan()
        apply_plan(self.col, plan, self.config, self.root)
        after = self.snapshot()
        self.assertEqual(after['notes'], before['notes'])
        self.assertEqual(after['cards'], before['cards'])
        self.assertEqual(after['revlog'], before['revlog'])
        self.assertEqual(after['schema'], before['schema'])
        before_ids = {id: name for id, name in before['decks']}
        after_ids = {id: name for id, name in after['decks']}
        self.assertEqual(before_ids.keys(), after_ids.keys())
        for did, original in before_ids.items():
            expected = original
            for family in OLD:
                old, new = OLD[family], NEW[family]
                if original == old or original.startswith(old + '::'):
                    expected = new + original[len(old):]
                    break
            self.assertEqual(after_ids[did], expected)
        self.assertEqual(len([n for n in after_ids.values()
                              if n.startswith(NEW['connections'] + '::')]), 9)
        cross_note = self.col.get_note(self.note_ids['cross_family'])
        self.assertEqual(self.col.decks.name(cross_note.cards()[0].did), NEW['patterns'])
        self.assertTrue(self.plan().empty)
        self.assertEqual(self.plan().deck_renames, [])

    def test_already_migrated_install_is_noop(self) -> None:
        self.populate(legacy=False)
        before = self.snapshot()
        plan = self.plan()
        self.assertTrue(plan.empty)
        self.assertEqual(plan.deck_renames, [])
        self.assertEqual(plan.additions, [])
        self.assertEqual(self.snapshot(), before)
        apply_plan(self.col, plan, self.config, self.root)
        self.assertEqual(self.snapshot(), before)

    def test_second_run_is_idempotent(self) -> None:
        self.populate(legacy=True)
        apply_plan(self.col, self.plan(), self.config, self.root)
        after = self.snapshot()
        second = self.plan()
        self.assertTrue(second.empty)
        apply_plan(self.col, second, self.config, self.root)
        self.assertEqual(self.snapshot(), after)

    def test_conflicting_old_and_new_names_abort_before_writing(self) -> None:
        self.populate(legacy=True)
        self.col.decks.id(NEW['connections'])
        before = self.snapshot()
        with self.assertRaisesRegex(SyncAbort, 'both deck paths exist'):
            self.plan()
        self.assertEqual(self.snapshot(), before)

    def test_stale_preview_cannot_rename_when_new_deck_was_created(self) -> None:
        self.populate(legacy=True)
        plan = self.plan()
        self.col.decks.id(NEW['patterns'])
        before = self.snapshot()
        with self.assertRaisesRegex(SyncAbort, 'no longer safe'):
            apply_plan(self.col, plan, self.config, self.root)
        self.assertEqual(self.snapshot(), before)

    def test_fresh_install_creates_only_new_routing(self) -> None:
        plan = self.plan()
        self.assertEqual(plan.deck_renames, [])
        self.assertEqual(len(plan.additions), 3)
        apply_plan(self.col, plan, self.config, self.root)
        self.assertTrue(self.plan().empty)
        for deck in NEW.values():
            self.assertIsNotNone(self.col.decks.by_name(deck))
        for deck in OLD.values():
            self.assertIsNone(self.col.decks.by_name(deck))

    def test_note_identity_rename_is_separate_from_deck_rename(self) -> None:
        self.populate(legacy=True)
        before_id = self.note_ids['patterns']
        before_card = self.col.get_note(before_id).cards()[0].id
        path = self.root / 'patterns.tsv'
        path.write_text(path.read_text(encoding='utf-8').replace(
            'Reusable frame\t', 'Reusable frame revised\t'), encoding='utf-8')
        changes = {'renames': [{'family': 'patterns', 'from': 'Reusable frame',
                                'to': 'Reusable frame revised'}], 'removals': []}
        plan = self.plan(changes)
        self.assertEqual(len(plan.deck_renames), 3)
        self.assertEqual(len(plan.renames), 1)
        apply_plan(self.col, plan, self.config, self.root)
        note = self.col.get_note(before_id)
        self.assertEqual(note['Front'], 'Reusable frame revised')
        self.assertEqual(note.cards()[0].id, before_card)
        self.assertEqual(note.cards()[0].ivl, 35)
        self.assertEqual(self.col.db.scalar('select count(*) from revlog where cid=?', before_card), 1)
        self.assertTrue(self.plan(changes).empty)


if __name__ == '__main__':
    unittest.main()
