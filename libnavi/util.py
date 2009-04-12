from __future__ import with_statement

from libnavi.thirdparty.path import path as Path

import re
import sys
from functools import update_wrapper
import traceback
import locale
import string



def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]

def file_alphanum_key(s):
    return alphanum_key(s.abspath().stripext())

def error_handler(callback_fn):
    """Decorator that catches any exceptions and calls a callback function
    as callback_fn(exception, args, kwargs)
    """
    def error_handler_with_callback(fn):
        def error_handler_fn(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except Exception, e:
                callback_fn(e, args, kwargs)
        return update_wrapper(error_handler_fn, fn)
    return error_handler_with_callback


class ExceptionStr(object):
    def __init__(self, content):
        self.content = content
        self.infos = []
        
    def add_info(self, info):
        self.infos.insert(0, info)
        
    def __call__(self):
        return '\n'.join(self.infos + ['(' + self.content + ')']) 

def add_exception_info(exception, additional_info):
    str_fn = getattr(exception, "__str__", None)
    if not isinstance(str_fn, ExceptionStr):
        str_fn = ExceptionStr(unicode(exception))
        setattr(exception, 'get_custom_msg', str_fn)
    str_fn.add_info(additional_info)
    
def add_exception_custom_msg(exception, msg):
    def get_msg():
        return msg
    setattr(exception, 'get_custom_msg', get_msg)


def is_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""
    return hasattr(sys, "frozen")

def get_exe_path():
    return Path(unicode(sys.executable, sys.getfilesystemencoding())).abspath()

def get_traceback():
    return traceback.format_exc()

def synchronized_method(lock_name):
    """ Synchronization decorator. """
    def decorator(f):
        def synchronized_fn(self, *args, **kwargs):
            lock = getattr(self, lock_name)
            with lock:
                return f(self, *args, **kwargs)
        return synchronized_fn
    return decorator

def get_formatted_zoom(zoom):
    text = locale.format('%5.2f', zoom * 100)
    for i in xrange(len(text)):
        if text[-1] == '0':
            text = text[:-1]
        if text[-1] not in string.digits:
            text = text[:-1]
            break
    return text + '%'

def monkeypatch_method(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

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


import difflib
from pprint import pformat


class DiffTestCaseMixin(object):

    def get_diff_msg(self, first, second,
                     fromfile='First', tofile='Second'):
        """Return a unified diff between first and second."""
        # Force inputs to iterables for diffing.
        # use pformat instead of str or repr to output dicts and such
        # in a stable order for comparison.
        if isinstance(first, (tuple, list, dict)):
            first = [pformat(d) for d in first]
        else:
            first = [pformat(first)]

        if isinstance(second, (tuple, list, dict)):
            second = [pformat(d) for d in second]
        else:
            second = [pformat(second)]

        diff = difflib.unified_diff(
            first, second, fromfile=fromfile, tofile=tofile)
        # Add line endings.
        return ''.join([d + '\n' for d in diff])

    def failIfDiff(self, first, second, fromfile='First', tofile='Second'):
        """If not first == second, fail with a unified diff."""
        if not first == second:
            msg = self.get_diff_msg(first, second, fromfile, tofile)
            raise self.failureException, msg

    assertNoDiff = failIfDiff
