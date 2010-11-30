import wx
import EnhancedStatusBar as ESB



class StatusBar(ESB.EnhancedStatusBar):
    def __init__(self, parent, log):
        ESB.EnhancedStatusBar.__init__(self, parent, -1)

        self.STATUS_ICONS = {
            'error' : wx.ArtProvider_GetBitmap(wx.ART_ERROR, wx.ART_TOOLBAR, (16,16)),
            'warning' : wx.ArtProvider_GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (16,16)),
            'ok' :  wx.ArtProvider_GetBitmap(wx.ART_TICK_MARK, wx.ART_MESSAGE_BOX,(16,16))
            }


        #Make the SB with 3 feilds
        self.SetFieldsCount(3)
        self.SetSize((-1, 23))
        #Set the relative Widths
        self.SetStatusWidths( [-1,-3, -1] )
        self.log = log
        self.sizeChanged = False
        self.progress =  wx.Gauge(self, -1)#, size=(400, 20))
        #self.progresstext = wx.StaticText(self, -1, "Inactive")
        self.statusicon = wx.StaticBitmap(self, -1, self.STATUS_ICONS['ok']) 
        
        self.AddWidget(self.progress, ESB.ESB_EXACT_FIT, ESB.ESB_EXACT_FIT, pos=1)
        #self.AddWidget(self.progresstext, pos=1)
        self.AddWidget(self.statusicon, pos=2)


        #self.Bind(wx.EVT_SIZE, self.OnSize)
        #self.Bind(wx.EVT_IDLE, self.OnIdle)

        #Field 0: Text
        #self.SetStatusText("status goes here", 0)

        #Field 1: A control
        #self.cb = wx.CheckBox(self, 1001, 'toggle ctrl')
        #self.Bind(wx.EVT_CHECKBOX, self.OnToggleClock, self.cb)
        #self.cb.SetValue(True)
        #set initial position of checkbox
        #self.Reposition()

        #Field 3: 
    
    '''
    def OnSize(self, evt):
        self.Reposition() #for normal size events
        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()

    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        self.sizeChanged = False
    '''

    def setTextStatus(self, text):
        pass

    def setProgress(self, value, progressdescription = ""):
        self.progress.SetValue(value)
        self.progresstext.SetValue(progressdescription)


    def getProgress(self):
        return self.progress.GetValue()

    def setIconStatus(self, icon):
        pass
