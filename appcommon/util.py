from collections import Iterable
import sys

def flattened_chain(iterables):
    for it in iterables:
        if isinstance(it, Iterable):
            for elem in flattened_chain(it):
                yield elem
        else:
            yield it

def flattened_full_chain(iterables):
    for it in iterables:
        if isinstance(it, Iterable):
            yield it
            for elem in flattened_full_chain(it):
                yield elem
        else:
            yield it
            
def format_exception(exception, tb):
    try:
        msg = exception.get_custom_msg()
    except AttributeError:
        if sys.platform == 'win32' and isinstance(exception, WindowsError):
            #Python bug (fixed on 3.0), the error is not unicode
            msg = str(exception).decode('mbcs')
        else:
            msg = unicode(exception)
    if msg == '':
        msg = exception.__class__.__name__
    #Due to the bug above, unicode coercing tb might fail. Take a safe approach.
    tb = tb.decode('ascii', 'ignore')
    return msg, tb