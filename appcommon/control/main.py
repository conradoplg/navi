from __future__ import with_statement, absolute_import

from appcommon.thirdparty.path import path as Path
from appcommon.control import app
import wx



class BaseMainController(object):
    
    def __init__(self, main_script, meta, config):
        self.main_script = Path(main_script)
        
        wx.GetApp().SetAppName(meta.APPNAME)
        
        program_path = app.get_program_path(self.main_script)
        app.init_data_dir()
        app.setup_log(config.LOG_FILE_NAME, meta.DEBUG, meta.LOG_LEVEL)
        self.settings_path = app.get_settings_path(program_path, config.INI_FILE_NAME)

