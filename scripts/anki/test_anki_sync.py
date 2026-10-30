"""Offline tests for anki_sync planning and applying, using throwaway collections."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anki_sync import SyncAbort, apply_plan, build_plan, schema_stamp  # noqa: E402

VOCAB_FIELDS = ['Term', 'Priority', 'PartsOfSpeech', 'PronunciationHTML', 'TTS_Text', 'BackHTML']


class AnkiSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.col = Collection(str(self.root / 'c.anki2'))
        mm = self.col.models
        vocab = mm.new('EN_Vocabulary')
        for name in VOCAB_FIELDS:
            mm.add_field(vocab, mm.new_field(name))
        template = mm.new_template('Card 1')
        template['qfmt'], template['afmt'] = '{{Term}}', '{{BackHTML}}'
        mm.add_template(vocab, template)
        vocab['css'] = '.card {}'
        mm.add(vocab)
        (self.root / 'front.html').write_text('{{Term}}', encoding='utf-8')
        (self.root / 'back.html').write_text('{{BackHTML}}', encoding='utf-8')
        (self.root / 'style.css').write_text('.card {}', encoding='utf-8')
        self.config = {
            'families': [
                {'name': 'vocabulary', 'export': 'vocab.csv', 'notetype': 'EN_Vocabulary',
                 'fields': VOCAB_FIELDS, 'deck_root': 'EN::Vocabulary', 'sync_tags': True,
                 'templates': {'Card 1': {'front': 'front.html', 'back': 'back.html'}}, 'css': 'style.css'},
                {'name': 'connections', 'export': 'conn.tsv', 'notetype': 'Basic',
                 'fields': ['Front', 'Back'], 'deck_root': 'EN::Connection Patterns', 'sync_tags': False},
            ],
            'limits': {'max_additions': 10, 'max_updates': 10},
        }
        self.vocab_rows = [['apple', 'ACTIVE', 'noun', '/ˈæpəl/', 'apple', '<div>fruit</div>', 'pos::noun']]
        self.conn_rows = [['EN::Connection Patterns::01 Prepositions', 'Front &amp; one', 'Back one']]
        self.write_exports()
        self.add('EN_Vocabulary', 'EN::Vocabulary', self.vocab_rows[0][:6], ['pos::noun'])
        self.add('Basic', 'EN::Connection Patterns::01 Prepositions', self.conn_rows[0][1:])
        self.add('Basic', 'LeetCode', ['Two Sum', 'hash map'])

    def tearDown(self) -> None:
        self.col.close()
        self.tmp.cleanup()

    def write_exports(self) -> None:
        import csv
        with open(self.root / 'vocab.csv', 'w', encoding='utf-8', newline='') as handle:
            handle.write('#separator:Comma\n#html:true\n#notetype:EN_Vocabulary\n#deck:EN::Vocabulary\n')
            handle.write('#columns:' + ','.join(VOCAB_FIELDS + ['Tags']) + '\n')
            csv.writer(handle, lineterminator='\n').writerows(self.vocab_rows)
        lines = ['#separator:tab', '#html:true', '#deck column:1'] + ['\t'.join(r) for r in self.conn_rows]
        (self.root / 'conn.tsv').write_text('\n'.join(lines) + '\n', encoding='utf-8')

    def add(self, notetype: str, deck: str, values: list[str], tags: list[str] | None = None) -> int:
        note = self.col.new_note(self.col.models.by_name(notetype))
        for index, value in enumerate(values):
            note.fields[index] = value
        note.tags = tags or []
        self.col.add_note(note, self.col.decks.id(deck))
        return note.id

    def plan(self):
        return build_plan(self.col, self.config, self.root)

    def test_identical_collection_needs_no_changes(self) -> None:
        plan = self.plan()
        self.assertTrue(plan.empty)
        self.assertEqual(plan.unchanged, {'vocabulary': 1, 'connections': 1})

    def test_changed_back_updates_note_and_keeps_scheduling(self) -> None:
        nid = self.col.find_notes('Front:"Front &amp; one"')[0]
        card = self.col.get_note(nid).cards()[0]
        card.ivl, card.due, card.type, card.queue = 30, 500, 2, 2
        self.col.update_card(card)
        self.conn_rows[0][2] = 'Back one, revised'
        self.write_exports()
        plan = self.plan()
        self.assertEqual([u[4] for u in plan.updates], [['Back']])
        apply_plan(self.col, plan, self.config, self.root)
        note = self.col.get_note(nid)
        self.assertEqual(note['Back'], 'Back one, revised')
        self.assertEqual((note.cards()[0].id, note.cards()[0].ivl), (card.id, 30))

    def test_new_row_is_added_to_a_new_subdeck(self) -> None:
        self.conn_rows.append(['EN::Connection Patterns::02 Verb Patterns', 'Front two', 'Back two'])
        self.write_exports()
        plan = self.plan()
        self.assertEqual(len(plan.additions), 1)
        apply_plan(self.col, plan, self.config, self.root)
        nid = self.col.find_notes('"deck:EN::Connection Patterns::02 Verb Patterns"')
        self.assertEqual(len(nid), 1)
        self.assertTrue(self.plan().empty)

    def test_vocabulary_tags_are_synced(self) -> None:
        self.vocab_rows[0][6] = 'pos::noun domain::ielts'
        self.write_exports()
        plan = self.plan()
        self.assertEqual(plan.updates[0][4], ['tags'])
        apply_plan(self.col, plan, self.config, self.root)
        self.assertTrue(self.plan().empty)

    def test_css_update_does_not_change_schema(self) -> None:
        (self.root / 'style.css').write_text('.card { color: red; }', encoding='utf-8')
        plan = self.plan()
        self.assertEqual(plan.notetype_updates, [('vocabulary', ['css'])])
        before = schema_stamp(self.col)
        apply_plan(self.col, plan, self.config, self.root)
        self.assertEqual(schema_stamp(self.col), before)
        self.assertIn('color: red', self.col.models.by_name('EN_Vocabulary')['css'])

    def test_anki_only_notes_are_reported_not_deleted(self) -> None:
        self.add('Basic', 'EN::Connection Patterns::01 Prepositions', ['Only in Anki', 'x'])
        plan = self.plan()
        self.assertEqual(plan.anki_only['connections'], ['Only in Anki'])
        apply_plan(self.col, plan, self.config, self.root)
        self.assertEqual(len(self.col.find_notes('"Front:Only in Anki"')), 1)

    def test_field_mismatch_aborts(self) -> None:
        self.config['families'][0]['fields'] = VOCAB_FIELDS + ['Extra']
        with self.assertRaisesRegex(SyncAbort, 'has fields'):
            self.plan()

    def test_same_front_outside_the_deck_tree_aborts(self) -> None:
        self.conn_rows.append(['EN::Connection Patterns::01 Prepositions', 'Two Sum', 'collides'])
        self.write_exports()
        with self.assertRaisesRegex(SyncAbort, 'already exists outside'):
            self.plan()

    def test_export_routed_outside_deck_root_aborts(self) -> None:
        self.conn_rows[0][0] = 'Default'
        self.write_exports()
        with self.assertRaisesRegex(SyncAbort, 'outside'):
            self.plan()

    def test_change_limits_abort(self) -> None:
        self.config['limits']['max_updates'] = 0
        self.conn_rows[0][2] = 'changed'
        self.write_exports()
        with self.assertRaisesRegex(SyncAbort, 'exceed max_updates'):
            self.plan()


if __name__ == '__main__':
    unittest.main()
