from __future__ import with_statement, absolute_import

from libnavi import meta, config
from libnavi.gui.main import MainWindow
from libnavi.settings import DEFAULTS as SETTINGS_DEFAULTS
from libnavi.model import App
from libnavi.control.notes import NotesController
from appcommon.control.main import BaseMainController
from appcommon.model.settings import BaseSettings
from pubsub import pub
from libnavi.control.command import CommandController
import wx
import logging



class MainController(BaseMainController):
    
    def __init__(self, main_script):        
        BaseMainController.__init__(self, main_script, meta, config)
        
        self.settings = BaseSettings(self.settings_path, SETTINGS_DEFAULTS)
        self.view = MainWindow()
        self.model = App(self.settings)
        self.notes = NotesController(self.model, self.settings, self.view, self.settings_path.parent)
        self.commands = CommandController(self, self.settings)
        
        pub.subscribe(self.on_program_closed, 'program.closed')
        pub.subscribe(self.on_page_key_down, 'page.key_down')
        
        #TODO: use call after? handle exceptions
        self.notes.open_initial()
        
    def quit(self):
        self.view.Close()
        
    def open_options(self):
        pass
    
    def hide(self):
        self.notes.save(self.view.pages)
        self.view.hide()
        
    def on_program_closed(self, pages):
        self.settings.save()
        logging.shutdown()
        
    def on_page_key_down(self, key_code, flags):
        if key_code == wx.WXK_ESCAPE:
            self.hide()
