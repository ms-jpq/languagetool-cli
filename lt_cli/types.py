from dataclasses import dataclass
from typing import Literal, Optional, Sequence, Union


@dataclass(frozen=True)
class _DataNode1:
    markup: str


@dataclass(frozen=True)
class _DataNode2:
    text: str


_Data = Sequence[Union[_DataNode1, _DataNode2]]


@dataclass(frozen=True)
class Req:
    language: Union[Literal["auto"], str]
    level: Literal["default", "picky"]
    text: Optional[str]
    data: Optional[_Data]

    dicts: Sequence[str]
    motherTongue: Sequence[str]
    preferredVariants: Sequence[str]

    enabledOnly: bool
    enabledRules: Sequence[str]
    disabledRules: Sequence[str]
    enabledCategories: Sequence[str]
    disabledCategories: Sequence[str]


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
