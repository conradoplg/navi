from appcommon.thirdparty.path import path as Path
from libnavi import util
import wx

def setup_log(log_file_name, debug, level):
    import logging as log
    if debug:
        log.basicConfig()
    else:
        log_file = Path(wx.StandardPaths.Get().GetUserDataDir()) / log_file_name
        log.basicConfig(filename=log_file, filemode='w')
    log.getLogger().setLevel(level)

def init_data_dir():
    try:
        Path(wx.StandardPaths.Get().GetUserDataDir()).mkdir()
    except:
        pass
    
def should_save_settings_locally(program_path, file_name):
    settings_path = program_path / file_name
    try:
        if settings_path.exists():
            with settings_path.open(mode='a'):
                pass
        else:
            return False
    except:
        return False
    return True

def get_settings_path(program_path, file_name):
    if should_save_settings_locally(program_path, file_name):
        return program_path / file_name
    else:
        return Path(wx.StandardPaths.Get().GetUserDataDir()) / file_name
    
def get_program_path(main_script):
    if util.is_frozen():
        return util.get_exe_path().dirname()
    else:
        return main_script.dirname()

def change_settings_location(settings, program_path, file_name, local):
    if local:
        settings_path = program_path / file_name
        try:
            if not settings_path.exists():
                with settings_path.open(mode='w'):
                    pass
                settings.path = settings_path
        except:
            pass
    else:
        settings_path = program_path / file_name
        try:
            settings_path.remove()
            settings_path = Path(wx.StandardPaths.Get().GetUserDataDir()) / file_name
            settings.path = settings_path
        except:
            pass