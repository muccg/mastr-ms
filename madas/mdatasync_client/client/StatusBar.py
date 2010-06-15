import wx

class StatusBar(wx.StatusBar):
    def __init__(self, parent, log):
        wx.StatusBar.__init__(self, parent, -1)

        #Make the SB with 3 feilds
        self.SetFieldsCount(3)
        #Set the relative Widths
        self.SetStatusWidths( [-1,-3,-1] )
        self.log = log
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        #Field 0: Text
        self.SetStatusText("status goes here", 0)

        #Field 1: A control
        #self.cb = wx.CheckBox(self, 1001, 'toggle ctrl')
        #self.Bind(wx.EVT_CHECKBOX, self.OnToggleClock, self.cb)
        #self.cb.SetValue(True)
        #set initial position of checkbox
        #self.Reposition()

        #Field 3: 
        
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
        #self.cb.SetPosition((rect.x+2, rect.y+2))
        #self.cb.SetSize((rect.width-4, rect.height-4))
        self.sizeChanged = False

