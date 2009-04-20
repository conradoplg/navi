from appcommon.util import flattened_chain, flattened_full_chain
import unittest


class Test(unittest.TestCase):

    def test_flattened_chain(self):
        lst = [0, 1, [2, 3], [4, [5, 6]], [7]]
        flattened_lst = range(8)
        self.assertEquals(flattened_lst, list(flattened_chain(lst))) 

    def test_flattened_full_chain(self):
        lst = [0, 1, [2, 3], [4, [5, 6]], [7]]
        flattened_lst = [0, 1, [2, 3], 2, 3, [4, [5, 6]], 4, [5, 6], 5, 6, [7], 7]
        self.assertEquals(flattened_lst, list(flattened_full_chain(lst))) 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_flattened_chain']
    unittest.main()