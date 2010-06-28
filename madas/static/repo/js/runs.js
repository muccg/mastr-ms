//run.js needs to manage a few things
//the list of runs
//the current run being manipulated
//the current samples in the run being manipulated

MA.CurrentRun = {
    
};

MA.CreateNewRun = function() {
	var detailPanel = Ext.getCmp('runDetails');

    detailPanel.getComponent('id').setValue(0);
    detailPanel.getComponent('title').setValue('New Untitled Run');
    detailPanel.getComponent('method').clearValue();
    detailPanel.getComponent('machine').clearValue();
};

MA.RunCmpRowSelect = function(view, nodes) {
	var detailPanel = Ext.getCmp('runDetails');
    	
    if (nodes.length == 0) {
        detailPanel.getComponent('id').setValue(0);
        detailPanel.getComponent('title').clearValue();
        detailPanel.getComponent('method').clearValue();
        detailPanel.getComponent('machine').clearValue();
        
        MA.CurrentRun.id = 0;
        MA.CurrentRun.title = 'New Untitled Run';
    } else {
        var r = view.getSelectedRecords()[0];
        
        detailPanel.getComponent('id').setValue(r.data.id);
        detailPanel.getComponent('title').setValue(r.data.title);
        detailPanel.getComponent('method').setValue(r.data.method);
        detailPanel.getComponent('machine').setValue(r.data.machine);
        
        MA.CurrentRun.id = r.data.id;
        MA.CurrentRun.title = r.data.title;
        MA.CurrentRun.machine = r.data.machine;
        MA.CurrentRun.method = r.data.method;
        
    }
    
    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
};

MA.RunSaveCallback = function() {
    //here is where I would call
    //Ext.getCmp('runlistview').refresh();
    //except that it doesn't work and the error is swallowed in the framework
    //note: do not use close() because, unlike the close button, it actually kills the window
    MA.RunCmp.hide();
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
    tbar: [{
        text: 'create new',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/add.gif',
        handler : function(){
                MA.CreateNewRun();
            }
        }
    ],
    items:[
    
        {
            xtype:'listview',
            id:'runlistview',
            region:'west',
            width:150,
            store:runStore,
            loadingText:'Loading...',
            columns: [
	            {header: "or select existing", dataIndex: 'title', sortable: true}
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
            labelWidth:160,
            bodyStyle:'padding:20px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
            items:[
                {
                    xtype:'hidden',
                    itemId:'id'
                },
                {
                    fieldLabel:'Title',
                    xtype:'textfield',
                    itemId:'title',
                    value:'New Untitled Run',
                    allowBlank:false
                },
                new Ext.form.ComboBox({
                    fieldLabel: 'Instrument method',
                    itemId: 'method',
                    name: 'method',
                    editable:false,
                    forceSelection:true,
                    displayField:'value',
                    valueField:'key',
                    hiddenName:'method',
                    lazyRender:true,
                    allowBlank:false,
                    typeAhead:false,
                    triggerAction:'all',
                    listWidth:230,
                    store: methodStore
                }),
                new Ext.form.ComboBox({
                    fieldLabel: 'Machine',
                    itemId: 'machine',
                    name: 'machine',
                    editable:false,
                    forceSelection:true,
                    displayField:'value',
                    valueField:'key',
                    hiddenName:'machine',
                    lazyRender:true,
                    allowBlank:false,
                    typeAhead:false,
                    triggerAction:'all',
                    listWidth:230,
                    store: machineStore
                }),
                {
                    fieldLabel:'Samples',
                    xtype:'listview',
                    width:200,
                    height:200,
                    store:runSampleStore,
                    loadingText:'Loading...',
                    columns: [
                        {header: "id", dataIndex: 'id', sortable: true},
                        {header: "label", dataIndex: 'label', sortable: true},
                        {header: "class", dataIndex: 'sample_class__unicode', sortable: true}
                    ],
                    viewConfig:{
                        forceFit:true
                    },
                    singleSelect:true,
                    multiSelect:true,
                    style:'background:white;',
                    autoScroll:true,
                    reserveScrollOffset:true
                }
            ],
            buttons:[
                {
                    text:'Generate Worklist'
                },
                { 
                    text:'Save',
                    handler:function() {
                    	var detailPanel = Ext.getCmp('runDetails');

                        if (detailPanel.getComponent('id').getValue() == 0) {
                            //create new
                            values = {};
                            values.title = detailPanel.getComponent('title').getValue();
                            values.method_id = detailPanel.getComponent('method').getValue();
                            values.machine_id = detailPanel.getComponent('machine').getValue();
                            
                            MA.CRUDSomething('create/run/', values, MA.RunSaveCallback);
                        } else {
                            //update
                            values = {};
                            values.id = detailPanel.getComponent('id').getValue();
                            values.title = detailPanel.getComponent('title').getValue();
                            values.method_id = detailPanel.getComponent('method').getValue();
                            values.machine_id = detailPanel.getComponent('machine').getValue();
                            
                            MA.CRUDSomething('update/run/'+values.id+'/', values, MA.RunSaveCallback);
                        }
                    }
                }
            ]
        }
    
    ]
});