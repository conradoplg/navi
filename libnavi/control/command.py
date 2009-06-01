from appcommon.i18n import _
from appcommon.control.command import BaseCommandController
from appcommon.model.command import CommandCategory, Command
from libnavi import config
from appcommon.model.shortcut import Shortcut
from functools import partial
from pubsub import pub
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
            10005, _('&Open...'), _('Open a previously created note'),
            self.control.notes.open_note,
            [Shortcut(wx.ACCEL_CTRL, ord('O'))]))
        note_cat.append(Command(
            10002, _('&Close'), _('Close the opened note'),
            self.control.notes.close_current,
            [Shortcut(wx.ACCEL_CTRL, ord('W'))]))
        note_cat.append(Command(
            10006, _('Move &right'), _('Moved the opened note to the right'),
            partial(pub.sendMessage, 'note.move_right'),
            [Shortcut(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, wx.WXK_PAGEDOWN)]))
        note_cat.append(Command(
            10007, _('Move &left'), _('Moved the opened note to the left'),
            partial(pub.sendMessage, 'note.move_left'),
            [Shortcut(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, wx.WXK_PAGEUP)]))
        note_cat.append(None)
        note_cat.append(Command(
            10003, _('O&ptions...'), _('Open the application options'),
            self.control.open_options,
            [Shortcut(wx.ACCEL_NORMAL, wx.WXK_F4)]))
        note_cat.append(None)
        note_cat.append(Command(
            10004, _('&Quit'), _('Quit the application'),
            self.control.quit,
            [Shortcut(wx.ACCEL_CTRL, ord('Q'))]))
        commands.append(note_cat)
        
        edit_cat = CommandCategory(_('&Edit'))
        edit_cat.append(Command(
            30001, _('&Find'), _('Find some text in the current note'),
            self.control.find,
            [Shortcut(wx.ACCEL_CTRL, ord('F'))]))
        edit_cat.append(Command(
            30002, _('&Delete line'), _('Delete the current line'),
            partial(pub.sendMessage, 'note.edit.delete_line'),
            [Shortcut(wx.ACCEL_CTRL, ord('D'))]))
        edit_cat.append(Command(
            30003, _('Du&plicate lines'), _('Duplicate (below) the current line or the selected lines below'),
            partial(pub.sendMessage, 'note.edit.duplicate_lines'),
            [Shortcut(wx.ACCEL_ALT|wx.ACCEL_SHIFT, wx.WXK_DOWN)]))
        edit_cat.append(Command(
            30004, _('Cop&y lines'), _('Copy (above) the current line or the selected lines below'),
            partial(pub.sendMessage, 'note.edit.copy_lines'),
            [Shortcut(wx.ACCEL_ALT|wx.ACCEL_SHIFT, wx.WXK_UP)]))
        edit_cat.append(Command(
            30005, _('Move lines do&wn'), _('Move the current line or the selected lines down'),
            partial(pub.sendMessage, 'note.edit.move_lines_down'),
            [Shortcut(wx.ACCEL_ALT, wx.WXK_DOWN)]))
        edit_cat.append(Command(
            30006, _('Move lines &up'), _('Move the current line or the selected lines up'),
            partial(pub.sendMessage, 'note.edit.move_lines_up'),
            [Shortcut(wx.ACCEL_ALT, wx.WXK_UP)]))
        commands.append(edit_cat)
        
        program_cat = CommandCategory(_('&Program'), hidden=True)
        program_cat.append(Command(
            20001, _('&Hide'), _('Minimize the program to the notification area'),
            self.control.hide,
            [Shortcut(wx.ACCEL_NORMAL, wx.WXK_ESCAPE)]))
        commands.append(program_cat) 
        
        return commands
