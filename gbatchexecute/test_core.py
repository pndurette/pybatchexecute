from gbatchexecute import gBatchExecute, gBatchPayload, gBatchExecuteDecodeException
import pytest


def test_init_payload():
    """Payload parameter test: payload gets converted to list"""

    payload = gBatchPayload("abc", [123])
    url = "http://test.com"

    gbe1 = gBatchExecute(payload, url=url)
    gbe2 = gBatchExecute([payload], url=url)

    assert gbe1.payload == gbe2.payload


def test_init_url_mandatory():
    """URL parameter tests: mandatory parameters"""

    payload = gBatchPayload("abc", [123])

    with pytest.raises(AssertionError) as exc1:
        gbe1 = gBatchExecute(payload)

    with pytest.raises(AssertionError) as exc2:
        gbe2 = gBatchExecute(payload, host="abc")

    assert "'host' is required" in str(exc1.value)
    assert "'app' is required" in str(exc2.value)


def test_init_url_output():
    """URL parameter tests: building URLs from parameters"""

    payload = gBatchPayload("abc", [123])

    gbe1 = gBatchExecute(payload, host="abc", app="def")
    gbe2 = gBatchExecute(payload, host="abc", app="def", user="ghi")
    gbe3 = gBatchExecute(payload, url="jkl")

    assert gbe1.url == "https://abc/_/def/data/batchexecute"
    assert gbe2.url == "https://abc/u/ghi/_/def/data/batchexecute"
    assert gbe3.url == "jkl"


def test_init_params():
    """Query 'params' parameter tests: query 'params' and constraints"""

    payload1 = gBatchPayload("abc", [123])
    payload2 = gBatchPayload("def", [123])

    gbe1 = gBatchExecute([payload1, payload2], url="xyz")

    # 'rpcids' is a join and the order is not garanteed
    assert gbe1.params["rpcids"] == "abc,def" or gbe1.params["rpcids"] == "def,abc"

    # 'rt' is always 'c'
    assert gbe1.params["rt"] == "c"

    # '_reqid' is calculated with 'reqid' and 'idx':
    # _reqid = reqid + (idx * 100000)

    # a) explicit 'reqid' and 'idx'
    #    i.e. _reqid = 3 + (3 * 100000)
    gbe2 = gBatchExecute(payload1, url="xyz", idx=3, reqid=3)
    assert gbe2.params["_reqid"] == 3 + (3 * 100000)

    # b) 'idx' is 1 by default
    #    i.e _reqid = 2 + (1 * 100000)
    gbe2 = gBatchExecute(payload1, url="xyz", reqid=2)
    assert gbe2.params["_reqid"] == 2 + (1 * 100000)

    # c) 'reqid' is rand(1, 99999) by default
    #    i.e. _reqid = rand(1, 99999) + (2 * 100000)
    gbe3 = gBatchExecute(payload1, url="xyz", idx=2)
    assert 200001 <= gbe3.params["_reqid"] <= 299999

    # Custom params merged in
    gbe4 = gBatchExecute(payload1, url="xyz", params={"custom": 123})
    assert gbe4.params["custom"] == 123

    # Custom params setter: required keys
    gbe4 = gBatchExecute(payload1, url="xyz")

    with pytest.raises(AssertionError) as exc1:
        # missing 'rpcids'
        gbe4.params = {"rt": 2, "_reqid": 3}

    with pytest.raises(AssertionError) as exc2:
        # missing 'rt'
        gbe4.params = {"rpcids": 1, "_reqid": 3}

    with pytest.raises(AssertionError) as exc3:
        # # missing '_reqid'
        gbe4.params = {"rpcids": 1, "rt": 2}

    assert "params is missing key 'rpcids'" in str(exc1.value)
    assert "params is missing key 'rt'" in str(exc2.value)
    assert "params is missing key '_reqid'" in str(exc3.value)


def test_envelope():
    """_envelope() (or frame) tests for a given payload used to determine 'f.req'"""

    payload = gBatchPayload("abc", [123])
    gbe = gBatchExecute(payload, url="xyz")

    # 1 payload (last elem: 'generic')
    assert gbe._envelope(payload, 0) == ["abc", "[123]", None, "generic"]

    # > 1 payload (last elem: payload index)
    assert gbe._envelope(payload, 1) == ["abc", "[123]", None, "1"]


def test_freq():
    """_freq data value tests, uses _envelope()"""

    payload1 = gBatchPayload("abc", [123])
    payload2 = gBatchPayload("def", [123])

    gbe1 = gBatchExecute(payload1, url="xyz")
    gbe2 = gBatchExecute([payload1, payload2], url="xyz")

    assert gbe1._freq() == """[[["abc","[123]",null,"generic"]]]"""
    assert gbe2._freq() == """[[["abc","[123]",null,"1"],["def","[123]",null,"2"]]]"""


def test_init_data():
    """'data' tests: POST data passed to request, uses _freq"""

    payload = gBatchPayload("abc", [123])

    gbe1 = gBatchExecute(payload, url="xyz")
    assert gbe1.data == {"f.req": """[[["abc","[123]",null,"generic"]]]"""}

    # Custom data setter: required keys
    gbe4 = gBatchExecute(payload, url="xyz")

    with pytest.raises(AssertionError) as exc1:
        # missing 'f.req'
        gbe4.data = {}

    assert f"data is missing key 'f.req'" in str(exc1.value)


def test_init_headers():
    """'headers' tests: default and custom headers"""

    payload = gBatchPayload("abc", [123])

    # Default headers
    gbe1 = gBatchExecute(payload, url="xyz")
    assert gbe1.headers == {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    # Additional headers
    gbe2 = gBatchExecute(payload, url="xyz", headers={"custom": 123})
    assert gbe2.headers == {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "custom": 123,
    }

    # Custom headers setter
    gbe3 = gBatchExecute(payload, url="xyz")
    gbe3.headers = {"custom": 123}
    assert gbe3.headers == {"custom": 123}


def test_decode():
    """Test decoding of raw response string: simple responses"""

    # Simple response:
    # 1x rpcid:
    #   'abc', response: ['xyz']
    raw1 = r"""
)]}'

596
[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""

    assert gBatchExecute.decode(raw=raw1) == [(1, "abc", ["xyz"])]

    # Simple response:
    # 2x rpcid:
    #   'abc', response: ['xyz']
    #   'def', response: ['uvw']
    raw2 = r"""
)]}'

596
[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
596
[["wrb.fr","def","[\"uvw\"]\n",null,null,null,"2"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""

    assert gBatchExecute.decode(raw=raw2) == [
        (1, "abc", ["xyz"]),
        (2, "def", ["uvw"]),
    ]


def test_decode_broken_payload():
    """Test decoding of raw response string: malformed JSON response"""

    # Simple response:
    # 1x rpcid:
    #   'abc', response: malformed JSON string
    raw1 = r"""
)]}'

596
[["wrb.fr","abc","[\"xyz\"]\n bad_json_here ",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""

    with pytest.raises(gBatchExecuteDecodeException) as exc1:
        gBatchExecute.decode(raw=raw1)

    assert "Frame 1 (abc): data is not a valid JSON string" in str(exc1.value)


def test_decode_bad_payload():
    """Test decoding of raw response string: bad encoded string"""

    # Simple response:
    # Bad raw encoded string
    raw1 = r"""not a good raw"""

    with pytest.raises(gBatchExecuteDecodeException) as exc1:
        gBatchExecute.decode(raw=raw1)

    assert "Could not decode any frames" in str(exc1.value)


def test_decode_strict_empty_frame():
    """Test decoding of raw response string: strict mode with an empty frame"""

    # Simple response:
    # 1x rpcid:
    #   'abc', empty response ([])
    raw1 = r"""
)]}'

596
[["wrb.fr","abc","[]",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""
    with pytest.raises(gBatchExecuteDecodeException) as exc1:
        gBatchExecute.decode(raw=raw1, strict=True)

    assert "Frame 1 (abc): data is empty" in str(exc1.value)


def test_decode_strict_bad_inout_len():
    """Test decoding of raw response string: strict mode
    with bad expected number of frames
    """

    # Simple response:
    # 1x rpcid:
    #   'abc', response: ['xyz']
    raw1 = r"""
)]}'

596
[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""

    expected_rpcids = ["abc", "def"]
    with pytest.raises(gBatchExecuteDecodeException) as exc1:
        gBatchExecute.decode(raw=raw1, strict=True, expected_rpcids=expected_rpcids)

    assert "expected: 2, got: 1" in str(exc1.value)


def test_decode_strict_bad_inout_match():
    """Test decoding of raw response string: simple responses"""

    # Simple response:
    # 3x rpcid:
    #   'abc', response: ['xyz']
    #   'def', response: ['uvw']
    #   'ghi', response: ['rst']
    raw1 = r"""
)]}'

596
[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
596
[["wrb.fr","def","[\"uvw\"]\n",null,null,null,"2"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
596
[["wrb.fr","ghi","[\"rst\"]\n",null,null,null,"2"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""

    expected_rpcids = ["def", "def", "mno"]
    with pytest.raises(gBatchExecuteDecodeException) as exc1:
        gBatchExecute.decode(raw=raw1, strict=True, expected_rpcids=expected_rpcids)

    assert "expected: ['def', 'mno'], got: ['abc', 'def', 'ghi']" in str(exc1.value)