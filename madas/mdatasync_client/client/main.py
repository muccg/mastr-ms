import wx
from MainWindow import MainWindow
from MSDataSyncAPI import MSDataSyncAPI #, MSDSCheckFn


class MDataSyncApp(wx.PySimpleApp):
    def OnInit(self):
        global MSDSCheckFn
        #w = wx.LogChain(wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogGui() )
        win = MainWindow(None)
        self.msds = MSDataSyncAPI( win.getLog() ) 
        
        #let the jobs execute in threads
        #disable this for debugging
        #msds.startThread() 
        
        win.MSDSCheckFn = self.msds.checkRsync
        win.config = self.msds.config #TODO make this weakref
        win.resetTimeTillNextSync()
        #wx.Log_SetActiveTarget( wx.LogWindow(None, 'loggin...') )
        win.Show(True)
        self.SetTopWindow(win)
        return True

    


m = MDataSyncApp()
m.MainLoop()
m.msds.stopThread() #stop the thread if there is one.
