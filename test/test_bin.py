from unittest.mock import Mock, call, patch

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
