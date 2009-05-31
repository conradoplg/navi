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
        pub.subscribe(self.on_duplicate_lines, 'note.edit.duplicate_lines')
        pub.subscribe(self.on_copy_lines, 'note.edit.copy_lines')
        pub.subscribe(self.on_move_lines_down, 'note.edit.move_lines_down')
        pub.subscribe(self.on_move_lines_up, 'note.edit.move_lines_up')
        
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
        before, after, sel_text = self._get_selected_lines()
        self.text.Remove(before, after)
        
    def on_duplicate_lines(self):
        if self.window.current_page is not self:
            return
        before, after, sel_text = self._get_selected_lines()
        self.text.Replace(after, after, sel_text)
        self.text.SetSelection(after, after + len(sel_text))
        
    def on_copy_lines(self):
        if self.window.current_page is not self:
            return
        before, after, sel_text = self._get_selected_lines()
        self.text.Replace(before, before, sel_text)
        self.text.SetSelection(before, after)
        
    def on_move_lines_down(self):
        if self.window.current_page is not self:
            return
        before, after, sel_text = self._get_selected_lines()
        self.text.Remove(before, after)
        next_break = self.text.Value.find('\n', before)
        if next_break != -1:
            next_break += 1
        self.text.Replace(next_break, next_break, sel_text)
        if next_break != -1:
            self.text.SetSelection(next_break, next_break + len(sel_text))
        
    def on_move_lines_up(self):
        if self.window.current_page is not self:
            return
        before, after, sel_text = self._get_selected_lines()
        if before == 0:
            return
        self.text.Remove(before, after)
        prev_break = self.text.Value.rfind('\n', 0, before - 1)
        if prev_break == -1:
            prev_break = 0
        else:
            prev_break += 1
        self.text.Replace(prev_break, prev_break, sel_text)
        self.text.SetSelection(prev_break, prev_break + len(sel_text))
    
    def _get_selected_lines(self):
        sel_start, sel_end = self.text.GetSelection()
        text = self.text.Value
        #Don't consider line selected in selections ends in the start of a line
        if sel_end > 0 and sel_start != sel_end and self.text.GetRange(sel_end - 1, sel_end) == '\n':
            sel_end -= 1
        #-1 is handled implicitly
        before = text.rfind('\n', 0, sel_start) + 1
        after = text.find('\n', sel_end)
        if after != -1:
            after += 1
        sel_text = self.text.GetRange(before, after)
        return before, after, sel_text

