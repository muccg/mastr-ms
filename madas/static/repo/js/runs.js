//run.js needs to manage a few things
//the list of runs
//the current run being manipulated
//the current samples in the run being manipulated

MA.CurrentRun = {
    
};

MA.RunSampleCheckboxSM = new Ext.grid.CheckboxSelectionModel({ width: 25 });

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
        MA.ClearCurrentRun;
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
    //note: do not use close() because, unlike the close button, it actually kills the window
    MA.RunCmp.hide();

    //here is where I would call
    runStore.reload();
};

MA.RunDeleteCallback = function() {
    MA.ClearCurrentRun();

//    Ext.getCmp('runlistview').clearSelections();
    
    runStore.reload();
    
};

MA.RunSampleRemoveSuccess = function() {
    runSampleStore.load();
};

MA.ClearCurrentRun = function() {
	var detailPanel = Ext.getCmp('runDetails');

    detailPanel.getComponent('id').setValue(0);
    detailPanel.getComponent('title').setValue("New Untitled Run");
    detailPanel.getComponent('method').clearValue();
    detailPanel.getComponent('machine').clearValue();
    
    MA.CurrentRun.id = 0;
    MA.CurrentRun.title = 'New Untitled Run';
}

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
            xtype:'form',
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
                    xtype:'grid',
                    width:310,
                    height:200,
                    store:runSampleStore,
                    loadingText:'Loading...',
                    columns: [
                        MA.RunSampleCheckboxSM,
                        {header: "id", dataIndex: 'id', sortable: true},
                        {header: "label", dataIndex: 'label', sortable: true},
                        {header: "class", dataIndex: 'sample_class__unicode', sortable: true}
                    ],
                    viewConfig:{
                        forceFit:true
                    },
                    sm: MA.RunSampleCheckboxSM,
                    style:'background:white;',
                    autoScroll:true,
                    reserveScrollOffset:true,
                    tbar: {
                        { 
                            text:'remove',
                            cls: 'x-btn-text-icon',
                            icon:'static/repo/images/no.gif',
                            listeners: {
                                'click': function(e) {
                                    //save changes to selected entries
                                    if (MA.RunSampleCheckboxSM.getCount() > 0) {
                                        var selections = MA.RunSampleCheckboxSM.getSelections();
                                        
                                        if (!Ext.isArray(selections)) {
                                            selections = [selections];
                                        }
                                        
                                        var ids = [];
                                        for (var idx in selections) {
                                            if (!Ext.isObject(selections[idx])) {
                                                continue;
                                            }
                                            
                                            ids.push(selections[idx].data.id);
                                        }
                                        
                                        var saver = new Ajax.Request(
                                            wsBaseUrl + 'remove_samples_from_run/?run_id='+escape(MA.CurrentRun.id)+'&sample_ids='+escape(ids.join(",")), 
                                            { 
                                                asynchronous:true, 
                                                evalJSON:'force',
                                                onSuccess:     MA.RunSampleRemoveSuccess
                                            });
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            buttons:[
                {
                    text:'Delete',
                    handler:function() {
                        var detailPanel = Ext.getCmp('runDetails');
                        if (detailPanel.getComponent('id').getValue() == 0) {
                            MA.RunDeleteCallback();
                        } else {
                            var agreed = window.confirm("Are you sure you wish to delete this Run?");
                            if (agreed) {
                                MA.CRUDSomething('delete/run/'+detailPanel.getComponent('id').getValue()+'/', null, MA.RunDeleteCallback);
                            }
                        }
                    }
                },
                {
                    text:'Generate Worklist'
                },
                { 
                    text:'Save',
                    handler:function() {
                    	var detailPanel = Ext.getCmp('runDetails');

                        if (detailPanel.isValid()) {
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
                }
            ],
            isValid: function() {
                var valid = true;
                if (this.getComponent("machine").getValue() == "None" ||
                    this.getComponent("machine").getValue() == "") {
                    valid = false;
                    this.getComponent("machine").markInvalid("Required");
                }
                if (this.getComponent("method").getValue() == "None" ||
                    this.getComponent("method").getValue() == "") {
                    valid = false;
                    this.getComponent("method").markInvalid("Required");
                }
                
                return valid;
            }
        }
    
    ]
});