from __future__ import with_statement, absolute_import

from libnavi import meta, util
from libnavi.thirdparty.path import path as Path
from libnavi.gui.main import MainWindow
from libnavi.model.settings import Settings
from libnavi.model import App
from libnavi.control import appcommon
from libnavi.control.notes import NotesController

import wx
from wx.lib.pubsub import Publisher

import logging as log

INI_FILE_NAME = u'%s.ini' % meta.APPNAME
LOG_FILE_NAME = u'%s.log' % meta.APPNAME

class MainController(object):
    
    def __init__(self, main_script):
        self.main_script = Path(main_script)
        wx.GetApp().SetAppName(meta.APPNAME)
        
        program_path = appcommon.get_program_path(self.main_script)
        appcommon.init_data_dir()
        appcommon.setup_log(LOG_FILE_NAME, meta.DEBUG, meta.LOG_LEVEL)
        settings_path = appcommon.get_settings_path(program_path, INI_FILE_NAME)

        self.settings = Settings(settings_path)
        
        self.view = MainWindow(self)
        
        self.model = App(self.settings)
        
        self.notes = NotesController(self.model, self.settings, program_path)
        
        Publisher().subscribe(self.on_program_closed, 'program.closed')
        Publisher().sendMessage('settings.loaded', self.model.settings)
        
        #TODO: use call after? handle exceptions
        self.notes.open_initial_notes()
                
    def quit(self):
        self.view.Close()
        
    def on_program_closed(self, message):
        self.settings.save()
        log.shutdown()
