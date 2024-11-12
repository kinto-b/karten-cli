"""
Prompt templates
"""

import os
from enum import Enum
import json
import yaml

DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FP = my_file = os.path.join(DIR, "prompt.yaml")

with open(CONFIG_FP, "r", encoding="utf8") as f:
    CONFIG = yaml.safe_load(f)


def _prompt(lang, forms, examples):
    return f"""Hi I'm learning {lang}. I need your help making flashcards.

I will give you a word and I want you to give me a card formatted as JSON with the following fields

- word: the word in {lang}, with the article if it's a noun
- category: noun, verb, adjective, etc.
- definition: the meaning in English.
- forms: {forms}
- example: a few complex sentences using the word in {lang}. 
  These should should the usage with the different prepositions, cases, and tenses. 
  Include at least one complex example.
- reverse: the example sentences translated into English.

Here are some examples:

{"\n".join(json.dumps(e, ensure_ascii=False) for e in examples)}
"""


class CardPrompt(Enum):
    """Prompt templates for generating cards in a variety of languages"""

    DE = _prompt(CONFIG["de"]["lang"], CONFIG["de"]["forms"], CONFIG["de"]["examples"])
