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
        msds = MSDataSyncAPI( win.getLog() ) 
        win.MSDSCheckFn = msds.checkRsync
        win.config = msds.config #TODO make this weakref
        #wx.Log_SetActiveTarget( wx.LogWindow(None, 'loggin...') )
        win.Show(True)
        self.SetTopWindow(win)
        return True


m = MDataSyncApp()
m.MainLoop()
