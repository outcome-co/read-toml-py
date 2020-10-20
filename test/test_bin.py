from pathlib import Path
from unittest.mock import Mock, call, mock_open, patch

import pytest
import toml
from click.testing import CliRunner
from outcome.read_toml import bin as read_toml

check_value_present = '1'
check_value_missing = '0'


def test_read_called_in_main():
    m = Mock()
    with patch('outcome.read_toml.bin.read_toml_cli', new=m.read):
        read_toml.main()
        assert m.mock_calls == [call.read()]


# read_toml can take multiple types for the path param
# this test checks that whatever we pass in, we ultimately send
# a file handle to the underlying read method
@pytest.mark.parametrize('path,mocked_open', [('file.toml', mock_open()), (Path('file.toml'), mock_open())])
def test_read_toml_path_types(path, mocked_open):
    with patch('outcome.read_toml.bin.read', autospec=True) as mocked_read:
        with patch('builtins.open', mocked_open, create=True):
            mocked_read.return_value = 'value'

            read_toml.read_toml(path, 'key')

            mocked_read.assert_called_once()
            assert mocked_read.call_args.args[0] == mocked_open(path)


def test_read_toml_path_file_handle():
    with patch('outcome.read_toml.bin.read', autospec=True) as mocked_read:
        mocked_read.return_value = 'value'
        mocked_open_handle = mock_open()('file')

        read_toml.read_toml(mocked_open_handle, 'key')

        mocked_read.assert_called_once()
        assert mocked_read.call_args.args[0] == mocked_open_handle


@pytest.fixture
def isolated_filesystem_runner(sample_toml):
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('sample.toml', 'w') as handle:
            toml.dump(sample_toml, handle)

        yield runner


class TestCommand:
    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code == 0
        mock_write.assert_called_once_with('123')

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call_only_check(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_write.assert_called_once_with(check_value_present)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call_with_github_actions(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code == 0
        mock_write.assert_called_once_with('123')

    @patch('outcome.read_toml.bin.read', autospec=True)
    def test_call_failure(self, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code != 0

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call_failure_only_check(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_write.assert_called_once_with(check_value_missing)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call_failure_default(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--default', 'foo'],
        )
        assert result.exit_code == 0
        mock_write.assert_called_once_with('foo')

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.console.write', autospec=True)
    def test_call_failure_default_falsy_value(self, mock_write: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--default', ''],
        )
        assert result.exit_code == 0
        mock_write.assert_called_once_with('')
