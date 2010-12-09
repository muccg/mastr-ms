import os
import os.path
#This version must be incremented each build
VERSION = "0.2.7"

#We need a strange looking datadir because of esky.
#Esky has an outer 'bootstrapper' exe, and all contents and
#updates are installed in directories under that.
#So if we keep config and other data in a subdir of our 'working dir' or even in it,
#it will be lost when we install a new version. We need our data dir to be in a common
#place. 
#The logic is:
#if your parent dir's parent contains a dir called 'appdata', then store your datadir at that level.
#otherwise, store your data dir in your parent dir. This is because of how Esky packages 
#the app initially as opposed to what it looks like once you have done an update.

DATADIRNAME = 'data' #what we want the final leaf dir to be called
DATADIR = os.path.join('..', DATADIRNAME) #in parent as a default
if os.path.exists(os.path.join('..', '..', 'appdata') ):
    DATADIR = os.path.join('..','..', DATADIRNAME)


#Identifiers used in main window
ID_TEST_CONNECTION = 101
ID_CHECK_NOW = 102
ID_MINIMISE = 103
ID_QUIT = 104
ID_PREFERENCES = 201
ID_PYCRUST = 202
ID_PROGRAMUPDATES = 203
ID_ABOUT = 211

#Preferences window
ID_NODESELECTOR_DIALOG = 204
ID_CHOOSENODE_BUTTON = 205
ID_SENDLOGS_BUTTON = 206
ID_SENDKEY_BUTTON = 207
ID_HANDSHAKE_BUTTON = 210
ID_GENERATEFILES_BUTTON = 208 #in the simulator application
ID_CLEARINPUT_BUTTON = 209 #in the simulator application
#Node config selector window
ID_SENDSCREENSHOT_BUTTON = 212

