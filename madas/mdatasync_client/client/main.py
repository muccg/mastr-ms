import wx
from MainWindow import MainWindow
from MSDataSyncAPI import MSDataSyncAPI #, MSDSCheckFn
import sys


class MDataSyncApp(wx.PySimpleApp):
    def OnInit(self):
        global MSDSCheckFn
        #w = wx.LogChain(wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogGui() )
        win = MainWindow(None)
        self.win = win
        self.msds = MSDataSyncAPI( win.getLog() )#, False ) #false is no threading  
        
        #let the jobs execute in threads
        #disable this for debugging
        self.msds.startThread() 
        
        win.MSDSCheckFn = self.msds.checkRsync
        win.config = self.msds.config #TODO make this weakref
        win.resetTimeTillNextSync()
        #wx.Log_SetActiveTarget( wx.LogWindow(None, 'loggin...') )
        win.Show(True)
        self.SetTopWindow(win)
        return True

    


m = MDataSyncApp()
#sys.stdout = m.win.log 
m.MainLoop()
m.msds.stopThread() #stop the thread if there is one.
