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
from appcommon.thirdparty.path import path as Path
from libnavi import util

import wx

import traceback

try:
    script = __file__
    script = Path(script)
    script = script.abspath()
except NameError:
    script = None

if sys.platform == 'win32':
    from appcommon.windows.util import get_unicode_argv
    argv = get_unicode_argv()
else:
    argv = sys.argv

app = wx.App(False)
font = wx.NORMAL_FONT

try:
    controller = MainController(script)
    app.SetTopWindow(controller.view)
    if '-m' in argv:
        controller.view.Show(False)
except Exception, e:
    tb = traceback.format_exc()
    msg, tb = util.format_exception(e, tb)
    logging.error(tb)
    dlg = ErrorDialog(parent=None, error=msg, tb=tb)
    dlg.ShowModal()
    dlg.Destroy()

app.MainLoop()
