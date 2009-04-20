from __future__ import with_statement, absolute_import

from appcommon.model.shortcut import Shortcut
from appcommon.model.command import Command
from appcommon.util import flattened_chain, flattened_full_chain

import wx
from wx.lib.pubsub import Publisher

class BaseCommandController(object):
    def __init__(self, control, settings, section):
        self.settings = settings
        self.control = control
        self.section = section
        
        self.command_tree, self.commands = self._make_commands()
        _load_shortcuts(self.settings, section, self.commands)
        self.accel_table = _get_accelerator_table(self.commands)
        #These must be sent in this order
        Publisher().sendMessage('commands.created', self.command_tree)
        Publisher().sendMessage('commands.changed', (self.command_tree, self.commands, self.accel_table))
        
        Publisher().subscribe(self.on_language_changed, 'language.changed')
        Publisher().subscribe(self.on_command_execute, 'command.execute')
        
    def set_shortcuts(self, shortcuts_dic):
        """Set new shortcuts.
        
        @type shortcuts_dic: dict(Command -> list(Shortcut))
        """
        for cmd, shortcuts in shortcuts_dic.iteritems():
            cmd.shortcuts = shortcuts
        _save_shortcuts(self.settings, self.commands)
        self.accel_table = _get_accelerator_table(self.commands)
        Publisher().sendMessage('commands.changed', (self.command_tree, self.commands, self.accel_table))
        
    def on_language_changed(self, message):
        self._update_commands()
        Publisher().sendMessage('commands.changed', (self.command_tree, self.commands, self.accel_table))
        
    def on_command_execute(self, message):
        ide = message.data
        [cmd() for cmd in self.commands if cmd.ide == ide]
        
    def _make_commands(self):
        command_tree = self._get_commands()
        return command_tree, list(flattened_chain(command_tree))
    
    def _update_commands(self):
        command_tree = self._get_commands()
        cmd_dic = dict((cmd.ide, cmd) for cmd in self.commands)
        for cmd in flattened_full_chain(command_tree):
            cmd_dic[cmd.ide].name = cmd.name
            if isinstance(cmd, Command):
                cmd_dic[cmd.ide].description = cmd.description
    
    def _get_commands(self):
        raise NotImplementedError()
    
def _load_shortcuts(settings, section, commands):
    """Load shortcuts from a ini file.
    
    If the file does not have a shortcut section, load the default shortcuts
    specified in the Command objects.
    
    @param settings: the ini file
    @type settings: ConfigParser
    @param section: the name of the section in the ini file to read from
    @type section: unicode
    @param commands: the command list from the application
    @type commands: list of appcommon.model.command.Command
    """
    if settings.has_section(section):
        cmd_dic = dict((cmd.ide, cmd) for cmd in commands)
        items = settings.items(section)
        for cmd_id_str, shcut_lst_str in items:
            cmd_id = int(cmd_id_str)
            for shcut_str in shcut_lst_str.split():
                #The shortcut is in <key_code>,<flags> format
                shcut_lst = shcut_str.split(',')
                key_code = int(shcut_lst[0])
                flags = int(shcut_lst[1])
                shcut = Shortcut(flags, key_code)
                if cmd_id in cmd_dic:
                    cmd_dic[cmd_id].shortcuts.append(shcut)
    else:
        _load_default_shortcuts(commands)
        
def _save_shortcuts(settings, section, commands):
    """Save shortcuts in a ini file.
    
    @param settings: the ini file
    @type settings: ConfigParser
    @param section: the name of the section in the ini file to read from
    @type section: unicode
    @param commands: the command list from the application
    @type commands: list of appcommon.model.command.Command
    """
    settings.remove_section(section)
    settings.add_section(section)
    for cmd in commands:
        cmd_id_str = str(cmd.ide)
        shcut_lst_str = ' '.join('%d,%d' % (shcut.key_code, shcut.flags)
                                 for shcut in cmd.shortcuts)
        settings.set(section, cmd_id_str, shcut_lst_str)

def _load_default_shortcuts(commands):
    for cmd in commands:
        cmd.load_default_shortcut()

def _get_accelerator_table(commands):
    """Create an accelerator table from a command list.
    
    @param commands: the command list from the application
    @type commands: list of appcommon.model.command.Command
    """
    lst = [(shcut.flags, shcut.key_code, cmd.ide) for cmd in commands
           for shcut in cmd.shortcuts] 
    return wx.AcceleratorTable(lst)
