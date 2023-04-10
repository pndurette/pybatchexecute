import unittest
from typing import List

from pybatchexecute.encode import BatchExecuteRpc, PreparedBatchExecute


class TestPreparedBatchExecuteRpcs(unittest.TestCase):
    def setUp(self):
        self.url_params = {"host": "uvw", "app": "xyz"}

    def test_set_valid_rpcs(self):
        valid_rpcs: List[BatchExecuteRpc] = [
            {"rpcid": "rpc1", "args": [1, 2]},
            {"rpcid": "rpc2", "args": ["a", "b"]},
        ]
        pbe = PreparedBatchExecute(valid_rpcs, **self.url_params)
        self.assertEqual(pbe.rpcs, valid_rpcs)

    def test_set_invalid_rpcs_not_list(self):
        with self.assertRaises(ValueError):
            PreparedBatchExecute("not a list", **self.url_params)

    def test_validate_rpc_not_dict(self):
        pbe = PreparedBatchExecute([], **self.url_params)
        with self.assertRaises(ValueError):
            pbe._validate_rpc("not a dictionary")

    def test_validate_rpc_missing_rpcid(self):
        pbe = PreparedBatchExecute([], **self.url_params)
        invalid_rpc: BatchExecuteRpc = {"args": [1, 2]}
        with self.assertRaises(ValueError):
            pbe._validate_rpc(invalid_rpc)

    def test_validate_rpc_missing_args(self):
        pbe = PreparedBatchExecute([], **self.url_params)
        invalid_rpc: BatchExecuteRpc = {"rpcid": "rpc1"}
        with self.assertRaises(ValueError):
            pbe._validate_rpc(invalid_rpc)

    def test_validate_rpc_invalid_rpcid_type(self):
        pbe = PreparedBatchExecute([], **self.url_params)
        # rpcid must be a string
        invalid_rpc: BatchExecuteRpc = {"rpcid": 123, "args": [1, 2]}
        with self.assertRaises(ValueError):
            pbe._validate_rpc(invalid_rpc)

    def test_validate_rpc_invalid_args_type(self):
        pbe = PreparedBatchExecute([], **self.url_params)
        # args must be a list
        invalid_rpc: BatchExecuteRpc = {
            "rpcid": "rpc1",
            "args": "not a list",
        }
        with self.assertRaises(ValueError):
            pbe._validate_rpc(invalid_rpc)


class TestPreparedBatchExecuteURL(unittest.TestCase):
    def setUp(self):
        self.rpcs = [{"rpcid": "abc", "args": [123]}]

    def test_set_valid_url(self):
        pbe = PreparedBatchExecute(self.rpcs, host="abc", app="def")
        self.assertEqual(pbe.url, "https://abc/_/def/data/batchexecute")

    def test_set_valid_url_with_user(self):
        pbe = PreparedBatchExecute(self.rpcs, host="abc", app="def", user="ghi")
        self.assertEqual(pbe.url, "https://abc/u/ghi/_/def/data/batchexecute")


class TestPreparedBatchExecuteParams(unittest.TestCase):
    def setUp(self):
        self.rpc1 = {"rpcid": "abc", "args": [123]}
        self.rpc2 = {"rpcid": "def", "args": [123]}

        self.url_params = {"host": "uvw", "app": "xyz"}

    def test_rpcids(self):
        """'rpcids' parameter tests: join of 'rpcid' values"""
        pbe = PreparedBatchExecute([self.rpc1, self.rpc2], **self.url_params)
        # 'rpcids' is a join and the order is not garanteed
        self.assertIn(pbe.params["rpcids"], ["abc,def", "def,abc"])

    def test_reqid(self):
        """'_reqid' parameter tests: 'reqid' + (index * 100000)"""
        # a) explicit 'reqid' and 'idx'
        #    i.e. _reqid = 1000 + (3 * 100000)
        pbe1 = PreparedBatchExecute([self.rpc1], reqid=1000, index=3, **self.url_params)
        self.assertEqual(pbe1.params["_reqid"], 1000 + (3 * 100000))

        # b) 'index' is 0 by default
        #    i.e _reqid = 1000 + (0 * 100000)
        pbe2 = PreparedBatchExecute([self.rpc1], reqid=1000, **self.url_params)
        self.assertEqual(pbe2.params["_reqid"], 1000 + (0 * 100000))

        # c) 'reqid' is rand(1000, 9999) by default
        #    i.e. _reqid = rand(1000, 9999) + (2 * 100000)
        gbe3 = PreparedBatchExecute([self.rpc1], index=2, **self.url_params)
        self.assertTrue(200000 <= gbe3.params["_reqid"] <= 209999)

    def test_rt(self):
        """'rt' is set (if not None)"""
        pbe1 = PreparedBatchExecute([self.rpc1], rt="a", **self.url_params)
        pbe2 = PreparedBatchExecute([self.rpc1], rt=None, **self.url_params)
        assert pbe1.params["rt"] == "a"
        assert "rt" not in pbe2.params


class TestPreparedBatchExecuteExecuteData(unittest.TestCase):
    def setUp(self):
        self.rpc1 = {"rpcid": "abc", "args": [123]}
        self.rpc2 = {"rpcid": "def", "args": [123]}

        self.url_params = {"host": "uvw", "app": "xyz"}

    def test_data_freq(self):
        """'data' data value tests"""
        pbe1 = PreparedBatchExecute([self.rpc1], **self.url_params)
        pbe2 = PreparedBatchExecute([self.rpc1, self.rpc2], **self.url_params)

        # 1 RPC (last elem: 'generic')
        assert pbe1.data["f.req"] == '[[["abc","[123]",null,"generic"]]]'

        # > 1 RPC (last elem: RPC index)
        assert (
            pbe2.data["f.req"]
            == '[[["abc","[123]",null,"1"],["def","[123]",null,"2"]]]'
        )


class TestPreparedBatchExecuteExecuteHeaders(unittest.TestCase):
    def setUp(self):
        self.rpc = {"rpcid": "abc", "args": [123]}
        self.url_params = {"host": "uvw", "app": "xyz"}

    def test_headers(self):
        """'headers' data value tests"""
        pbe = PreparedBatchExecute([self.rpc], **self.url_params)
        assert pbe.headers == {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }


if __name__ == "__main__":
    unittest.main()
