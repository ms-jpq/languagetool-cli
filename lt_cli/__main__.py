from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import stderr, stdin

from .pprn import PrintFmt, pprn
from .req import send_req
from .types import Req


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
        text = stdin.read() if args.stdin else Path(args.source).read_text()
    except (FileNotFoundError, PermissionError) as e:
        print(e, file=stderr)
        exit(1)
    else:
        req = Req(
            level=args.level,
            text=text,
            data=None,
            dicts=args.dicts,
            motherTongue=args.mother_tongue,
            preferredVariants=args.preferred_variants,
            enabledOnly=args.enabled_only,
            enabledRules=args.enabled_rules,
            disabledRules=args.disabled_rules,
            enabledCategories=args.enabled_categories,
            disabledCategories=args.disabled_categories,
        )
        try:
            resp = send_req(args.server, req=req)
        except Exception as e:
            print(e, file=stderr)
            exit(1)
        else:
            for out in pprn(fmt, text=text, resp=resp, l_pad=args.left_pad):
                print(out, sep="", end="")


try:
    main()
except BrokenPipeError:
    exit(13)
except KeyboardInterrupt:
    exit(130)
