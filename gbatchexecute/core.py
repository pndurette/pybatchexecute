# -*- coding: utf-8 -*
from dataclasses import dataclass
from urllib.parse import quote, urlencode
from typing import List, Tuple
import random
import json
import re


@dataclass
class gBatchPayload:
    rpcid: str
    args: list


class gBatchExecute:
    """gBatchExecute -- Construct

    An interface to Google Translate's Text-to-Speech API.

    Args:
        text (string): The text to be read.

    Raises:
        ValueError: When ``lang_check`` is ``True`` and ``lang`` is not supported.
        RuntimeError: When ``lang_check`` is ``True`` but there's an error loading
            the languages dictionary.

    """

    REQ_PARAMS = ["rpcids", "rt", "_reqid"]
    OPT_PARAMS = ["f.sid", "bl", "hl"]
    REQ_DATA = ["f.req"]
    OPT_DATA = ["at"]

    def __init__(
        self,
        payload: List[gBatchPayload],
        url: str = "",
        host: str = "",
        user: str = "",
        app: str = "",
        params: dict = {},
        reqid: int = 0,
        idx: int = 1,
        data: dict = {},
        headers: dict = {},
    ) -> None:

        # payload
        if isinstance(payload, list):
            self.payload = payload
        else:
            self.payload = [payload]

        # url
        if not url:
            assert host, "'host' is required if 'url' is ommited"
            assert app, "'app' is required if 'url' is ommited"
            if not user:
                self.url = f"https://{host}/_/{app}/data/batchexecute"
            else:
                self.url = f"https://{host}/u/{user}/_/{app}/data/batchexecute"
        else:
            self.url = url

        # params
        if reqid:
            assert 0 < reqid < 99999, "'reqid' must be in the 1-99999 range"
        else:
            reqid = random.randrange(1, 99999)

        assert idx > 0, "idx must be great than 0"
        self.params = {**self._base_params(reqid, idx), **params}

        # data
        self.data = {**self._base_data(), **data}

        # headers
        self.headers = {**self._base_headers(), **headers}

    @property
    def url(self) -> str:

        return self._url

    @url.setter
    def url(self, url: str) -> None:

        self._url = url

    @property
    def params(self) -> dict:

        return self._params

    @params.setter
    def params(self, params: dict) -> None:

        for k in self.REQ_PARAMS:
            assert params.get(k), f"params is missing key '{k}'"

        self._params = params

    def _base_params(self, reqid: int, idx: int) -> dict:

        return {
            "rpcids": ",".join(set([p.rpcid for p in self.payload])),
            "rt": "c",
            "_reqid": reqid + (idx * 100000),
        }

    @property
    def data(self) -> dict:

        return self._data

    @data.setter
    def data(self, data: dict) -> None:

        for k in self.REQ_DATA:
            assert data.get(k), f"data is missing key '{k}'"

        self._data = data

    def _base_data(self) -> dict:

        return {"f.req": self._freq()}

    @property
    def headers(self) -> dict:

        return self._headers

    @headers.setter
    def headers(self, headers: dict):

        self._headers = headers

    def _base_headers(self) -> dict:

        return {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    def _freq(self) -> str:

        freq = []

        for payload_idx, p in enumerate(self.payload, start=1):

            if len(self.payload) == 1:
                payload_idx = 0

            freq.append(self._envelope(p, payload_idx))

        freq = [freq]
        return json.dumps(freq, separators=(",", ":"))

    def _envelope(self, payload: gBatchPayload, payload_idx: int = 0) -> list:

        return [
            payload.rpcid,
            json.dumps(payload.args, separators=(",", ":")),
            None,
            str(payload_idx) if payload_idx > 0 else "generic",
        ]

    @staticmethod
    def decode(
        raw: str, strict: bool = False, expected_rpcids: list = []
    ) -> List[Tuple[int, str, list]]:

        # Regex pattern to extract raw data responses (frames)
        p = re.compile(
            pattern=r"""
                (\d+\n)         # <number><\n>
                (?P<frame>.+?)  # 'frame': anything incl. <\n> (re.DOTALL)
                (?=\d+\n|$)     # until <number><\n> or <end>
            """,
            flags=re.DOTALL | re.VERBOSE,
        )

        decoded = []

        for item in p.finditer(raw):

            # A 'frame' group is a json string
            # e.g.: '[["wrb.fr","jQ1olc","[\"abc\"]\n",null,null,null,"generic"]]'
            #          ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
            #          [0][0]    [0][1]   [0][2]                       [0][6]
            #          constant  rpc id   rpc response                 frame index or
            #          (str)     (str)    (json str)                   "generic" if single frame
            #                                                          (str)
            frame_raw = item.group("frame")
            frame = json.loads(frame_raw)

            # Ignore frames that don't have 'wrb.fr' at [0][0]
            # (they're not rpc reponses but analytics etc.)
            if frame[0][0] != "wrb.fr":
                continue

            # index (at [0][6], string)
            # index is 1-based
            # index is "generic" if the response contains a single frame
            if frame[0][6] == "generic":
                index = 1
            else:
                index = int(frame[0][6])

            # rpcid (at [0][1])
            # rpcid's response (at [0][2], a json string)
            rpcid = frame[0][1]

            try:
                data = json.loads(frame[0][2])
            except json.decoder.JSONDecodeError as e:
                raise gBatchExecuteDecodeException(
                    f"Frame {index} ({rpcid}): data is not a valid JSON string. "
                    + "JSON decode error was: "
                    + str(e)
                )

            if strict and data == []:
                raise gBatchExecuteDecodeException(
                    f"Frame {index} ({rpcid}): data is empty (strict)."
                )

            # Append as tuple
            decoded.append((index, rpcid, data))

        # The regex did not match anything
        if len(decoded) == 0:
            raise gBatchExecuteDecodeException(
                "Could not decode any frames. Check format of 'raw'."
            )

        # Sort responses by index ([0])
        decoded = sorted(decoded, key=lambda frame: frame[0])

        if strict:
            in_rpcids = expected_rpcids
            out_rpcids = [rpcid for idx, rpcid, data in decoded]

            in_len = len(in_rpcids)
            out_len = len(out_rpcids)

            if in_len != out_len: # pragma: no cover
                raise gBatchExecuteDecodeException(
                    "Strict: mismatch in/out rcpids numbers, "
                    + f"expected: {in_len}, got: {out_len}."
                    )

            in_set = sorted(set(in_rpcids))
            out_set = sorted(set(out_rpcids))

            if in_set != out_set: # pragma: no cover
                raise gBatchExecuteDecodeException(
                    "Strict: mismatch in/out rcpids, "
                    + f"expected: {in_set}, got: {out_set}."
                    )

        return decoded


"""
https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c
https://github.com/Boudewijn26/gTTS-token/blob/master/docs/november-2020-translate-changes.md
"""


class gBatchExecuteException(Exception):
    pass


class gBatchExecuteDecodeException(gBatchExecuteException):
    pass
