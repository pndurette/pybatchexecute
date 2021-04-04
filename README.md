# gbatchexecute

> Python module to ease interactions with Google's batchexecute batch RPC system"

# Table of Contents

* [core](#core)
  * [gBatchExecute](#core.gBatchExecute)

<a name="core"></a>
# core

<a name="core.gBatchExecute"></a>
## gBatchExecute Objects

```python
class gBatchExecute()
```

gBatchExecute -- Construct

An interface to Google Translate's Text-to-Speech API.

**Arguments**:

- `text` _string_ - The text to be read.
  

**Raises**:

- `ValueError` - When ``lang_check`` is ``True`` and ``lang`` is not supported.
- `RuntimeError` - When ``lang_check`` is ``True`` but there's an error loading
  the languages dictionary.


# The end