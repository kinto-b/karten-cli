"""
Manage CSV decks of flashcards 
"""

from typing import Iterable
import csv

from .card import CardFormatted, CARD_FIELDS


def deck_write(deck: Iterable[CardFormatted], stream: str) -> None:
    """Write a deck of cards as CSV to the stream"""
    writer = csv.DictWriter(stream, CARD_FIELDS, lineterminator="\n")
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
