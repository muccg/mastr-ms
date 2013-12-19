MA.FilesInit = function() {
    var expId = MA.ExperimentController.currentId();

    //reload trees
    Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());

    Ext.getCmp('uploadExperimentId').setValue(expId);
};

MA.Files = {
    baseCls: 'x-plain',
    border:'false',
    layout:'fit',
    items: [{
       title: 'Files',
       //       bodyStyle:'padding:0px;background:transparent;',
       collapsible: false,
       layout:'border',
       tbar: {
           items: [
               { xtype:'tbtext', text:'Checkmarks indicate files that are visible to clients' }
           ]
       },
       bbar: {
           items: [{
               xtype:'form',
               id:'pendingFileUpload',
               fileUpload:true,
               method:'POST',
               width:200,
               height:30,
               border:false,
               bodyStyle:'background:transparent;padding:4px;',
               url:wsBaseUrl + 'uploadFile',
               labelWidth: 120,
               items: [
               {
                   hideLabel:true,
                   xtype: 'fileuploadfield',
                   emptyText: '',
                   fieldLabel: 'File',
                   name: 'attachfile'
               },
               {
                   xtype:'hidden',
                   id:'uploadExperimentId',
                   name:'experimentId'
               },
               {
                   xtype:'hidden',
                   id:'uploadParentNodeId',
                   name:'parentId'
               },
               {
                   xtype: 'hidden',
                   name: 'csrfmiddlewaretoken',
                   value: Ext.util.Cookies.get("csrftoken_mastrms")
               }]
           },{
               text: 'Upload',
               id:'upload file',
               handler: function(){
                 var form = Ext.getCmp('pendingFileUpload').getForm();
                 var tree = Ext.getCmp('filesTree');
                 var nodes = tree.getSelectionModel().getSelectedNodes();
                 var parentId = nodes.length > 0 ? nodes[0].id : "";

                 if (parentId == tree.getRootNode().id) {
                   parentId = "";
                 }

                 // set the destination to be the selected folder
                 Ext.getCmp("uploadParentNodeId").setValue(parentId);
                 Ext.getCmp("uploadExperimentId").setValue(MA.ExperimentController.currentId());

                   form.submit(
                   {   successProperty: 'success',
                       success: function (form, action) {
                           if (action.result.success === true) {
                               form.reset();

                               //reload the pending files tree
                               Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                               Ext.getCmp('filesTree').getRootNode().expand();

                           }
                       },
                       failure: function (form, action, response) {
                         console.log("action", action);
                         console.log("response", response);
                           //do nothing special. this gets called on validation failures and server errors
                           alert('error submitting form\n' + response.msg);
                       }
                   });
               }
           }, { xtype: "tbseparator" },
           {
               text: 'New Folder...',
               id:'new folder',
               handler: function(){
                 var tree = Ext.getCmp('filesTree');
                 var nodes = tree.getSelectionModel().getSelectedNodes();
                 var node = null;

                 if (nodes.length == 0) {
                   node = tree.getRootNode();
                 } else if (nodes.length > 1) {
                   Ext.Msg.alert("Please select just one folder.",
                                 "(this message will auto-close in 2 seconds)");
                   window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                   return;
                 } else {
                   node = nodes[0];
                 }

                 var msg = "";

                 if (node.id != tree.getRootNode().id) {
                   msg = "Folder will be created under:<br/>" + node.id + "<br/>";
                 }
                 msg += "Please choose a name:";
                 Ext.Msg.prompt("Folder Name", msg, function(btn, text){
                   if (btn == 'ok' && text.length > 0) {
                     Ext.Ajax.request({
                       method:'POST',
                       url: wsBaseUrl + 'newFolder',
                       success: function(response) {
                         var result = Ext.util.JSON.decode(response.responseText);
                         if (result.success) {
                           Ext.Msg.alert("Folder Created", "(this message will auto-close in 1 second)");
                           window.setTimeout(function() {Ext.Msg.hide();}, 1000);
                         } else {
                           Ext.Msg.alert("Could not create the folder here",
                                         "(this message will auto-close in 2 seconds)");
                           window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                         }

                         //reload the pending files tree
                         tree.getLoader().clearOnLoad = true;
                         tree.getLoader().load(Ext.getCmp('filesTree').getRootNode());
                         tree.getRootNode().expand();
                       },
                       failure: function() {
                         Ext.Msg.alert("Fail", "Could not create the folder.");
                       },
                       params: {
                         parent: node.id === tree.getRootNode().id ? '' : node.id,
                         name: text,
                         experiment_id: MA.ExperimentController.currentId(),
                         csrfmiddlewaretoken: Ext.util.Cookies.get("csrftoken_mastrms")
                       }
                     });
                   }
               });

               }
           }, {
               text: 'Delete',
               id:'delete',
               handler: function(){
                 var tree = Ext.getCmp('filesTree');
                 var nodes = tree.getSelectionModel().getSelectedNodes();
                 var node = null;

                 if (nodes.length == 0) {
                   node = tree.getRootNode();
                 } else if (nodes.length > 1) {
                   Ext.Msg.alert("Please select just one item.",
                                 "(this message will auto-close in 2 seconds)");
                   window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                   return;
                 } else {
                   node = nodes[0];
                 }

                 var name = node.id == tree.getRootNode() ? "Experiment" : node.id;

                 if (node.id == tree.getRootNode().id || node.childNodes.length > 0) {
                   Ext.Msg.alert("Folder " + name + " is not empty.",
                                 "(this message will auto-close in 2 seconds)");
                   window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                   return;
                 }

                 Ext.Msg.show({
                   title: "Are you sure?",
                   msg: "Really delete " + name + "?",
                   buttons: Ext.Msg.YESNO,
                   icon: Ext.MessageBox.QUESTION,
                   fn: function(btn) {
                     if (btn == 'yes') {
                       Ext.Ajax.request({
                         method:'POST',
                         url: wsBaseUrl + 'deleteFile',
                         success: function() {
                           Ext.Msg.alert("Deleted " + name, "(this message will auto-close in 1 second)");
                           window.setTimeout(function() {Ext.Msg.hide();}, 1000);

                           //reload the pending files tree
                           tree.getLoader().clearOnLoad = true;
                           tree.getLoader().load(Ext.getCmp('filesTree').getRootNode());
                           tree.getRootNode().expand();
                         },
                         failure: function() {
                           Ext.Msg.alert("Fail", "Could not delete " + name + ".");
                         },
                         params: {
                           target: node.id,
                           csrfmiddlewaretoken: Ext.util.Cookies.get("csrftoken_mastrms"),
                           experiment_id: MA.ExperimentController.currentId()
                         }
                       });
                     }
                   }
                 });
               }
           }, {
               text: 'Rename',
               id:'rename',
               handler: function(){
                 var tree = Ext.getCmp('filesTree');
                 var nodes = tree.getSelectionModel().getSelectedNodes();
                 var node = null;

                 if (nodes.length === 0 || nodes.length > 1) {
                   Ext.Msg.alert("Please select just one item.",
                                 "(this message will auto-close in 2 seconds)");
                   window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                   return;
                 } else {
                   node = nodes[0];
                 }

                 if (node.id === tree.getRootNode() ||
                     node.id === "Raw Data" ||
                     node.id === "QC Data") {
                   Ext.Msg.alert("Can't rename this folder.",
                                 "(this message will auto-close in 2 seconds)");
                   window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                   return;
                 }

                 var pieces = node.id.split("/")
                 var path = "", name = node.id;

                 if (pieces.length >= 2) {
                   path = pieces.slice(0, -1).join("/") + "/";
                   name = pieces[pieces.length - 1];
                 } else {
                   path = ""
                   name = node.id;
                 }

                 Ext.Msg.show({
                   title: "Rename",
                   msg: "Please enter a new filename.",
                   value: name,
                   prompt: true,
                   buttons: Ext.MessageBox.OKCANCEL,
                   icon: Ext.MessageBox.QUESTION,
                   fn: function(btn, text) {
                     if (btn == 'ok' && text.length > 0) {
                       Ext.Ajax.request({
                         method:'POST',
                         url: wsBaseUrl + 'moveFile',
                         success: function(response) {
                           var result = Ext.util.JSON.decode(response.responseText);
                           if (result.success) {
                             Ext.Msg.alert("Renamed", "(this message will auto-close in 1 second)");
                             window.setTimeout(function() {Ext.Msg.hide();}, 1000);
                           } else {
                             Ext.Msg.alert("Could not rename the file",
                                           "(this message will auto-close in 2 seconds)");
                             window.setTimeout(function() {Ext.Msg.hide();}, 2000);
                           }

                           //reload the pending files tree
                           tree.getLoader().clearOnLoad = true;
                           tree.getLoader().load(Ext.getCmp('filesTree').getRootNode());
                           tree.getRootNode().expand();
                         },
                         failure: function() {
                           Ext.Msg.alert("Fail", "Could not rename the file.");
                         },
                         params: {
                           file: node.id === tree.getRootNode().id ? '' : node.id,
                           target: path + text,
                           rename: true,
                           experiment_id: MA.ExperimentController.currentId(),
                           csrfmiddlewaretoken: Ext.util.Cookies.get("csrftoken_mastrms")
                         }
                       });
                     }
                   }
                 });
               }
           }, { xtype: "tbseparator" },{
               text: 'Download ',
               handler: function(){
                    var tree = Ext.getCmp('filesTree');
                    var checkedNodes = tree.getChecked();
                    var filesToDownload;
                    if (checkedNodes.length === 1 && !checkedNodes[0].attributes.metafile) {
                        node = checkedNodes[0];
                        window.location = wsBaseUrl + 'downloadFile?file=' + node.id + '&experiment_id=' + MA.ExperimentController.currentId();
                    } else {
                        filesToDownload = []
                        for (var i = 0; i < checkedNodes.length; i++) {
                            node = checkedNodes[i];
                            filesToDownload.push(node.attributes.id);
                        }
                        Ext.Ajax.request({
                            url: wsBaseUrl + 'packageFilesForDownload',
                            method: 'POST',
                            params: {
                                'experiment_id': MA.ExperimentController.currentId(),
                                'files': filesToDownload.join(","),
                                'package_type': Ext.getCmp('downloadPackageTypeCmb').getValue()
                            },
                            success: function(response, opts) {
                                var jsonData = Ext.util.JSON.decode(response.responseText);
                                var packageName = jsonData.package_name;
                                window.location = wsBaseUrl + 'downloadPackage?packageName=' + packageName;
                            }
                        });
                    }
               }
           }, {
                xtype: 'combo',
                id: 'downloadPackageTypeCmb',
                fieldLabel: 'Package type',
                store: new Ext.data.ArrayStore({
                    fields: ['ext', 'description'],
                    data : [
                        ['tgz', '.tgz'],
                        ['tbz2', '.tbz2'],
                        ['zip', '.zip'],
                        ['tar', '.tar']
                    ]
                }),
                displayField:'description',
                valueField:'ext',
                lazyRender:true,
                triggerAction:'all',
                editable: false,
                width: 80,
                listWidth: 80,
                mode: 'local',
                forceSelection: true
           }]
       },
       items: [
               {
               xtype:'treepanel',
               border: false,
               autoScroll: true,
               id:'filesTree',
               animate: true,
               region:'center',
               enableDrop:true,
               enableDD: true,
               useArrows: true,
               dropConfig: { appendOnly: true },
               dataUrl:wsBaseUrl + 'files',
               requestMethod:'GET',
               root: {
                   nodeType: 'async',
                   text: 'Experiment',
                   draggable: false,
                   id: 'experimentRoot',
                   'metafile': true
               },
               selModel: new Ext.tree.MultiSelectionModel(),
               listeners:{
                   render: function() {
                        Ext.getCmp('filesTree').getLoader().on("beforeload", function(treeLoader, node) {
                            treeLoader.baseParams.experiment = MA.ExperimentController.currentId();
                            }, this);
                        //Ext.getCmp('filesTree').getRootNode().expand();
                    },
                   nodedrop: function(de) {
                        Ext.Ajax.request({
                                         method:'POST',
                                    url: wsBaseUrl + 'moveFile',
                                         success: function() { Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                                         Ext.getCmp('filesTree').getRootNode().expand(); },
                                         failure: function() { Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                                         Ext.getCmp('filesTree').getRootNode().expand(); },
                                    headers: {
    //                                'my-header': 'foo'
                                    },
                                         params: { file: de.dropNode.id, target: de.target.id, experiment_id: MA.ExperimentController.currentId() }
                                    });
                   },
                   checkchange: function(node, checked){
                     Ext.Ajax.request({
                       method:'POST',
                       url: wsBaseUrl + 'shareFile',
                       success: function() {  },
                       failure: function() {  },
                       params: { file: node.id, checked: checked, experiment_id: MA.ExperimentController.currentId() }
                     });
                   }
                }
               }


               ]
       }
       ]
};
