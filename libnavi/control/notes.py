from appcommon.thirdparty.path import path as Path
from libnavi import util, config
from libnavi.model.note import Note

from pubsub import pub


class NotesController(object):
    def __init__(self, model, settings, view, default_data_dir):
        self.model = model
        self.view = view
        self.settings = settings
        self.data_dir = get_data_dir(self.settings.get('Options', 'DataDir'),
                                     default_data_dir)
        self.notes_paths = get_notes_paths(self.data_dir)
        
        opened_notes = self.settings.get('Notes', 'Opened').split(config.PATH_SEP)
        self.model.notes = []
        for opened_note in opened_notes:
            if opened_note:
                path = self.data_dir / (opened_note + config.DEFAULT_NOTE_EXTENSION)
                note = Note(opened_note, path)
                self.model.notes.append(note)
        
        if not self.model.notes:
            path = self.data_dir / config.DEFAULT_NOTE_FILE_NAME
            note = Note(get_name_from_path(path), path)
            self.model.notes = [note]
        
        pub.subscribe(self.on_program_close, 'program.closed')
        pub.subscribe(self.on_page_closing, 'page.closing')
        
    def open_initial(self):
        current_note_name = self.settings.get('Notes', 'CurrentOpened')
        current_note = None
        for note in self.model.notes:
            note.open(create=True)
            if note.name == current_note_name:
                current_note = note
        if current_note:
            pub.sendMessage('note.show', note=current_note)
    
    def create_new(self):
        name = self.view.ask_note_name()
        if not name:
            return
        path = self.data_dir / (name + config.DEFAULT_NOTE_EXTENSION)
        note = Note(get_name_from_path(path), path)
        self.model.notes.append(note)
        note.open(create=True)
        
    def save(self, pages):
        for page in pages:
            page.note.save(page.text.GetValue())
            
    def close(self, page):
        page.note.save(page.text.GetValue())
        page.note.close()
            
    def close_current(self):
        """Close the currently opened note."""
        self.close(self.view.current_page)
        
    def on_program_close(self, pages):
        self.save(pages)         
        
    def on_page_closing(self, page):
        self.close(page)
        
        
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
