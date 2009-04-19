from appcommon.thirdparty.path import path as Path
from libnavi import util, config
from libnavi.model.note import Note

from wx.lib.pubsub import Publisher

class NotesController(object):
    def __init__(self, model, settings, default_data_dir):
        self.model = model
        self.settings = settings
        self.data_dir = get_data_dir(self.settings.get('Options', 'DataDir'),
                                     default_data_dir)
        self.notes_paths = get_notes_paths(self.data_dir)
        self.model.notes = [Note(get_name_from_path(path), path)
                            for path in self.notes_paths]
        if not self.model.notes:
            path = self.data_dir / config.DEFAULT_NOTE_FILE_NAME
            note = Note(get_name_from_path(path), path)
            self.model.notes = [note]
        Publisher().subscribe(self.on_program_close, 'program.closed')
        
    def open_initial_notes(self):
        for note in self.model.notes:
            note.open(create=True)
    
    def open_new_note(self, name):
        path = self.data_dir / (name + config.DEFAULT_NOTE_EXTENSION)
        note = Note(get_name_from_path(path), path)
        self.model.notes.append(note)
        note.open(create=True)
        
    def save_notes(self, pages):
        for page in pages:
            page.note.save(page.text.GetValue())
        
    def on_program_close(self, message):
        pass

def get_data_dir(data_dir_specified, default_data_dir):
    isdir = True
    try:
        if data_dir_specified:
            isdir = data_dir_specified.isdir()
        else:
            isdir = False
    except EnvironmentError:
        isdir = False
        
    if not isdir:
        return default_data_dir
    else:
        return data_dir_specified
    
def get_notes_paths(data_dir):
    #ensure we list unicode file names
    data_dir = Path(unicode(data_dir))
    return sorted(data_dir.files('*.txt'), key=util.file_alphanum_key)

def get_name_from_path(path):
    return Path(path.name).stripext()
