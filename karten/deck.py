"""
Manage CSV decks of flashcards
"""

import csv
from typing import IO, Iterable

from .card import CARD_FIELDS, CardFormatted


def deck_write(deck: Iterable[CardFormatted], stream: IO[str]) -> None:
    """Write a deck of cards as CSV to the stream"""
    writer = csv.DictWriter(stream, CARD_FIELDS, lineterminator="\n")  # type: ignore[arg-type]
    for card in deck:
        writer.writerow(card)  # type: ignore[arg-type]


def deck_read(file: str) -> list[CardFormatted]:
    """Read a deck of cards from CSV"""
    deck = []
    with open(file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f, CARD_FIELDS)
        for card in reader:
            deck.append(card)
    return deck
