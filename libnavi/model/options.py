class Options(object):
    def __init__(self):
        self.font = None
        self.hotkey = None
        
    def read(self, settings):
        """Read options from the settings file."""
        self.hotkey = settings.get('Options', 'HotKey')        
        