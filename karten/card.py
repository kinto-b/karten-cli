"""
Collect card data from an LLM
"""

import json

import google.generativeai as genai
import typing_extensions as typing

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


def initialise_model(key: str, model: str) -> genai.GenerativeModel:
    """Initialises a model"""
    genai.configure(api_key=key)
    return genai.GenerativeModel(
        model,
        generation_config={
            "candidate_count": 1,
            "response_mime_type": "application/json",
            # "response_schema": Card,
        },
    )


def card_prompt(word: str, lang: str) -> str:
    """Prepares the prompt"""
    return CardPrompt[lang.upper()].value + f"\n\nWord: {word}"


def card_collect(word: str, lang: str, model: genai.GenerativeModel) -> Card:
    """Creates a card using Google LLM"""
    prompt = card_prompt(word, lang)
    response = model.generate_content(prompt)
    return _card_parse(response.text)


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
