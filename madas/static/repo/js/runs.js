//run.js needs to manage a few things
//the list of runs
//the current run being manipulated
//the current samples in the run being manipulated

MA.CurrentRun = {};


MA.RunCmpRowSelect = function(view, nodes) {
	var detailPanel = Ext.getCmp('runDetails');
    	
    if (nodes.length == 0) {
        detailPanel.disable();
        detailPanel.getComponent('title').setValue('');
    } else {
        detailPanel.enable();
        var r = view.getSelectedRecords()[0];
    	console.log(r);
        
        detailPanel.getComponent('title').setValue(r.data.title);
    }
};

MA.RunCmp = new Ext.Window({
    id:'runCmp',
    title:'Current Run',
    width:680,
    height:600,
    x:170,
    y:50,
    closeAction:'hide',
    layout:'border',
    items:[
    
        {
            xtype:'listview',
            region:'west',
            width:150,
            store:runStore,
            columns: [
	            {header: "Select a Run", dataIndex: 'title', sortable: true}
            ],
            listeners:{
                'selectionchange':MA.RunCmpRowSelect
            },
            viewConfig:{
                forceFit:true
            },
            singleSelect:true,
            multiSelect:false,
            style:'background:white;',
            autoScroll:true,
            reserveScrollOffset:true
        },
        {
            id:'runDetails',
            region:'center',
            layout:'form',
            disabled:true,
            bodyStyle:'padding:20px;',
            items:[
                {
                    fieldLabel:'title',
                    xtype:'textfield',
                    itemId:'title'
                },
                {
                    fieldLabel:'method',
                    xtype:'textfield',
                    itemId:'method'
                },
                {
                    fieldLabel:'machine',
                    xtype:'textfield',
                    itemId:'machine'
                }
            ]
        }
    
    ]
});