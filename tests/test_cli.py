"""Test CLI commands"""

import os
import sqlite3
import unittest
from tempfile import NamedTemporaryFile
from unittest.mock import patch

from click.testing import CliRunner

from karten.card import Card, CardError
from karten.cli import cli
from karten.deck import Deck


def mock_card_collect(self, word, lang=None):  # pylint: disable=unused-argument
    """Overwrite the method which serves cards using the LLM"""
    # When called directly from test (not as method), self is actually word
    if lang is None:
        word = self

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
            ["deck"] + words + ["--file", file, "--key", "fake_api_key"],
        )

        self.assertEqual(result.exit_code, 0)
        mock_card.assert_called()

        expected = [mock_card_collect(e, None) for e in expected]
        output = Deck.read(file)
        for e, o in zip(expected, output.cards):
            self.assertEqual(e, o)

        return result

    @patch("karten.card_generator.CardGenerator.collect", side_effect=mock_card_collect)
    def test_deck_file_fresh(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["some", "words"]

        try:
            self.helper_deck(fp, words, words, mock_card)
        finally:
            os.remove(fp)

    @patch("karten.card_generator.CardGenerator.collect", side_effect=mock_card_collect)
    def test_deck_some_fail(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["some", "fail", "words"]
        expected = ["some", "words"]
        try:
            res = self.helper_deck(fp, words, expected, mock_card)
            self.assertIn("Error processing 'fail'", res.output)
        finally:
            os.remove(fp)

    @patch("karten.card_generator.CardGenerator.collect", side_effect=mock_card_collect)
    def test_deck_all_fail(self, mock_card):
        """Test deck command with a fresh file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name

        words = ["fail", "fail"]
        try:
            res = self.helper_deck(fp, words, [], mock_card)
            self.assertIn("Error processing 'fail'", res.output)
        finally:
            os.remove(fp)

    @patch("karten.card_generator.CardGenerator.collect", side_effect=mock_card_collect)
    def test_deck_file_append(self, mock_card):
        """Test deck command with a pre-existing file"""
        with NamedTemporaryFile("w+", delete=False) as file:
            fp = file.name
            # Add some content to the file
            deck = Deck([mock_card_collect("first", None)])
            deck.write(fp)

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
