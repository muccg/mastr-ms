import wx
from MainWindow import MainWindow
from MSDataSyncAPI import MSDataSyncAPI #, MSDSCheckFn
import sys
import esky
from identifiers import *
import os
import os.path
import plogging

import tendo
from tendo import singleton

SINGLE_LOCK = None

class MDataSyncApp(wx.PySimpleApp):
    def OnInit(self):
        global MSDSCheckFn
        #w = wx.LogChain(wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogGui() )
        

        win = MainWindow(None)
        self.win = win
        self.msds = MSDataSyncAPI( win.getLog() )#, False ) #false is no threading  
        
        self.msds.isMSWINDOWS = False
        if wx.Platform == "__WXMSW__":
            sys.stderr = open(os.path.join(DATADIR, "errorlogfile.txt"),"w")  #log to file
            sys.stdout = open(os.path.join(DATADIR, "outlogfile.txt"),"w")  #log to file
            win.getLog()("Running on Windows")
            self.msds.isMSWINDOWS = True
        elif wx.Platform == "__WXMAC__":
            win.getLog()("Running on Macintosh")
        elif wx.Platform == "__WXGTK__":
            win.getLog()("Running on Linux (GTK)") 
        

        #let the jobs execute in threads
        #disable this for debugging
        self.msds.startThread() 
        
        win.MSDSCheckFn = self.msds.checkRsync
        win.MSDSHandshakeFn = self.msds.handshakeRsync
        win.msds = self.msds
        win.resetTimeTillNextSync()
        #wx.Log_SetActiveTarget( wx.LogWindow(None, 'loggin...') )
        win.Show(True)
        self.SetTopWindow(win)
        return True

    

if __name__ == "__main__":
    if not os.path.exists(DATADIR):
        try:
            os.mkdir(DATADIR)
        except:
            print 'Unable to create data directory. Please create manually: %s' % os.normpath(DATADIR)
            exit()
    plogging.init_logger(name='client', logfile=os.path.join(DATADIR, 'clientlog.log'))
    

    should_exit = False
    try:
        SINGLE_LOCK = singleton.SingleInstance()
        print 'Successfully made single lock'
    except Exception, e:
        print 'The exception was: ', e
        should_exit = True

    if not should_exit:
        m = MDataSyncApp()
        #sys.stdout = m.win.log 
        m.MainLoop()
        m.msds.stopThread() #stop the thread if there is one
    
