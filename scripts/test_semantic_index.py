#!/usr/bin/env python3
"""Check full indexing and avoid false-semantic-merges regressions."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import build_semantic_index as semantic
import find_cards

class SemanticIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=semantic.build()
        cls.groups={g["id"]:g for g in cls.data["groups"]}

    def test_all_families(self):
        self.assertEqual({c["family"] for c in self.data["cards"]},
                         {"vocabulary","patterns","connections"})
        self.assertGreaterEqual(len(self.data["cards"]),1327)

    def test_separate_behavior_from_admiration(self):
        admire=self.groups["admiration"]
        example=self.groups["exemplary_behavior"]
        self.assertEqual(admire["owner"],{"family":"vocabulary","key":"regard"})
        self.assertNotEqual(admire["owner"],example["owner"])
        self.assertTrue(find_cards.semantic_matches("look up to",self.data))

    def test_tradeoff_distinctions(self):
        e={x["text"]:x["relationship"] for x in self.groups["contrast_tradeoffs"]["expressions"]}
        self.assertEqual(e["the downside"],"related")
        self.assertEqual(e["on the flip side"],"variant")

    def test_same_help_family(self):
        found=find_cards.semantic_matches("can't help but",self.data)
        self.assertEqual(found[0][0]["owner"]["key"],
                         "can't help + V-ing · find myself + V-ing")


    def test_every_note_has_semantic_metadata(self):
        for card in self.data["cards"]:
            self.assertTrue(card["function"], card["key"])
            self.assertTrue(card["meaning"], card["key"])
        self.assertEqual(len(self.data["cards"]), 1327)

    def test_meaning_search_finds_admiration_owner(self):
        results = find_cards.meaning_candidates("respect admiration", self.data, 15)
        self.assertTrue(any(c["key"] == "regard" for _score, c in results))

    def test_generated_index(self):
        self.assertEqual(semantic.OUTPUT.read_text(encoding="utf-8"),semantic.render())

if __name__=="__main__":
    unittest.main()
