"""Test CLI commands"""

from tempfile import TemporaryFile
import os

import unittest
from unittest.mock import patch
from click.testing import CliRunner

from karten.cli import cli
from karten.card import Card, card_format
from karten.deck import deck_read, deck_write


def mock_card_collect(word, key):  # pylint: disable=unused-argument
    """Overwrite the function which serves cards using the LLM"""
    return Card(
        word=word,
        category="cat",
        definition=["def1", "def2", "def3"],
        forms=["form1", "form2"],
        example=["ex1", "ex2"],
        reverse=["rev1", "rev2"],
        notes=["note"],
    )


class TestCLI(unittest.TestCase):
    """Test CLI functions"""

    def setUp(self):
        self.runner = CliRunner()

    def helper_deck(self, file, words, expected, mock_card):
        """Check that output written to file is as expected"""
        result = self.runner.invoke(
            cli,
            ["deck"] + words + ["--file", file],
        )

        self.assertEqual(result.exit_code, 0)
        mock_card.assert_called()

        expected = [card_format(mock_card_collect(e, "")) for e in expected]
        output = deck_read(file)
        for e, o in zip(expected, output):
            self.assertDictEqual(e, o)

    @patch("karten.deck.card_collect", side_effect=mock_card_collect)
    def test_deck_file_fresh(self, mock_card):
        """Test deck command with a fresh file"""
        with TemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["some", "words"]

        try:
            self.helper_deck(fp, words, words, mock_card)
        finally:
            os.remove(fp)

    @patch("karten.deck.card_collect", side_effect=mock_card_collect)
    def test_deck_file_append(self, mock_card):
        """Test deck command with a pre-existing file"""
        with TemporaryFile("w+", delete=False) as file:
            fp = file.name
            # Add some content to the file
            deck_write([card_format(mock_card_collect("skip", ""))], file)

        words = ["some", "words", "skip"]
        expected = [
            "skip",
            "some",
            "words",
        ]  # 'skip' should come first, we're appending!

        try:
            self.helper_deck(fp, words, expected, mock_card)
        finally:
            os.remove(fp)

    # TODO: test kindle functions


if __name__ == "__main__":
    unittest.main()
