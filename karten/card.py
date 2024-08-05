"""
Collect card data from an LLM
"""

import json

import google.generativeai as genai
import typing_extensions as typing

from .prompt import CONTEXT_PROMPT


class Karte(typing.TypedDict):
    """Card response schema"""

    word: str
    definition: list[str]
    forms: list[str]
    preposition: list[str]
    example: list[str]
    reverse: list[str]
    notes: list[str]


def initialise_model(key: str) -> genai.GenerativeModel:
    """Initialises a model"""
    genai.configure(api_key=key)
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config={
            "candidate_count": 1,
            "response_mime_type": "application/json",
            "response_schema": Karte,
        },
    )


def build_prompt(word: str) -> str:
    """Prepares the prompt"""
    return CONTEXT_PROMPT + f"\n\nWord: {word}"


def build_card(word: str, key: str) -> dict:
    """Creates a card using Google LLM"""
    model = initialise_model(key)
    prompt = build_prompt(word)
    response = model.generate_content(prompt)
    return json.loads(response.text)
