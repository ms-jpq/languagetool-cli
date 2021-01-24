from json import dumps, loads
from json.decoder import JSONDecodeError
from typing import Iterable, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlunparse
from urllib.request import Request

from std2.pickle import DecodeError, decode
from std2.urllib import urlopen

from .types import Req, Resp


def _encode_eq(req: Req) -> bytes:
    def cont() -> Iterable[Tuple[str, str]]:
        yield "language", req.language

        if req.data:
            yield "data", dumps(req.data)
        elif req.text:
            yield "text", req.text
        else:
            assert False

        yield "level", req.level
        yield "dicts", ",".join(req.dicts)

        yield "motherTongue", ",".join(req.motherTongue)
        yield "preferredVariants", ",".join(req.preferredVariants)

        yield "enabledOnly", str(req.enabledOnly).lower()
        yield "enabledRules", ",".join(req.enabledRules)
        yield "disabledRules", ",".join(req.disabledRules)
        yield "enabledCategories", ",".join(req.enabledCategories)
        yield "disabledCategories", ",".join(req.disabledCategories)

    return "&".join(f"{k}={quote(v)}" for k, v in cont() if v).encode()


def send_req(server: str, req: Req) -> Resp:
    srv = urlparse(server)
    url = urlunparse((srv.scheme, srv.netloc, "/v2/check", None, None, None))
    data = _encode_eq(req)
    try:
        with urlopen(Request(url=url, data=data)) as resp:
            reply = resp.read().decode()
        json = loads(reply)
        linted: Resp = decode(Resp, json, strict=False)
    except (URLError, HTTPError, JSONDecodeError, DecodeError):
        raise
    else:
        return linted
