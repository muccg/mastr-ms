import wx
from MainWindow import MainWindow
from MSDataSyncAPI import MSDataSyncAPI
from config import MSDSConfig
import sys
from identifiers import *
import os
import os.path
import plogging

import tendo
from tendo import singleton

SINGLE_LOCK = None

class MDataSyncApp(wx.PySimpleApp):
    def __init__(self, config=None, *args, **kwargs):
        self.config = config or MSDSConfig.load()
        super(MDataSyncApp, self).__init__(*args, **kwargs)

    def OnInit(self):
        #w = wx.LogChain(wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogStderr() )
        #wx.Log_SetActiveTarget( wx.LogGui() )

        win = MainWindow(self.config, None)
        self.win = win
        self.msds = MSDataSyncAPI(self.config, win.getLog())

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


def main():
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

    return 0

if __name__ == "__main__":
    sys.exit(main())
