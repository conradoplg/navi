#!/usr/bin/env python

import sys
import wxversion
#I'd like to require 2.8.9.0 but on Ubuntu it just records the first two numbers...
if not hasattr(sys, 'frozen'):
    wxversion.ensureMinimal('2.8')

import logging
logging.getLogger().setLevel(logging.DEBUG)

from libnavi.control.main import MainController
from libnavi.gui.error import ErrorDialog
from libnavi.thirdparty.path import path as Path
from libnavi import util

import wx

import sys
import traceback



class MyApp(wx.App):
    def __init__(self, redir, script, argv):
        self.script = script
        self.argv = argv
        wx.App.__init__(self, redir, script)
        
    def OnInit(self):
        try:
            self.controller = MainController(self.script)
            self.SetTopWindow(self.controller.view)
            self.controller.view.Show(True)
            return True
        except Exception, e:
            tb = traceback.format_exc()
            msg, tb = util.format_exception(e, tb)
            logging.error(tb)
            dlg = ErrorDialog(parent=None, error=msg, tb=tb)
            dlg.ShowModal()
            dlg.Destroy()
        return False

try:
    script = __file__
    script = Path(script)
    script = script.abspath()
except NameError:
    script = None

if sys.platform == 'win32':
    from libnavi.windows.util import get_unicode_argv
    argv = get_unicode_argv()
else:
    argv = sys.argv

app = MyApp(redir=False, script=script, argv=argv)
app.MainLoop()
