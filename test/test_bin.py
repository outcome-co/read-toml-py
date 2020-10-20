from unittest.mock import Mock, call, patch

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


@patch('outcome.read_toml.bin.console.write')
class TestOutput:
    def test_with_github(self, mock_write: Mock, output_case):
        read_toml.output(output_case['key'], output_case['value'], github_actions=True)
        mock_write.assert_called_once_with(output_case['github_value'])

    def test_without_github(self, mock_write: Mock, output_case):
        read_toml.output(output_case['key'], output_case['value'])
        mock_write.assert_called_once_with(output_case['value'])


@pytest.fixture
def isolated_filesystem_runner(sample_toml):
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open('sample.toml', 'w') as handle:
            toml.dump(sample_toml, handle)

        yield runner


class TestCommand:
    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', '123', github_actions=False)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_only_check(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', check_value_present, github_actions=False)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_with_github_actions(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--github-actions'],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', '123', github_actions=True)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_failure(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code != 0

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_failure_only_check(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', check_value_missing, github_actions=False)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_failure_default(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--default', 'foo'],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', 'foo', github_actions=False)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_failure_default_falsy_value(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml_cli, ['--path', './sample.toml', '--key', 'my_key', '--default', ''],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', '', github_actions=False)
