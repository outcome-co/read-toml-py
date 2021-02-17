from pathlib import Path
from typing import Any, MutableMapping
from unittest.mock import Mock, patch

import pytest
from outcome.read_toml import lib as read_toml

from .types import ReadCase  # noqa: WPS300


class TestGetKeyAndIndex:
    def test_get_non_index(self):
        key = 'my_key'
        ki = read_toml.get_key_and_index(key)
        assert ki is None

    def test_get_index(self):
        key = 'my_key[0]'
        maybe_key_and_index = read_toml.get_key_and_index(key)
        assert maybe_key_and_index
        key, index = maybe_key_and_index
        assert key == 'my_key'
        assert index == 0


class TestReadPath:
    def test_read_case(self, sample_toml: MutableMapping[str, object], read_path_case: ReadCase):
        assert isinstance(read_path_case, dict)

        key = read_path_case['key']
        assert isinstance(key, str)

        assert read_toml.read_path(sample_toml, key) == read_path_case['value']

    def test_incorrect_keys(self, sample_toml: MutableMapping[str, object]):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'bad.path')

    def test_too_many_keys(self, sample_toml: MutableMapping[str, object]):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'info.version.too.many.keys')

    def test_read_index_from_non_array(self, sample_toml: MutableMapping[str, object]):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'info[0]')


@pytest.fixture(params=[{1}, {'key': 'value'}, Path('/')])
def bad_value(request: Any) -> object:
    return request.param


@pytest.fixture
def mock_loads():
    with patch('outcome.read_toml.lib.toml.loads', autospec=True):
        yield


@pytest.mark.usefixtures('mock_loads')
@patch('outcome.read_toml.lib.read_path', autospec=True)
class TestRead:
    def test_read_scalar(self, mock_read: Mock):
        mock_read.return_value = 1
        assert read_toml.read(Mock(), 'some_key') == '1'

    def test_read_list(self, mock_read: Mock):
        mock_read.return_value = [1, 2]
        assert read_toml.read(Mock(), 'some_key') == '1 2'

    def test_read_other(self, mock_read: Mock, bad_value: object):
        mock_read.return_value = bad_value

        with pytest.raises(KeyError):
            read_toml.read(Mock(), 'some_key')
