from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr, stdin

from .pprn import PrintFmt, pprn
from .req import req


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("server")
    parser.add_argument(
        "source", nargs="?", help="either <source> or <--stdin> must be specified"
    )
    parser.add_argument("-", "--stdin", action="store_true")
    parser.add_argument(
        "-f",
        "--format",
        choices=tuple(f.name for f in PrintFmt),
        default=PrintFmt.pretty.name,
    )
    parser.add_argument("--left-pad", type=int, default=16)
    args = parser.parse_args()
    if not args.stdin and not args.source:
        parser.print_help()
        exit(1)
    else:
        return args


def main() -> None:
    args = _parse_args()
    fmt = PrintFmt[args.format]
    try:
        if args.stdin:
            text = stdin.read()
        elif args.source:
            text = Path(args.source).read_text()
        else:
            assert False
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
            for out in pprn(fmt, text=text, resp=resp, l_pad=args.left_pad):
                print(out, sep="", end="")


try:
    main()
except BrokenPipeError:
    exit()
except KeyboardInterrupt:
    exit(130)
