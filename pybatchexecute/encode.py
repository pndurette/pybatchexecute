import json
import random
from typing import List, TypedDict

__all__ = ["PreparedBatchExecute"]


class BatchExecuteRpc(TypedDict):
    """Type hint for a batchexecute RPC"""

    rpcid: str
    args: List[str]


class PreparedBatchExecute(object):
    """A prepared ``batchexecute`` RPC

    This class prepares a ``batchexecute`` RPC for sending.
    It provides the URL, URL parameters, headers and POST data for the request,
    which can be used to send a POST request using any HTTP library.

    **Properties**:
      * ``url`` _str_ - The URL to send the request to
      * ``params`` _dict_ - The URL parameters to send with the request
      * ``data`` _dict_ - The POST data to send with the request
      * ``headers`` _dict_ -  The request headers to send with the request

    """

    def __init__(
        self,
        rpcs: List[BatchExecuteRpc],
        host: str,
        app: str,
        user: str = None,
        reqid: int = None,
        index: int = 0,
        rt: str = None,
    ) -> None:
        """Prepare a ``batchexecute`` request

        _The URL_: The URL is built from the ``host``, ``app``, and ``user`` parameters
        (each parameter can be obtained by inspecting an existing request):
        ``https://{host}/_/{app}/data/batchexecute`` or
        ``https://{host}/u/{user}/_/{app}/data/batchexecute`` (if ``user`` is not ``None``)

        _Notes about ``reqid`` and ``index``_:
        The ``_reqid`` parameter is calculated from the ``reqid`` and ``index`` parameters.
        It is meant for when many ``PreparedBatchExecute`` are prepared to be sent sequentially:
        each prepared request should have an incremental ``index`` and use the same ``reqid``.
        It is calculated as ``reqid + (index * 100000)`` (four digits, with ``100000`` added
        onto it with each subsequent request, e.g. ``1234`` , ``101234`` , ``201234``, etc.)

        _Notes about ``rt``_:
        The ``rt`` parameter defines the response. It can be ``"c"`` (compressed),
        ``"b"`` (ProtoBuf), or ``None`` (JSON-ish). See [``decode`` module methods](#decode)
        for more information.

        Args:
            rpcs (list): A list of rpcs to execute. Each RPC is a dictionary with 2 keys:
                * ``rpcid``: The ``rpcid`` of the RPC to execute
                * ``args``: A list of arguments to pass to the RPC
            host (str): The host to send the request to
            app (str): The app to send the request to
            user (str): The user to send the request to (default: ``None``)
            reqid (int): The request ID. Must be a four digit number (default: random if ``None``)
            index (int): The index of this ``PreparedBatchExecute``, in case many are prepared to
                be sent sequentially. Each prepared request should have an incremental ``index``
                and use the same ``reqid`` (default: ``0``)
            rt (str): The response type. Can be``"c"`` (compressed),
                ``"b"`` (ProtoBuf), or ``None`` (JSON) (default: ``None``)

        Raises:
            ValueError: If ``reqid`` is not a four digit number
            ValueError: If any RPC is of an invalid format

        """
        # rpcs
        self.rpcs = rpcs

        # URL components
        self.host = host
        self.app = app
        self.user = user

        # Paramemter components
        self.reqid = reqid
        self.index = index
        self.rt = rt

    @property
    def headers(self) -> dict:
        """Get request headers"""
        return {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    @property
    def rpcs(self) -> List[BatchExecuteRpc]:
        """Get the rpcs to be called"""
        return self._rpcs

    @rpcs.setter
    def rpcs(self, rpcs: List[BatchExecuteRpc]) -> None:
        """Set the rpcs to be called"""
        # rpcs must be a list
        if not isinstance(rpcs, list):
            raise ValueError("'rpcs' must be a list")

        # Validate each RPC
        for fct in rpcs:
            self._validate_rpc(fct)

        self._rpcs = rpcs

    @property
    def url(self) -> str:
        """Get the URL"""
        if not self.user:
            return f"https://{self.host}/_/{self.app}/data/batchexecute"
        else:
            return f"https://{self.host}/u/{self.user}/_/{self.app}/data/batchexecute"

    @property
    def reqid(self) -> int:
        """Get the request ID"""
        return self._reqid

    @reqid.setter
    def reqid(self, reqid) -> None:
        """Set the request ID"""
        if reqid and not 1000 <= reqid <= 9999:
            raise ValueError("'reqid' must be a four digit positive integer")
        elif reqid:
            self._reqid = reqid
        else:
            self._reqid = random.randrange(1000, 9999)

    @property
    def params(self) -> dict:
        """Build the URL parameters for a ``batchexecute`` RPC"""

        params = {
            "rpcids": ",".join(set([fct["rpcid"] for fct in self.rpcs])),
            "_reqid": self._reqid + (self.index * 100000),
        }

        if self.rt:
            params["rt"] = self.rt

        return params

    @property
    def data(self) -> dict:
        """Build the POST data for a ``batchexecute`` RPC

        The data is a dictionary with a single key ``f.req``,
        which looks like, as stringified JSON:

        ```
        [ # Outer array
            [ # List of rpcs
                [ # RPC 'envelope'
                    "<RPC rpcid>",
                    "<RPC args stringified JSON>",
                    null,
                    "<index of RPC or 'generic'>"
                ],
                [...]
            ]
        ]
        ```

        Returns:
            dict: The POST data

        """

        def _envelope(rpc: BatchExecuteRpc, rpc_idx: int = 0) -> list:
            """Build an 'envelope' of a RPC

            Args:
                rpc (dict): A dictionary with 2 keys:
                    * ``rpcid``: The ``rpcid`` of the RPC to execute
                    * ``args``: A list of arguments to pass to the RPC
                rpc_idx (int): The index of the RPC in the list of rpcs

            Returns:
                list: The RPC 'envelope', of the form::

                    [
                        "<RPC rpcid>",
                        "<RPC args stringified JSON>",
                        None,
                        <index of RPC or "generic" if index is 0>
                    ]

            """

            return [
                rpc["rpcid"],
                json.dumps(rpc["args"], separators=(",", ":")),
                None,
                str(rpc_idx) if rpc_idx > 0 else "generic",
            ]

        # List of RPC 'envelopes' to request
        freq = []

        for fct_idx, fct in enumerate(self.rpcs, start=1):
            if len(self.rpcs) == 1:
                fct_idx = 0

            freq.append(_envelope(fct, fct_idx))

        # Wrap in outer array, dump to JSON string
        freq = json.dumps([freq], separators=(",", ":"))

        return {"f.req": freq}

    def _validate_rpc(self, rpc: BatchExecuteRpc) -> None:
        """Validate a RPC format for a ``batchexecute`` RPC

        Args:
            rpc (dict): A dictionary with 2 keys:
                rpcid: The ``rpcid`` of the RPC to execute
                args: A list of arguments to send to the ``rpcid`` RPC

        """
        if not isinstance(rpc, dict):
            raise ValueError("RPC must be a dictionary")

        if not "rpcid" in rpc:
            raise ValueError("RPC must have a 'rpcid' key")

        if not "args" in rpc:
            raise ValueError("RPC must have an 'args' key")

        if not isinstance(rpc["rpcid"], str):
            raise ValueError("RPC 'rpcid' must be a string")

        if not isinstance(rpc["args"], list):
            raise ValueError("RPC 'args' must be a list")
