"""
Prompt templates
"""

CONTEXT_PROMPT = """Hi I'm learning German. I need your help making flashcards.

I will give you a word and I want you to give me a card formatted as JSON with the following fields

- word: the word in German, with the article if it's a noun
- category: noun, verb, adjective, etc.
- definition: the meaning in English.
- forms: one of:
  + the plural if it's a noun, (e.g. 'Erinnerungen')
  + the past participle and simple past if it's a verb, OR 
  + the comparative and superlative if it's an adjective (e.g. ['witziger', 'am witizgsten']).
- example: a few sentences using the word in German. These should should the usage with the different prepositions and different cases.
- reverse: the example sentences translated into English.

Here's two examples

{
  "word": "abholen",
  "category": "verb",
  "definition": ["to pick up"],
  "forms": ["hat abgeholt", "holte ab"],
  "example": [
    "Ich hole dich am Bahnhof ab.",
    "Er hat das Paket bei der Post abgeholt."
  ],
  "reverse": [
    "I will pick you up at the train station.",
    "He picked up the package at the post office."
  ],
}

{
  "word": "die Schlägerei",
  "category": "noun",
  "definition": ["brawl"],
  "forms": ["die Schlägereien"],
  "example": ["Es gab eine Schlägerei zwischen zwei Männern."],
  "reverse": ["There was a brawl between two men."],
}
"""
