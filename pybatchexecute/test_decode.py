import unittest

from pybatchexecute.decode import (BatchExecuteDecodeException,
                                   _decode_rt_compressed, _decode_rt_default,
                                   decode)


class TestDecodeRtCompressed(unittest.TestCase):
    def test_single_rpc(self):
        raw = r"""
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
        expected_output1 = [(1, "abc", ["xyz"])]

        self.assertEqual(_decode_rt_compressed(raw), expected_output1)

    def test_multiple_rpcs(self):
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
26
[["e",4,null,null,643]
]
"""

        expected_output1 = [(1, "abc", ["xyz"]), (2, "def", ["uvw"])]

        self.assertEqual(_decode_rt_compressed(raw1), expected_output1)

    def test_strict_invalid_json_response(self):
        raw = r"""
)]}'
596
[["wrb.fr","abc","[xyz]\n",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""
        with self.assertRaises(BatchExecuteDecodeException):
            _decode_rt_compressed(raw, strict=True)

    def test_strict_empty_response(self):
        raw = r"""
)]}'
596
[["wrb.fr","abc","[]\n",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6]
]
26
[["e",4,null,null,643]
]
"""
        with self.assertRaises(BatchExecuteDecodeException):
            _decode_rt_compressed(raw, strict=True)


class TestDecodeRtDefault(unittest.TestCase):
    def test_single_rpc(self):
        raw = r"""
)]}'

[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"generic"],
["di",38],
["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
"""
        expected_output = [(1, "abc", ["xyz"])]

        self.assertEqual(_decode_rt_default(raw), expected_output)

    def test_multiple_rpcs(self):
        raw1 = r"""
)]}'

[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,1],
["wrb.fr","def","[\"uvw\"]\n",null,null,null,2],
["di",38],
["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
"""

        expected_output1 = [(1, "abc", ["xyz"]), (2, "def", ["uvw"])]

        self.assertEqual(_decode_rt_default(raw1), expected_output1)

    def test_strict_invalid_json_response(self):
        raw = r"""
)]}'

[["wrb.fr","abc","[xyz]\n",null,null,null,"generic"],
["di",38],
["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
"""
        with self.assertRaises(BatchExecuteDecodeException):
            _decode_rt_default(raw, strict=True)

    def test_strict_empty_response(self):
        raw = r"""
)]}'

[["wrb.fr","abc","[]\n",null,null,null,"generic"],
["di",38],
["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
"""
        with self.assertRaises(BatchExecuteDecodeException):
            _decode_rt_default(raw, strict=True)


class TestDecode(unittest.TestCase):
    def test_valid_rt_compressed(self):
        raw = r"""
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
        expected_output = [(1, "abc", ["xyz"])]
        self.assertEqual(decode(raw, rt="c"), expected_output)

    def test_valid_rt_default(self):
        raw = r"""
)]}'

[["wrb.fr","abc","[\"xyz\"]\n",null,null,null,"generic"]
,["di",38]
,["af.httprm",37,"5314567270682293609",6],
["e",4,null,null,643]]
"""
        expected_output = [(1, "abc", ["xyz"])]
        self.assertEqual(decode(raw, rt=None), expected_output)

    def test_invalid_rt(self):
        with self.assertRaises(ValueError):
            decode("test", rt="invalid")

    def test_strict_true_expected_rpcids(self):
        raw = r"""
)]}'

123
[["wrb.fr","abc","[\"xyz\"]",null,null,null,"1"]]
123
[["wrb.fr","def","[\"uvw\"]",null,null,null,"2"]]
"""
        expected_output = [(1, "abc", ["xyz"]), (2, "def", ["uvw"])]
        self.assertEqual(
            decode(raw, rt="c", strict=True, expected_rpcids=["abc", "def"]),
            expected_output,
        )

    def test_strict_true_mismatched_rpcids(self):
        raw = r"""
)]}'

123
[["wrb.fr","abc","[\"xyz\"]",null,null,null,"1"]]
123
[["wrb.fr","ijk","[\"uvw\"]",null,null,null,"2"]]
"""
        with self.assertRaises(BatchExecuteDecodeException):
            decode(raw, rt="c", strict=True, expected_rpcids=["abc", "def"])


if __name__ == "__main__":
    unittest.main()
