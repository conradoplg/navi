from libnavi.gui.main import MainWindow
from libnavi.model.note import Note
from appcommon.thirdparty.path import path
import unittest


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
