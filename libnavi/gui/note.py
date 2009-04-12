from wx.richtext import RichTextCtrl
import wx

class NotePage(wx.Panel):
    def __init__(self, note, *args, **kwargs):
        self.note = note
        wx.Panel.__init__(self, *args, **kwargs)
        self.text = RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS)
        self.__do_layout()
        
    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        self.Layout()
        