"""Tests for gathering per-commit change records from git history (stdlib only)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exports import change_records, validate_changes  # noqa: E402

GIT = shutil.which('git') or str(Path.home() / '.local/bin/git')


class ChangeRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / 'cards').mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Test')

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull)
        result = subprocess.run([GIT, '-C', str(self.repo), *args], capture_output=True, text=True, env=env)
        if check and result.returncode != 0:
            raise RuntimeError(result.stderr)
        return result

    def commit(self, message: str, record: dict | None = None, other: str | None = None) -> str:
        if record is not None:
            (self.repo / 'cards/anki_changes.json').write_text(json.dumps(record), encoding='utf-8')
        if other is not None:
            (self.repo / 'cards/other.txt').write_text(other, encoding='utf-8')
        self.git('add', '-A')
        self.git('commit', '-q', '-m', message)
        return self.git('rev-parse', 'HEAD').stdout.strip()

    @staticmethod
    def rename(old: str, new: str) -> dict:
        return {'renames': [{'family': 'patterns', 'from': old, 'to': new}], 'removals': []}

    def test_records_since_last_applied_commit_come_back_in_order(self) -> None:
        applied = self.commit('baseline', {'renames': [], 'removals': []})
        self.commit('agent 1', self.rename('A', 'B'))
        self.commit('unrelated edit', other='x')
        self.commit('agent 2', {'renames': [], 'removals': [{'family': 'vocabulary', 'key': 'occupy'}]})
        head = self.commit('agent 3', self.rename('B', 'C'))
        records, note = change_records(self.git, applied, head)
        self.assertEqual([r['renames'][0]['to'] if r['renames'] else r['removals'][0]['key'] for r in records],
                         ['B', 'occupy', 'C'])
        self.assertIn('3 change record(s)', note)

    def test_nothing_new_since_last_applied_commit(self) -> None:
        self.commit('agent 1', self.rename('A', 'B'))
        head = self.commit('unrelated edit', other='x')
        self.assertEqual(change_records(self.git, head, head)[0], [])

    def test_first_run_uses_only_the_current_record(self) -> None:
        self.commit('agent 1', self.rename('A', 'B'))
        head = self.commit('agent 2', self.rename('C', 'D'))
        records, note = change_records(self.git, None, head)
        self.assertEqual([r['renames'][0]['to'] for r in records], ['D'])
        self.assertIn('first run', note)

    def test_unknown_last_commit_falls_back_to_the_current_record(self) -> None:
        head = self.commit('agent 1', self.rename('A', 'B'))
        records, _note = change_records(self.git, '0' * 40, head)
        self.assertEqual(len(records), 1)


class ValidateChangesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'p.tsv').write_text('#separator:tab\n#html:true\n#deck column:1\n'
                                         'EN::Patterns\tNew front\tBack\n', encoding='utf-8')
        self.config = {'families': [{'name': 'patterns', 'export': 'p.tsv', 'fields': ['Front', 'Back']}]}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def errors(self, renames=(), removals=()) -> list[str]:
        return validate_changes({'renames': list(renames), 'removals': list(removals)}, self.config, self.root)

    def test_valid_rename_and_removal(self) -> None:
        self.assertEqual(self.errors([{'family': 'patterns', 'from': 'Old front', 'to': 'New front'}],
                                     [{'family': 'patterns', 'key': 'Merged away'}]), [])

    def test_rejects_removing_a_live_card(self) -> None:
        self.assertTrue(self.errors(removals=[{'family': 'patterns', 'key': 'New front'}]))

    def test_rejects_rename_to_a_missing_card(self) -> None:
        self.assertTrue(self.errors([{'family': 'patterns', 'from': 'Old', 'to': 'Typo front'}]))

    def test_rejects_rename_from_a_live_card(self) -> None:
        self.assertTrue(self.errors([{'family': 'patterns', 'from': 'New front', 'to': 'New front'}]))


if __name__ == '__main__':
    unittest.main()
