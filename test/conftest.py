import json
from pathlib import Path
from typing import Any, List, Union, cast

import pytest
import toml
from pydantic import BaseModel

from .types import ReadCase  # noqa: WPS300

sample_file = Path(Path(__file__).parent, 'fixtures', 'sample.toml')
read_cases_file = Path(Path(__file__).parent, 'fixtures', 'read_cases.json')
output_cases_file = Path(Path(__file__).parent, 'fixtures', 'output_cases.json')


class ReadCaseValidator(BaseModel):
    name: str
    key: str
    value: Union[str, List[str]]


@pytest.fixture(scope='session')
def sample_toml():
    with open(sample_file, 'r') as handle:
        return toml.load(handle)


def read_cases():
    with open(read_cases_file, 'r') as handle:
        records = json.load(handle)
        assert isinstance(records, list)
        return cast(List[object], records)


def output_cases():
    with open(output_cases_file, 'r') as handle:
        return json.load(handle)


@pytest.fixture(params=read_cases())
def read_path_case(request: Any) -> ReadCase:
    return cast(ReadCase, ReadCaseValidator(**request.param).dict())


@pytest.fixture(params=output_cases())
def output_case(request: Any) -> object:
    return request.param
