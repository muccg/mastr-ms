MA.ExperimentListCmp = {
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
                MA.MenuHandler({'id':'experiment:new'});
            }
        },
        {
        text: 'remove experiment',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/no.gif',
        handler: function(){
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
           for (var i = 0; i < delIds.length; i++) {
               MA.CRUDSomething('delete/experiment/'+delIds[i], {}, function() { experimentListStore.load(); });
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
                      { header: "id", sortable:false, menuDisabled:true, dataIndex:'id', width:50 },
                { header: "title", sortable:false, menuDisabled:true, dataIndex:'title' },
                      { header: "Principal", sortable:false, menuDisabled:true, dataIndex:'principal' },
                      { header: "Client", sortable:false, menuDisabled:true, dataIndex:'client' },
                { header: "description", sortable:false, menuDisabled:true, width:300, dataIndex:'description' },
                { header: "status", sortable:false, menuDisabled:true, renderer:renderStatus, dataIndex:'status' }
            ],
            store: experimentListStore,
            listeners: {
                'rowdblclick':function(el, ev) {
                    var sm = Ext.getCmp('experiments').getSelectionModel();
                    var rec = sm.getSelected();
                    MA.LoadExperiment(rec.data.id);
                }
            }
        }
    ]
};
