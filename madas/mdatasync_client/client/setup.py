from distutils.core import setup
from esky import bdist_esky
import py2exe

class Target:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.version = "0.1"
        self.company_name = "None"
        self.copyright = "None"
        self.name = "None"

freeze_includes = ['encodings','encodings.*'] 

freeze_excludes = [#'_ssl',  # Exclude _ssl
                      'pyreadline', 'difflib', 'doctest',
                      'pickle', 'calendar']  # Exclude standard library


py2exe_options = dict(
            ascii=True,  # Exclude encodings
            excludes= freeze_excludes,
            dll_excludes=['msvcr71.dll', 'MSVCP90.dll'],  # Exclude msvcr71
            includes= freeze_includes,
            compressed=True,  # Compress library.zip
                    )

bdist_esky_options_py2exe = dict(
            includes = freeze_includes,
            freezer_options = py2exe_options,
            freezer_module = 'py2exe')

# I can use this to fool py2exe! Docs -
#http://www.py2exe.org/index.cgi/OverridingCriteraForIncludingDlls
origIsSystemDLL = py2exe.build_exe.isSystemDLL
import os

def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in ("msvcp90.dll","gdiplus.dll"):
        return 0
    return origIsSystemDLL(pathname)

py2exe.build_exe.isSystemDLL = isSystemDLL


mdatasync_target = Target(
    description = "Application to sync data from clients to server",
    script = "main.py",
    dest_base = "mdatasync")

mssimulator_target = Target(
    description = "A tool to generate sample mass spec files from worklists",
    script = "Simulator.py",
    dest_base = "simulator")

setup(name='msDataSync',
      version='0.1',
      description='msDataSync application',
      author='Brad Power',
      scripts = ["main.py", "Simulator.py"],
      #console=['main.py'],
      windows = [mdatasync_target, mssimulator_target],
      options={'py2exe': py2exe_options, 'bdist_esky' : bdist_esky_options_py2exe},
      )


