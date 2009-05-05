# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sat Apr 11 16:00:27 2009
from appcommon.i18n import _
from libnavi.gui.options import OptionsDialog
from pubsub import pub
from libnavi.gui.note import NotePage
from libnavi import meta, images
from appcommon.gui.main import BaseMainWindow, unregister_hotkey, register_hotkey

import wx

# begin wxGlade: dependencies
# end wxGlade

import wx.lib.flatnotebook as fnb

#To workaround the FlatNotebook focus stealing, we replace its PageContainer
#class with a subclassed one where we can control the focus.
OldPageContainer = fnb.PageContainer

class PageContainer(fnb.PageContainer):
    def __init__(self, *args, **kwargs):
        OldPageContainer.__init__(self, *args, **kwargs)
        
    def SetFocus(self):
        pass
            
fnb.PageContainer = PageContainer


class MainWindow(BaseMainWindow):
    def __init__(self):
        # begin wxGlade: MainWindow.__init__
        BaseMainWindow.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE)
        self.main_notebook = fnb.FlatNotebook(self)
        self.taskbar_icon = wx.TaskBarIcon()
        
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.on_page_closing)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        # end wxGlade
        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.taskbar_icon.Bind(wx.EVT_TASKBAR_CLICK, self.on_hotkey)
        self.taskbar_icon.Bind(wx.EVT_TASKBAR_LEFT_UP, self.on_hotkey)
        
        self._programatically_closing_page = False
        self._last_hotkey = None
        
        pub.subscribe(self.on_note_opened, 'note.opened')
        pub.subscribe(self.on_note_closed, 'note.closed')
        pub.subscribe(self.on_settings_changed, 'settings.changed')
        pub.subscribe(self.on_setting_changed, 'setting.changed')

    def __set_properties(self):
        # begin wxGlade: MainWindow.__set_properties
        self.SetTitle(meta.APPNAME)
        self.SetSize((720, 540))
        # end wxGlade
        style = self.main_notebook.GetWindowStyleFlag()
        style |= fnb.FNB_NO_X_BUTTON|fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS
        style &= ~(fnb.FNB_TABS_BORDER_SIMPLE)
        style &= ~(fnb.FNB_VC71 | fnb.FNB_VC8 | fnb.FNB_FANCY_TABS | fnb.FNB_FF2)
        style |= fnb.FNB_VC8
        self.main_notebook.SetWindowStyleFlag(style)
        bundle = wx.IconBundle()
        bundle.AddIcon(images.navi16.Icon)
        bundle.AddIcon(images.navi32.Icon)
        bundle.AddIcon(images.navi48.Icon)
        bundle.AddIcon(images.navi256.Icon)
        self.SetIcons(bundle)
        self.taskbar_icon.SetIcon(images.navi16.Icon, meta.APPNAME)

    def __do_layout(self):
        # begin wxGlade: MainWindow.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
#        self.main_notebook.AddPage(self.main_text, _("tab1"))
        main_sizer.Add(self.main_notebook, 1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)
        self.Layout()
        # end wxGlade
        
    def ask_note_name(self):
        dlg = wx.TextEntryDialog(self, _('Enter the note name:'), _('Note name'), '')
        name = ''
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
        dlg.Destroy()
        return name
    
    def hide(self):
        self.Show(False)
        
    def open_options(self, options):
        dlg = OptionsDialog(self, options)
        dlg.ShowModal()
        dlg.Destroy()
    
    @property
    def current_page(self):
        sel = self.main_notebook.GetSelection()
        if sel == -1:
            return None
        else:
            return self.main_notebook.GetPage(sel)
        
    @property
    def pages(self):
        return [self.main_notebook.GetPage(i) for i
                in xrange(self.main_notebook.GetPageCount())]

    def on_new_item_click(self, event): # wxGlade: MainWindow.<event_handler>
        event.Skip()
        
    def on_close_item_click(self, event): # wxGlade: MainWindow.<event_handler>
        event.Skip()
        
    def on_options_item_click(self, event): # wxGlade: MainWindow.<event_handler>
        options = OptionsDialog(self)
        options.ShowModal()
        event.Skip()

    def on_quit_item_click(self, event): # wxGlade: MainWindow.<event_handler>
        self.Close()

    def on_close(self, event):
        #Needed because the event handler can be called after the the notebook is destroyed 
        self.Unbind(wx.EVT_ACTIVATE)
        pub.sendMessage('program.closed', pages=self.pages)
        #Cosmetic, don't show the window being destroyed
        self.Show(False)
        self.Destroy()
        
    def on_page_closing(self, event):
        if self._programatically_closing_page:
            return
        sel = event.GetSelection()
        pub.sendMessage('page.closing', page=self.main_notebook.GetPage(sel))
        #The listeners to the event will close the page, so veto here
        event.Veto()
        
    def on_hotkey(self, event):
        self.Show()
        self.Raise()
        
    def on_activate(self, event):
        if self.current_page:
            self.current_page.text.SetFocus()
            
    def on_page_changed(self, event):
        sel = event.GetSelection()
        page = self.main_notebook.GetPage(sel)
        page.text.SetFocus()
        
    def on_note_opened(self, note):
        page = NotePage(note, self.main_notebook)
        self.main_notebook.AddPage(page, note.name)
        page.text.SetValue(note.text)
        page.text.SetFocus()
        
    def on_note_closed(self, note):
        idx, page = [(idx, page) for idx, page in enumerate(self.pages)
                     if page.note is note][0]
        self._programatically_closing_page = True
        try:
            self.main_notebook.DeletePage(idx)
        finally:
            self._programatically_closing_page = False
            
    def on_settings_changed(self, settings):
        value = settings.get('Options', 'HotKey')
        self.on_setting_changed(settings, 'Options', 'HotKey', value)
        
    def on_setting_changed(self, settings, section, option, value):
        if (section, option) == ('Options', 'HotKey'):
            if self._last_hotkey:
                if unregister_hotkey(self, self._last_hotkey):
                    self._last_hotkey = None
            if value:
                hotkey = 1
                modifiers = int(value.split(',')[0])
                key_code = int(value.split(',')[1])
                
                if register_hotkey(self, hotkey, modifiers, key_code):
                    self._last_hotkey = hotkey
    

# end of class MainWindow

if __name__ == '__main__':
    app = wx.App(False)
    main = MainWindow(None)
    app.SetTopWindow(main)
    main.Show()
    app.MainLoop()

