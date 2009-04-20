from libnavi import config
from appcommon.model.settings import BaseSettings
from libnavi.control.command import CommandController
import mox
import unittest


class Test(unittest.TestCase):

    def test_command(self):
        settings = mox.MockObject(BaseSettings)
        control = mox.MockAnything()
        control.notes = mox.MockAnything()
        
        settings.has_section(config.SHORTCUTS_KEY).AndReturn(False)
        mox.Replay(settings)
        #mox.Replay(control)
        
        c = CommandController(control, settings)
        self.assert_(c.commands)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_command']
    unittest.main()