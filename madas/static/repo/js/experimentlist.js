Ext.madasExperimentListCmp = {
    title: 'experiments',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
id:'experiment-list',
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [{
        text: 'new experiment',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/add.gif',
        handler : function(){
                Ext.madasMenuHandler({'id':'experiment:new'});
            }
        },
        {
        text: 'remove experiment',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/no.gif',
        handler : function(){
           var grid = Ext.getCmp('experiments');
           var delIds = []; 
           
           var selections = grid.getSelectionModel().getSelections();
           if (!Ext.isArray(selections)) {
           selections = [selections];
           }
           
           for (var index = 0; index < selections.length; index++) {
           if (!Ext.isObject(selections[index])) {
           continue;
           }
           
           delIds.push(selections[index].data.id);
           }
           //console.log(delIds);
           for (var i = 0; i < delIds.length; i++) {
               Ext.madasCRUDSomething('delete/experiment/'+delIds[i], {}, function() { experimentListStore.load(); });
           }                        
           }
           
        }
    ],
    items: [
        {
            xtype:'grid',
            border: false,
            id:'experiments',
            trackMouseOver: false,
            sm: new Ext.grid.RowSelectionModel( {singleSelect:true}),
            viewConfig: {
                forceFit: true,
                autoFill:true
            },
            columns: [
                { header: "id", sortable:false, menuDisabled:true, dataIndex:'id' },
                { header: "title", sortable:false, menuDisabled:true, dataIndex:'title' },
                { header: "description", sortable:false, menuDisabled:true, width:300, dataIndex:'description' },
                { header: "status", sortable:false, menuDisabled:true, renderer:renderStatus, dataIndex:'status' }
            ],
            store: experimentListStore,
            listeners: {
                'rowdblclick':function(el, ev) {
                    var sm = Ext.getCmp('experiments').getSelectionModel();
                    var rec = sm.getSelected();
                    Ext.madasLoadExperiment(rec.data.id);
                }
            }
        }
    ]
};
