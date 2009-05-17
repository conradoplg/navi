from appcommon.thirdparty.moxpatch import patch
from appcommon.model.settings import BaseSettings
from libnavi.gui.main import MainWindow
from libnavi.model import App
from libnavi.control.notes import NotesController
from libnavi.control.command import CommandController
from libnavi.model.options import Options
from libnavi import config
import unittest

from libnavi.control import main as M
import mox


class Test(mox.MoxTestBase):

    def _init(self):
        self.mox.StubOutWithMock(M, 'MainWindow', True)
        self.mox.StubOutWithMock(M, 'BaseSettings', True)
        self.mox.StubOutWithMock(M, 'App', True)
        self.mox.StubOutWithMock(M, 'NotesController', True)
        self.mox.StubOutWithMock(M, 'CommandController', True)
        
        self.main_window = mox.MockAnything()
        self.settings = mox.MockAnything()
        self.app = mox.MockAnything()
        self.notes = mox.MockAnything()
        self.commands = mox.MockAnything()
        
        M.MainWindow().AndReturn(self.main_window)
        M.BaseSettings(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(self.settings)
        M.App(self.settings).AndReturn(self.app)
        M.NotesController(self.app, self.settings, self.main_window, mox.IgnoreArg()).AndReturn(self.notes)
        M.CommandController(mox.IgnoreArg(), self.settings).AndReturn(self.commands)
        
    def test_init(self):
        self._init()
        self.mox.ReplayAll()
        
        c = M.MainController('')

    def test_quit(self):
        self._init()
        self.main_window.Close()
        self.mox.ReplayAll()
        
        c = M.MainController('')
        c.quit()
        
    def test_open_options(self):
        self.mox.StubOutWithMock(M, 'Options', True)
        self._init()
        
        options = mox.MockObject(Options)
        
        M.Options().AndReturn(options)
        options.read(self.settings)
        self.main_window.open_options(options)
        self.mox.ReplayAll()
        
        c = M.MainController('')
        c.open_options()
        
    def test_hide(self):
        self._init()
        
        self.main_window.pages = []

        self.notes.save(self.main_window.pages)
        self.main_window.hide()
        self.mox.ReplayAll()
        
        c = M.MainController('')
        c.hide()
        
    def test_on_program_closed(self):
        self.mox.StubOutWithMock(M, 'logging', True)
        self._init()
        
        page1 = self.mox.CreateMockAnything()
        page1.note = self.mox.CreateMockAnything()
        page1.note.name = 'page1'
        page2 = self.mox.CreateMockAnything()
        page2.note = self.mox.CreateMockAnything()
        page2.note.name = 'page2'
        pages = [page1, page2]
        self.main_window.current_page = None

        self.settings.set('Notes', 'Opened', config.PATH_SEP.join(('page1', 'page2')))
        self.settings.set('Notes', 'Opened', '')
        self.settings.save()
        M.logging.shutdown()
        self.mox.ReplayAll()
        
        c = M.MainController('')
        c.on_program_closed(pages)
        
        