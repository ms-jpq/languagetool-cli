from json import loads
from json.decoder import JSONDecodeError
from typing import Mapping, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlunparse
from urllib.request import Request

from std2.pickle import DecodeError, decode, encode
from std2.urllib import urlopen

from .types import Req, Resp


def req(server: str, text: str) -> Resp:
    srv = urlparse(server)
    url = urlunparse((srv.scheme, srv.netloc, "/v2/check", None, None, None))
    form_data = Req(text=text, data=None)

    data = "&".join(
        f"{key}={quote(val)}"
        for key, val in cast(Mapping[str, str], encode(form_data)).items()
        if val is not None
    ).encode()
    req = Request(url=url, data=data)
    try:
        with urlopen(req) as resp:
            reply = resp.read().decode()
        json = loads(reply)
        linted: Resp = decode(Resp, json, strict=False)
    except (URLError, HTTPError, JSONDecodeError, DecodeError):
        raise
    else:
        return linted
