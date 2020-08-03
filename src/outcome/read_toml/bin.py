#! /usr/bin/env python3

"""A utility to read values from TOML files."""

import os
import sys

import click
from outcome.read_toml.lib import read  # noqa: WPS347


@click.command()
@click.option('--path', help='The path to the TOML file', required=True, type=click.File('r'))
@click.option('--key', help='The path to read from the TOML file', required=True)
@click.option('--check-only', help='If present, only checks if the key is present in the TOML file', is_flag=True, default=False)
def read_toml(path, key: str, check_only: bool):
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

    """
    try:
        output(key, read(path, key), check_only=check_only)
    except KeyError as ex:
        if check_only:
            say(0)
        else:
            fail(str(ex))


def output(key: str, value: str, check_only: bool = False):
    if check_only:
        say(1)
    elif os.environ.get('GITHUB_ACTIONS', False):
        action_key = key.replace('.', '_')
        say(f'::set-output name={action_key}::{value}')
    else:
        say(value)


def fail(key: str):  # pragma: no cover
    say(f'Invalid key: {key}', file=sys.stderr)
    sys.exit(-1)


def say(*args, **kwargs):  # pragma: no cover
    print(*args, **kwargs)  # noqa: T001


def switch_working_directory():
    # If we're in a Github Action, the GITHUB_WORKSPACE variable
    # will be set, and corresponds to the directory mounted as a volume
    # in the Docker.
    #
    # Since we're likely to be working on the files in the GITHUB_WORKSPACE
    # we automatically change directories
    workspace = os.environ.get('GITHUB_WORKSPACE')
    if workspace:
        say(f'Switching to Github Workspace: {workspace}')
        os.chdir(workspace)


def main():
    switch_working_directory()
    read_toml()
