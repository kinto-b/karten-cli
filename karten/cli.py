"""CLI functions"""

import json
import os

import click

from .card import build_card


@click.group()
def cli():
    pass


@cli.command()
@click.argument("word")
@click.option(
    "--key",
    default=os.getenv("GOOGLE_API_KEY"),
    help="API key for authentication. Defaults to GOOGLE_API_KEY environment variable.",
)
def wort(word, key):
    """Fetch and display JSON data for a given word"""
    if not key:
        click.echo("Error: API key must be provided.")
        return
    card = build_card(word, key)
    click.echo(json.dumps(card, indent=2))


if __name__ == "__main__":
    cli()
