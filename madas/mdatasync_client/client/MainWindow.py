import wx
from StatusBar import StatusBar
from SysTrayIcon import SystrayIcon
from FileList import ListCtrlPanel
import time

from identifiers import *

class Log(wx.PyLog):
    def __init__(self, textCtrl, logTime=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime
        self.DebugOn = True

    def setDebug(boolvalue):
        self.DebugOn = boolvalue

    def DoLogString(self, message, timeStamp=0, Debug = False):
        #print message, timeStamp
        #if self.logTime:
        #    message = time.strftime("%X", time.localtime(timeStamp)) + \
        #              ": " + message
        if Debug:
            message = 'DEBUG: ' + message

        #add in the time:
        message = '[%s] %s' % (time.strftime("%X", time.localtime() ), message) 


        if self.tc and (not Debug or (Debug and self.DebugOn)):
            self.tc.AppendText(message + '\n')

    #other methods that may be being called.
    write = DoLogString
    WriteText = DoLogString


class APPSTATE:  

    CHECKING_SYNCHUB = 'Negotiating with server'
    UPLOADING_DATA   = 'Uploading data'
    IDLE             = 'Idle'


import weakref
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)
class MainWindow(wx.Frame):
    def __init__(self, parent):

        wx.Frame.__init__(self, parent, -1, 'Test sync window')
        
        #First thing, set up the log.
        self.logTextCtrl = wx.TextCtrl(self, -1, 
                                    style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        if wx.Platform == "__WXMAC__":
            self.logTextCtrl.MacCheckSpelling(False)
        self.log = Log(self.logTextCtrl)
        wx.Log_SetActiveTarget(Log(self.log)) 

        #self.ListCtrlPanel = ListCtrlPanel(self, self.log)

        #status bar
        self.StatusBar = StatusBar(self, self.log)
        self.SetStatusBar(self.StatusBar)
        self.state = APPSTATE.IDLE
        self.StatusBar.SetStatusText(self.state)

        #sys tray icon
        self.SystrayIcon = SystrayIcon(self, self.log)
        self.SystrayIcon.SetIconTimer()
      
        self.setState(APPSTATE.IDLE)
   
        #Create a timer.
        self.timer = wx.Timer(self, -1)
        self.Bind(wx.EVT_TIMER, self.OnTimerTick, self.timer)
        self.timer.Start(milliseconds = 1000, oneShot = False)
        self.secondsUntilNextSync = 0
        self.syncFreq = 0 #local cache of syncfreq
        

        #menu bar
        self.menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(ID_TEST_CONNECTION, "&Test Connection", "Test your connection to the server")
        fileMenu.Append(ID_CHECK_NOW, "&Check Now", "Check for required uploads now")
        fileMenu.AppendSeparator()
        fileMenu.Append(ID_MINIMISE, "&Minimize", "Minimize the app to the system tray")
        fileMenu.Append(ID_QUIT, "&Quit", "Quits the application completely")

        editMenu = wx.Menu()
        editMenu.Append(ID_PREFERENCES, "&Preferences", "Application Preferences")
        editMenu.Append(ID_PYCRUST, "&Pycrust", "Pycrust")

        self.menuBar.Append(fileMenu, "&File")
        self.menuBar.Append(editMenu, "&Edit")


        #Menu Events
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.OnMenuHighlight)
        self.Bind(wx.EVT_MENU, self.__testMenuFunction, id=ID_TEST_CONNECTION )
        self.Bind(wx.EVT_MENU, self.OnCheckNow, id=ID_CHECK_NOW )
        self.Bind(wx.EVT_MENU, self.OnMenuMinimise, id=ID_MINIMISE )
        self.Bind(wx.EVT_MENU, self.OnMenuQuit, id=ID_QUIT)
        self.Bind(wx.EVT_MENU, self.OnMenuPreferences, id=ID_PREFERENCES )
        self.Bind(wx.EVT_MENU, self.__testMenuFunction, id=ID_PYCRUST )
        

        
        self.SetSize((640,480))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.log.WriteText('Finished loading application')
        self.log.WriteText('Testing Debug', Debug=True)

    def resetTimeTillNextSync(self, forceReset = False):
        f = int(self.config.getValue('syncfreq'))
        if forceReset or self.syncFreq != f:
            self.syncFreq = f
            self.secondsUntilNextSync = 60 * f

    def setState(self, state):
        self.state = state
        self.StatusBar.SetStatusText(state)

    def OnMenuHighlight(self, event):
        # Show how to get menu item info from this event handler
        id = event.GetMenuId()
        item = self.GetMenuBar().FindItemById(id)
        if item:
            text = item.GetText()
            help = item.GetHelp()

        # but in this case just call Skip so the default is done
        event.Skip() 

    def OnMenuMinimise(self, event):
        if not self.IsIconized():
            self.Iconize(True)
        if self.IsShown():
            self.Show(False)
        self.Lower()
        self.log.WriteText('Minimising App', Debug=True)

    def OnMenuQuit(self, evt):
        '''Close (quit) the parent app.'''
        self.log.WriteText('Quitting...')
        #wx.CallAfter(self.Close())
        self.Close()

    def OnMenuPreferences(self, evt):
        '''open the prefs dialog which BLOCKS'''
        import AutoPreferences
        a = AutoPreferences.AutoPreferences(self, -1, self.config, self.log) 
         # this does not return until the dialog is closed.
        val = a.ShowModal()
        #do something here with val if you like (==wx.ID_OK for instance)
        a.Destroy()

    def OnCheckNow(self, evt):
        #MSDSCheckFn is defined by the main app - MDataSyncApp. It just sets the method in a hacky way :(
        self.setState(APPSTATE.CHECKING_SYNCHUB)
        self.MSDSCheckFn(self, APPSTATE.UPLOADING_DATA, 'notused', self.CheckReturnFn)

    def CheckReturnFn(self, *args):
        self.setState(APPSTATE.IDLE)
        self.log.WriteText('Check function returned')


    def __testMenuFunction(self, event):
        self.log.WriteText('Menu event! %s' % str(event))

    def getLog(self):
        #return weakref.ref(self.log) 
        return self.log

    def OnCloseWindow(self, event):
        self.StatusBar.Destroy()
        self.SystrayIcon.Destroy()
        #self.MenuBar.Destroy() #this causes a seg fault!
        self.log.WriteText('Called Exit. Cleaning up...')
        self.Destroy()

    def OnTimerTick(self, event):
        if self.secondsUntilNextSync > 0:
            self.secondsUntilNextSync -= 1
            self.StatusBar.SetStatusText("Next sync in %s" % (str(self.secondsUntilNextSync) ), 1 )
        else:
            self.resetTimeTillNextSync(forceReset = True)
            self.OnCheckNow(None)
        
