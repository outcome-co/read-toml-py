from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from outcome.read_toml import lib as read_toml


class TestGetKeyAndIndex:
    def test_get_non_index(self):
        key = 'my_key'
        ki = read_toml.get_key_and_index(key)
        assert ki is None

    def test_get_index(self):
        key = 'my_key[0]'
        key, index = read_toml.get_key_and_index(key)
        assert key == 'my_key'
        assert index == 0


class TestReadPath:
    def test_read_case(self, sample_toml, read_path_case):
        assert read_toml.read_path(sample_toml, read_path_case['key']) == read_path_case['value']

    def test_incorrect_keys(self, sample_toml):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'bad.path')

    def test_too_many_keys(self, sample_toml):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'info.version.too.many.keys')

    def test_read_index_from_non_array(self, sample_toml):
        with pytest.raises(KeyError):
            read_toml.read_path(sample_toml, 'info[0]')


@pytest.fixture(params=[{1}, {'key': 'value'}, Path('/')])
def bad_value(request):
    return request.param


@patch('outcome.read_toml.lib.read_path', autospec=True)
@patch('outcome.read_toml.lib.toml.loads', autospec=True)
class TestRead:
    def test_read_scalar(self, mock_loads: Mock, mock_read: Mock):
        mock_read.return_value = 1
        assert read_toml.read(Mock(), 'some_key') == '1'

    def test_read_list(self, mock_loads: Mock, mock_read: Mock):
        mock_read.return_value = [1, 2]
        assert read_toml.read(Mock(), 'some_key') == '1 2'

    def test_read_other(self, mock_loads: Mock, mock_read: Mock, bad_value):
        mock_read.return_value = bad_value

        with pytest.raises(KeyError):
            read_toml.read(Mock(), 'some_key')
