# -*- coding: utf-8 -*-
from libnavi import util
from libnavi.control.notes import NotesController
from libnavi.model import App
from appcommon.model.settings import BaseSettings
from libnavi.model.note import Note
from libnavi.gui.main import MainWindow
import mox
import unittest

from libnavi.control import notes
from appcommon.thirdparty.path import path as Path


class Test(unittest.TestCase, util.DiffTestCaseMixin):
    
    def test_create(self):
        mocker = mox.Mox()
        settings = mocker.CreateMock(BaseSettings)
        view = mocker.CreateMockAnything()
        
        settings.get('Options', 'DataDir').AndReturn('')
        settings.get('Notes', 'Opened').AndReturn('')
        mocker.ReplayAll()
        
        model = App(settings)
        c = NotesController(model, settings, view, Path('./tests/dummy'))
        self.assert_(model.notes)
        
    def test_create_empty(self):
        mocker = mox.Mox()
        settings = mocker.CreateMock(BaseSettings)
        view = mocker.CreateMockAnything()
        
        settings.get('Options', 'DataDir').AndReturn('')
        settings.get('Notes', 'Opened').AndReturn('')
        mocker.ReplayAll()
        
        model = App(settings)
        c = NotesController(model, settings, view, Path('./tests/dummy/nonotes'))
        self.assertEquals(1, len(model.notes))
        
    def test_open_initial(self):
        mocker = mox.Mox()
        settings = mocker.CreateMock(BaseSettings)
        note = mocker.CreateMock(Note)
        view = mocker.CreateMockAnything()
        note.name = 'Name'
        
        settings.get('Options', 'DataDir').AndReturn('')
        settings.get('Notes', 'Opened').AndReturn('')
        settings.get('Notes', 'CurrentOpened').AndReturn('Name')
        note.open(create=True)
        mocker.ReplayAll()
        
        model = App(settings)
        c = NotesController(model, settings, view, Path('./tests/dummy/nonotes'))
        model.notes = [note]
        c.open_initial()
        
    def test_create_new(self):
        mocker = mox.Mox()
        settings = mocker.CreateMock(BaseSettings)
        view = mocker.CreateMock(MainWindow)
        
        settings.get('Options', 'DataDir').AndReturn('')
        settings.get('Notes', 'Opened').AndReturn('')
        view.ask_note_name().AndReturn('subdummy2')
        mocker.ReplayAll()
        
        model = App(settings)
        c = NotesController(model, settings, view, Path('./tests/dummy/subdummy'))
        c.create_new()
        self.assertEquals(2, len(model.notes))
        self.assertEquals('subdummy2.txt', model.notes[-1].path.name)
        
    def test_create_new_empty_name(self):
        mocker = mox.Mox()
        settings = mocker.CreateMock(BaseSettings)
        view = mocker.CreateMock(MainWindow)
        
        settings.get('Options', 'DataDir').AndReturn('')
        settings.get('Notes', 'Opened').AndReturn('')
        view.ask_note_name().AndReturn('')
        mocker.ReplayAll()
        
        model = App(settings)
        c = NotesController(model, settings, view, Path('./tests/dummy/subdummy'))
        c.create_new()
        self.assertEquals(1, len(model.notes))

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