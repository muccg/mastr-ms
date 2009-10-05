import wx

class NodeConfigSelector(wx.Dialog):

    def __init__(self, parent, ID, log, nodes):

        wx.Dialog.__init__(self, parent, ID, "Node Locator", size=(400,400))#, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
        self.log = log
        self.parentApp = parent

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "Locate your client")
        sizer.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        #draw the tree control
        self.tree = wx.TreeCtrl(self)
        root = self.tree.AddRoot("Nodes")
        items = nodes 
        self.AddTreeNodes(root, items)
        sizer.Add(self.tree, 2, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 5)

        
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)
        self.tree.Expand(root)


        #BUTTONS
        btnsizer = wx.StdDialogButtonSizer()

        #OK Button
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn.Bind(wx.EVT_BUTTON, self.OnOKClicked)
        btn.Enable(False)
        self.OKButton = btn

        #Cancel Button
        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("Cancel changes")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Layout()

        self.nodeconfigdict = {}

    def OnOKClicked(self, *args):
        self.parentApp.setNodeConfigName(self.nodeconfigdict)
        self.EndModal(0)

    def GetItemText(self, item):
        if item:
            return self.tree.GetItemText(item)
        else:
            return ""   

    #once you are sure you have a leaf node, use this function to get 
    #the stationname, sitename, and organisation name
    def getNodeConfigName(self, item):
        
        self.nodeconfigdict['stationname'] = self.GetItemText(item)
        p = self.tree.GetItemParent(item)
        self.nodeconfigdict['sitename'] = self.GetItemText(p)
        p = self.tree.GetItemParent(p)
        self.nodeconfigdict['organisation'] = self.GetItemText(p)
        return self.nodeconfigdict
        

    def OnItemExpanded(self, evt):
        print "OnItemExpanded: ", self.GetItemText(evt.GetItem() )
        self.Layout()

    def OnItemCollapsed(self, evt):
        print "OnItemCollapsed: ", self.GetItemText(evt.GetItem() )
    #
    def OnSelChanged(self, evt):
        item = evt.GetItem()
        if self.tree.GetChildrenCount(item) == 0:
            print self.getNodeConfigName(item)
            self.OKButton.Enable(True)

        else:
            self.OKButton.Enable(False)
        print "OnSelChanged: ", self.GetItemText(evt.GetItem())

    #
    def OnActivated(self, evt):
        print "OnActivated: ", self.GetItemText(evt.GetItem()) 

   
    def AddTreeNodes(self, parentItem, items):
        if type(items) == dict:
            for key in items.keys(): #assuming keys are strings
                new = self.tree.AppendItem(parentItem, key)
                self.AddTreeNodes(new, items[key])

        else:
            for item in items:
                if type(item) == str:
                    self.tree.AppendItem(parentItem, item)
                else:
                    newItem = self.tree.AppendItem(parentItem, item[0])
                    self.AddTreeNodes(newItem, item[0])
            


    
