"""Tests card formatting"""

import unittest

from karten.card import Card

DUMMY_RESPONSE = """
{
  "word": "auf Anhieb",
  "category": "adverbial phrase",
  "definition": "at once",
  "forms": null,
  "example": [
    "Das hat auf Anhieb funktioniert!",
    "Ich war überrascht, dass sie die schwierige Frage auf Anhieb richtig beantwortet hat, obwohl sie sich nicht darauf vorbereitet hatte.",
    "Leider habe ich den richtigen Weg nicht auf Anhieb gefunden."
  ],
  "reverse": [
    "That worked immediately!",
    "I was surprised that she answered the difficult question correctly right away, even though she hadn't prepared for it.",
    "Unfortunately, I didn't find the right way immediately."
  ]
}
"""


class TestCLI(unittest.TestCase):
    """Test CLI functions"""

    def test_null_fields(self):
        """Test that null fields are handled correctly"""
        card_data = Card.from_json(DUMMY_RESPONSE)
        formatted = card_data.to_csv_row()
        self.assertEqual(formatted["forms"], "")

    def test_singleton_fields(self):
        """Test that singleton list fields are handled correctly"""
        card_data = Card.from_json(DUMMY_RESPONSE)
        formatted = card_data.to_csv_row()
        self.assertEqual(formatted["definition"], "at once")


if __name__ == "__main__":
    unittest.main()
