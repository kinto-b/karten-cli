"""
Manage CSV decks of flashcards
"""

import csv
from typing import IO, Iterable, Optional

from .card import Card


class Deck:
    """A collection of flashcards"""

    def __init__(self, cards: Optional[Iterable[Card]] = None):
        self.cards = []
        if cards:
            for card in cards:
                self.add(card)

    def add(self, card: Card) -> None:
        """Add a card to the deck"""
        self.cards.append(card)

    def write(self, file: str, append: bool = False) -> None:
        """Write deck to CSV file"""
        if not self.cards:
            return

        mode = "a" if append else "w"
        with open(file, mode, encoding="utf8") as f:
            self._write_to_stream(f)

    def _write_to_stream(self, stream: IO[str]) -> None:
        """Write deck to a stream"""
        fieldnames = list(Card.model_fields.keys())
        writer = csv.DictWriter(stream, fieldnames, lineterminator="\n")
        for card in self.cards:
            writer.writerow(card.to_csv_row())

    @classmethod
    def read(cls, file: str) -> "Deck":
        """Read deck from CSV file"""
        fieldnames = list(Card.model_fields.keys())
        deck = cls()
        with open(file, "r", encoding="utf8") as f:
            reader = csv.DictReader(f, fieldnames)
            for row in reader:
                deck.cards.append(Card.from_csv_row(row))
        return deck

    def __len__(self) -> int:
        """Return the number of cards in the deck"""
        return len(self.cards)

    def __bool__(self) -> bool:
        """Return True if deck has cards"""
        return bool(self.cards)
