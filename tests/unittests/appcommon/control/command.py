from appcommon.control.command import BaseCommandController
from appcommon.model.settings import BaseSettings
from appcommon.model.command import CommandCategory, Command
from appcommon.control.main import BaseMainController
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
NAME1 = 'Name'
NAME2 = 'Nome'
DESC1 = 'Description'
DESC2 = 'Descricao'

class DummyCommandController(BaseCommandController):
    def __init__(self, control, settings, section):
        self._name = NAME1
        self._cat_name = NAME1
        self._desc = DESC1
        self._called = False
        BaseCommandController.__init__(self, control, settings, section)
        
    def _get_commands(self):
        cat = CommandCategory(self._name)
        cat.append(Command(IDE, self._name, self._desc, self.dummy,
                           [Shortcut(DEF_FLAGS, DEF_KEY_CODE)]))
        return [cat]
    
    def dummy(self):
        self._called = True
    
    def change_language(self):
        self._name = NAME2
        self._cat_name = NAME2
        self._desc = DESC2

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
        mox.Replay(control)
        
        c = DummyCommandController(control, settings, SECTION)
        self.assertEquals(1, len(c.commands))
        self.assertEquals(1, len(c.command_tree))
        self.assertEquals(KEY_CODE, c.commands[0].shortcuts[0].key_code)
        self.assertEquals(FLAGS, c.commands[0].shortcuts[0].flags)
        
    def test_set_shortcuts(self):
        control = mox.MockObject(BaseMainController)
        settings = mox.MockObject(BaseSettings)
        
        settings.has_section(SECTION).AndReturn(False)
        settings.remove_section(SECTION)
        settings.add_section(SECTION)
        settings.set(SECTION, '%d' % IDE, '%d,%d' % (KEY_CODE, FLAGS))
        mox.Replay(settings)
        mox.Replay(control)
        
        c = DummyCommandController(control, settings, SECTION)
        shortcuts_dic = {c.commands[0]: [Shortcut(FLAGS, KEY_CODE)]}
        c.set_shortcuts(shortcuts_dic)

    def test_change_language(self):
        control = mox.MockObject(BaseMainController)
        settings = mox.MockObject(BaseSettings)
        
        settings.has_section(SECTION).AndReturn(False)
        mox.Replay(settings)
        mox.Replay(control)
        
        c = DummyCommandController(control, settings, SECTION)
        c.change_language()
        c.on_language_changed(None)
        self.assertEquals(NAME2, c.commands[0].name)
        self.assertEquals(DESC2, c.commands[0].description)
        self.assertEquals(NAME2, c.command_tree[0].name)

    def test_command_execute(self):
        control = mox.MockObject(BaseMainController)
        settings = mox.MockObject(BaseSettings)
        
        settings.has_section(SECTION).AndReturn(False)
        mox.Replay(settings)
        mox.Replay(control)
        
        c = DummyCommandController(control, settings, SECTION)
        class Dummy(object): data = 1
        c.on_command_execute(Dummy)
        self.assert_(c._called)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_command']
    unittest.main()