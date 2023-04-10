# `batchexecute` response formats

The `rt` parameter[^1] can be used to specify the response format. The following formats are supported:

## No `rt` parameter

The response is a JSON array (minus the initial `)]}'`)
See: [`_decode_rt_default()`](../pybatchexecute/decode.py)

**Example:**

```
)]}'

[["wrb.fr","rpc1id","[\"some\",\"response1\"]",null,null,null,1],
["wrb.fr","rpc2id","[\"some\",\"response2\"]",null,null,null,2],
["di",38],
["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
```

**Explanation:**

```
)]}'

[<envelope 0>,<...>,<envelope n>]
```

**Relevant envelopes are a JSON array of the form:**

```
["wrb.fr","rpc1id","[\"abc\"]\n",null,null,null,"generic"]
 ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
 [0][0]    [0][1]   [0][2]                       [0][6]
 constant  rpc id   rpc response                 envelope index or
 (str)     (str)    (json str)                   "generic" if single envelope
                                                 (str)
```

## `rt` set to `c`

This is the default response format made from Google's own websites.
See: [`_decode_rt_compressed()`](../pybatchexecute/decode.py)

**Example:**

```
)]}'

123
[["wrb.fr","rpc1id","[\"xyz\"]",null,null,null,"1"]]
123
[["wrb.fr","rpc1i2","[\"uvw\"]",null,null,null,"2"]]
12
[["di",38]
123
[["af.httprm",37,"5314567270682293609",6]]
12
[["e",4,null,null,643]]
```

**Explanation:**

```
)]}'

<lenght (int of bytes) of envelope 0>
<envelope 0>
<...>
<lenght (int of bytes) of envelope n>
<envelope n>
```

**Relevant 'envelopes' are a JSON array wrapped in an array of the form:**

```
[["wrb.fr","rpc1id","[\"abc\"]\n",null,null,null,"generic"]]
  ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
  [0][0]    [0][1]   [0][2]                       [0][6]
  constant  rpc id   rpc response                 envelope index or
  (str)     (str)    (json str)                   "generic" if single envelope
                                                  (str)
```

[^1]: [Deciphering Google’s mysterious 'batchexecute' system](https://kovatch.medium.com/deciphering-google-batchexecute-74991e4e446c)
