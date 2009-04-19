# -*- coding: utf-8 -*-
from appcommon.model.settings import UnicodeAwareConfigParser
from ConfigParser import NoSectionError
import unittest


class Test(unittest.TestCase):

    def test_unicode_parser(self):
        VALUE = u'ダーミー'
        OPTION = 'option'
        SECTION = 'section'
        
        p = UnicodeAwareConfigParser()
        
        p.add_section(SECTION)
        p.set(SECTION, OPTION, VALUE)
        self.assertEquals(VALUE, p.get(SECTION, OPTION))
        
        self.assertRaises(NoSectionError, p.items, 'not exists')
        self.assertEquals([(OPTION, VALUE)], p.items(SECTION))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_settings']
    unittest.main()
