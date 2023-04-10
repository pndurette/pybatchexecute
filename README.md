# pybatchexecute

> Python package to ease interactions with Google's `batchexecute` batch RPC system. It assists in preparing requests for it and decoding responses returned from it.

This package codifies the research of Ryan Kovatch[^1] and Boudewijn van Groos[^2] about Google's `/batchexecute` endpoint used accross Google Web applications.

## Usage

### Prepare a request

```python
>>> from pybatchexecute import PreparedBatchExecute
>>>
>>> # RPCs to call
>>> rpc1 = {"rpcid": "rpc1id", "args": ["some", "args"]}
>>> rpc2 = {"rpcid": "rpc2id", "args": ["some", "args"]}
>>>
>>> # Prepare request
>>> pbe = PreparedBatchExecute(
...     rpcs=[rpc1, rpc2],
...     host="example.com",
...     app="example",
... )
>>>
>>> # Access request attributes
>>> pbe.url
'https://example.com/_/example/data/batchexecute'
>>> pbe.headers
{'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
>>> pbe.params
{'rpcids': 'rpc1id,rpc2id', '_reqid': 3807}
>>> pbe.data
{'f.req': '[[["rpc1id","[\\"some\\",\\"args\\"]",null,"1"],["rpc2id","[\\"some\\",\\"args\\"]",null,"2"]]]'}
```

Use the `url`, `headers`, `params` and `data` attributes (optionally combined with your own, e.g. an `at` parameter[^1] or a `Cookie` header[^1] for authenticated requests) to make a POST request with the HTTP library of your choice (e.g. [`requests`](https://requests.readthedocs.io/en/latest/)).

## Decode a response

```python
>>> from pybatchexecute import decode
>>>
>>> # Raw response
>>> # (from a request made with no `rt` parameter)
>>> raw_reponse = r"""
... )]}'
...
... [["wrb.fr","rpc1id","[\"some\",\"response1\"]",null,null,null,1],
... ["wrb.fr","rpc2id","[\"some\",\"response2\"]",null,null,null,2],
... ["di",38],
... ["af.httprm",37,"5314567270682293609",6],
... ["e",4,null,null,643]]
... """
>>>
>>> # Decode response
>>> # List of tuples (index, rpcid, response)
>>> decode(raw)
[(1, 'rpc1id', ['some', 'response1']), (2, 'rpc2id', ['some', 'response2'])]
```

### Documentation

See [docs/](docs/) for more:

* [API reference](docs/api.md)
* [Response formats](docs/response-formats.md)

## Disclaimer

This project is *not* affiliated with Google. It is intended for use in accordance with [Google's Terms of Service](https://policies.google.com/terms).

## Licence

[The MIT License (MIT)](LICENSE) Copyright © 2023 Pierre Nicolas Durette

[^1]: [Deciphering Google’s mysterious 'batchexecute' system](https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c)

[^2]: [November 2020 Google Translate API Changes](https://github.com/Boudewijn26/gTTS-token/blob/master/docs/november-2020-translate-changes.md)