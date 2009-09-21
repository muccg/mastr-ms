#test app
import time
import wx
import string
ID_ICON_TIMER = wx.NewId()


class IconBar:

    numIcons = 5
    ##
    # \brief the constructor default left: red, default right: green
    #
    def __init__(self,l_off=[128,0,0],l_on=[255,0,0],r_off=[0,128,0],r_on=[0,255,0]):
        self.s_line = "\xff\xff\xff"+"\0"*45
        self.s_border = "\xff\xff\xff\0\0\0"
        self.s_point = "\0"*3
        self.sl_off = string.join(map(chr,l_off),'')*6
        self.sl_on = string.join(map(chr,l_on),'')*6
        self.sr_off = string.join(map(chr,r_off),'')*6
        self.sr_on = string.join(map(chr,r_on),'')*6

    ##
    # \brief gets a new icon with 0 <= l,r <= 5
    #
    def Get(self,l,r):
        s=""+self.s_line
        for i in range(5):
            if i<(self.numIcons-l):
                sl = self.sl_off
            else:
                sl = self.sl_on

            if i<(self.numIcons-r):
                sr = self.sr_off
            else:
                sr = self.sr_on

            s+=self.s_border+sl+self.s_point+sr+self.s_point
            s+=self.s_border+sl+self.s_point+sr+self.s_point
            s+=self.s_line

        image = wx.EmptyImage(16,16)
        image.SetData(s)

        bmp = image.ConvertToBitmap()
        bmp.SetMask(wx.Mask(bmp, wx.WHITE)) #sets the transparency colour to white 

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)

        return icon



#A class exhibiting the sys tray behaviour that we want.
class SystrayIcon(wx.TaskBarIcon):
    l = 0 #iconbar offsets
    r = 0
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = frame
        self.IconBar = IconBar( (127,127,0), (255,255,0), (0,127,127), (0,255,255) )
        self.SetIconBar(self.l, self.r)

    def SetIconTimer(self):
        self.icon_timer = wx.Timer(self, ID_ICON_TIMER)
        wx.EVT_TIMER(self, ID_ICON_TIMER, self.BlinkIcon) #set the timer event callback
        self.icon_timer.Start(100)

    def BlinkIcon(self, event):
        self.SetIconBar(self.l, self.r)
        self.l += 1
        if self.l > self.IconBar.numIcons-1:
            self.l = 0
            self.r += 1
            if self.r > self.IconBar.numIcons-1:
                self.r = 0

    def SetIconBar(self, l, r):
        icon = self.IconBar.Get(l, r)
        self.SetIcon(icon, "L:%d,R:%d"%(l,r) )


class StatusBar(wx.StatusBar):
    def __init__(self, parent, log):
        wx.StatusBar.__init__(self, parent, -1)

        #Make the SB with 3 feilds
        self.SetFieldsCount(3)
        #Set the relative Widths
        self.SetStatusWidths( [-2,-1,-2] )
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
        self.cb.SetPosition((rect.x+2, rect.y+2))
        self.cb.SetSize((rect.width-4, rect.height-4))
        self.sizeChanged = False

    

class winWithStatusBar(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, 'Test sync window')

        self.sb = StatusBar(self, log)
        self.SetStatusBar(self.sb)
        tc = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY|wx.TE_MULTILINE)

        self.SetSize((640,480))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.SystrayIcon = SystrayIcon(self)
        self.SystrayIcon.SetIconTimer()

    def OnCloseWindow(self, event):
        self.Destroy()


class MDataSyncApp(wx.PySimpleApp):
    def OnInit(self):
        win = winWithStatusBar(None, None)
        win.Show(True)
        self.SetTopWindow(win)
        return True

app = MDataSyncApp()
app.MainLoop()
