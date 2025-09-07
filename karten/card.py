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
    try:
        card = json.loads(response.text)
    except ValueError as e:
        raise CardError(f"LLM returned a non-conforming response for '{word}'") from e

    if not isinstance(card, dict):
        raise CardError(
            f"LLM returned a non-conforming response for '{word}' (not a dict)"
        )

    for field in CARD_FIELDS:
        if field not in card:
            raise CardError(
                f"LLM returned a non-conforming response for '{word}' (missing field '{field}')"
            )

    return typing.cast(Card, card)


def card_format(card: Card) -> CardFormatted:
    """Format a card so that it can be written as CSV"""
    return CardFormatted(
        word=card["word"],
        category=card["category"],
        definition="; ".join(card["definition"]),
        forms=" | ".join(card["forms"]),
        example="<br/><br/>".join(card["example"]),
        reverse="<br/><br/>".join(card["reverse"]),
    )
