"""CLI functions"""

import json
import os

import click

from .card import card_collect
from .deck import deck_collect, deck_read, deck_write
from .kindle import kindle_read


@click.group()
def cli():  # pylint: disable=missing-docstring
    pass


@cli.command()
@click.argument("word")
@click.option(
    "--key",
    default=os.getenv("GOOGLE_API_KEY"),
    help="API key for authentication. Defaults to GOOGLE_API_KEY environment variable.",
)
def card(word, key):
    """Fetch and display JSON data for WORD"""
    if not key:
        click.echo("Error: API key must be provided.")
        return
    card = card_collect(word, key)  # pylint: disable=redefined-outer-name
    click.echo(json.dumps(card, indent=2))


@cli.command()
@click.argument("words", nargs=-1)
@click.argument("output", type=click.Path())
@click.option(
    "--append",
    default=1,
    type=click.BOOL,
    help="A flag determining whether words are appended to OUTPUT.\
        If true, duplicates will be excluded.",
)
@click.option(
    "--key",
    default=os.getenv("GOOGLE_API_KEY"),
    help="API key for authentication. Defaults to GOOGLE_API_KEY environment variable.",
)
def deck(words, output, append, key):
    """Creates a csv of cards ready for import into Anki (or equivalent)"""
    _create_deck(set(words), output, append, key)


@cli.command()
@click.argument("kindle_dir", type=click.Path())
@click.argument("output", type=click.Path())
@click.option(
    "--lang",
    default="de",
    help="The ISO 639 code of the target language. Currently only 'de' supported.",
)
@click.option(
    "--append",
    default=1,
    type=click.BOOL,
    help="A flag determining whether words are appended to OUTPUT.\
        If true, duplicates will be excluded.",
)
@click.option(
    "--key",
    default=os.getenv("GOOGLE_API_KEY"),
    help="API key for authentication. Defaults to GOOGLE_API_KEY environment variable.",
)
def kindle_deck(kindle_dir, output, lang, append, key):
    """
    Creates a csv of cards ready for import into Anki (or equivalent) using
    the vocabulary lookups in language LANG from the kindle at KINDLE_DIR.
    Note that currently only LANG='de' is supported.
    """

    if lang != "de":
        click.echo(f"Error: LANG='{lang}' not supported")

    db = os.path.join(kindle_dir, "system", "vocabulary", "vocab.db")
    words = kindle_read(db, lang)
    _create_deck(words, output, append, key)


def _create_deck(words: set[str], output: str, append: bool, key: str) -> None:
    """Adds cards for new words to the deck at OUTPUT"""
    append = append and os.path.exists(output)
    if append:
        old_deck = deck_read(output)
        old_words = set([d["word"] for d in old_deck])
        words = words.difference(old_words)

    if not click.confirm(f"Processing {len(words)} card(s). Ready to continue?"):
        click.echo("Aborting...")
        return

    with click.progressbar(words) as progress:
        deck = deck_collect(progress, key)  # pylint: disable=redefined-outer-name

    deck_write(deck, output, append)


if __name__ == "__main__":
    cli()
