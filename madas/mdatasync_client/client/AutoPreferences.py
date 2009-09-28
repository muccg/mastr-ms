import wx
import urllib
import simplejson
import NodeConfigSelector

from identifiers import *

class AutoPreferences(wx.Dialog):
    def __init__(self, parent, ID, config, log):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, 'Preferences', wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
        pre.width = 400
        #Turn the object into a proper dialog wrapper.
        self.PostCreate(pre)

        
        self.log = log
        self.parentApp = parent
        self.config = config

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "DataSync Preferences")
        label.SetHelpText("Preference settings for the DataSync application")
        sizer.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 5)



        #get the data
        f = urllib.urlopen(self.config.getValue('synchub') + 'nodes/')
        jsonret = f.read()
        print 'node config: %s' % jsonret 
        j = simplejson.loads(jsonret)
        print 'node config loaded object is: %s' % j 

        #node chooser
        self.nodeconfigselector = NodeConfigSelector.NodeConfigSelector(self, ID_NODESELECTOR_DIALOG, self.log, j) 

        k = self.config.getConfig().keys()
        k.sort()
        
        #report current node config name, and give button to choose
        box = wx.BoxSizer(wx.HORIZONTAL)
        configname = "%s.%s.%s" % (self.config.getValue('organisation'), self.config.getValue('sitename'), self.config.getValue('stationname') )
        label = wx.StaticText(self, -1, "Node is currently %s" % (configname) ) 
        box.Add(label, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        btn = wx.Button(self, ID_CHOOSENODE_BUTTON)
        btn.SetLabel("Choose")
        btn.Bind(wx.EVT_BUTTON, self.openNodeChooser)
        box.Add(btn, 0,  wx.ALIGN_RIGHT|wx.ALL, 5)

        
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        self.fields = {}
        for key in k:
            if self.config.getShowVar(key):
                box = wx.BoxSizer(wx.HORIZONTAL)
                label = wx.StaticText(self, -1, self.config.getFormalName(key))
                label.SetHelpText(self.config.getHelpText(key))
                box.Add(label, 0, wx.ALIGN_LEFT|wx.ALL, 5)
                #the text entry field
                text = wx.TextCtrl(self, -1, str(self.config.getValue(key)), size=(80,-1))
                text.SetHelpText(self.config.getHelpText(key))
                box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
                sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
                
                #store the field so we can serialise it later
                self.fields[key] = text

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn.Bind(wx.EVT_BUTTON, self.save)


        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("Cancel changes")
        btnsizer.AddButton(btn)
        btnsizer.Realize()



        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        #self.SetAutoLayout(True)
        self.SetSizer(sizer)
        #sizer.Layout()
        sizer.Fit(self)
        #self.Layout()

    def save(self, *args):
        k = self.config.getConfig().keys()
        for key in k:
            if self.config.getShowVar(key): #if this is var shown on this dialog (not in the tree)
                print 'Setting config at %s to %s' % (str(key), self.fields[key].GetValue())
                self.config.setValue(key, self.fields[key].GetValue())

        #call the method that will serialise the config.
        self.config.save()
        self.parentApp.resetTimeTillNextSync()
       
    def openNodeChooser(self, *args):
        self.nodeconfigselector.ShowModal()
        self.nodeconfigselector.Destroy()
