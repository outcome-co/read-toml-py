import pytest
import toml
import json
from pathlib import Path


sample_file = Path(Path(__file__).parent, 'fixtures', 'sample.toml')
read_cases_file = Path(Path(__file__).parent, 'fixtures', 'read_cases.json')
output_cases_file = Path(Path(__file__).parent, 'fixtures', 'output_cases.json')


@pytest.fixture(scope='session')
def sample_toml():
    with open(sample_file, 'r') as handle:
        return toml.load(handle)


def read_cases():
    with open(read_cases_file, 'r') as handle:
        return json.load(handle)


def output_cases():
    with open(output_cases_file, 'r') as handle:
        return json.load(handle)


@pytest.fixture(params=read_cases())
def read_path_case(request):
    return request.param


@pytest.fixture(params=output_cases())
def output_case(request):
    return request.param
