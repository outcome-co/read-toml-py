#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import sys
from typing import Optional

import click
from outcome.read_toml.lib import read  # noqa: WPS347
from outcome.utils import console


@click.command()
@click.option('--path', help='The path to the TOML file', required=True, type=click.File('r'))
@click.option('--key', help='The path to read from the TOML file', required=True)
@click.option('--default', help='The value to provide if the key is missing', required=False)
@click.option('--check-only', help='If present, only checks if the key is present in the TOML file', is_flag=True, default=False)
@click.option('--github-actions', help='If present, formats the output for github actions', is_flag=True, default=False)
def read_toml(path, key: str, check_only: bool, github_actions: bool, default: Optional[str] = None):  # noqa: WPS216
    """Read the value specified by the path from a TOML file.

    The path parameter should be a '.' separated sequences of keys
    that correspond to a path in the TOML structure.

    Example TOML file:

    ---
    title = "My TOML file"

    [info]
    version = "1.0.1"

    [tools.poetry]
    version = "1.1.2"
    files = ['a.py', 'b.py']
    ---

    Read standard keys:

    read_toml.py --path my_file.toml --key title -> "My TOML file"
    read_toml.py --path my_file.toml --key info.version -> "1.0.1"

    Read arrays:

    read_toml.py --path my_file.toml --key tools.poetry.files -> "a.py b.py"

    Read non-leaf keys:

    read_toml.py --path my_file.toml --key tools -> #ERROR

    Check if key exists:

    read_toml.py --path my_file.toml --key tools --check-only -> 1 if key exists
    read_toml.py --path my_file.toml --key tools --check-only -> 0 if key does not exist

    Args:
        path (str): The path to the file.
        key (str): The path to the key to read.
        check_only (bool): If True, only checks if key exists
        github_actions (bool): If True, formats output for Github actions
        default (str, optional): If the key doesn't exist, print this value.
    """
    try:
        output(key, read(path, key), check_only=check_only, github_actions=github_actions)
    except KeyError as ex:
        if check_only:
            console.write('0')
        elif default is not None:
            console.write(default)
        else:
            fail(str(ex))


def output(key: str, value: str, check_only: bool = False, github_actions: bool = False):
    if check_only:
        console.write('1')
    elif github_actions:
        action_key = key.replace('.', '_')
        console.write(f'::set-output name={action_key}::{value}')
    else:
        console.write(value)


def fail(key: str):  # pragma: no cover
    console.error(f'Invalid key: {key}')
    sys.exit(-1)


def main():
    read_toml()
