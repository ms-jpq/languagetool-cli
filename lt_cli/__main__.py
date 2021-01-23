from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr, stdin

from .pprn import PrintFmt, pprn
from .req import req


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("server")
    parser.add_argument("source", default="-")
    parser.add_argument(
        "-f",
        "--format",
        choices=tuple(f.name for f in PrintFmt),
        default=PrintFmt.pretty.name,
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    fmt = PrintFmt[args.format]
    try:
        text = stdin.read() if args.source == "-" else Path(args.source).read_text()
    except (FileNotFoundError, PermissionError) as e:
        print(e, file=stderr)
        exit(1)
    else:
        try:
            resp = req(args.server, text=text)
        except Exception as e:
            print(e, file=stderr)
            exit(1)
        else:
            for out in pprn(fmt, text=text, resp=resp):
                print(out, sep="", end="")


try:
    main()
except BrokenPipeError:
    exit()
except KeyboardInterrupt:
    exit(130)
