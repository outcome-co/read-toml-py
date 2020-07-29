# from pathlib import Path

# import pytest
# from bin import read_toml
# from unittest.mock import patch, Mock, call


# def test_switch_called_before_read():
#     m = Mock()
#     with patch('bin.read_toml.read_toml', new=m.read):
#         with patch('bin.read_toml.switch_working_directory', new=m.switch):
#             read_toml.main()
#             assert m.mock_calls == [call.switch(), call.read()]


# @patch('bin.read_toml.say', autospec=True)
# @patch('bin.read_toml.os.chdir', autospec=True)
# class TestSwitch:

#     @patch.dict('os.environ', {'GITHUB_WORKSPACE': '/workspace'})
#     def test_switch(self, mock_chdir: Mock, mock_say: Mock):
#         read_toml.switch_working_directory()
#         mock_chdir.assert_called_once_with('/workspace')

#     @patch.dict('os.environ', {}, clear=True)
#     def test_no_switch(self, mock_chdir: Mock, mock_say: Mock):
#         read_toml.switch_working_directory()
#         mock_chdir.assert_not_called()


# class TestGetKeyAndIndex:
#     def test_get_non_index(self):
#         key = 'my_key'
#         ki = read_toml.get_key_and_index(key)
#         assert ki is None

#     def test_get_index(self):
#         key = 'my_key[0]'
#         key, index = read_toml.get_key_and_index(key)
#         assert key == 'my_key'
#         assert index == 0


# class TestReadPath:

#     def test_read_case(self, sample_toml, read_path_case):
#         assert read_toml.read_path(sample_toml, read_path_case['key']) == read_path_case['value']

#     def test_incorrect_keys(self, sample_toml):
#         with pytest.raises(KeyError):
#             read_toml.read_path(sample_toml, 'bad.path')

#     def test_too_many_keys(self, sample_toml):
#         with pytest.raises(KeyError):
#             read_toml.read_path(sample_toml, 'info.version.too.many.keys')

#     def test_read_index_from_non_array(self, sample_toml):
#         with pytest.raises(KeyError):
#             read_toml.read_path(sample_toml, 'info[0]')


# @patch('bin.read_toml.say')
# class TestOutput:

#     @patch.dict('os.environ', {'GITHUB_ACTIONS': 'true'})
#     def test_with_github(self, mock_say: Mock, output_case):
#         read_toml.output(output_case['key'], output_case['value'])
#         mock_say.assert_called_once_with(output_case['github_value'])

#     @patch.dict('os.environ', {}, clear=True)
#     def test_without_github(self, mock_say: Mock, output_case):
#         read_toml.output(output_case['key'], output_case['value'])
#         mock_say.assert_called_once_with(output_case['value'])


# @pytest.fixture(params=[
#     {1},
#     {'key': 'value'},
#     Path('/')
# ])
# def bad_value(request):
#     return request.param


# @patch('bin.read_toml.read_path', autospec=True)
# @patch('bin.read_toml.output', autospec=True)
# @patch('bin.read_toml.toml.loads', autospec=True)
# @patch('bin.read_toml.fail', autospec=True)
# class TestRead:

#     def test_read_scalar(self, mock_fail: Mock, mock_loads: Mock, mock_output: Mock, mock_read: Mock):
#         mock_read.return_value = 1

#         read_toml.read(Mock(), 'some_key')
#         mock_output.assert_called_once_with('some_key', 1)

#     def test_read_list(self, mock_fail: Mock, mock_loads: Mock, mock_output: Mock, mock_read: Mock):
#         mock_read.return_value = [1, 2]

#         read_toml.read(Mock(), 'some_key')
#         mock_output.assert_called_once_with('some_key', '1 2')

#     def test_read_other(self, mock_fail: Mock, mock_loads: Mock, mock_output: Mock, mock_read: Mock, bad_value):
#         mock_read.return_value = bad_value

#         read_toml.read(Mock(), 'some_key')
#         mock_fail.assert_called_once()
