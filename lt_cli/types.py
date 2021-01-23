from dataclasses import dataclass
from typing import Optional, Sequence, Union


@dataclass(frozen=True)
class _DataNode1:
    markup: str


@dataclass(frozen=True)
class _DataNode2:
    text: str


_Data = Sequence[Union[_DataNode1, _DataNode2]]


@dataclass(frozen=True)
class Req:
    text: Optional[str]
    data: Optional[_Data]
    language: str = "auto"


@dataclass(frozen=True)
class _Lang:
    name: str


@dataclass(frozen=True)
class _Replacement:
    value: str


@dataclass(frozen=True)
class Context:
    text: str
    offset: int
    length: int


@dataclass(frozen=True)
class Match:
    message: str
    shortMessage: str
    offset: int
    length: int
    context: Context
    replacements: Sequence[_Replacement]


@dataclass(frozen=True)
class Resp:
    language: _Lang
    matches: Sequence[Match]
