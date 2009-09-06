class Options(object):
    def __init__(self):
        self.font = None
        self.hotkey = None
        
    def read(self, settings):
        """Read options from the settings file."""
        self.hotkey = settings.get('Options', 'HotKey')
        self.modifiers = None
        self.key_code = None
        if self.hotkey:
            arr = self.hotkey.split(',')
            if len(arr) >= 2:
                self.modifiers, self.key_code = arr[0:2] 
                self.modifiers = int(self.modifiers) 
                self.key_code = int(self.key_code) 
        
        self.font = settings.get('Options', 'Font') 
        