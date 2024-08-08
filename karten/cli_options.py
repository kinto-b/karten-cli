"""Commonly used CLI options"""

import os
import click


def option_file(func):
    """File option"""
    return click.option(
        "--file",
        default="-",
        type=click.Path(),
        help="The filepath to redirect the output to",
    )(func)


def option_key(func):
    """API key"""
    return click.option(
        "--key",
        default=os.getenv("GOOGLE_API_KEY"),
        help="API key for authentication. Defaults to GOOGLE_API_KEY environment variable.",
    )(func)


def option_date_from(func):
    """Extract lookups from this date on"""
    return click.option(
        "--date-from",
        default="2000-01-01",
        type=click.DateTime(),
        help="Only Kindle lookups from this date on are included",
    )(func)


def option_lang(func):
    """Word language"""
    return click.option(
        "--lang",
        default="de",
        help="The ISO 639 code of the target language. Currently only 'de' supported.",
    )(func)
