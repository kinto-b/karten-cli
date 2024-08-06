# Karten CLI (WIP)

A simple CLI application for creating German vocabulary flashcards from Kindle dictionary lookups using generative AI. It is very geared to my tastes so your milage may vary. Pull requests are of course welcome.

## Getting started

To install, simply clone this repo and then

```bash
$ pip install -e .
```

You'll need a key for Google's Generative Language service. Once you've got one, export it 

```bash
$ export GOOGLE_API_KEY="your_key"
```

otherwise you'll need to pass the key around all the time, e.g.

```bash
$ karten card befassen --key "your_key"
```

## Basic usage

The core of the application is a function which sends a word to Google Gemini and requests back a flashcard. 

```bash
$ karten card befassen

{
  "word": "befassen",
  "definition": [
    "to deal with",
    "to concern oneself with"
  ],
  "forms": [
    "hat sich befasst",
    "befasste sich"
  ],
  "preposition": [
    "mit+Dat."
  ],
  "example": [
    "Ich befasse mich mit der deutschen Grammatik.",
    "Er hat sich mit dem Thema Umweltschutz befasst."
  ],
  "reverse": [
    "I am dealing with German grammar.",
    "He has dealt with the topic of environmental protection."
  ],
  "notes": [
    "refexive verb",
    "separable prefix",
    "usually followed by 'mit'"
  ]
}
```

You probably won't use this function directly. Instead of a JSON representation of a single card, you'll probably want a CSV representation of a whole deck of cards, which you can import into Anki (or whatever flashcard app you use). If you already have a list of words, then use

```bash
$ karten deck Erinnerung witzig verschwören --file=./cards.csv
$ cat ./cards.csv | cut -c -80

Erinnerung,memory; reminder,,an+Akk. | an+Dat. | über+Akk.,Die Erinnerung an de
verschwören,to conspire; to swear (an oath),verschwor | hat verschworen,gegen+A
witzig,funny; humorous,,,Der Film war wirklich witzig.<br/><br/>Er erzählt imme
```

If you point to the same output, by default new cards will be *appended*. Duplicates will be avoided. For example, notice that 'umarbeiten' gets added but 'witzig' is not duplicated if we now call:


```bash
$ karten deck witzig umarbeiten --file=./cards.csv
$ cat ./cards.csv | cut -c -80

Erinnerung,memory; reminder,,an+Akk. | an+Dat. | über+Akk.,Die Erinnerung an de
verschwören,to conspire; to swear (an oath),verschwor | hat verschworen,gegen+A
witzig,funny; humorous,,,Der Film war wirklich witzig.<br/><br/>Er erzählt imme
umarbeiten,to rework; to revise; to redo,hat umgearbeitet | arbeitete um,an+Dat.
```

You can import the .csv into Anki to get cards like this,

![Example Anki cards after import](./assets/example-deck.png)

(First download and import the example deck at [./assets/example-deck.apkg](./assets/example-deck.apkg), which contains a card-type with all the required fields.)

## Usage with Kindle

If you've got the 'vocabulary builder' feature turned on on your Kindle, you'll be able to create flashcards by extracting your dictionary lookups. Simply plug in your Kindle, find out which drive it is at (for me thats' `D:/`), and then run

```bash
$ karten kindle-deck D:/ --file=./cards.csv
```

This will extract the dictionary lookups from your kindle and export flashcards to `./cards.csv`

You might prefer to inspect the words before you create cards for them. There will undoubtedly be a bit of dreck in there, so you might be able to save some cloud credits by editing the word list before using it to create cards. You can export just the raw kindle lookups using

```bash
$ karten kindle-words D:/ > words.txt
```

Then once you've filtered out the dreck,

```bash
$ words=$(<words.txt tr -d '\r' | tr '\n' ' ')
$ karten deck $words --file=./cards.csv
```




