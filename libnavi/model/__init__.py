from __future__ import with_statement, absolute_import

from appcommon.thirdparty.path import path



class App(object):
    def __init__(self, settings):
        self.settings = settings
        self.notes = []
