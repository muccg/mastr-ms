from distutils.core import setup
import py2exe

py2exe_options = dict(
            ascii=True,  # Exclude encodings
            excludes=['_ssl',  # Exclude _ssl
                      'pyreadline', 'difflib', 'doctest',
                      'optparse', 'pickle', 'calendar'],  # Exclude standard library
                      dll_excludes=['msvcr71.dll', 'MSVCP90.dll'],  # Exclude msvcr71
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



setup(name='msDataSync',
      version='0.1',
      description='msDataSync application',
      author='Brad Power',
      console=['main.py'],
      options={'py2exe': py2exe_options},
      )


