from __future__ import with_statement, absolute_import

from libnavi import meta, config
from libnavi.gui.main import MainWindow
from libnavi.settings import DEFAULTS as SETTINGS_DEFAULTS
from libnavi.model import App
from libnavi.control.notes import NotesController
from appcommon.control.main import BaseMainController
from appcommon.model.settings import BaseSettings
from pubsub import pub
import logging



class MainController(BaseMainController):
    
    def __init__(self, main_script):        
        BaseMainController.__init__(self, main_script, meta, config)
        
        self.settings = BaseSettings(self.settings_path, SETTINGS_DEFAULTS)
        self.view = MainWindow(self)
        self.model = App(self.settings)        
        self.notes = NotesController(self.model, self.settings, self.settings_path.parent)
        
        pub.subscribe(self.on_program_closed, 'program.closed')
        
        #TODO: use call after? handle exceptions
        self.notes.open_initial()
        
    def quit(self):
        self.view.Close()
        
    def on_program_closed(self, pages):
        self.settings.save()
        logging.shutdown()
