# -*- coding: utf-8 -*-
from libnavi import util
import unittest

from libnavi.control import notes
from appcommon.thirdparty.path import path as Path


class Test(unittest.TestCase, util.DiffTestCaseMixin):


    def test_get_data_dir(self):
        inexistent_dir = Path('./oroaraoroara')
        default_dir = Path('DEFAULT')
        existent_dir = Path('.')
        existent_file = Path('./test.py')
        empty_dir = ''
        
        res_dir = notes.get_data_dir(inexistent_dir, default_dir)
        self.assertEquals(res_dir, default_dir)
        
        res_dir = notes.get_data_dir(existent_dir, default_dir)
        self.assertEquals(res_dir, existent_dir)

        res_dir = notes.get_data_dir(existent_file, default_dir)
        self.assertEquals(res_dir, default_dir)

        res_dir = notes.get_data_dir(empty_dir, default_dir)
        self.assertEquals(res_dir, default_dir)
        
    def test_get_notes_paths(self):
        correct_notes_paths = [
            Path(u'./tests/dummy/a_2.txt'),
            Path(u'./tests/dummy/a_10.txt'),
            Path(u'./tests/dummy/dummy.txt'),
            Path(u'./tests/dummy/dummy with spaces.txt'),
            Path(u'./tests/dummy/ヅーミー.txt'),
        ]
        notes_paths = notes.get_notes_paths(Path(u'./tests/dummy/'))
        self.assertNoDiff(notes_paths, correct_notes_paths)
        
    def test_get_name_from_path(self):
        path = Path('./test/dummy.txt')
        name = notes.get_name_from_path(path)
        self.assertEquals('dummy', name)
        
        path = Path('./test/dummy')
        name = notes.get_name_from_path(path)
        self.assertEquals('dummy', name)
        
        path = Path('./test/dummy.tmp.txt')
        name = notes.get_name_from_path(path)
        self.assertEquals('dummy.tmp', name)
        
        path = Path('./test/dummy.tmp.txt')
        name = notes.get_name_from_path(path)
        self.assertEquals('dummy.tmp', name)
        
if __name__ == "__main__":
    unittest.main()