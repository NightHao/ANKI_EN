"""Regression coverage for grouped rendering, sense ownership, and merge safety."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_vocabulary as vocab


def block(term, definition):
    return {"entry_term": term, "part_of_speech": "verb", "common_patterns": term + " something",
            "senses": [{"definition": definition, "example": 'Use <x> & "y".', "synonyms": [], "antonyms": []}]}


class GroupedVocabularyTests(unittest.TestCase):
    def test_same_pos_different_terms_never_share_senses(self):
        merged = vocab.merge_senses([block("assure", "give confidence")], [block("guarantee", "promise outcome")])
        self.assertEqual([b["entry_term"] for b in merged], ["assure", "guarantee"])
        self.assertEqual(merged[0]["senses"][0]["definition"], "give confidence")

    def test_comparison_is_after_definitions_and_before_patterns(self):
        blocks = [block("assure", "give confidence"), block("guarantee", "promise outcome")]
        blocks[0]["comparison"] = {"note": "Both <can> overlap.", "situations": [
            {"situation": "A <problem>", "examples": "A & B", "guidance": "Either works."}]}
        rendered = vocab.render_back_html(blocks)
        self.assertLess(rendered.index("promise outcome"), rendered.index('<table'))
        self.assertLess(rendered.index('</table>'), rendered.index('Common patterns'))
        self.assertIn('&lt;problem&gt;', rendered)
        self.assertIn('A &amp; B', rendered)
        self.assertNotIn('<x>', rendered)
        self.assertEqual(rendered.count('No useful synonym for this word.'), 2)
        parser = vocab.BalancedHTMLParser()
        parser.feed(rendered)
        parser.close()

    def test_group_without_comparison_is_rejected(self):
        row = {"Term": "assure / guarantee", "SensesJSON": json.dumps([
            block("assure", "give confidence"), block("guarantee", "promise outcome")])}
        with self.assertRaisesRegex(ValueError, "exactly one comparison"):
            vocab.validate_senses(row, True)

    def test_ordinary_card_rendering_stays_ordinary(self):
        b = block("assure", "give confidence")
        del b["entry_term"]
        rendered = vocab.render_back_html([b])
        self.assertNotIn('<table', rendered)
        self.assertNotIn('lexical-entry', rendered)
        self.assertIn('No useful antonym for this word.', rendered)

    def test_lossy_merge_is_rejected_before_writing(self):
        source = vocab.row_from_record({"term": "assure", "priority": "ACTIVE",
            "parts_of_speech": ["verb"], "senses": [block("assure", "old retained definition")]})
        record = {"term": "assure / guarantee", "priority": "ACTIVE", "parts_of_speech": ["verb"],
                  "senses": [block("assure", "different definition")], "merge_from": ["assure"]}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "update.json"
            p.write_text(json.dumps([record]))
            with patch.object(vocab, "load_master", return_value=[source]), patch.object(vocab, "write_master") as write:
                with self.assertRaisesRegex(ValueError, "lose a sense"):
                    vocab.upsert(p)
                write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
