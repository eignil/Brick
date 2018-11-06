import unittest

import json_util
import print_util
import dict_util

class TestPrintUtil(unittest.TestCase):
    json_data = {"nodename":"aaa","ip-address":"172","test1":{"test1_node":"test1_node_val","test2_node":True}}


    def test_print_json(self):
        print_util.print_json(TestPrintUtil.json_data)

class TestDictUtil(unittest.TestCase):
    def setUp(self):
        self.dict_a = {"test1":{"test1_node":"test1_node_val","test2_node":True}}
        self.dict_b = {"test1":{"test1_node":"test1_node_val","test2_node":False}}
        self.dict_c = {"nodename":"aaa","ip-address":"172","test1":{"test1_node":"test1_node_val","test2_node":True}}

    def test_is_dict_in(self):
        res = dict_util.is_dict_in(self.dict_a,self.dict_c)
        self.assertTrue(res)
        res = dict_util.is_dict_in(self.dict_b,self.dict_c)
        self.assertFalse(res)
        res = dict_util.is_dict_in(self.dict_c,self.dict_c)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()