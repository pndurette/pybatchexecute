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

[The MIT License (MIT)](LICENSE) Copyright © 2023 Pierre Nicolas Durette

--

payload: (rpcid='abc', args=[123])

from gbatchexecute import encode, decode
import gbatchexecute

gbatchexecute.encode()
gbatchexecute.decode()

encode
decode

url
params
form_data
headers

gbe = gbatchexecute(...)

request(url = gbe.url, params = gbe.params, data = gbe.data, headers = gbe.headers)

class PreparedBatchExecute:
    pass