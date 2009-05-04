"""Distutils setup script."""

from libnavi import meta

import sys
import os
import re
from glob import glob
from shutil import copy

if sys.platform == 'win32':
    # ModuleFinder can't handle runtime changes to __path__, but win32com uses them
    try:
        # if this doesn't work, try import modulefinder
        import py2exe.mf as modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass



from distutils.core import setup

#If we want to build a py2exe dist, patch distutils with py2exe
try:
    if 'py2exe' in sys.argv:
        import py2exe
except ImportError:
    pass

#If we want to build a egg dist, patch distutils with setuptools
try:
    if 'bdist_egg' in sys.argv:
        from setuptools import setup
except ImportError:
    pass


#Auto find subpackages

def add_package(found_packages, directory, local_names):
    if '__init__.py' in local_names:
        s = re.sub('.*libnavi', 'libnavi', directory)
        s = re.sub('.*appcommon', 'appcommon', directory)
        s = s.replace(os.path.sep, '.')
        found_packages.append(s)
    else:
        local_names = []

packages = []
os.path.walk('libnavi', add_package, packages)
os.path.walk('appcommon', add_package, packages)

if sys.platform == 'win32':
    main_files = ['LICENSE.txt', 'msvcp90.dll', 'msvcr90.dll',
                  'Microsoft.VC90.CRT.manifest']
#    translation_files = glob('localization/*.mo') + ['localization/default.pot']
    data_files = [('', main_files),
#                  ('localization', translation_files)
    ]
    scripts = ['navi.pyw']
else:
#    data_files = [
#                  ('share/applications', ['resources/quivi.desktop']),
#                  ('share/pixmaps', ['resources/icons/48x48/quivi.png']),
#                  ('share/icons/hicolor/scalable/apps', ['resources/icons/scalable/quivi.svg']),
#                  ('share/icons/hicolor/16x16/apps', ['resources/icons/16x16/quivi.png']),
#                  ('share/icons/hicolor/32x32/apps', ['resources/icons/32x32/quivi.png']),
#                  ('share/icons/hicolor/48x48/apps', ['resources/icons/48x48/quivi.png']),
#                 ]
#    MO_DIR = 'localization'
#    for mo in glob(os.path.join(MO_DIR, '*.mo')):
#        lang = os.path.basename(mo[:-3])
#        nmo = os.path.join(MO_DIR, lang, 'quivi.mo')
#        directory = os.path.dirname(nmo)
#        if not os.path.exists(directory):
#            os.makedirs(directory)
#        copy(mo, nmo)
#        dest = os.path.dirname(os.path.join('share', 'locale', lang, 'LC_MESSAGES', 'quivi.mo'))
#        data_files.append((dest, [nmo]))
    copy('navi.pyw', 'navi')
    scripts = ['navi']


exclude_packages = ["Tkconstants", "Tkinter", "tcl", 'pydoc', '_ssl']


setup(name=meta.APPNAME,
      version=meta.VERSION,
      description=meta.APPNAME,
      author=meta.AUTHOR,
      author_email=meta.AUTHOR_EMAIL,
      packages = packages,
      license = "MIT",
      url = meta.URL,
      options = {'py2exe': {'dist_dir': 'bin',
                            'excludes': exclude_packages
                            }
                },
      windows= [{'script': 'navi.pyw',
                 'icon_resources': [(1, 'resources/navi.ico')],
                 'other_resources': [(24,1,meta.MANIFEST)]
                 }],
      scripts = scripts,
      data_files = data_files
      )
