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


def option_append(func):
    """Append words or overwrite pre-existing file?"""
    return click.option(
        "--append",
        default=1,
        type=click.BOOL,
        help="A flag determining whether words are appended to OUTPUT.\
            If true, duplicates will be excluded.",
    )(func)


def option_prompt(func):
    """Prompt for confirmation?"""
    return click.option(
        "--prompt/--no-prompt",
        "-p/ ",
        default=False,
        help="Whether to ask for confirmation before producing cards",
    )(func)


def option_lang(func):
    """Word language"""
    return click.option(
        "--lang",
        default="de",
        help="The ISO 639 code of the target language. Currently only 'de' supported.",
    )(func)
