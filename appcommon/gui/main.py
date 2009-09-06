from pubsub import pub
from appcommon.model.command import Command, CommandCategory
from appcommon import util
from appcommon.gui.error import ErrorDialog
from appcommon.util import flattened_full_chain
import logging
import traceback
import wx
import sys


if 'win' in sys.platform:
    import win32con
    from appcommon.windows import keys
    
    def _convert_modifiers_to_wsw(modifiers):
        flags = 0
        if modifiers & wx.MOD_CONTROL:
            flags |= win32con.MOD_CONTROL
        if modifiers & wx.MOD_SHIFT:
            flags |= win32con.MOD_SHIFT
        if modifiers & wx.MOD_ALT:
            flags |= win32con.MOD_ALT
        return flags
    
    def register_hotkey(window, hotkey_id, modifiers, key_code):
        modifiers = _convert_modifiers_to_wsw(modifiers)
        key_code = keys.convert_wx_to_msw(key_code)
        res = window.RegisterHotKey(hotkey_id, modifiers, key_code)
        if res:
            window.Bind(wx.EVT_HOTKEY, window.on_hotkey, id=hotkey_id)
        return res

    def unregister_hotkey(window, hotkey_id):
        return window.UnregisterHotKey(hotkey_id)


class BaseMainWindow(wx.Frame):
    def __init__(self, meta, *args, **kwargs):
        self.meta = meta
        wx.Frame.__init__(self, *args, **kwargs)
        pub.subscribe(self.on_commands_created, 'commands.created')
        pub.subscribe(self.on_commands_changed, 'commands.changed')
        
        self.main_menu = wx.MenuBar()
        self.SetMenuBar(self.main_menu)
        
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_MOVE, self.on_move)
        
        self._hidden_menus = []
        self._accel_table = None
        self._last_size = self.GetSizeTuple() 
        self._last_pos = self.GetPositionTuple()

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
    
    def on_resize(self, event):
        if not self.IsMaximized():
            self._last_size = self.GetSizeTuple()
        event.Skip()
            
    def on_move(self, event):
        if not self.IsMaximized():
            self._last_pos = self.GetPositionTuple()
        event.Skip()
    
    def save_position(self, settings):
        settings.set('Window', 'MainWindowX', self._last_pos[0])
        settings.set('Window', 'MainWindowY', self._last_pos[1])
        settings.set('Window', 'MainWindowWidth', self._last_size[0])
        settings.set('Window', 'MainWindowHeight', self._last_size[1])
        settings.set('Window', 'MainWindowMaximized', '1' if self.IsMaximized() else '0')
        
    def load_position(self, settings):
        width = max(settings.getint('Window', 'MainWindowWidth'), 200)
        height = max(settings.getint('Window', 'MainWindowHeight'), 200)
        x = max(settings.getint('Window', 'MainWindowX'), 0)
        y = max(settings.getint('Window', 'MainWindowY'), 0)
        self.SetDimensions(x, y, width, height)
        #For some reason the windows must be shown before maximized,
        #otherwise the text editor won't fill the window
        self.Show(True)
        self.Maximize(settings.getboolean('Window', 'MainWindowMaximized'))
        # Check that the window is on a valid display and move if necessary:
        if wx.Display.GetFromWindow(self) == wx.NOT_FOUND:
            self.SetDimensions(0, 0, width, height)
        
    def _handle_error(self, exception, tb=None):
        if not tb:
            tb = traceback.format_exc()
        msg, tb = util.format_exception(exception, tb)
        logging.error(tb)
        def fn():
            dlg = ErrorDialog(self.meta, msg, tb, self)
            dlg.ShowModal()
            dlg.Destroy()
        #TODO: (2,?) Investigate
        #This is a workaround for a bizarre bug in wx.
        wx.CallLater(400, fn)
