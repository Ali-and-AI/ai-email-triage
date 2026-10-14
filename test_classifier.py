import unittest
from classifier import parse_decision

class TestGuard(unittest.TestCase):

    def test_confident_answer(self):
        result = parse_decision('{"category": "spam", "confidence": 0.9, "reason": "x"}')
        self.assertEqual(result["category"], "spam")
        self.assertFalse(result["needs_human"])

    def test_garbage_answer(self):
        result = parse_decision('Sorry, I cannot help with that')
        self.assertEqual(result["category"], "other")
        self.assertTrue(result["needs_human"])

    def test_low_confidence(self):
        result = parse_decision('{"category": "spam", "confidence": 0.4, "reason": "x"}')
        self.assertEqual(result["category"], "spam")
        self.assertTrue(result["needs_human"])

    def test_unknown_category(self):
        result = parse_decision('{"category": "urgent", "confidence": 0.95, "reason": "x"}')
        self.assertEqual(result["category"], "other")
        self.assertTrue(result["needs_human"])

if __name__ == "__main__":
    unittest.main()