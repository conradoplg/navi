from appcommon.control.command import BaseCommandController
from appcommon.model.settings import BaseSettings
from appcommon.model.command import CommandCategory, Command
from appcommon.control.main import BaseMainController
from ConfigParser import NoSectionError
from appcommon.model.shortcut import Shortcut
import wx
import unittest
import mox

SECTION = 'section'
DEF_FLAGS = wx.ACCEL_CTRL
DEF_KEY_CODE = ord('A')
KEY_CODE = wx.ACCEL_SHIFT
FLAGS = ord('B')
IDE = 1

class DummyCommandController(BaseCommandController):
    def __init__(self, *args):
        BaseCommandController.__init__(self, *args)
        
    def _get_commands(self):
        cat = CommandCategory('Name')
        cat.append(Command(IDE, 'Name', 'Desc', self.dummy,
                           [Shortcut(DEF_FLAGS, DEF_KEY_CODE)]))
        return [cat]
    
    def dummy(self):
        pass

class Test(unittest.TestCase):

    def test_no_section(self):
        control = mox.MockObject(BaseMainController)
        settings = mox.MockObject(BaseSettings)
        
        settings.has_section(SECTION).AndReturn(False)
        mox.Replay(settings)
        mox.Replay(control)
        
        c = DummyCommandController(control, settings, SECTION)
        self.assertEquals(1, len(c.commands))
        self.assertEquals(1, len(c.command_tree))
        self.assertEquals(DEF_KEY_CODE, c.commands[0].shortcuts[0].key_code)
        self.assertEquals(DEF_FLAGS, c.commands[0].shortcuts[0].flags)

    def test_has_section(self):
        control = mox.MockObject(BaseMainController)
        settings = mox.MockObject(BaseSettings)
        
        settings.has_section(SECTION).AndReturn(True)
        settings.items(SECTION).AndReturn([('%d' % IDE, '%d,%d' % (KEY_CODE, FLAGS))])
        mox.Replay(settings)
        
        c = DummyCommandController(control, settings, SECTION)
        self.assertEquals(1, len(c.commands))
        self.assertEquals(1, len(c.command_tree))
        self.assertEquals(KEY_CODE, c.commands[0].shortcuts[0].key_code)
        self.assertEquals(FLAGS, c.commands[0].shortcuts[0].flags)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_command']
    unittest.main()