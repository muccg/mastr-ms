import wx
import time
from WxLogger import Log
from identifiers import *
import  wx.lib.filebrowsebutton as filebrowse
import os
import os.path

class GeneratePopup(wx.Dialog):
    def __init__(self, log, parent, fileslist, destdir):
        self.log = log
        wx.Dialog.__init__(self, parent, -1)
        self.destdir = destdir
        self.contentPanel = wx.Panel(self, -1)
        _cp = self.contentPanel
        self.listctrl = wx.ListBox(_cp, -1, style=wx.LB_MULTIPLE)


        self.listctrl.InsertItems([i for i in fileslist], 0)
        for p in xrange(0, len(fileslist)):
            self.listctrl.Select(p)

        self.textlabel = wx.StaticText(_cp, -1, "Files to Generate:") 
        self.OkButton = wx.Button(_cp, id=wx.ID_OK)
        self.OkButton.Bind(wx.EVT_BUTTON, self.GenerateFiles)
        self.CancelButton = wx.Button(_cp, id=wx.ID_CANCEL)
        self.buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsizer.Add(self.OkButton, 0, flag=wx.ALL, border=2)
        self.buttonsizer.Add(self.CancelButton, 0, flag=wx.ALL, border=2)
        
        self.contentsizer = wx.BoxSizer(wx.VERTICAL)
        self.contentsizer.Add(self.textlabel, 0, flag=wx.ALL, border=2)
        self.contentsizer.Add(self.listctrl, 0, flag=wx.ALL|wx.GROW, border=2)
        self.contentsizer.Add(self.buttonsizer, 1, flag=wx.ALL|wx.GROW, border=2)
        _p = self.contentsizer

        self.contentPanel.SetSizerAndFit(_p)
        _p.Fit(self)

    def GenerateFiles(self, evt):
        selindexes = self.listctrl.GetSelections()
        print self.destdir
        for selindex in selindexes:
            listitem = self.listctrl.Items[selindex]
            if listitem.endswith('.d'):
                #create a directory instead, and blat a bunch of files there.

            
            try:
                fname = os.path.join(self.destdir, listitem)
                if not os.path.exists(fname):
                    open(fname, 'w').close()
                    self.log("Wrote item %d: %s" % (selindex, fname))
                else:
                    self.log("Item %d already exits: %s" % (selindex, fname) )
            except Exception, e:
                self.log("Error writing item %d:%s - %s" % (selindex, fname, str(e)), type=self.log.LOG_ERROR)
        self.EndModal(0)
    

class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "MS Simulator")

        self.contentPanel = wx.Panel(self, -1)
        _cp = self.contentPanel
        self.inputText =  wx.TextCtrl(_cp, -1, 
                                    style = wx.TE_MULTILINE|wx.HSCROLL)

        self.outputText =  wx.TextCtrl(_cp, -1, 
                                    style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        
        self.inputLabel = wx.StaticText(parent = _cp)
        self.inputLabel.SetLabel(label='Paste worklist here')
        
        self.outputLabel = wx.StaticText(parent = _cp)
        self.outputLabel.SetLabel(label='Log')

        self.genButton = wx.Button(_cp, ID_GENERATEFILES_BUTTON)
        self.genButton.SetLabel("Generate Files")
        self.genButton.Bind(wx.EVT_BUTTON, self.OnGenerate)

        self.clearButton = wx.Button(_cp, ID_CLEARINPUT_BUTTON)
        self.clearButton.SetLabel("Clear")
        self.clearButton.Bind(wx.EVT_BUTTON, self.OnClear)


        self.filectrl = filebrowse.DirBrowseButton(_cp, -1, size=(450, -1), changeCallback = None, labelText='Choose Dir', startDirectory = str('.') )
        #ctrl.SetValue(str(self.config.getValue(key)) )
        
        self.panelSizer = wx.BoxSizer(wx.VERTICAL)
       
        self.log = Log(self.outputText)
        wx.Log_SetActiveTarget(self.log)

        if wx.Platform == "__WXMAC__":
            self.inputText.MacCheckSpelling(False)
            self.outputText.MacCheckSpelling(False)




        _p = self.panelSizer
        #tsizer.Add(self.inputText, 1, flag=wx.ALL, border=2)
        _p.Add(self.inputLabel, 0, flag=wx.ALL, border=2) 
        _p.Add(self.inputText, 1, flag=wx.ALL|wx.GROW, border=2) 
        _p.Add(self.clearButton, 0, flag=wx.ALL, border=2)
        _p.Add(self.filectrl, 1, flag=wx.ALL|wx.GROW, border=2)
        _p.Add(self.genButton, 0, flag=wx.ALL, border=2)
        _p.Add(self.outputLabel, 0, flag=wx.ALL, border=2) 
        _p.Add(self.outputText, 1, flag=wx.ALL|wx.GROW, border=2)

        self.contentPanel.SetSizerAndFit(_p)
        self.panelSizer.Fit(self)

    def OnGenerate(self, event):
        self.log('Generate')
        lineslist = self.inputText.GetValue().splitlines()
        fileslist = []
        for line in lineslist:
            try:
                uname, srcdir, fname, methdir, methfile, sampname = line.split(',')
                fileslist.append(fname)
            except:
                pass
        print fileslist

        dlg = GeneratePopup(self.log, self, fileslist, self.filectrl.GetValue() )  
        dlg.ShowModal()
        dlg.Destroy()


    def OnClear(self, event):
        self.log('Clear')
        self.inputText.Clear()

class MSSimulatorApp(wx.PySimpleApp):
    def OnInit(self):
        self.win = MainWindow(None)
        self.win.Show(True)
        self.SetTopWindow(self.win)
        return True

m = MSSimulatorApp(None)
m.MainLoop()

