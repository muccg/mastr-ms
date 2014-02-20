#!/bin/sh

OUTDIR=$(dirname $0)

cd $OUTDIR

while read dep
do
    wget -c $dep
done <<EOF
https://www.itefix.no/download/cwRsync_5.2.2_Free.zip
https://bitbucket.org/ccgmurdoch/mastr-ms/downloads/cwRsync_4.0.5_Installer.exe
http://downloads.sourceforge.net/project/py2exe/py2exe/0.6.9/py2exe-0.6.9.win32-py2.7.exe
http://downloads.sourceforge.net/project/nsis/NSIS%202/2.46/nsis-2.46-setup.exe
http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
http://downloads.sourceforge.net/project/wxpython/wxPython/2.8.12.1/wxPython2.8-win32-unicode-2.8.12.1-py27.exe
http://downloads.sourceforge.net/project/wxpython/wxPython/3.0.0.0/wxPython3.0-win32-3.0.0.0-py27.exe
EOF
