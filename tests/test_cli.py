"""Test CLI commands"""

from tempfile import NamedTemporaryFile
import os

import unittest
import sqlite3
from unittest.mock import patch
from click.testing import CliRunner

from karten.cli import cli
from karten.card import Card, CardError, card_format
from karten.deck import deck_read, deck_write


def mock_card_collect(word, model):  # pylint: disable=unused-argument
    """Overwrite the function which serves cards using the LLM"""
    if word == "fail":
        raise CardError("Fail!")

    return Card(
        word=word,
        category="cat",
        definition=["def1", "def2", "def3"],
        forms=["form1", "form2"],
        example=["ex1", "ex2"],
        reverse=["rev1", "rev2"],
    )


def mock_kindle_connect(kindle_dir):  # pylint: disable=unused-argument
    """Connect to test vocab file"""
    fp = os.path.join(os.path.dirname(__file__), "vocab.db")
    return sqlite3.connect(fp)


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

        expected = [card_format(mock_card_collect(e, None)) for e in expected]
        output = deck_read(file)
        for e, o in zip(expected, output):
            self.assertDictEqual(e, o)

        return result

    @patch("karten.cli.card_collect", side_effect=mock_card_collect)
    def test_deck_file_fresh(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["some", "words"]

        try:
            self.helper_deck(fp, words, words, mock_card)
        finally:
            os.remove(fp)

    @patch("karten.cli.card_collect", side_effect=mock_card_collect)
    def test_deck_some_fail(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["some", "fail", "words"]
        expected = ["some", "words"]
        try:
            res = self.helper_deck(fp, words, expected, mock_card)
            self.assertIn("Failed to create cards for: fail", res.output)
        finally:
            os.remove(fp)

    @patch("karten.cli.card_collect", side_effect=mock_card_collect)
    def test_deck_all_fail(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["fail", "fail"]
        try:
            res = self.helper_deck(fp, words, [], mock_card)
            self.assertIn("Failed to create cards for: fail, fail", res.output)
        finally:
            os.remove(fp)

    @patch("karten.cli.card_collect", side_effect=mock_card_collect)
    def test_deck_file_append(self, mock_card):
        """Test deck command with a pre-existing file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name
            # Add some content to the file
            deck_write([card_format(mock_card_collect("first", None))], file)

        words = ["some", "words"]
        expected = ["first", "some", "words"]
        try:
            self.helper_deck(fp, words, expected, mock_card)
        finally:
            os.remove(fp)

    @patch("karten.kindle.kindle_connect", side_effect=mock_kindle_connect)
    def test_kindle_read(self, mock_connect):
        """Test reading words from Kindle"""
        result = self.runner.invoke(
            cli,
            ["kindle-words", ".", "--date-from", "2024-08-01"],
        )
        mock_connect.assert_called()
        self.assertEqual("Wams\nfesch\n", result.output)


if __name__ == "__main__":
    unittest.main()
