from __future__ import with_statement, absolute_import

from ConfigParser import SafeConfigParser

from wx.lib.pubsub import Publisher



class UnicodeAwareConfigParser(SafeConfigParser):
    def set(self, section, option, value):
        value = unicode(value).encode('utf-8')
        SafeConfigParser.set(self, section, option, value)

    def get(self, section, option):
        value = SafeConfigParser.get(self, section, option)
        return value.decode('utf-8')
    
    def items(self, section):
        options = self.options(section)
        return [(option, self.get(section, option)) for option in options]
    
    

class Settings(UnicodeAwareConfigParser):
    def __init__(self, path):
        UnicodeAwareConfigParser.__init__(self)
        self.path = path
        self.read(path)
        self.__defaults = self._load_defaults()
        Publisher().sendMessage('settings.changed', self)
        
    def _load_defaults(self):
        defaults = (
          ('Options', 'Font', ''),
          ('Options', 'DataDir', ''),
        )
        for section, option, value in defaults:
            if not self.has_section(section):
                self.add_section(section)
            if not self.has_option(section, option):
                self.set(section, option, value)
        return defaults
    
    def set(self, section, option, value):
        UnicodeAwareConfigParser.set(self, section, option, value)
        Publisher().sendMessage('settings.changed.%s.%s' % (section, option), self)
    
    def save(self):
        if not self.path.parent.exists():
            self.path.parent.makedirs()
        with self.path.open('w') as f:
            self.write(f)
            
    def get_default(self, section, option):
        for isection, ioption, ivalue in self.__defaults:
            if isection == section and ioption == option:
                return ivalue
        raise RuntimeError('Option %s has no default value' % option)
        