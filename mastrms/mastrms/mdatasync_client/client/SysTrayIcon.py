import wx
import time

from IconBar import IconBar
#A class exhibiting the sys tray behaviour that we want.
class SystrayIcon(wx.TaskBarIcon):
    '''This class puts an icon in the system tray (which wx calls a 'taskbar').
       We add a popup menu on this to add in our own functionality.
       We also have some functionality for changing the look of the icon
       if we like'''

    ID_ICON_TIMER = wx.NewId()
    #some ID's for our little menu
    TBMENU_RESTORE          = wx.NewId()
    TBMENU_QUIT             = wx.NewId()
    TBMENU_CHECKNOW         = wx.NewId()
    TBMENU_TESTCONNECTION   = wx.NewId()
    TBMENU_HIDE             = wx.NewId()

    l = 0 #iconbar offsets
    r = 0
    def __init__(self, frame, log):
        self.log = log
        wx.TaskBarIcon.__init__(self)
        self.parentApp = frame
        self.IconBar = IconBar( (127,127,0), (255,255,0), (0,127,127), (0,255,255) )
        self.SetIconBar(self.l, self.r)

        #Now bind some events.
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        self.Bind(wx.EVT_MENU, self.OnTaskBarQuit, id=self.TBMENU_QUIT)
        self.Bind(wx.EVT_MENU, self.OnTaskBarCheckNow, id=self.TBMENU_CHECKNOW)
        self.Bind(wx.EVT_MENU, self.OnTaskBarTestConnection, id=self.TBMENU_TESTCONNECTION)
        self.Bind(wx.EVT_MENU, self.OnTaskBarHide, id=self.TBMENU_HIDE)


    def CreatePopupMenu(self):
        ''' create a popup menu to display when the icon is right clicked (every time)
            Called by the base class. So we just define it, the base class takes
            care of the rest'''
        menu = wx.Menu()
        menu.Append(self.TBMENU_CHECKNOW, "Check for updates")
        menu.Append(self.TBMENU_TESTCONNECTION, "Test connection")
        menu.AppendSeparator()
        menu.Append(self.TBMENU_HIDE, "Hide main window")
        menu.Append(self.TBMENU_RESTORE, "Open main window")
        menu.Append(self.TBMENU_QUIT,   "Quit")
        #grey out the 'check now' item if we are already uploading data
        from MainWindow import APPSTATE
        if self.parentApp.state == APPSTATE.UPLOADING_DATA:
            menu.Enable(self.TBMENU_CHECKNOW, False)
        return menu



    def OnTaskBarActivate(self, evt):
        '''activate the parent app if it is iconified or not
           shown for any reason'''
        if self.parentApp.IsIconized():
            self.parentApp.Iconize(False)
        if not self.parentApp.IsShown():
            self.parentApp.Show(True)
        self.parentApp.Raise()
        self.log('Raising App', type=self.log.LOG_DEBUG)


    def OnTaskBarQuit(self, evt):
        '''Close (quit) the parent app.'''
        #self.log.WriteText('Quiting...')
        self.parentApp.OnMenuQuit(evt)

    def OnTaskBarHide(self, evt):
        '''minimise/hide the main window'''
        #self.log.WriteText('Hiding...')
        self.parentApp.OnMenuMinimise(evt)


    def OnTaskBarCheckNow(self, evt):
        self.log('CheckNow chosen', type=self.log.LOG_DEBUG)
        #from MSDataSyncAPI import MSDSCheckFn
        self.parentApp.OnCheckNow(evt)


    def OnTaskBarTestConnection(self, evt):
        self.log('TestConnection chosen', type=self.log.LOG_DEBUG)

    def SetIconTimer(self):
        '''fires a timer which calls BlinkIcon'''
        self.icon_timer = wx.Timer(self, self.ID_ICON_TIMER)
        wx.EVT_TIMER(self, self.ID_ICON_TIMER, self.BlinkIcon) #set the timer event callback
        self.icon_timer.Start(500)

    def BlinkIcon(self, event):
        '''shifts the icon in the systray'''
        self.SetIconBar(self.l, self.r)
        self.l += 1
        if self.l > self.IconBar.numIcons-1:
            self.l = 0
            self.r += 1
            if self.r > self.IconBar.numIcons-1:
                self.r = 0

    def SetIconBar(self, l, r):
        '''sets the icon in the systray to whatever is in the iconbar at coordinates l/r'''
        icon = self.IconBar.Get(l, r)
        #self.SetIcon(icon, "L:%d,R:%d"%(l,r) )
        #Set the icon, and the mouseover text to be the apps statusbar's 0th field
        #print  str(self.parentApp.StatusBar.GetStatusText())
        self.SetIcon(icon, str(self.parentApp.StatusBar.GetStatusText()) )
