import json
import random
from typing import List, TypedDict

__all__ = ["PreparedBatchExecute"]


class BatchExecuteFunction(TypedDict):
    """Type hint for a batchexecute function"""

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
        functions: List[BatchExecuteFunction],
        host: str,
        app: str,
        user: str = None,
        reqid: int = None,
        index: int = 0,
        rt: str = None,
    ) -> None:
        """Prepare a ``batchexecute`` RPC

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
            functions (list): A list of functions to execute. Each function is a dictionary with 2 keys:
                * ``rpcid``: The ``rpcid`` of the function to execute
                * ``args``: A list of arguments to pass to the function
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
            ValueError: If any function is of an invalid format

        """
        # Functions
        self.functions = functions

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
    def functions(self) -> List[BatchExecuteFunction]:
        """Get the functions to be called"""
        return self._functions

    @functions.setter
    def functions(self, functions: List[BatchExecuteFunction]) -> None:
        """Set the functions to be called"""
        # Functions must be a list
        if not isinstance(functions, list):
            raise ValueError("'functions' must be a list")

        # Validate each function
        for fct in functions:
            self._validate_function(fct)

        self._functions = functions

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
            "rpcids": ",".join(set([fct["rpcid"] for fct in self.functions])),
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
            [ # List of functions
                [ # Function 'envelope'
                    "<function rpcid>",
                    "<function args stringified JSON>",
                    null,
                    "<index of function or 'generic'>"
                ],
                [...]
            ]
        ]
        ```

        Returns:
            dict: The POST data

        """

        def _envelope(function: BatchExecuteFunction, function_idx: int = 0) -> list:
            """Build an 'envelope' of a function

            Args:
                function (dict): A dictionary with 2 keys:
                    * ``rpcid``: The ``rpcid`` of the function to execute
                    * ``args``: A list of arguments to pass to the function
                function_idx (int): The index of the function in the list of functions

            Returns:
                list: The function 'envelope', of the form::

                    [
                        "<function rpcid>",
                        "<function args stringified JSON>",
                        None,
                        <index of function or "generic" if index is 0>
                    ]

            """

            return [
                function["rpcid"],
                json.dumps(function["args"], separators=(",", ":")),
                None,
                str(function_idx) if function_idx > 0 else "generic",
            ]

        # List of function 'envelopes' to request
        freq = []

        for fct_idx, fct in enumerate(self.functions, start=1):
            if len(self.functions) == 1:
                fct_idx = 0

            freq.append(_envelope(fct, fct_idx))

        # Wrap in outer array, dump to JSON string
        freq = json.dumps([freq], separators=(",", ":"))

        return {"f.req": freq}

    def _validate_function(self, function: BatchExecuteFunction) -> None:
        """Validate a function format for a ``batchexecute`` RPC

        Args:
            function (dict): A dictionary with 2 keys:
                rpcid: The ``rpcid`` of the function to execute
                args: A list of arguments to send to the ``rpcid`` function

        """
        if not isinstance(function, dict):
            raise ValueError("Function must be a dictionary")

        if not "rpcid" in function:
            raise ValueError("Function must have a 'rpcid' key")

        if not "args" in function:
            raise ValueError("Function must have an 'args' key")

        if not isinstance(function["rpcid"], str):
            raise ValueError("Function 'rpcid' must be a string")

        if not isinstance(function["args"], list):
            raise ValueError("Function 'args' must be a list")
