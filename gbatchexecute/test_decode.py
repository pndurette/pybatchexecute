import pytest

from gbatchexecute.decode import decode, _decode_rt_compressed, _decode_rt_default

# def test_decode():
#     """Test decoding of raw response string: simple responses"""

#     # Simple response:
#     # 1x rpcid:
#     #   'abc', response: ['xyz']
#     raw1 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"generic"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """

#     assert gBatchExecute.decode(raw=raw1) == [(1, "abc", ["xyz"])]

#     # Simple response:
#     # 2x rpcid:
#     #   'abc', response: ['xyz']
#     #   'def', response: ['uvw']
#     raw2 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 596
# [["wrb.fr","def","[\"uvw\"]\n",null,null,null,"2"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """

#     assert gBatchExecute.decode(raw=raw2) == [
#         (1, "abc", ["xyz"]),
#         (2, "def", ["uvw"]),
#     ]


# def test_decode_broken_payload():
#     """Test decoding of raw response string: malformed JSON response"""

#     # Simple response:
#     # 1x rpcid:
#     #   'abc', response: malformed JSON string
#     raw1 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[\"xyz\"]\n bad_json_here ",null,null,null,"generic"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """

#     with pytest.raises(gBatchExecuteDecodeException) as exc1:
#         gBatchExecute.decode(raw=raw1)

#     assert "Frame 1 (abc): data is not a valid JSON string" in str(exc1.value)


# def test_decode_bad_payload():
#     """Test decoding of raw response string: bad encoded string"""

#     # Simple response:
#     # Bad raw encoded string
#     raw1 = r"""not a good raw"""

#     with pytest.raises(gBatchExecuteDecodeException) as exc1:
#         gBatchExecute.decode(raw=raw1)

#     assert "Could not decode any frames" in str(exc1.value)


# def test_decode_strict_empty_frame():
#     """Test decoding of raw response string: strict mode with an empty frame"""

#     # Simple response:
#     # 1x rpcid:
#     #   'abc', empty response ([])
#     raw1 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[]",null,null,null,"generic"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """
#     with pytest.raises(gBatchExecuteDecodeException) as exc1:
#         gBatchExecute.decode(raw=raw1, strict=True)

#     assert "Frame 1 (abc): data is empty" in str(exc1.value)


# def test_decode_strict_bad_inout_len():
#     """Test decoding of raw response string: strict mode
#     with bad expected number of frames
#     """

#     # Simple response:
#     # 1x rpcid:
#     #   'abc', response: ['xyz']
#     raw1 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """

#     expected_rpcids = ["abc", "def"]
#     with pytest.raises(gBatchExecuteDecodeException) as exc1:
#         gBatchExecute.decode(raw=raw1, strict=True, expected_rpcids=expected_rpcids)

#     assert "expected: 2, got: 1" in str(exc1.value)


# def test_decode_strict_bad_inout_match():
#     """Test decoding of raw response string: simple responses"""

#     # Simple response:
#     # 3x rpcid:
#     #   'abc', response: ['xyz']
#     #   'def', response: ['uvw']
#     #   'ghi', response: ['rst']
#     raw1 = r"""
# )]}'

# 596
# [["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"1"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 596
# [["wrb.fr","def","[\"uvw\"]\n",null,null,null,"2"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 596
# [["wrb.fr","ghi","[\"rst\"]\n",null,null,null,"2"]
# ,["di",38]
# ,["af.httprm",37,"5314567270682293609",6]
# ]
# 26
# [["e",4,null,null,643]
# ]
# """

#     expected_rpcids = ["def", "def", "mno"]
#     with pytest.raises(gBatchExecuteDecodeException) as exc1:
#         gBatchExecute.decode(raw=raw1, strict=True, expected_rpcids=expected_rpcids)

#     assert "expected: ['def', 'mno'], got: ['abc', 'def', 'ghi']" in str(exc1.value)
