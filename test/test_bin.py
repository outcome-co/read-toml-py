from unittest.mock import Mock, call, patch

import pytest
import toml
from click.testing import CliRunner
from outcome.read_toml import bin as read_toml


def test_switch_called_before_read():
    m = Mock()
    with patch('outcome.read_toml.bin.read_toml', new=m.read):
        with patch('outcome.read_toml.bin.switch_working_directory', new=m.switch):
            read_toml.main()
            assert m.mock_calls == [call.switch(), call.read()]


@patch('outcome.read_toml.bin.say', autospec=True)
@patch('outcome.read_toml.bin.os.chdir', autospec=True)
class TestSwitch:
    @patch.dict('os.environ', {'GITHUB_WORKSPACE': '/workspace'})
    def test_switch(self, mock_chdir: Mock, mock_say: Mock):
        read_toml.switch_working_directory()
        mock_chdir.assert_called_once_with('/workspace')

    @patch.dict('os.environ', {}, clear=True)
    def test_no_switch(self, mock_chdir: Mock, mock_say: Mock):
        read_toml.switch_working_directory()
        mock_chdir.assert_not_called()


@patch('outcome.read_toml.bin.say')
class TestOutput:
    @patch.dict('os.environ', {'GITHUB_ACTIONS': 'true'})
    def test_with_github(self, mock_say: Mock, output_case):
        read_toml.output(output_case['key'], output_case['value'])
        mock_say.assert_called_once_with(output_case['github_value'])

    @patch.dict('os.environ', {}, clear=True)
    def test_without_github(self, mock_say: Mock, output_case):
        read_toml.output(output_case['key'], output_case['value'])
        mock_say.assert_called_once_with(output_case['value'])

    @patch.dict('os.environ', {}, clear=True)
    def test_check_only_without_github(self, mock_say: Mock, output_case):
        read_toml.output(output_case['key'], output_case['value'], check_only=True)
        mock_say.assert_called_once_with(0)


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
        result = isolated_filesystem_runner.invoke(read_toml.read_toml, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', '123', check_only=False)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_only_check(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.return_value = '123'
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_output.assert_called_once_with('my_key', '123', check_only=True)

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.output', autospec=True)
    def test_call_failure(self, mock_output: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(read_toml.read_toml, ['--path', './sample.toml', '--key', 'my_key'])
        assert result.exit_code != 0

    @patch('outcome.read_toml.bin.read', autospec=True)
    @patch('outcome.read_toml.bin.say', autospec=True)
    def test_call_failure_only_check(self, mock_say: Mock, mock_read: Mock, isolated_filesystem_runner):
        mock_read.side_effect = KeyError('my_key')
        result = isolated_filesystem_runner.invoke(
            read_toml.read_toml, ['--path', './sample.toml', '--key', 'my_key', '--check-only'],
        )
        assert result.exit_code == 0
        mock_say.assert_called_once_with(1)
