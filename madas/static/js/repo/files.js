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
defaults: {
    //bodyStyle:'padding:15px;background:transparent;'
},
items:[
       {
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
           items: [
           {
               xtype:'form',
               id:'pendingFileUpload',
               fileUpload:true,
               method:'POST',
               width:200,
               height:30,
               border:false,
               bodyStyle:'background:transparent;padding:4px;',
               url:wsBaseUrl + 'uploadFile',
               items: [
               {
                   hideLabel:true,
                   xtype: 'fileuploadfield',
                   id: 'quo-attach',
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
           }, 
           {
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
           }

           ]
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
               selModel: new Ext.tree.DefaultSelectionModel(
                   { listeners:
                       {
                           selectionchange: function(sm, node) {
                               if (node != null && !node.attributes.metafile) {
                                   window.location = wsBaseUrl + 'downloadFile?file=' + node.id + '&experiment_id=' + MA.ExperimentController.currentId();
                               }
                           }
                       }
                   }),
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
