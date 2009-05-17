import wx
import win32con
import win32api

_specialKeys = {
    win32con.VK_CANCEL:        wx.WXK_CANCEL,
    win32con.VK_BACK:          wx.WXK_BACK,
    win32con.VK_TAB:           wx.WXK_TAB,
    win32con.VK_CLEAR:         wx.WXK_CLEAR,
    win32con.VK_SHIFT:         wx.WXK_SHIFT,
    win32con.VK_CONTROL:       wx.WXK_CONTROL,
    win32con.VK_MENU :         wx.WXK_ALT,
    win32con.VK_PAUSE:         wx.WXK_PAUSE,
    win32con.VK_CAPITAL:       wx.WXK_CAPITAL,
    win32con.VK_SPACE:         wx.WXK_SPACE,
    win32con.VK_ESCAPE:        wx.WXK_ESCAPE,
    win32con.VK_SELECT:        wx.WXK_SELECT,
    win32con.VK_PRINT:         wx.WXK_PRINT,
    win32con.VK_EXECUTE:       wx.WXK_EXECUTE,
    win32con.VK_SNAPSHOT:      wx.WXK_SNAPSHOT,
    win32con.VK_HELP:          wx.WXK_HELP,

    win32con.VK_NUMPAD0:       wx.WXK_NUMPAD0,
    win32con.VK_NUMPAD1:       wx.WXK_NUMPAD1,
    win32con.VK_NUMPAD2:       wx.WXK_NUMPAD2,
    win32con.VK_NUMPAD3:       wx.WXK_NUMPAD3,
    win32con.VK_NUMPAD4:       wx.WXK_NUMPAD4,
    win32con.VK_NUMPAD5:       wx.WXK_NUMPAD5,
    win32con.VK_NUMPAD6:       wx.WXK_NUMPAD6,
    win32con.VK_NUMPAD7:       wx.WXK_NUMPAD7,
    win32con.VK_NUMPAD8:       wx.WXK_NUMPAD8,
    win32con.VK_NUMPAD9:       wx.WXK_NUMPAD9,
    win32con.VK_MULTIPLY:      wx.WXK_NUMPAD_MULTIPLY,
    win32con.VK_ADD:           wx.WXK_NUMPAD_ADD,
    win32con.VK_SUBTRACT:      wx.WXK_NUMPAD_SUBTRACT,
    win32con.VK_DECIMAL:       wx.WXK_NUMPAD_DECIMAL,
    win32con.VK_DIVIDE:        wx.WXK_NUMPAD_DIVIDE,

    win32con.VK_F1:            wx.WXK_F1,
    win32con.VK_F2:            wx.WXK_F2,
    win32con.VK_F3:            wx.WXK_F3,
    win32con.VK_F4:            wx.WXK_F4,
    win32con.VK_F5:            wx.WXK_F5,
    win32con.VK_F6:            wx.WXK_F6,
    win32con.VK_F7:            wx.WXK_F7,
    win32con.VK_F8:            wx.WXK_F8,
    win32con.VK_F9:            wx.WXK_F9,
    win32con.VK_F10:           wx.WXK_F10,
    win32con.VK_F11:           wx.WXK_F11,
    win32con.VK_F12:           wx.WXK_F12,
    win32con.VK_F13:           wx.WXK_F13,
    win32con.VK_F14:           wx.WXK_F14,
    win32con.VK_F15:           wx.WXK_F15,
    win32con.VK_F16:           wx.WXK_F16,
    win32con.VK_F17:           wx.WXK_F17,
    win32con.VK_F18:           wx.WXK_F18,
    win32con.VK_F19:           wx.WXK_F19,
    win32con.VK_F20:           wx.WXK_F20,
    win32con.VK_F21:           wx.WXK_F21,
    win32con.VK_F22:           wx.WXK_F22,
    win32con.VK_F23:           wx.WXK_F23,
    win32con.VK_F24:           wx.WXK_F24,

    win32con.VK_NUMLOCK:       wx.WXK_NUMLOCK,
    win32con.VK_SCROLL:        wx.WXK_SCROLL,

    win32con.VK_LWIN:          wx.WXK_WINDOWS_LEFT,
    win32con.VK_RWIN:          wx.WXK_WINDOWS_RIGHT,
    win32con.VK_APPS:          wx.WXK_WINDOWS_MENU,
}

_specialTable = {
    wx.WXK_PAGEUP: win32con.VK_PRIOR,
    wx.WXK_NUMPAD_PAGEUP: win32con.VK_PRIOR,
    wx.WXK_PAGEDOWN: win32con.VK_NEXT,
    wx.WXK_NUMPAD_PAGEDOWN: win32con.VK_NEXT,
    wx.WXK_END: win32con.VK_END,
    wx.WXK_NUMPAD_END: win32con.VK_END,
    wx.WXK_HOME: win32con.VK_HOME,
    wx.WXK_NUMPAD_HOME: win32con.VK_HOME,
    wx.WXK_LEFT: win32con.VK_LEFT,
    wx.WXK_NUMPAD_LEFT: win32con.VK_LEFT,
    wx.WXK_UP: win32con.VK_UP,
    wx.WXK_NUMPAD_UP: win32con.VK_UP,
    wx.WXK_RIGHT: win32con.VK_RIGHT,
    wx.WXK_NUMPAD_RIGHT: win32con.VK_RIGHT,
    wx.WXK_DOWN: win32con.VK_DOWN,
    wx.WXK_NUMPAD_DOWN: win32con.VK_DOWN,
    wx.WXK_INSERT: win32con.VK_INSERT,
    wx.WXK_NUMPAD_INSERT: win32con.VK_INSERT,
    wx.WXK_DELETE: win32con.VK_DELETE,
    wx.WXK_NUMPAD_DELETE: win32con.VK_DELETE,
}

def convert_wx_to_msw(wxk):
    """Convert a wx key code to a windows one.
    
    Based on code in:
    http://svn.wxwidgets.org/viewvc/wx/wxWidgets/trunk/src/msw/window.cpp
    
    @param wxk: the wx key code
    """
    for vk in _specialKeys:
        if _specialKeys[vk] == wxk:
            return vk
    if wxk in _specialTable:
        return _specialTable[wxk]
    vks = win32api.VkKeyScan(chr(wxk)) & 0xFF
    if vks != 0xFF:
        return vks
    return wxk
