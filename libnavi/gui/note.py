from wx.richtext import RichTextCtrl
from pubsub import pub
import wx

class NotePage(wx.Panel):
    def __init__(self, window, note, *args, **kwargs):
        self.window = window
        self.note = note
        wx.Panel.__init__(self, *args, **kwargs)
#        self.text = RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS)
        self.text = wx.TextCtrl(self, style=wx.NO_BORDER|wx.TE_PROCESS_TAB|wx.TE_MULTILINE|wx.TE_RICH2|wx.TE_AUTO_URL|wx.TE_NOHIDESEL)
        self.__do_layout()
        
        self.text.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
        pub.subscribe(self.on_delete_line, 'note.edit.delete_line')
        
    def __do_layout(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        self.Layout()
        
    def on_key_down(self, event):
        pub.sendMessage('page.key_down', key_code=event.KeyCode, flags=event.Modifiers)
        event.Skip()
        
    def on_delete_line(self):
        if self.window.current_page is not self:
            return
        cur = self.text.GetInsertionPoint()
        text = self.text.Value
        #-1 is handled implicitly
        before = text.rfind('\n', 0, cur) + 1
        after = text.find('\n', cur + 1)
        if after != -1:
            after += 1
        self.text.Remove(before, after)
