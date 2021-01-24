from dataclasses import dataclass
from enum import Enum, auto
from itertools import accumulate
from json import dumps
from os import linesep
from shutil import get_terminal_size
from typing import Iterable, Iterator, Sequence

from std2.pickle import encode
from std2.tree import recur_sort
from std2.types import never

from .types import Context, Match, Resp


class PrintFmt(Enum):
    json = auto()
    pretty = auto()


@dataclass(frozen=True)
class _PrintMatch:
    row: int
    col_begin: int
    col_end: int
    text: str
    context: Context
    rule: str
    short_reason: str
    reason: str
    replacements: Sequence[str]


def _parse_matches(text: str, matches: Iterable[Match]) -> Iterator[_PrintMatch]:
    lens = tuple(len(line) for line in text.splitlines(keepends=True))
    acc_l = tuple(accumulate(lens))
    l_acc_l = tuple(zip(lens, acc_l))

    for match in matches:
        row = sum(l < match.offset for l in acc_l)
        col_begin = match.offset - sum(l for l, a in l_acc_l if a < match.offset)
        col_end = col_begin + match.length - 1

        match_text = text[match.offset : match.offset + match.length]
        replacements = tuple(r.value for r in match.replacements)

        yield _PrintMatch(
            row=row,
            col_begin=col_begin,
            col_end=col_end,
            text=match_text,
            context=match.context,
            rule=match.rule.id,
            short_reason=match.shortMessage,
            reason=match.message,
            replacements=replacements,
        )


def _pprn_match(match: _PrintMatch, l_pad: int) -> Iterator[str]:
    idx = f"{match.row + 1}:{match.col_begin + 1}:{match.col_end + 1}"
    yield idx.ljust(l_pad)
    yield match.text
    yield linesep

    ctx = match.context
    yield " " * l_pad
    yield ctx.text
    yield linesep
    yield " " * l_pad
    yield " " * ctx.offset
    yield "^" * ctx.length
    yield linesep

    yield " " * l_pad
    yield match.short_reason or match.reason
    yield linesep
    yield linesep


def pprn(fmt: PrintFmt, text: str, resp: Resp, l_pad: int) -> Iterator[str]:
    cols, _ = get_terminal_size()
    if fmt is PrintFmt.json:
        yield dumps(
            recur_sort(encode(resp)),
            check_circular=False,
            ensure_ascii=False,
        )
    elif fmt is PrintFmt.pretty:
        yield resp.language.name
        yield linesep
        yield linesep
        for match in _parse_matches(text, resp.matches):
            yield cols * "*"
            yield linesep
            yield from _pprn_match(match, l_pad=l_pad)
    else:
        never(fmt)
