import wx
import os
import os.path
import plogging
import wx.lib.filebrowsebutton as filebrowse
from config import *

outlog = plogging.getLogger('client')

class AdvancedPreferences(wx.Dialog):
    def __init__(self, parent, ID, config, log):
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, 'Advanced Preferences', wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
        pre.width = 400
        #Turn the object into a proper dialog wrapper.
        self.PostCreate(pre)
        
        self.log = log
        self.parentApp = parent
        self.config = config

        self.preference_keys = ['syncold', 'archivesynced', 'archivedfilesdir']
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.fields = {}

        #Sync Old:
        for key in self.preference_keys:
            if self.config.getShowVar(key):
                box = wx.BoxSizer(wx.HORIZONTAL)
                if key == 'syncold':
                    ctrl = wx.CheckBox(self, -1, "Re-sync completed experiment files. (If available)")
                    self.Bind(wx.EVT_CHECKBOX, self.toggleSyncChoose, ctrl)
                    #populate the checkbox with the current value
                    val = self.config.getValue(key)
                    if val:
                        ctrl.SetValue(wx.CHK_CHECKED)
                    else:
                        ctrl.SetValue(wx.CHK_UNCHECKED)
                    ctrl.SetHelpText(self.config.getHelpText(key))    
                    box.Add(ctrl, 1, wx.ALIGN_RIGHT|wx.ALL, border=INTERNAL_BORDER_WIDTH)
                elif key == 'archivedfilesdir':
                    ctrl = filebrowse.DirBrowseButton(self, -1, size=(450, -1), changeCallback = None, labelText=self.config.getFormalName(key), startDirectory = str(self.config.getValue(key)) )
                    ctrl.SetValue(str(self.config.getValue(key)) )
                    ctrl.SetHelpText(self.config.getHelpText(key))
                    box.Add(ctrl, 1, wx.ALIGN_RIGHT|wx.ALL, border=INTERNAL_BORDER_WIDTH)
                elif key == 'archivesynced':
                    ctrl = wx.CheckBox(self, -1, self.config.getFormalName(key))
                    self.Bind(wx.EVT_CHECKBOX, self.toggleArchiveChoose, ctrl)
                    #populate the checkbox with the current value
                    val = self.config.getValue(key)
                    if val:
                        ctrl.SetValue(wx.CHK_CHECKED)
                    else:
                        ctrl.SetValue(wx.CHK_UNCHECKED)
                    ctrl.SetHelpText(self.config.getHelpText(key))    
                    box.Add(ctrl, 1, wx.ALIGN_RIGHT|wx.ALL, border=INTERNAL_BORDER_WIDTH) 


            sizer.Add(box, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=EXTERNAL_BORDER_WIDTH)
            self.fields[key] = ctrl

        self.updateArchivedControls()

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn.Bind(wx.EVT_BUTTON, self.OKPressed)
        
        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("Cancel changes")
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        sizer.Add(btnsizer, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL, border=EXTERNAL_BORDER_WIDTH)

        self.SetSizer(sizer)
        sizer.Fit(self)


    def toggleSyncChoose(self, event):
        currentvalue = self.config.getValue('syncold')
        self.config.setValue('syncold', not currentvalue)

    def toggleArchiveChoose(self, event):
        currentvalue = self.config.getValue('archivesynced')
        self.config.setValue('archivesynced', not currentvalue)
        self.updateArchivedControls()

    def updateArchivedControls(self):
        dirctrl = self.fields['archivedfilesdir']
        if self.config.getValue('archivesynced'):
            dirctrl.Enable()
        else:
            dirctrl.Disable()
    

    def OKPressed(self, *args):
        self.save(args)
        self.EndModal(0)

    def save(self, *args):
        #k = self.config.getConfig().keys()
        for key in self.preference_keys:
            if self.config.getShowVar(key): #if this is var shown on this dialog (not in the tree)
                outlog.debug('Setting config at %s to %s' % (str(key), self.fields[key].GetValue()) )
                self.config.setValue(key, self.fields[key].GetValue())

        #call the method that will serialise the config.
        self.config.save()


        

    
