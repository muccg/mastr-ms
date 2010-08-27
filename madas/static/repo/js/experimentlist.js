MA.ExperimentListCmp = {
    title: 'Experiments',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'experiment-list',
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [{
        text: 'New Experiment',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/add.png',
        handler : function(){
                MA.MenuHandler({'id':'experiment:new'});
            }
        },
        {
        text: 'Remove Experiment',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/delete.png',
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
            view: new Ext.grid.GroupingView({
                forceFit: true,
                autoFill: true,
                hideGroupedColumn: true
            }),
            columns: [
                      { header: "ID", sortable:false, menuDisabled:true, dataIndex:'id', width:50 },
                { header: "Title", sortable:false, menuDisabled:true, dataIndex:'title' },
                      { header: "Principal", sortable:false, menuDisabled:true, dataIndex:'principal' },
                      { header: "Client", sortable:false, menuDisabled:true, dataIndex:'client' },
                { header: "Description", sortable:false, menuDisabled:true, width:300, dataIndex:'description' },
                { header: "Status", sortable:false, groupable:true, menuDisabled:true, renderer:renderStatus, dataIndex:'status' }
            ],
            store: experimentListStore,
            listeners: {
                'rowdblclick':function(el, ev) {
                    var sm = Ext.getCmp('experiments').getSelectionModel();
                    var rec = sm.getSelected();
                    MA.ExperimentController.loadExperiment(rec.data.id);
                }
            }
        }
    ]
};
