import wx
from StatusBar import StatusBar
from SysTrayIcon import SystrayIcon
from FileList import ListCtrlPanel
import time

from identifiers import *


from WxLogger import Log

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

        wx.Frame.__init__(self, parent, -1, 'MS Datasync Application')
       


        self.contentPanel = wx.Panel(self, -1)
        _cp = self.contentPanel

        
        logLabel = wx.StaticText(parent = _cp)
        logLabel.SetLabel(label="Log")

        progressLabel = wx.StaticText(parent = _cp)
        progressLabel.SetLabel(label="Progress")

        #First thing, set up the log.
        self.logArea = wx.CollapsiblePane(_cp, -1, name='LogArea')
        self.logAreaPane = self.logArea.GetPane() 
        self.logAreaSizer = wx.BoxSizer(wx.VERTICAL) 
        self.logTextCtrl = wx.TextCtrl(self.logAreaPane, -1, 
                                    style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        
        


        progress = wx.Gauge(parent = _cp, range=100, size=(500, 20))
        self.progress = progress
        

        #modify the log
        if wx.Platform == "__WXMAC__":
            self.logTextCtrl.MacCheckSpelling(False)
        
        self.log = Log(self.logTextCtrl)
        wx.Log_SetActiveTarget(self.log) 

        #self.ListCtrlPanel = ListCtrlPanel(self, self.log)

        #menu bar
        #We set this up fairly early on in the piece so that the things below
        #status bars and timers etc, can enable/disable items in it.
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
        

        
        #Menu Events
        self.SetMenuBar(self.menuBar)
        self.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.OnMenuHighlight)
        self.Bind(wx.EVT_MENU, self.__testMenuFunction, id=ID_TEST_CONNECTION )
        self.Bind(wx.EVT_MENU, self.OnCheckNow, id=ID_CHECK_NOW )
        self.Bind(wx.EVT_MENU, self.OnMenuMinimise, id=ID_MINIMISE )
        self.Bind(wx.EVT_MENU, self.OnMenuQuit, id=ID_QUIT)
        self.Bind(wx.EVT_MENU, self.OnMenuPreferences, id=ID_PREFERENCES )
        self.Bind(wx.EVT_MENU, self.pycrust, id=ID_PYCRUST )
        
       
        #Collapsible pane event (the logArea):
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged, self.logArea)

        #now lay everything out.
        
        self.logAreaSizer.Add(self.logTextCtrl, 1, flag=wx.ALL|wx.GROW|wx.EXPAND, border=2)
        self.logAreaPane.SetSizerAndFit(self.logAreaSizer)
        #sizer.Fit(self)
        
        contentpanelsizer = wx.BoxSizer(wx.VERTICAL)
        contentpanelsizer.Add(progressLabel, 0, flag=wx.ALL, border=2)
        contentpanelsizer.Add(progress, 0, wx.ALL | wx.GROW|wx.EXPAND | wx.FIXED_MINSIZE, border=2)
        contentpanelsizer.Add(logLabel, 0, wx.ALL, border=2)
        contentpanelsizer.Add(self.logArea, 1, flag=wx.ALL | wx.GROW | wx.EXPAND | wx.FIXED_MINSIZE, border=2)
        #mainpanelsizer.Add(self.StatusBar, 0, flag=wx.ALL, border=2)

        #self.SetAutoLayout(True)
        self.contentPanel.SetSizerAndFit(contentpanelsizer)
        self.contentpanelsizer = contentpanelsizer
        #self.contentpanelsizer.SetSizeHints(self)
        
        
        #self.SetSizer(contentpanelsizer)
        
        self.OnPaneChanged() #force a layout fit

        
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.log('Finished loading application')

    def OnPaneChanged(self, event=None):
        if event:
            print 'wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % event.Collapsed

        # redo the layout
        self.logAreaSizer.Fit(self)#.contentPanel)
        self.contentpanelsizer.Fit(self)


    def resetTimeTillNextSync(self, forceReset = False):
        f = int(self.config.getValue('syncfreq'))
        if forceReset or self.syncFreq != f:
            self.syncFreq = f
            self.secondsUntilNextSync = 60 * f

    def setState(self, state):
        '''setState needs to set the statusbar text, and enable/disable the menu item for 'check now' '''
        #The menu on the system tray icon is created every time it is clicked:
        #We don't need to do anything here, as long as the state is set.
        self.state = state
        self.StatusBar.SetStatusText(state)
        if state == APPSTATE.UPLOADING_DATA:
            self.menuBar.Enable(ID_CHECK_NOW, False)
        else:
            self.menuBar.Enable(ID_CHECK_NOW, True)

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
        self.log('Minimising App', type=self.log.LOG_DEBUG)

    def OnMenuQuit(self, evt):
        '''Close (quit) the parent app.'''
        #This is the only way to quit the app.
        self.log('Quitting...', type=self.log.LOG_DEBUG)
        self.Bind(wx.EVT_TIMER, None)
        self.timer.Stop()
        self.StatusBar.Destroy()
        self.SystrayIcon.Destroy()
        #self.MenuBar.Destroy() #this causes a seg fault!
        self.log('Called Exit. Cleaning up...', type=self.log.LOG_DEBUG)
        self.Destroy()


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
        self.SetProgress(0) #set progress to 0 
        self.setState(APPSTATE.CHECKING_SYNCHUB)
        self.MSDSCheckFn(self, APPSTATE.UPLOADING_DATA, 'notused', self.CheckReturnFn)

    def SetProgress(self, prognum, add=False):
        #may be being called from a thread
        thread = self.msds.useThreading #see main.py for how msds got set
        if (thread):
            wx.CallAfter(self._SetProgress, prognum, add=add)
        else:
            self._SetProgress(prognum, add=add)

    def _SetProgress(self, prognum, add = False):
        if (add):
            prognum += self.progress.GetValue()

        self.progress.SetValue(prognum)


    def CheckReturnFn(self, retcode = True, retstring = "", *args):
        #we may have come back from a thread here.
        thread = self.msds.useThreading #see main.py for how msds got set
        if thread:
            wx.CallAfter(self.setState, APPSTATE.IDLE)
            wx.CallAfter(self.SetProgress, 100)
        else:

            self.setState(APPSTATE.IDLE)
            self.SetProgress(100)
        
        print 'return function called'
        if retcode:
            self.log('Check function returned', type=self.log.LOG_DEBUG, thread = thread)
        #else:
        #    self.log(retstring, type=self.log.LOG_DEBUG)
        

    def __testMenuFunction(self, event):
        self.log('Menu event! %s' % str(event), type = self.log.LOG_DEBUG)

    def getLog(self):
        #return weakref.ref(self.log) 
        return self.log

    def OnCloseWindow(self, event):
        self.OnMenuMinimise(event) #closing minimises

    def OnTimerTick(self, event):
        if self.secondsUntilNextSync > 0:
            self.secondsUntilNextSync -= 1
            self.StatusBar.SetStatusText("Next sync in %s" % (str(self.secondsUntilNextSync) ), 1 )
        else:
            self.resetTimeTillNextSync(forceReset = True)
            self.OnCheckNow(None)
        
    def pycrust(self,event):
        import wx.py as py
        w= py.crust.CrustFrame(parent = self)
        w.Show()
