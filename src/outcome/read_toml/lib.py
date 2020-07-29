"""A utility to read values from TOML files."""

import re
from typing import IO, Any, Dict, Optional, Tuple

import toml

_scalar_types = [int, str, bool, float]


def read(path: IO[str], key: str) -> str:
    parsed_toml = toml.loads(path.read())
    value = read_path(parsed_toml, key)

    # Just print scalars
    if type(value) in _scalar_types:  # noqa: WPS516
        return str(value)

    elif isinstance(value, list):
        return ' '.join(map(str, value))

    # We could theoretically just print out the dict, but we'll fail instead
    raise KeyError(key)


def read_path(node: Dict[str, Any], key: str) -> Any:
    keys = key.split('.')
    keys.reverse()

    while keys:
        # If we still have keys left, and the current node isn't a dict
        # that's an invalid path
        if not isinstance(node, dict):
            raise KeyError

        current_key = keys.pop()
        node = read_key(node, current_key)

    return node


def read_key(node: Any, key: str) -> Any:
    # If the user specified an index on a key,
    # then we want to retrieve the correct map in the list of maps
    key_and_index = get_key_and_index(key)

    if key_and_index:
        key, index = key_and_index
        if not isinstance(node[key], list):
            # This should always be a list when an index is specified
            raise KeyError
        return node[key][index]

    value = node[key]

    # If no index is specified but the object is a list, we assume index is O
    if isinstance(value, list) and len(value) == 1:
        return value[0]

    # This will also throw a KeyError if key isn't available in node
    return value


def get_key_and_index(key: str) -> Optional[Tuple[str, int]]:
    match = re.search(r'\[([0-9]+)\]$', key)
    if match:
        index = int(match.group(1))
        # Get the key without index
        key_without_index = key[: key.find('[')]
        return (key_without_index, index)
    return None
