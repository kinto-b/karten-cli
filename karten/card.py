"""
Collect card data from an LLM
"""

import json

import google.generativeai as genai
import typing_extensions as typing

from .prompt import CONTEXT_PROMPT

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


def initialise_model(key: str) -> genai.GenerativeModel:
    """Initialises a model"""
    genai.configure(api_key=key)
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={
            "candidate_count": 1,
            "response_mime_type": "application/json",
            # "response_schema": Card,
        },
    )


def card_prompt(word: str) -> str:
    """Prepares the prompt"""
    return CONTEXT_PROMPT + f"\n\nWord: {word}"


def card_collect(word: str, model: genai.GenerativeModel) -> Card:
    """Creates a card using Google LLM"""
    prompt = card_prompt(word)
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except ValueError as e:
        raise CardError(f"Card could not be created for {word}") from e


def card_format(card: Card) -> CardFormatted:
    """Format a card so that it can be written as CSV"""
    card["definition"] = "; ".join(card["definition"])
    card["forms"] = " | ".join(card["forms"])
    card["example"] = "<br/><br/>".join(card["example"])
    card["reverse"] = "<br/><br/>".join(card["reverse"])
    return card
