import wx

class AutoPreferences(wx.Dialog):
    def __init__(self, parent, ID, config, log):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, 'Preferences', wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_DIALOG_STYLE)
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
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        k = self.config.getConfig().keys()
        k.sort()
        self.fields = {}
        for key in k:
            box = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, -1, self.config.getFormalName(key))
            label.SetHelpText(self.config.getHelpText(key))
            box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
            #the text entry field
            text = wx.TextCtrl(self, -1, self.config.getValue(key), size=(80,-1))
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

        self.SetSizer(sizer)
        sizer.Fit(self)

    def save(self, *args):
        k = self.config.getConfig().keys()
        for key in k:
            print 'Setting config at %s to %s' % (str(key), self.fields[key].GetValue())
            self.config.setValue(key, self.fields[key].GetValue())

        #call the method that will serialise the config.
        self.config.save()
   




            

        
