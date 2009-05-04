from appcommon.i18n import _
from appcommon.control.command import BaseCommandController
from appcommon.model.command import CommandCategory, Command
from libnavi import config
from appcommon.model.shortcut import Shortcut
import wx



class CommandController(BaseCommandController):
    def __init__(self, control, settings):
        self.control = control
        self.settings = settings
        BaseCommandController.__init__(self, control, settings, config.SHORTCUTS_KEY)
        
    def _get_commands(self):
        commands = []
        
        note_cat = CommandCategory(_('&Note'))
        note_cat.append(Command(
            10001, _('&New...'), _('Create a new note'),
            self.control.notes.create_new,
            [Shortcut(wx.ACCEL_CTRL, ord('N'))]))
        note_cat.append(Command(
            10002, _('&Close'), _('Close the opened note'),
            self.control.notes.close_current,
            [Shortcut(wx.ACCEL_CTRL, ord('W'))]))
        note_cat.append(None)
        note_cat.append(Command(
            10003, _('&Options...'), _('Open the application options'),
            self.control.open_options,
            [Shortcut(wx.ACCEL_NORMAL, wx.WXK_F4)]))
        note_cat.append(None)
        note_cat.append(Command(
            10004, _('&Quit'), _('Quit the application'),
            self.control.quit,
            [Shortcut(wx.ACCEL_CTRL, ord('Q'))]))
        commands.append(note_cat)
        
        program_cat = CommandCategory(_('&Program'), hidden=True)
        program_cat.append(Command(
            20001, _('&Hide'), _('Minimize the program to the notification area'),
            self.control.hide,
            [Shortcut(wx.ACCEL_NORMAL, wx.WXK_ESCAPE)]))
        commands.append(program_cat) 
        
        return commands
