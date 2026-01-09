"""CLI functions"""

import os
from typing import Iterable

import click

from . import __version__
from .card import CardError
from .card_generator import CardGenerator
from .cli_options import (
    option_date_from,
    option_file,
    option_key,
    option_lang,
    option_model,
)
from .deck import Deck
from .kindle import kindle_read


@click.group()
@click.version_option(__version__, prog_name="karten")
def cli():  # pylint: disable=missing-docstring
    pass


@cli.command()
@click.argument("word")
@option_lang
@option_key
@option_model
def card(word, lang, key, model):
    """Fetch and display JSON data for WORD"""
    try:
        generator = CardGenerator(api_key=key, model_name=model)
        card = generator.collect(word, lang)  # pylint: disable=redefined-outer-name
        click.echo(card.model_dump_json(indent=2, exclude_none=True))
    except CardError as e:
        click.echo(e)


@cli.command()
@click.argument("words", nargs=-1)
@option_lang
@option_file
@option_key
@option_model
def deck(words, lang, file, key, model):
    """Creates a csv of cards ready for import into Anki (or equivalent)"""
    _create_deck(words, lang, file, key, model)


@cli.command()
@click.argument("kindle_dir", type=click.Path())
@option_file
@option_lang
@option_date_from
@option_key
@option_model
def kindle_deck(kindle_dir, file, lang, date_from, key, model):
    """
    Creates a csv of cards ready for import into Anki (or equivalent) using
    the vocabulary lookups in language LANG from the kindle at KINDLE_DIR.
    Note that currently only LANG='de' is supported.
    """
    words = kindle_read(kindle_dir, lang, date_from)
    _create_deck(words, lang, file, key, model)


def _create_deck(
    words: Iterable[str], lang: str, file: str, key: str, model_name: str
) -> None:
    """Adds cards for new words to the deck at OUTPUT"""
    append = os.path.exists(file)

    try:
        generator = CardGenerator(api_key=key, model_name=model_name)
    except CardError as e:
        click.echo(f"Error: {e}")
        return

    deck = Deck()
    words_list = list(words)
    with click.progressbar(words_list) as progress:
        for word in progress:
            try:
                card = generator.collect(word, lang)
                deck.add(card)
            except CardError as e:
                click.echo(f"Error processing '{word}': {e}")

    # Write the deck
    deck.write(file, append=append)


@cli.command()
@click.argument("kindle_dir", type=click.Path())
@option_lang
@option_date_from
def kindle_words(kindle_dir, lang, date_from):
    """
    Extract the words from your Kindle dictionary lookups.
    """
    words = kindle_read(kindle_dir, lang, date_from)
    for word in words:
        click.echo(word)


if __name__ == "__main__":
    cli()
