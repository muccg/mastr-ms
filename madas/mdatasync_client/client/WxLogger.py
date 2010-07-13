import wx
import time

class Log(wx.PyLog):
    def __init__(self, textCtrl, logTime=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime

        #type constants
        self.LOG_NORMAL = 0
        self.LOG_DEBUG = 1
        self.LOG_WARNING = 2
        self.LOG_ERROR = 3

    def DoLogString(self, message, timeStamp=0, type = 0, **kwargs): #small type hardcoding sin here
        textstyle = wx.TextAttr()
        
        if type == self.LOG_DEBUG:
            message = 'DEBUG: ' + message
            textstyle.SetTextColour(wx.Colour(0,0,255) ) #blue
        elif type == self.LOG_WARNING:
            message = 'WARNING: ' + message
            textstyle.SetTextColour(wx.Colour(255,128,64) ) #orange
        elif type == self.LOG_ERROR:
            message = 'ERROR: ' + message
            textstyle.SetTextColour(wx.Colour(255,0,0) ) #red
        else: #type == normal
            textstyle.SetTextColour(wx.Colour(0,0,0) ) #black
        #add in the time:
        message = '[%s] %s' % (time.strftime("%X", time.localtime() ), message) 

        if self.tc: # and (not Debug or (Debug and self.DebugOn)):
            self.tc.SetDefaultStyle(textstyle)
            self.tc.AppendText(message + '\n')

    def __call__(self, *args, **kwargs):
        print 'startlog',
        #print '__call__ with args:%s and kwargs:%s' % (str(*args), str(**kwargs))
        thread = kwargs.get('thread', False)

        if (thread):
            #print 'LOG: callafter:', args
            wx.CallAfter(self.DoLogString, *args, **kwargs) 
        else:
            #print 'LOG: notcallafter:', args
            self.DoLogString(*args, **kwargs)
        print 'endlog'

