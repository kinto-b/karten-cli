"""CLI functions"""

import json
import os
from typing import Iterable

import click

from . import __version__
from .card import initialise_model, card_collect, card_format, CardError
from .deck import deck_write
from .kindle import kindle_read
from .cli_options import (
    option_model,
    option_date_from,
    option_file,
    option_key,
    option_lang,
)


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
    if not key:
        click.echo("Error: API key must be provided.")
        return
    model = initialise_model(key, model)
    try:
        card = card_collect(word, lang, model)  # pylint: disable=redefined-outer-name
        click.echo(json.dumps(card, indent=2, ensure_ascii=False))
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
    words: Iterable[str], lang: str, file: str, key: str, model: str
) -> None:
    """Adds cards for new words to the deck at OUTPUT"""
    append = os.path.exists(file)

    model = initialise_model(key, model)
    deck, err = [], []  # pylint: disable=redefined-outer-name
    with click.progressbar(words) as progress:
        for word in progress:
            try:
                deck.append(card_format(card_collect(word, lang, model)))
            except CardError:
                err.append(word)

    if err:
        click.echo(f"Failed to create cards for: {', '.join(err)}")
    if not deck:
        return

    mode = "a" if append else "w"
    with click.open_file(file, mode, encoding="utf8") as stream:
        deck_write(deck, stream)


@cli.command()
@click.argument("kindle_dir", type=click.Path())
@option_lang
@option_date_from
def kindle_words(kindle_dir, lang, date_from):
    """
    Extract the words from your Kindle dictionary lookups.
    """

    if lang != "de":
        click.echo(f"Error: LANG='{lang}' not supported")

    words = kindle_read(kindle_dir, lang, date_from)
    for word in words:
        click.echo(word)


if __name__ == "__main__":
    cli()
