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
               }
               ]
           },{
               text: 'Upload',
               id:'upload file',
               handler: function(){
                   Ext.getCmp('pendingFileUpload').getForm().submit(
                   {   successProperty: 'success',        
                       success: function (form, action) {
                           if (action.result.success === true) {
                               form.reset(); 
                               
                               //reload the pending files tree
                               Ext.getCmp('filesTree').getLoader().load(Ext.getCmp('filesTree').getRootNode());
                               Ext.getCmp('filesTree').getRootNode().expand();
                               
                           } 
                       },
                       failure: function (form, action) {
                           //do nothing special. this gets called on validation failures and server errors
                           alert('error submitting form\n' + action.response );
                       }
                   });
               }
           }, { xtype: "tbseparator" },{
               text: 'Download ',
               handler: function(){
                    var tree = Ext.getCmp('filesTree');
                    var selModel = tree.getSelectionModel();
                    var selectedNodes = selModel.getSelectedNodes();
                    var node;
                    var filesToDownload;
                    if (selectedNodes.length === 1 && !selectedNodes[0].attributes.metafile) {
                        node = selectedNodes[0];
                        window.location = wsBaseUrl + 'downloadFile?file=' + node.id + '&experiment_id=' + MA.ExperimentController.currentId();
                    } else {
                        filesToDownload = []
                        for (var i = 0; i < selectedNodes.length; i++) {
                            node = selectedNodes[i];
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
                                         method:'GET',
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
