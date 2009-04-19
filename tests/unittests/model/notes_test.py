# -*- coding: utf-8 -*-
from libnavi.model.note import Note
from appcommon.thirdparty.path import path as Path
import unittest


class Test(unittest.TestCase):


    def test_open(self):
        note = Note('', Path('./tests/dummy/dummy.txt'))
        note.open()
        self.assertEquals('', note.text)

        note = Note('', Path(u'./tests/dummy/ヅーミー.txt'))
        note.open()
        self.assertEquals(u'ヅーミー\n', note.text)
        
        note = Note('', Path(u'./inexistent'))
        self.assertRaises(EnvironmentError, note.open)
        
        note = Note('', Path(u'./inexistent'))
        note.open(create=True)
        self.assertEquals('', note.text)
        
    def test_save(self):
        note = Note('', Path('./tests/dummy/other.tmp'))
        note.save('test')
        note.open()
        self.assertEquals('test', note.text)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_open']
    unittest.main()