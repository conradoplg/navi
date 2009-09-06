import logging
import sys

APPNAME = 'Navi'
VERSION = '1.0.1'
DESCRIPTION = 'Notes editor'
URL = ''
UPDATE_URL = ''
REPORT_URL = ''
HELP_URL = ''
AUTHOR = u'Conrado Porto Lopes Gouvea'
AUTHOR_EMAIL = 'conradoplg@gmail.com'
COPYRIGHT = u"Copyright (c) 2009, %s <%s>\nAll rights reserved." % (AUTHOR, AUTHOR_EMAIL)

DEBUG = True
LOG_LEVEL = logging.ERROR

if sys.platform == 'win32':
    PATH_SEP = ';'
else:
    PATH_SEP = ':'

MANIFEST = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="0.64.1.0"
        processorArchitecture="x86"
        name="Controls"
        type="win32"
    />
    <description>Quivi</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity 
                type='win32' 
                name='Microsoft.VC90.CRT' 
                version='9.0.21022.8' 
                processorArchitecture='*' 
                publicKeyToken='1fc8b3b9a1e18e3b' />
        </dependentAssembly>
    </dependency>
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
        <security>
            <requestedPrivileges>
                <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
            </requestedPrivileges>
        </security>
    </trustInfo>
</assembly> 
"""
