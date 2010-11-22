import wx
from MainWindow import MainWindow
from MSDataSyncAPI import MSDataSyncAPI #, MSDSCheckFn
import sys
import esky


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
            sys.stderr = open("errorlogfile.txt","w")  #log to file
            sys.stdout = open("outlogfile.txt","w")  #log to file
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
        win.msds = self.msds
        win.resetTimeTillNextSync()
        #wx.Log_SetActiveTarget( wx.LogWindow(None, 'loggin...') )
        win.Show(True)
        self.SetTopWindow(win)
        return True

    


m = MDataSyncApp()
#sys.stdout = m.win.log 
m.MainLoop()
m.msds.stopThread() #stop the thread if there is one.
