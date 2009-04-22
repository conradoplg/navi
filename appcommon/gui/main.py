from pubsub import pub
from appcommon.model.command import Command, CommandCategory
from appcommon import util
from appcommon.gui.error import ErrorDialog
from appcommon.util import flattened_full_chain
import logging
import traceback
import wx


class BaseMainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        pub.subscribe(self.on_commands_created, 'commands.created')
        pub.subscribe(self.on_commands_changed, 'commands.changed')
        
        self.main_menu = wx.MenuBar()
        self.SetMenuBar(self.main_menu)
        
        self._hidden_menus = []
        self._accel_table = None

    def on_commands_created(self, command_tree):
        pos = 0
        for cmd in command_tree:
            menu = self._make_menu(cmd)
            if cmd.hidden:
                self._hidden_menus.append(menu)
            else:
                self.main_menu.Append(menu, cmd.name)
                cmd.idx = pos
                pos += 1

    def on_commands_changed(self, command_tree, accel_table):
        self._accel_table = accel_table
        self.SetAcceleratorTable(self._accel_table)
        for cmd in flattened_full_chain(command_tree):
            if isinstance(cmd, Command):
                menu_item = self.main_menu.FindItemById(cmd.ide)
                if menu_item is not None:
                    menu_item.SetItemLabel(cmd.name_and_shortcut)
                    menu_item.SetHelp(cmd.description)
            elif isinstance(cmd, CommandCategory):
                if hasattr(cmd, 'idx'):
                    self.main_menu.SetMenuLabel(cmd.idx, cmd.name)
                elif hasattr(cmd, 'ide'):
                    menu_item = self.main_menu.FindItemById(cmd.ide)
                    if menu_item is not None:
                        menu_item.SetItemLabel(cmd.name)

    def _make_menu(self, commands):
        menu = wx.Menu()
        for cmd in commands:
            if isinstance(cmd, Command):
                def event_fn(event, cmd=cmd):
                    try:
                        cmd()
                    except Exception, e:
                        self._handle_error(e)
                menu.Append(cmd.ide, cmd.name_and_shortcut, cmd.description)
                self.Bind(wx.EVT_MENU, event_fn, id=cmd.ide)
            elif isinstance(cmd, CommandCategory):
                submenu = self._make_menu(cmd)
                item = menu.AppendSubMenu(submenu, cmd.name)
                cmd.ide = item.Id
            else:
                menu.AppendSeparator()
        return menu
    
    def _handle_error(self, exception, tb=None):
        if not tb:
            tb = traceback.format_exc()
        msg, tb = util.format_exception(exception, tb)
        logging.error(tb)
        def fn():
            dlg = ErrorDialog(parent=self, error=msg, tb=tb)
            dlg.ShowModal()
            dlg.Destroy()
        #TODO: (2,?) Investigate
        #This is a workaround for a bizarre bug in wx.
        wx.CallLater(400, fn)