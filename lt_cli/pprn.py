from dataclasses import dataclass
from enum import Enum, auto
from itertools import accumulate
from json import dumps
from os import linesep
from typing import Iterable, Iterator, Sequence

from std2.pickle import encode
from std2.tree import recur_sort
from std2.types import never

from .consts import L_PAD
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
        reason = match.message or match.shortMessage

        yield _PrintMatch(
            row=row,
            col_begin=col_begin,
            col_end=col_end,
            text=match_text,
            context=match.context,
            reason=reason,
            replacements=replacements,
        )


def _pprn_match(match: _PrintMatch, just: int) -> Iterator[str]:
    idx = f"{match.row + 1}:{match.col_begin + 1}:{match.col_end + 1}"
    yield idx.ljust(just)
    yield match.text
    yield linesep

    ctx = match.context
    yield " " * just
    yield ctx.text
    yield linesep
    yield " " * just
    yield " " * ctx.offset
    yield "^" * ctx.length
    yield linesep

    yield " " * just
    yield match.reason
    yield linesep
    yield linesep


def pprn(fmt: PrintFmt, text: str, resp: Resp) -> Iterator[str]:
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
            yield from _pprn_match(match, just=L_PAD)
    else:
        never(fmt)
