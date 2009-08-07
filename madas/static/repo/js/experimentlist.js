Ext.madasExperimentListCmp = {
    title: 'experiments',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [{
        text: 'new experiment',
        cls: 'x-btn-text-icon',
        icon:'images/add.gif',
        handler : function(){
                Ext.madasMenuHandler({'id':'experiment:new'});
            }
        },
        {
        text: 'remove experiment',
        cls: 'x-btn-text-icon',
        icon:'images/no.gif',
        handler : function(){
            //TODO delete hook
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
                { header: "progress", sortable:false, menuDisabled:true, renderer:renderProgress, dataIndex:'progress' }
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
