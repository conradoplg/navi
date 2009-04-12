from wx.lib.pubsub import Publisher

class Note(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
    def open(self, create=False):
        self.text = u''
        if self.path:
            try:
                with self.path.open('r') as f:
                    #TODO: detect encoding
                    self.text = f.read().decode('utf-8')
            except EnvironmentError:
                #TODO: add nicer message
                if not create:
                    raise
            except UnicodeDecodeError:
                #TODO: add nicer message
                raise
        Publisher().sendMessage('note.opened', self)
        
    def save(self, text):
        self.text = text
        if self.path:
            try:
                with self.path.open('w') as f:
                    f.write(text.encode('utf-8'))
            except EnvironmentError:
                #TODO: add nicer message
                raise
            except UnicodeEncodeError:
                #TODO: add nicer message
                raise
        Publisher().sendMessage('note.saved', self)