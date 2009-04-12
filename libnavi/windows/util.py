import wx
import sys
import ctypes

if sys.platform == 'win32':
    from win32com.shell import shell, shellcon
    from win32con import FILE_ATTRIBUTE_NORMAL, FILE_ATTRIBUTE_DIRECTORY

def get_icon_for_extension(extension):
    """dot is mandatory in extension"""

    flags = shellcon.SHGFI_SMALLICON | \
            shellcon.SHGFI_ICON | \
            shellcon.SHGFI_USEFILEATTRIBUTES

    retval, info = shell.SHGetFileInfo(extension,
                             FILE_ATTRIBUTE_NORMAL,
                             flags)
    # non-zero on success
    assert retval

    hicon, iicon, attr, display_name, type_name = info

    # Get the bitmap
    icon = wx.EmptyIcon()
    icon.SetHandle(hicon)
    return icon

def get_icon_for_directory():
    flags = shellcon.SHGFI_SMALLICON | \
            shellcon.SHGFI_ICON | \
            shellcon.SHGFI_USEFILEATTRIBUTES

    retval, info = shell.SHGetFileInfo('dummy',
                             FILE_ATTRIBUTE_DIRECTORY,
                             flags)
    # non-zero on success
    assert retval

    hicon, iicon, attr, display_name, type_name = info

    # Get the bitmap
    icon = wx.EmptyIcon()
    icon.SetHandle(hicon)
    return icon

def logical_cmp(a, b):
    assert isinstance(a, unicode) and isinstance(b, unicode) 
    return ctypes.windll.shlwapi.StrCmpLogicalW(a, b)

def get_unicode_argv():                                                                                               
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of UTF-8                                           
    strings.                                                                                                         
                                                                                                                     
    Versions 2.5 and older of Python don't support Unicode in sys.argv on                                            
    Windows, with the underlying Windows API instead replacing multi-byte                                            
    characters with '?'.                                                                                             
                                                                                                                     
    Returns None on failure.                                                                                         
                                                                                                                     
    Example usage:                                                                                                   
                                                                                                                     
    >>> def main(argv=None):                                                                                         
    ...    if argv is None:                                                                                          
    ...        argv = win32_utf8_argv() or sys.argv                                                                  
    ...
    """

    from ctypes import POINTER, byref, cdll, c_int, windll
    from ctypes.wintypes import LPCWSTR, LPWSTR
    
    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR
    
    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)
    
    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        return [argv[i] for i in xrange(argc.value)][-len(sys.argv):]
    else:
        return []

