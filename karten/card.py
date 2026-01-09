"""
Collect card data from an LLM
"""

import json

import typing_extensions as typing
from google import genai
from google.genai import types

from .prompt import CardPrompt

CARD_FIELDS = (
    "word",
    "category",
    "definition",
    "forms",
    "example",
    "reverse",
)


class Card(typing.TypedDict):
    """Card response schema"""

    word: str
    category: str
    definition: list[str]
    forms: list[str]
    example: list[str]
    reverse: list[str]


class CardFormatted(typing.TypedDict):
    """Formatted card schema"""

    word: str
    category: str
    definition: str
    forms: str
    example: str
    reverse: str


class CardError(Exception):
    """Card could not be created"""


class CardModel:
    """Wrapper for Google GenAI client configured for card generation"""

    def __init__(self, api_key: str, model_name: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Card,
        )

    def _prepare_prompt(self, word: str, lang: str) -> str:
        """Prepares the prompt for a given word and language"""
        return CardPrompt[lang.upper()].value + f"\n\nWord: {word}"

    def generate_content(self, prompt: str) -> str:
        """Generate content using the configured model"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=self.config,
        )
        if response.text is None:
            raise CardError("No response text from model")
        return response.text

    def collect(self, word: str, lang: str) -> Card:
        """Creates a card for the given word using the LLM"""
        prompt = self._prepare_prompt(word, lang)
        response_text = self.generate_content(prompt)
        return _card_parse(response_text)


def _card_parse(raw_card: str) -> Card:
    """Parse raw card JSON string into Card dict"""
    try:
        card = json.loads(raw_card)
    except ValueError as e:
        raise CardError(f"Failed to parse card JSON: {raw_card}") from e

    if not isinstance(card, dict):
        raise CardError(f"Card JSON is not a dictionary: {raw_card}")

    for field in CARD_FIELDS:
        if field not in card:
            raise CardError(f"Card JSON missing field '{field}': {raw_card}")

        if card[field] is None:
            card[field] = ""

        # Ensure list fields are lists
        field_type = Card.__annotations__.get(field)
        if field_type == list[str]:
            if isinstance(card[field], str):
                card[field] = [card[field]]
            elif not isinstance(card[field], list):
                raise CardError(
                    f"Card field '{field}' has unexpected format: {raw_card}"
                )

    return typing.cast(Card, card)


def card_format(card: Card) -> CardFormatted:
    """Format a card so that it can be written as CSV"""
    try:
        return CardFormatted(
            word=card["word"],
            category=card["category"],
            definition="; ".join(card["definition"]),
            forms=" | ".join(card["forms"]),
            example="<br/><br/>".join(card["example"]),
            reverse="<br/><br/>".join(card["reverse"]),
        )
    except Exception as e:
        raise CardError(
            f"Failed to format card for '{card.get('word', 'unknown')}': {e}"
        ) from e
