"""
Prompt templates
"""

CONTEXT_PROMPT = """Hi I'm learning German. I need your help making flashcards.

I will give you a word and I want you to give me a card formatted as JSON with the following fields

- word: the word in German
- definition: the meaning in English.
- forms: the plural if it's a noun, the past participle and simple past if it's a verb, the comparative and superlative if it's an adjective.
- preposition: the corresponding prepositions, if applicable
- example: a few sentences using the word in German. These should should the usage with the different prepositions and different cases.
- reverse: the example sentences translated into English.
- note: any particularly important information about a word's usage

Here's an example 

{
  "word": "abholen",
  "definition": ["to pick up"],
  "forms": ["hat abgeholt", "holte ab"],
  "preposition": ["von+Dat."],
  "example": [
    "Ich hole dich am Bahnhof ab.",
    "Er hat das Paket bei der Post abgeholt."
  ],
  "reverse": [
    "I will pick you up at the train station.",
    "He picked up the package at the post office."
  ],
  "notes": ["Trennbares Verb"]
}
"""
