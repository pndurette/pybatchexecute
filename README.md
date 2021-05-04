# gbatchexecute

gbatchexecute is a Python module to ease interactions with Google's `batchexecute` batch RPC system. It is based on the research of **Ryan Kovatch** ([_Deciphering Google’s mysterious `batchexecute` system_](https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c)) and **Boudewijn van Groos** ([_November 2020 Google Translate API Changes_](https://github.com/Boudewijn26/gTTS-token/blob/master/docs/november-2020-translate-changes.md)).

See Ryan Kovatch's [_Deciphering Google’s mysterious `batchexecute` system_](https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c) for an in-depth understanding of all the fields.

## Usage

```python
hello
```

## Disclaimer

This project is *not* affiliated with Google. Breaking upstream changes *can* occur without notice.

## Licence

[The MIT License (MIT)](LICENSE) Copyright © 2021 Pierre Nicolas Durette

---

<!--
The refreshed API reference is inserted after this token
See $.hooks.post-render in pydoc-markdown.yaml
-->

<!--API_REF-->
# API Reference

* [core](#core)
  * [gBatchPayload](#core.gBatchPayload)
  * [gBatchExecute](#core.gBatchExecute)
    * [\_\_init\_\_](#core.gBatchExecute.__init__)
    * [url](#core.gBatchExecute.url)
    * [url](#core.gBatchExecute.url)
    * [params](#core.gBatchExecute.params)
    * [params](#core.gBatchExecute.params)
    * [data](#core.gBatchExecute.data)
    * [data](#core.gBatchExecute.data)
    * [headers](#core.gBatchExecute.headers)
    * [headers](#core.gBatchExecute.headers)

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L2)

## gBatchPayload

```python
@dataclass
class gBatchPayload()
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L11)

A payload for ``batchexecute`` RPCs

**Arguments**:

- `rpcid` _string_ - The RPCid of the function to execute.
- `args` _list_ - A list of arguments to send to the ``rpcid`` function.

## gBatchExecute

```python
class gBatchExecute()
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L24)

A class to help with the preparation of Web requests for Google's
``batchexecute`` RPC-type functions and the decoding of its responses

#### \_\_init\_\_

```python
 | __init__(payload: List[gBatchPayload], url: str = "", host: str = "", user: str = "", app: str = "", params: dict = {}, reqid: int = 0, idx: int = 1, data: dict = {}, headers: dict = {}) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L35)

Intereact with ``batchexecute`` RPCs

**Arguments**:

- `payload` _List[gBatchPayload]_ - A list of payloads (gBatchExecute) to send ``batchexecute``.
- `url` _string_ - Something
- `host` _string_ - Something
- `user` _string_ - Something
- `app` _string_ - Something
- `params` _dict_ - Something
- `reqid` _int_ - Something
- `idx` _int_ - Something
- `data` _dict_ - Something
- `headers` _dict_ - Something

#### url

```python
 | @property
 | url() -> str
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L97)

Get the full URL of a request

#### url

```python
 | @url.setter
 | url(url: str) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L103)

Set the full URL of a request

#### params

```python
 | @property
 | params() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L109)

Get the url request parameters

#### params

```python
 | @params.setter
 | params(params: dict) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L115)

Set the request url parameters

#### data

```python
 | @property
 | data() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L133)

Get the request POST data

#### data

```python
 | @data.setter
 | data(data: dict) -> None
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L139)

Set the request POST data

#### headers

```python
 | @property
 | headers() -> dict
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L153)

Get request headers

#### headers

```python
 | @headers.setter
 | headers(headers: dict)
```

[[view_source]](https://github.com/pndurette/gbatchexecute/blob/4ce5af31edca67a68008b21220e1000ea9fbc28c/gbatchexecute/core.py#L159)

Set the request headers

