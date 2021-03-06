# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun May 31 19:32:15 2009
from libnavi.util import alphanum_key

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
from appcommon.i18n import _
# end wxGlade

class OpenDialog(wx.Dialog):
    def __init__(self, parent, notes_names):
        notes_names.sort(key=alphanum_key)
        # begin wxGlade: OpenDialog.__init__
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME)
        self.select_lbl = wx.StaticText(self, -1, _("Select a note to open:"))
        self.filter_txt = wx.TextCtrl(self, -1, "")
        self.matching_lst = wx.ListBox(self, -1, choices=notes_names)
        self.ok_btn = wx.Button(self, wx.ID_OK, _("&OK"))
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL, _("&Cancel"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT, self.on_filter_text, self.filter_txt)
        self.Bind(wx.EVT_BUTTON, self.on_ok_click, id=wx.ID_OK)
        # end wxGlade
        self.filter_txt.Bind(wx.EVT_KEY_DOWN, self.on_filter_key_down)
        
        self.notes_names = notes_names

    def __set_properties(self):
        # begin wxGlade: OpenDialog.__set_properties
        self.SetTitle(_("Open note"))
        self.SetSize((300, 300))
        # end wxGlade
        self.ok_btn.SetDefault()
        if self.matching_lst.Count:
            self.matching_lst.SetSelection(0)

    def __do_layout(self):
        # begin wxGlade: OpenDialog.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        std_dialog_sizer = wx.StdDialogButtonSizer()
        main_sizer.Add(self.select_lbl, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10)
        main_sizer.Add(self.filter_txt, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 10)
        main_sizer.Add(self.matching_lst, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 10)
        std_dialog_sizer.AddButton(self.ok_btn)
        std_dialog_sizer.AddButton(self.cancel_btn)
        std_dialog_sizer.Realize()
        main_sizer.Add(std_dialog_sizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(main_sizer)
        self.Layout()
        # end wxGlade

    def on_filter_text(self, event): # wxGlade: OpenDialog.<event_handler>
        filter = event.GetString()
        filtered_notes = [name for name in self.notes_names
                          if filter.lower() in name.lower()]
        self.matching_lst.Items = filtered_notes
        self.ok_btn.Enable(self.matching_lst.Count)
        if self.matching_lst.Count:
            self.matching_lst.SetSelection(0)
        event.Skip()

    def on_ok_click(self, event): # wxGlade: OpenDialog.<event_handler>
        self.selected_note = self.matching_lst.GetStringSelection()
        event.Skip()

    def on_filter_key_down(self, event):
        sel = self.matching_lst.Selection
        if event.KeyCode in (wx.WXK_UP, wx.WXK_DOWN):
            if event.KeyCode == wx.WXK_UP:
                sel -= 1
            else:
                sel += 1
            if 0 <= sel < self.matching_lst.Count:
                self.matching_lst.Select(sel)
                self.matching_lst.EnsureVisible(sel)
        else:
            event.Skip()
            
# end of class OpenDialog


if __name__ == '__main__':
    app = wx.App(False)
    dialog = OpenDialog(None, ["teste", "abc", "oro", u"Ação", u"AÇÃO"])
    app.SetTopWindow(dialog)
    dialog.Show()
    app.MainLoop()
