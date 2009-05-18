class Options(object):
    def __init__(self):
        self.font = None
        self.hotkey = None
        
    def read(self, settings):
        """Read options from the settings file."""
        self.hotkey = settings.get('Options', 'HotKey')
        self.modifiers, self.key_code = self.hotkey.split(',')
        self.modifiers = int(self.modifiers) 
        self.key_code = int(self.key_code) 
        
        self.font = settings.get('Options', 'Font') 
        