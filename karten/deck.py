"""
Manage CSV decks of flashcards 
"""

from typing import Iterable
import csv

from .card import card_format, card_collect, CardFormatted, CARD_FIELDS


def deck_collect(words: Iterable[str], key: str) -> list[CardFormatted]:
    """Collect a deck of cards"""
    return [card_format(card_collect(word, key)) for word in words]


def deck_write(deck: Iterable[CardFormatted], file: str, append: bool) -> None:
    """Write a deck of cards as CSV"""
    mode = "a" if append else "w"
    with open(file, mode, encoding="utf8") as stream:
        writer = csv.DictWriter(stream, CARD_FIELDS)
        for card in deck:
            writer.writerow(card)


def deck_read(file: str) -> list[CardFormatted]:
    """Read a deck of cards from CSV"""
    deck = []
    with open(file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f, CARD_FIELDS)
        for card in reader:
            deck.append(card)
    return deck
