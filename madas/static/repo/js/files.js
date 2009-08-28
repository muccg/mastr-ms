Ext.madasFilesInit = function() {
    var expId = Ext.madasCurrentExperimentId();

    //reload tree TODO
}

Ext.madasFiles = {
baseCls: 'x-plain',
border:'false',
layout:'border',
defaults: {
bodyStyle:'padding:15px;background:transparent;'
},
items:[
       {
       title: 'files',
       region: 'center',
       bodyStyle:'padding:0px;background:transparent;',
       collapsible: false,
       layout:'fit',
       items: [
               {
               xtype:'treepanel',
               border: false,
               id:'filesTree',
               enableDD: true,
               animate: true,
               useArrows: true,
               dataUrl:wsBaseUrl + 'files/experiment_id/5',
               root: {
                   nodeType: 'async',
                   text: 'experiment',
                   draggable: false,
                   id: 'source'
               },
               tbar: [{
                      text: 'add files',
                      cls: 'x-btn-text-icon',
                      icon:'static/repo/images/add.gif',
                      handler : function(){
//                      userStore.add(new Ext.data.Record({'user':'', 'type':'1', 'additional_info':''}));
                      }
                      }
                ]
               }
               ]
       }
       ]
};
