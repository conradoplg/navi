from wx.richtext import RichTextCtrl
from pubsub import pub
import wx

class NotePage(wx.Panel):
    def __init__(self, note, *args, **kwargs):
        self.note = note
        wx.Panel.__init__(self, *args, **kwargs)
        self.text = RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS)
        self.__do_layout()
        
        self.text.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        self.Layout()
        
    def on_key_down(self, event):
        pub.sendMessage('page.key_down', key_code=event.KeyCode, flags=event.Modifiers)
        event.Skip()