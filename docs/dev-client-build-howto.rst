#summary How to build the sync client.

= Introduction =

The support libraries and binaries are in the mdatasync_client/client/supportwin32 directory.
You should be able to build the client on a 32 bit Windows XP box, by installing these resources as described below.

= Details =

==Initial Setup of build environment==

 * Copy client and supportwin32 over to the windows machine.
 * Install Python27 (utf8 encoding for json is broken in earlier versions)
 * Install wx for python 2.7
 * Install py2exe for python 2.7
 * Install NSIS
 * Install 7Zip
 * Extract the EnvVarUpdate extension
 * Copy the extension into c:\program files\nsis\include
 * Open a shell
 * Change dir to the 'client' dir

==Building the code==

First, make sure you have updated the version number in identifiers.py to be unique, and sequentially higher than previous ones.

on Windows box, get the latest client dir.
run c:\Python27\python.exe setup.py bdist_esky

Then unzip the build you just did (in dist/) so that the files are available to the installer.

If you then ran the nsi file (right click on the file and choose 'Compile with NSIS'), it would make an installer, using the build you just did (in /dist) as a source. So that is how you make an installer.

If you want to publish just the update, you take the .zip that is generated in the dist directory, and scp it to the distribution URL. Currently this is on faramir, in /usr/local/python/htdocs/ma

As long as the indentifiers VERSION string was incremented, a new version will be available to esky.

== Errors == 

When building with Esky, if you get the message 'cannot access ..../main.py. The file is in use by another process', this probably means your python code fails a syntax check or has some other runtime error.
