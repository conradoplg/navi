import unittest

from appcommon.model.command import Command, CommandCategory


class Test(unittest.TestCase):


    def test_command(self):
        IDE = 1
        NAME = '&Name...'
        DESC = 'desc'
        SHORTCUT_NAME = 'dummy'
        CLEAN_NAME = 'Name'
        NAME_AND_SHORTCUT = '&Name...\tdummy'
        
        self.flag = 0
        def dummy():
            self.flag = 1
        class DummyShortcut():
            name = SHORTCUT_NAME
            
        DEF_SHORTCUTS = [DummyShortcut()]
        
        c = Command(IDE, NAME, DESC, dummy, DEF_SHORTCUTS)
        
        self.assertEquals(IDE, c.ide)
        self.assertEquals(NAME, c.name)
        self.assertEquals(DESC, c.description)
        self.assertEquals(dummy, c._function)
        self.assertEquals(DEF_SHORTCUTS, c.default_shortcuts)
        self.assertEquals([], c.shortcuts)
        self.assertEquals(c.name_and_shortcut, NAME)
        self.assertEquals(c.clean_name, CLEAN_NAME)
        
        c.load_default_shortcut()
        self.assertEquals(DEF_SHORTCUTS, c.shortcuts)
        self.assertEquals(c.name_and_shortcut, NAME_AND_SHORTCUT)
        
        c()
        self.assertEquals(self.flag, 1)
        
    def test_command_category(self):
        NAME = '&Name'
        CLEAN_NAME = 'Name'
        
        c = CommandCategory(NAME, None)
        
        self.assertEquals(NAME, c.name)
        self.assertEquals(CLEAN_NAME, c.clean_name)
        self.assertEquals(None, c.commands)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_command']
    unittest.main()