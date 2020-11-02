# read-toml-py
![ci-badge](https://github.com/outcome-co/read-toml-py/workflows/Release/badge.svg?branch=v2.0.4) ![version-badge](https://img.shields.io/badge/version-2.0.4-brightgreen)

A small utility to read keys from TOML files.

## Usage

### Installation

```sh
poetry add outcome-read-toml
```

### Usage

The utility reads the value specified by the key from the provided TOML file, and prints it to stdout.

The path parameter should be a '.' separated sequences of keys that correspond to a path in the TOML structure.

Example TOML file:

```toml
title = "My TOML file"

[info]
version = "1.0.1"

[tools.poetry]
version = "1.1.2"
files = ['a.py', 'b.py']
```

Read standard keys:

```sh
read-toml --path my_file.toml --key title 
# "My TOML file"

read-toml --path my_file.toml --key info.version
# "1.0.1"
```

Read arrays:

```sh
read-toml --path my_file.toml --key tools.poetry.files
# "a.py b.py"

read-toml --path my_file.toml[0] --key tools.poetry.files
# "a.py"
```

You can't read non-leaf keys:

```sh
read_toml.py --path my_file.toml --key tools
# KeyError
```

You can check if a key exists:

```sh
read-toml --path my_file.toml --key title --check-only 
# 1

read-toml --path my_file.toml --key unknown_key --check-only
# 0
```

## Development

Remember to run `./pre-commit.sh` when you clone the repository.
