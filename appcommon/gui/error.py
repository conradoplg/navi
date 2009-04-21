from __future__ import absolute_import
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sun Sep 14 19:11:42 2008

import wx

# begin wxGlade: dependencies
# end wxGlade

from appcommon.i18n import _

# begin wxGlade: extracode
import wx.lib.hyperlink as hl
# end wxGlade

class ErrorDialog(wx.Dialog):
    def __init__(self, meta, error, tb, *args, **kwds):
        self.REQUEST_REPORT_TXT = _("If you think this may be a bug, please report it. Thank you.")
        self.REPORT_INSTRUCTIONS_TXT = _("Please copy the error information below and click the link in order to report this error.")
        
        error_msg = _('An error has ocurred:') + '\n'
        error_msg += error
        error_details = tb
        error_details += '\n%s %s' % (meta.APPNAME, meta.VERSION)
        # begin wxGlade: ErrorDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.error_bmp = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.error_lbl = wx.StaticText(self, -1, error_msg)
        self.feedback_lbl = wx.StaticText(self, -1, self.REQUEST_REPORT_TXT)
        self.traceback_txt = wx.TextCtrl(self, -1, error_details, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_NOHIDESEL)
        self.copy_btn = wx.Button(self, -1, _("&Copy error information"))
        self.report_link = hl.HyperLinkCtrl(self, -1, _('Report error'), URL=meta.REPORT_URL)
        self.report_btn = wx.Button(self, -1, _("&Report error"))
        self.ok_btn = wx.Button(self, wx.ID_OK, _("&OK"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.on_report_click, self.report_btn)
        self.Bind(wx.EVT_BUTTON, self.on_copy_click, self.copy_btn)
        self.Bind(wx.EVT_BUTTON, self.on_ok_click, self.ok_btn)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ErrorDialog.__set_properties
        self.SetTitle(_("Error"))
        # end wxGlade
        self.traceback_txt.Show(False)
        self.copy_btn.Show(False)
        self.report_link.Show(False)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_MESSAGE_BOX, (32, 32))
        self.error_bmp.SetBitmap(bmp)
        self.traceback_txt.SetSelection(-1, -1)
        self.ok_btn.SetDefault()
        self.ok_btn.SetFocus()

    def __do_layout(self):
        # begin wxGlade: ErrorDialog.__do_layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        stddialog_sizer_copy = wx.BoxSizer(wx.HORIZONTAL)
        report_sizer = wx.BoxSizer(wx.HORIZONTAL)
        error_sizer = wx.BoxSizer(wx.HORIZONTAL)
        error_sizer.Add(self.error_bmp, 0, wx.RIGHT, 10)
        error_sizer.Add(self.error_lbl, 1, 0, 0)
        main_sizer.Add(error_sizer, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 10)
        main_sizer.Add(self.feedback_lbl, 0, wx.LEFT|wx.RIGHT|wx.TOP, 10)
        main_sizer.Add(self.traceback_txt, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 10)
        report_sizer.Add(self.copy_btn, 0, wx.RIGHT|wx.ALIGN_CENTRE_VERTICAL, 10)
        report_sizer.Add(self.report_link, 1, wx.ALIGN_CENTRE_VERTICAL, 0)
        main_sizer.Add(report_sizer, 1, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 10)
        stddialog_sizer_copy.Add(self.report_btn, 0, wx.LEFT|wx.ALIGN_RIGHT, 10)
        stddialog_sizer_copy.Add(self.ok_btn, 0, wx.LEFT|wx.ALIGN_RIGHT, 10)
        main_sizer.Add(stddialog_sizer_copy, 1, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.SetSizer(main_sizer)
        main_sizer.Fit(self)
        self.Layout()
        # end wxGlade
        self.main_sizer = main_sizer

    def on_report_click(self, event): # wxGlade: ErrorDialog.<event_handler>
        self.feedback_lbl.SetLabel(self.REPORT_INSTRUCTIONS_TXT)
        self.traceback_txt.Show(True)
        self.copy_btn.Show(True)
        self.report_link.Show(True)
        self.report_btn.Show(False)
        self.main_sizer.Fit(self)
        self.Layout()
        event.Skip()
        
    def on_copy_click(self, event):
        data = wx.TextDataObject()
        data.SetText(self.traceback_txt.GetValue())
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()

    def on_ok_click(self, event): # wxGlade: ErrorDialog.<event_handler>
        self.EndModal(1)
        event.Skip()

# end of class ErrorDialog


if __name__ == '__main__':
    app = wx.App()
    dialog = ErrorDialog(parent=None, error='File not found', tb='aa\na\na\nan\n\n\n\n\n\n\n\na\n')
    dialog.ShowModal()
    dialog.Destroy()
    