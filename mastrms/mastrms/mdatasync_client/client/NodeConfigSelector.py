import wx
import urllib2
try: import json as simplejson
except ImportError: import simplejson
import plogging
outlog = plogging.getLogger('client')

class NodeConfigSelector(wx.Panel):

    def __init__(self, parent, ID, log, nodes):

        wx.Panel.__init__(self, parent, ID) #, size=(400,400))#, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
        self.log = log
        self.parentApp = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        syncsizer = wx.BoxSizer(wx.HORIZONTAL, )
        config = self.parentApp.config
        self.syncHubLabel = wx.StaticText(self, -1, config.getFormalName('synchub'))
        self.syncHubString = wx.TextCtrl(self, -1, config.getValue('synchub') ) #, size=(300,-1) )
        self.SuccessImage =  wx.ArtProvider_GetBitmap(wx.ART_TICK_MARK, wx.ART_MESSAGE_BOX,(16,16))
        self.FailImage =  wx.ArtProvider_GetBitmap(wx.ART_CROSS_MARK, wx.ART_MESSAGE_BOX,(16,16))

        self.syncHubOKIcon = wx.StaticBitmap(self, -1, self.FailImage)

        #Refresh Button
        #rbtnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, 0, label = 'Refresh', style = wx.BU_EXACTFIT)
        btn.SetDefault()
        #rbtnsizer.AddButton(btn)
        btn.Bind(wx.EVT_BUTTON, self.refreshWebData)
        btn.Enable(True)
        self.RefreshButton = btn

        #bind the onSetFocus
        self.syncHubString.Bind(wx.EVT_SET_FOCUS, self.focusResetButton)

        self.sizer.Add(self.syncHubLabel, 0, wx.ALIGN_CENTER | wx.ALL, 1)
        #Prepare the syncsizer
        syncsizer.Add(btn, 1, wx.ALIGN_LEFT | wx.ALL, border=0)
        syncsizer.Add(self.syncHubString, 4, wx.EXPAND | wx.CENTER | wx.ALL, border=0)
        syncsizer.Add(self.syncHubOKIcon, 1, wx.ALIGN_LEFT | wx.ALL, border=0)


        syncsizer.Layout()

        #Add syncsizer to this frames sizer
        self.sizer.Add(syncsizer, 0, wx.ALIGN_LEFT | wx.ALL, 1)

        label = wx.StaticText(self, -1, "Client Config")
        self.sizer.Add(label, 0, wx.ALIGN_CENTER|wx.ALL, 1)

        self.tree = wx.TreeCtrl(self)
        self.nodes = nodes
        self.createTree()
        self.sizer.Add(self.tree, 2, wx.GROW|wx.ALIGN_LEFT|wx.ALL, 1)

        self.SetSizer(self.sizer)
        self.sizer.Layout()

        self.nodeconfigdict = {}

        #self.refreshWebData()
        #self.selectNode()

    def focusResetButton(self, *args):
        self.RefreshButton.SetDefault()


    def refreshWebData(self, *args):
        self.parentApp.config.setValue('synchub', self.syncHubString.Value )
        self.parentApp.config.save()
        j = self.getNodeNamesFromWeb()
        if j is not None:
            self.syncHubOKIcon.SetBitmap(self.SuccessImage)
        else:
            outlog.debug('Data was not available from the web.')
            self.syncHubOKIcon.SetBitmap(self.FailImage)

        self.setNodes(j)


    def selectNode(self):
        orgname = self.parentApp.config.getValue('organisation')
        sitename = self.parentApp.config.getValue('sitename')
        stationname = self.parentApp.config.getValue('stationname')
        root = self.tree.GetRootItem()

        def findnodebytext(node, text):
            child, cookie = self.tree.GetFirstChild(node)
            while child:
                if self.tree.GetItemText(child) == text:
                    return child
                child, cookie = self.tree.GetNextChild(node, cookie)
            return None

        station = None
        org = findnodebytext(root, orgname)
        if org is not None:
            site = findnodebytext(org, sitename)
            if site is not None:
                station = findnodebytext(site, stationname)

        if station is not None:
            self.tree.Expand(station)
            self.tree.SelectItem(station)



    def getNodeNamesFromWeb(self):
        #get the data
        retval = None
        try:
            req = urllib2.Request(self.parentApp.config.getValue('synchub') + 'nodes/')
            f = urllib2.urlopen(req, None, 1) #one second timeout
            jsonret = f.read()
            outlog.debug('node config: %s' % jsonret  )
            retval = simplejson.loads(jsonret)
            assert isinstance(retval, dict), 'Returned json was not a dict'
            outlog.debug( 'node config loaded object is: %s' % (retval) )
        except Exception, e:
            outlog.warning( 'Error retrieving node config data: %s' % (str(e)) )
            retval = None

        return retval


    def createTree(self):
        '''creates the actual tree control from the 'nodes' class variable.
           call this function any time you change the 'nodes' variable to reinit
           the tree'''
        #draw the tree control
        if self.tree is not None:
            #cleanup
            outlog.info('removing tree')
            #self.sizer.Remove(self.tree)
            self.tree.DeleteAllItems()

        if self.nodes is None:
            root = self.tree.AddRoot("No data available")
        else:
            root = self.tree.AddRoot("Nodes")
            items = self.nodes
            self.AddTreeNodes(root, items)

        #bind the events to functions.
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated, self.tree)
        self.tree.Expand(root)



    def setNodes(self, nodes):
        self.nodes = nodes
        self.createTree()

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
        outlog.info( "OnItemExpanded: %s" % (self.GetItemText(evt.GetItem()) ) )
        self.Layout()

    def OnItemCollapsed(self, evt):
        outlog.info( "OnItemCollapsed: %s" % (self.GetItemText(evt.GetItem()) ) )
    #
    def OnSelChanged(self, evt):
        item = evt.GetItem()
        if self.tree.GetChildrenCount(item) == 0:
            self.getNodeConfigName(item) #get into the nodeconfigdict
            self.parentApp.setNodeConfigName(self.nodeconfigdict)
            #print self.getNodeConfigName(item)

        outlog.info( "OnSelChanged: %s" % (self.GetItemText(evt.GetItem()) ) )

    #
    def OnActivated(self, evt):
        outlog.info( "OnActivated: %s" % (self.GetItemText(evt.GetItem()) ) )


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
                    outlog.debug('item wasnt a string.: %s' % str(item))
                    newItem = self.tree.AppendItem(parentItem, str(item))
                    #self.AddTreeNodes(newItem, str(item[0]))




