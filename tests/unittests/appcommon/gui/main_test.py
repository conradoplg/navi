'''
Created on 21/04/2009

@author: Conrado
'''
from appcommon.gui.main import BaseMainWindow
from appcommon.model.command import Command, CommandCategory
from pubsub import pub
import wx
import unittest


class Test(unittest.TestCase):


    def test_commands_created(self):
        w = BaseMainWindow(None)
            
        cmd1 = Command(1, 'Name1', 'Desc1', lambda: 1, [])
        cmd2 = Command(2, 'Name2', 'Desc2', lambda: 1, [])
        cat1 = CommandCategory('Cat1')
        cat2 = CommandCategory('Cat2')
        
        cat1.append(cmd1)
        cat1.append(cat2)
        cat2.append(cmd2)
        
        tree = [cat1]
        
        pub.sendMessage('commands.created', command_tree=tree)
        
        self.assertEqual(1, w.main_menu.MenuCount)
        self.assertEqual(2, w.main_menu.GetMenu(0).MenuItemCount)
        self.assertEqual(1, w.main_menu.GetMenu(0).FindItemByPosition(1).SubMenu.MenuItemCount)
        
        cmd1.name = 'Nome1'
        cmd1.description = 'Descricao1'
        cmd2.name = 'Nome2'
        cmd2.description = 'Descricao2'
        cat1.name = 'Categoria1'
        cat2.name = 'Categoria2'
        
        pub.sendMessage('commands.changed', command_tree=tree, accel_table=wx.AcceleratorTable([]))
        
        self.assertEqual(cat1.name, w.main_menu.GetMenuLabel(0))
        self.assertEqual(cmd1.name, w.main_menu.GetMenu(0).FindItemByPosition(0).ItemLabel)
        self.assertEqual(cat2.name, w.main_menu.GetMenu(0).FindItemByPosition(1).ItemLabel)
        self.assertEqual(cmd2.name, w.main_menu.GetMenu(0).FindItemByPosition(1).SubMenu.FindItemByPosition(0).ItemLabel)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_menu_built']
    unittest.main()