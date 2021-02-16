from typing import List, TypedDict, Union


class ReadCase(TypedDict):
    name: str
    key: str
    value: Union[List[str], str]
