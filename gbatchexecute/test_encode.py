import pytest

from gbatchexecute.encode import PreparedBatchExecute


def test_init_url_output():
    """URL parameter tests: building URLs from parameters"""

    functions = [{"rpcid": "abc", "args": [123]}]

    pbe1 = PreparedBatchExecute(functions, host="abc", app="def")
    pbe2 = PreparedBatchExecute(functions, host="abc", app="def", user="ghi")

    assert pbe1.url == "https://abc/_/def/data/batchexecute"
    assert pbe2.url == "https://abc/u/ghi/_/def/data/batchexecute"


def test_init_functions():
    """Functions parameter tests: functions are validated"""
    # TODO: test for invalid functions
    pass


def test_init_params():
    """Query 'params' parameter tests: query 'params' and constraints"""

    function1 = {"rpcid": "abc", "args": [123]}
    function2 = {"rpcid": "def", "args": [123]}

    url_params = {"host": "uvw", "app": "xyz"}

    pbe1 = PreparedBatchExecute([function1, function2], **url_params)

    # 'rpcids' is a join and the order is not garanteed
    assert pbe1.params["rpcids"] == "abc,def" or pbe1.params["rpcids"] == "def,abc"

    # '_reqid' is calculated with 'reqid' and 'idx':
    # _reqid = reqid + (idx * 100000)

    # a) explicit 'reqid' and 'idx'
    #    i.e. _reqid = 1000 + (3 * 100000)
    pbe2 = PreparedBatchExecute([function1], reqid=1000, index=3, **url_params)
    assert pbe2.params["_reqid"] == 1000 + (3 * 100000)

    # b) 'index' is 0 by default
    #    i.e _reqid = 1000 + (0 * 100000)
    pbe3 = PreparedBatchExecute([function1], reqid=1000, **url_params)
    assert pbe3.params["_reqid"] == 1000 + (0 * 100000)

    # c) 'reqid' is rand(1000, 9999) by default
    #    i.e. _reqid = rand(1000, 9999) + (2 * 100000)
    gbe4 = PreparedBatchExecute([function1], index=2, **url_params)
    assert 200000 <= gbe4.params["_reqid"] <= 209999

    # 'rt' is set (if not None)
    pbe5 = PreparedBatchExecute([function1], rt="a", **url_params)
    pbe6 = PreparedBatchExecute([function1], rt=None, **url_params)
    assert pbe5.params["rt"] == "a"
    assert "rt" not in pbe6.params


# def test_envelope():
#     """_envelope() (or frame) tests for a given payload used to determine 'f.req'"""

#     payload = gBatchPayload("abc", [123])
#     gbe = gBatchExecute(payload, url="xyz")

#     # 1 payload (last elem: 'generic')
#     assert gbe._envelope(payload, 0) == ["abc", "[123]", None, "generic"]

#     # > 1 payload (last elem: payload index)
#     assert gbe._envelope(payload, 1) == ["abc", "[123]", None, "1"]


# def test_freq():
#     """_freq data value tests, uses _envelope()"""

#     payload1 = gBatchPayload("abc", [123])
#     payload2 = gBatchPayload("def", [123])

#     gbe1 = gBatchExecute(payload1, url="xyz")
#     gbe2 = gBatchExecute([payload1, payload2], url="xyz")

#     assert gbe1._freq() == """[[["abc","[123]",null,"generic"]]]"""
#     assert gbe2._freq() == """[[["abc","[123]",null,"1"],["def","[123]",null,"2"]]]"""


# def test_init_data():
#     """'data' tests: POST data passed to request, uses _freq"""

#     payload = gBatchPayload("abc", [123])

#     gbe1 = gBatchExecute(payload, url="xyz")
#     assert gbe1.data == {"f.req": """[[["abc","[123]",null,"generic"]]]"""}

#     # Custom data setter: required keys
#     gbe4 = gBatchExecute(payload, url="xyz")

#     with pytest.raises(AssertionError) as exc1:
#         # missing 'f.req'
#         gbe4.data = {}

#     assert f"data is missing key 'f.req'" in str(exc1.value)


# def test_init_headers():
#     """'headers' tests: default and custom headers"""

#     payload = gBatchPayload("abc", [123])

#     # Default headers
#     gbe1 = gBatchExecute(payload, url="xyz")
#     assert gbe1.headers == {
#         "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
#     }

#     # Additional headers
#     gbe2 = gBatchExecute(payload, url="xyz", headers={"custom": 123})
#     assert gbe2.headers == {
#         "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
#         "custom": 123,
#     }

#     # Custom headers setter
#     gbe3 = gBatchExecute(payload, url="xyz")
#     gbe3.headers = {"custom": 123}
#     assert gbe3.headers == {"custom": 123}
