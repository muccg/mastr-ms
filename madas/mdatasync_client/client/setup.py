from distutils.core import setup
import py2exe

py2exe_options = dict(
            ascii=True,  # Exclude encodings
            excludes=[#'_ssl',  # Exclude _ssl
                      'pyreadline', 'difflib', 'doctest',
                      'optparse', 'pickle', 'calendar'],  # Exclude standard library
            dll_excludes=['msvcr71.dll', 'MSVCP90.dll'],  # Exclude msvcr71
            includes=['encodings','encodings.*'],
            compressed=True,  # Compress library.zip
                    )



# I can use this to fool py2exe! Docs -
#http://www.py2exe.org/index.cgi/OverridingCriteraForIncludingDlls
origIsSystemDLL = py2exe.build_exe.isSystemDLL
import os

def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in ("msvcp90.dll","gdiplus.dll"):
        return 0
    return origIsSystemDLL(pathname)

py2exe.build_exe.isSystemDLL = isSystemDLL

class Target:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.version = "0.1"
        self.company_name = "None"
        self.copyright = "None"
        self.name = "None"

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
      #console=['main.py'],
      windows = [mdatasync_target, mssimulator_target],
      options={'py2exe': py2exe_options},
      )


