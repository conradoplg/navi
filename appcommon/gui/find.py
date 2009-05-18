# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.3 on Sun May 17 23:30:59 2009

import wx
from appcommon.i18n import _
from appcommon import images

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
from wx.lib.agw import buttonpanel as bp
# end wxGlade

class FindPanel(bp.ButtonPanel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FindPanel.__init__
        bp.ButtonPanel.__init__(self, *args, **kwds)
        self.search_ctrl = wx.SearchCtrl(self, -1)
        self.case_sensitive_chk = wx.CheckBox(self, -1, _("Case sensitive"))

        self.__set_properties()
        # end wxGlade
        
        self.AddControl(self.search_ctrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        btn = bp.ButtonInfo(self, bmp=images.down.Bitmap, text=_("Next"), shortHelp=_("Find next occurence of the text"))
        btn.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.AddButton(btn)
        btn = bp.ButtonInfo(self, bmp=images.up.Bitmap, text=_("Previous"), shortHelp=_("Find previous occurence of the text"))
        btn.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.AddButton(btn)
        btn = bp.ButtonInfo(self, bmp=images.pencil.Bitmap, kind=wx.ITEM_CHECK, text=_("Highlight all"), shortHelp=_("Highlight all occurences of the text"))
        btn.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.AddButton(btn)
        self.AddControl(self.case_sensitive_chk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        btn.SetTextAlignment(bp.BP_BUTTONTEXT_ALIGN_RIGHT)
        self.DoLayout()

    def __set_properties(self):
        # begin wxGlade: FindPanel.__set_properties
        # end wxGlade
        self.SetStyle(bp.BP_DEFAULT_STYLE)
        self.GetBPArt().SetMetric(bp.BP_BORDER_SIZE, 0)
        self.GetBPArt().SetMetric(bp.BP_PADDING_SIZE, wx.Size(5, 3))
        self.GetBPArt().SetMetric(bp.BP_MARGINS_SIZE, wx.Size(0, 0))
        self.GetBPArt().SetColor(bp.BP_SELECTION_BRUSH_COLOR, wx.Colour(242, 242, 235))
        self.GetBPArt().SetColor(bp.BP_SELECTION_PEN_COLOR, wx.Colour(206, 206, 195))
        width = self.search_ctrl.GetTextExtent("Dummy big string for example aaaaa")[0]
        self.search_ctrl.SetMinSize((width, -1))

# end of class FindPanel


