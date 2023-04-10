# API Reference

* [encode](#encode)
  * [BatchExecuteFunction](#encode.BatchExecuteFunction)
  * [PreparedBatchExecute](#encode.PreparedBatchExecute)
    * [\_\_init\_\_](#encode.PreparedBatchExecute.__init__)
    * [headers](#encode.PreparedBatchExecute.headers)
    * [functions](#encode.PreparedBatchExecute.functions)
    * [functions](#encode.PreparedBatchExecute.functions)
    * [url](#encode.PreparedBatchExecute.url)
    * [reqid](#encode.PreparedBatchExecute.reqid)
    * [reqid](#encode.PreparedBatchExecute.reqid)
    * [params](#encode.PreparedBatchExecute.params)
    * [data](#encode.PreparedBatchExecute.data)
* [decode](#decode)
  * [decode](#decode.decode)

## BatchExecuteFunction

```python
class BatchExecuteFunction(TypedDict)
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L8)

Type hint for a batchexecute function

## PreparedBatchExecute

```python
class PreparedBatchExecute(object)
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L15)

A prepared ``batchexecute`` RPC

This class prepares a ``batchexecute`` RPC for sending.
It provides the URL, URL parameters, headers and POST data for the request,
which can be used to send a POST request using any HTTP library.

**Properties**:
  * ``url`` _str_ - The URL to send the request to
  * ``params`` _dict_ - The URL parameters to send with the request
  * ``data`` _dict_ - The POST data to send with the request
  * ``headers`` _dict_ -  The request headers to send with the request

#### \_\_init\_\_

```python
def __init__(functions: List[BatchExecuteFunction],
             host: str,
             app: str,
             user: str = None,
             reqid: int = None,
             index: int = 0,
             rt: str = None) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L30)

Prepare a ``batchexecute`` RPC

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

**Arguments**:

- `functions` _list_ - A list of functions to execute. Each function is a dictionary with 2 keys:
  * ``rpcid``: The ``rpcid`` of the function to execute
  * ``args``: A list of arguments to pass to the function
- `host` _str_ - The host to send the request to
- `app` _str_ - The app to send the request to
- `user` _str_ - The user to send the request to (default: ``None``)
- `reqid` _int_ - The request ID. Must be a four digit number (default: random if ``None``)
- `index` _int_ - The index of this ``PreparedBatchExecute``, in case many are prepared to
  be sent sequentially. Each prepared request should have an incremental ``index``
  and use the same ``reqid`` (default: ``0``)
- `rt` _str_ - The response type. Can be``"c"`` (compressed),
  ``"b"`` (ProtoBuf), or ``None`` (JSON) (default: ``None``)
  

**Raises**:

- `ValueError` - If ``reqid`` is not a four digit number
- `ValueError` - If any function is of an invalid format

#### headers

```python
@property
def headers() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L92)

Get request headers

#### functions

```python
@property
def functions() -> List[BatchExecuteFunction]
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L99)

Get the functions to be called

#### functions

```python
@functions.setter
def functions(functions: List[BatchExecuteFunction]) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L104)

Set the functions to be called

#### url

```python
@property
def url() -> str
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L117)

Get the URL

#### reqid

```python
@property
def reqid() -> int
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L125)

Get the request ID

#### reqid

```python
@reqid.setter
def reqid(reqid) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L130)

Set the request ID

#### params

```python
@property
def params() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L140)

Build the URL parameters for a ``batchexecute`` RPC

#### data

```python
@property
def data() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/encode.py#L154)

Build the POST data for a ``batchexecute`` RPC

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

**Returns**:

- `dict` - The POST data

#### decode

```python
def decode(raw: str,
           rt: str = None,
           strict: bool = False,
           expected_rpcids: list = [])
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/7a05633b5c6642d4efa1b4865a7b9e0ed9554c47/gbatchexecute/decode.py#L194)

Decode a raw response from a ``batchexecute`` RPC

**Arguments**:

- `raw` _str_ - The raw response text from a ``batchexecute`` RPC
- `rt` _str_ - The ``rt`` parameter used in the ``batchexecute`` RPC (default: ``None``)
- `strict` _bool_ - Whether to raise an exception if the response is empty
  or the input ``rpcid``s are different from the output ``rpcid``s (default: ``False``)
- `expected_rpcids` _list_ - A list of expected ``rpcid`` values,
  ignored if ``strict`` is ``False`` (default: ``[]``)
  

**Returns**:

- `list` - A list of tuples, each tuple containing:
  * ``index`` (int): The index of the response
  * ``rpcid`` (str): The ``rpcid`` of the response
  * ``data`` (list): The JSON data returned by the ``rpcid`` function
  

**Raises**:

- `ValueError` - If ``rt`` is not ``"c"``, ``"b"``, or ``None``
- `BatchExecuteDecodeException` - If nothing could be decoded
- `BatchExecuteDecodeException` - If the count of input and output ``rpcid``s is different
  (if ``strict`` is ``True``)
- `BatchExecuteDecodeException` - If the input and out ``rpcid``s are different
  (if ``strict`` is ``True``)

