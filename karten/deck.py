"""
Manage CSV decks of flashcards
"""

import csv
from typing import IO, Iterable

from .card import Card


def deck_write(deck: Iterable[dict[str, str]], stream: IO[str]) -> None:
    """Write a deck of cards as CSV to the stream"""
    fieldnames = list(Card.model_fields.keys())
    writer = csv.DictWriter(stream, fieldnames, lineterminator="\n")  # type: ignore[arg-type]
    for card in deck:
        writer.writerow(card)  # type: ignore[arg-type]


def deck_read(file: str) -> list[dict[str, str]]:
    """Read a deck of cards from CSV"""
    fieldnames = list(Card.model_fields.keys())
    deck = []
    with open(file, "r", encoding="utf8") as f:
        reader = csv.DictReader(f, fieldnames)
        for card in reader:
            deck.append(card)  # type: ignore[arg-type]
    return deck
