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
- example: a few complex sentences using the word in German. These should should the usage with the different prepositions, cases, and tenses. Include at least one complex example.
- reverse: the example sentences translated into English.

Here's two examples

{
  "word": "abholen",
  "category": "verb",
  "definition": ["to pick up"],
  "forms": ["hat abgeholt", "holte ab"],
  "example": [
    "Ich hole dich am Bahnhof ab.",
    "Er hat gesagt, er habe das Paket bei der Post abgeholt, ohne sich auszuweisen."
  ],
  "reverse": [
    "I will pick you up at the train station.",
    "He said he picked the package up from the post office without showing ID."
  ],
}

{
  "word": "die Schlägerei",
  "category": "noun",
  "definition": ["brawl"],
  "forms": ["die Schlägereien"],
  "example": [
    "Es gab eine Schlägerei zwischen zwei Männern.",
    "Nach der Schlägerei in der Bar, die durch einen Streit um ein Fußballspiel ausgelöst wurde, musste die Polizei eingreifen, um die wütenden Partygänger zu trennen."
  ],
  "reverse": [
    "There was a brawl between two men."
    "After the brawl in the bar, which was triggered by a dispute over a football match, the police had to intervene to separate the angry partygoers."
  ],
}
"""
