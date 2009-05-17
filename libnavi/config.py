from libnavi import meta
import sys

DEFAULT_NOTE_FILE_NAME = u'Scratch.txt'
DEFAULT_NOTE_EXTENSION = u'.txt'

INI_FILE_NAME = u'%s.ini' % meta.APPNAME
LOG_FILE_NAME = u'%s.log' % meta.APPNAME

SHORTCUTS_KEY = 'shortcuts'

if sys.platform == 'win32':
    PATH_SEP = ';'
else:
    PATH_SEP = ':'
