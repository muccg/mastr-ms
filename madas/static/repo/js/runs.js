//run.js needs to manage a few things
//the list of runs
//the current run being manipulated
//the current samples in the run being manipulated

MA.CurrentRun = {
    id: 0,
    addSamples: function(ids) {
        if (this.id == 0) {
            if (this.pendingIDs == null ||
                this.pendingIDs == undefined) {
                this.pendingIDs = ids;
            } else {
                this.pendingIDs.concat(ids);
            }
            
            MA.RunCmp.show();
            Ext.Msg.alert('Adding Samples to a Fresh Run', 'As this Run is completely new, it needs to have a Title, Method and Machine assigned, and Saved. Then your selected samples will be automatically added.');
            
        } else {
            this.addSamplesCommit(ids);
        }
    },
    addSamplesCommit: function(ids) {
        var saver = new Ajax.Request(
            wsBaseUrl + 'add_samples_to_run/', 
            { 
                parameters:{
                    run_id:MA.CurrentRun.id,
                    sample_ids:ids.join(",")
                },
                asynchronous:true, 
                evalJSON:'force',
                onSuccess:     MA.RunSampleAddSuccess,
                onFailure:    function(transport) { MA.DSLoadException(transport.status, transport.responseText); }
            });
    },
    clear: function() {
        this.id = 0;
        this.pendingIDs = undefined;
    }
};

MA.RunSampleCheckboxSM = new Ext.grid.CheckboxSelectionModel({ width: 25 });

MA.CreateNewRun = function() {
    Ext.getCmp('runlistview').clearSelections();

	var detailPanel = Ext.getCmp('runDetails');

    MA.CurrentRun.clear();
    
    detailPanel.getComponent('title').setValue('New Untitled Run');
    detailPanel.getComponent('method').clearValue();
    detailPanel.getComponent('machine').clearValue();
    
    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
    
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

MA.RunCmpRowSelect = function(view, nodes) {
	var detailPanel = Ext.getCmp('runDetails');
    
    MA.CurrentRun.clear();
    
    if (nodes.length == 0) {
        MA.ClearCurrentRun();
    } else {
        var r = view.getSelectedRecords()[0];
        
        detailPanel.getComponent('title').setValue(r.data.title);
        detailPanel.getComponent('method').setValue(r.data.method);
        detailPanel.getComponent('machine').setValue(r.data.machine);
        
        Ext.getCmp('currentRunTitle').update(r.data.title);
        
        MA.CurrentRun.id = r.data.id;
    }
    
    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
};

MA.RunSaveCallback = function(store, records, options) {
    if (records.length > 0) {
        MA.CurrentRun.id = records[0].data.id;
    
        //note: do not use close() because, unlike the close button, it actually kills the window
        //MA.RunCmp.hide();
        
        MA.CurrentRun.addSamplesCommit(MA.CurrentRun.pendingIDs);

        //here is where I would call
        runStore.reload();
            
        Ext.getCmp('currentRunTitle').update(records[0].data.title);

    } else {
        Ext.Msg.alert('Error', 'An unknown error occurred while saving the Run');
    }
};

MA.RunDeleteCallback = function() {
    MA.ClearCurrentRun();

//    Ext.getCmp('runlistview').clearSelections();
    
    runStore.reload();
    
};

MA.RunSampleRemoveSuccess = function() {
    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
};

MA.ClearCurrentRun = function() {
	var detailPanel = Ext.getCmp('runDetails');
    detailPanel.getComponent('title').setValue("New Untitled Run");
    detailPanel.getComponent('method').clearValue();
    detailPanel.getComponent('machine').clearValue();
    
    MA.CurrentRun.id = 0;
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

MA.RunSampleAddSuccess = function() {
    MA.CurrentRun.pendingIDs = undefined;

    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
    
    MA.RunCmp.show();
};

MA.RunCmp = new Ext.Window({
    id:'runCmp',
    title:'Current Run',
    width:680,
    height:500,
    minHeight:500,
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
            columnSort:false,
            columns: [
	            {header: "or select existing", dataIndex: 'title', 
	                tpl: '<div style="padding:4px"><b>{title}</b><br><div style="color:#666"><i>{method__unicode}<br>{creator__unicode}</i></div></div>'}
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
                    height:300,
                    store:runSampleStore,
                    loadMask:true,
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
                    bbar: {
                        items: [
                            { 
                                text:'remove samples',
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
                                                wsBaseUrl + 'remove_samples_from_run/', 
                                                { 
                                                    parameters:{
                                                        run_id:MA.CurrentRun.id,
                                                        sample_ids:ids.join(",")
                                                    },
                                                    asynchronous:true, 
                                                    evalJSON:'force',
                                                    onSuccess:     MA.RunSampleRemoveSuccess
                                                });
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ],
            buttons:[
                {
                    text:'Delete Run',
                    handler:function() {
                        if (MA.CurrentRun.id == 0) {
                            MA.RunDeleteCallback();
                        } else {
                            var agreed = window.confirm("Are you sure you wish to delete this Run?");
                            if (agreed) {
                                MA.CRUDSomething('delete/run/'+MA.CurrentRun.id+'/', null, MA.RunDeleteCallback);
                            }
                        }
                    }
                },
                {
                    text:'Generate Worklist',
                    id:'generateWorklistButton',
                    handler:function() {
                        if (MA.CurrentRun.id == 0) {
                            Ext.Msg.alert('Save Required', 'Before you can generate a worklist, this Run must be Saved');
                        } else {
                            window.open(wsBaseUrl + 'generate_worklist/' + MA.CurrentRun.id, 'worklist');
                        }
                    }
                },
                { 
                    text:'Save Run',
                    handler:function() {
                    	var detailPanel = Ext.getCmp('runDetails');

                        if (detailPanel.isValid()) {
                            if (MA.CurrentRun.id == 0) {
                                //create new
                                values = {};
                                values.title = detailPanel.getComponent('title').getValue();
                                values.method_id = detailPanel.getComponent('method').getValue();
                                values.machine_id = detailPanel.getComponent('machine').getValue();
                                
                                MA.CRUDSomething('create/run/', values, MA.RunSaveCallback);
                            } else {
                                //update
                                values = {};
                                values.id = MA.CurrentRun.id;
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