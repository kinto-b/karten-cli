"""
Prompt templates
"""

import json
import os
from enum import Enum

import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FP = os.path.join(DIR, "prompt.yaml")

with open(CONFIG_FP, "r", encoding="utf8") as f:
    CONFIG = yaml.safe_load(f)


def _prompt(lang, forms, examples):
    examples_str = "\n".join(json.dumps(e, ensure_ascii=False) for e in examples)
    return f"""You are an expert {lang} teacher creating vocabulary flashcards.

CRITICAL REQUIREMENTS:
- MUST USE CASUAL SPOKEN {lang}!
- THE WORD MUST NOT APPEAR IN THE DEFINITION!
- definition: Give definition(s) in English. Be precise. Explicitly distinguish from words that SOUND the same. Note more common alternatives if applicable.
- forms: Include {forms}
- example: Show varied grammar (cases, tenses, moods). Include one simple + one complex sentence.
- reverse: Natural English translations.
- Focus on the target word! Only use similar words to clarify!

EXAMPLES:
{examples_str}"""


class CardPrompt(Enum):
    """Prompt templates for generating cards in a variety of languages"""

    DE = _prompt(CONFIG["de"]["lang"], CONFIG["de"]["forms"], CONFIG["de"]["examples"])
    ES = _prompt(CONFIG["es"]["lang"], CONFIG["es"]["forms"], CONFIG["es"]["examples"])
