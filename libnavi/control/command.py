from appcommon.i18n import _
from appcommon.control.command import BaseCommandController
from appcommon.model.command import CommandCategory, Command
from libnavi import config
import wx



class CommandController(BaseCommandController):
    def __init__(self, control, settings):
        self.control = control
        self.settings = settings
        BaseCommandController(control, settings, config.SHORTCUTS_KEY)
        
    def _get_commands(self):
        commands = []
        
        note_cat = CommandCategory(_('&Note'))
        note_cat.append(Command(
            10001, _('&New...'), _('Create a new note'),
            self.control.notes.create,
            wx.ACCEL_CTRL, ord('N')))
        note_cat.append(Command(
            10002, _('&Close'), _('Close the opened note'),
            self.control.notes.close,
            wx.ACCEL_CTRL, ord('W')))
        note_cat.append(Command(
            10003, _('&Options...'), _('Open the application options'),
            self.control.open_options,
            wx.ACCEL_CTRL, ord('W')))
        note_cat.append(Command(
            10004, _('&Quit'), _('Quit the application'),
            self.control.close,
            wx.ACCEL_CTRL, ord('Q')))
        commands.append(note_cat)
        
        return commands