from libnavi.gui.main import MainWindow
from libnavi.model.note import Note
from appcommon.thirdparty.path import path
from appcommon.model.settings import BaseSettings
import mox
import unittest
import wx


class Test(unittest.TestCase):

    def test_get_current_note(self):
        window = MainWindow()
        self.assert_(window.current_page is None)
        note = Note('dummy', path('./tests/dummy/dummy.txt'))
        note.open()
        self.assertEqual(note, window.current_page.note)
        window.Destroy()

    def test_on_note_closed(self):
        window = MainWindow()
        self.assertEqual(len(window.pages), 0)
        note = Note('dummy', path('./tests/dummy/dummy.txt'))
        note.open()
        self.assertEqual(len(window.pages), 1)
        note.close()
        self.assertEqual(len(window.pages), 0)
        self.assert_(window.current_page is None)
        window.Destroy()
        
    def test_on_settings_changed(self):
        window = MainWindow()
        mocker = mox.Mox()
        register = mocker.CreateMockAnything()
        window.RegisterHotKey = register
        unregister = mocker.CreateMockAnything()
        window.UnregisterHotKey = unregister
        settings = mocker.CreateMock(BaseSettings)
        
        modifiers = wx.MOD_ALT
        key_code = wx.WXK_F1
        register(1, modifiers, key_code)
        
        window.on_setting_changed(settings, 'Options', 'HotKey', '%d,%d' % (modifiers, key_code))
        
        mocker.ReplayAll()
        self.assertEqual(1, window._last_hotkey)
        
        mocker.ResetAll()
        
        unregister(1)
        
        window.on_setting_changed(settings, 'Options', 'HotKey', '')
        
        mocker.ReplayAll()
        self.assertEqual(None, window._last_hotkey)
        
        
        
