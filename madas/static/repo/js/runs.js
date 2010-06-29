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

MA.CreateNewRun = function() {
    Ext.getCmp('runlistview').clearSelections();

    MA.CurrentRun.clear();
    Ext.getCmp("runDetails").createRun();
    
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

MA.RunCmpRowSelect = function(view, nodes) {
    MA.CurrentRun.clear();
    
    if (nodes.length == 0) {
        MA.ClearCurrentRun();
    } else {
        var r = view.getSelectedRecords()[0];

        Ext.getCmp("runDetails").selectRun(r);
        Ext.getCmp('currentRunTitle').update(r.data.title);
        
        MA.CurrentRun.id = r.data.id;
    }
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
    Ext.getCmp("runDetails").clearRun();
    
    MA.CurrentRun.id = 0;
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

MA.RunSampleAddSuccess = function() {
    MA.CurrentRun.pendingIDs = undefined;

    runSampleStore.proxy.conn.url = adminBaseUrl + "repository/sample/ext/json?run__id__exact=" + MA.CurrentRun.id;
    runSampleStore.load();
    
    MA.RunCmp.show();
};

// Create a component we can use both here and from the run list.
MA.RunDetail = Ext.extend(Ext.form.FormPanel, {
    constructor: function (config) {
        var self = this;

        this.sampleSelModel = new Ext.grid.CheckboxSelectionModel({ width: 25 });

        this.sampleStore = new Ext.data.JsonStore({
            autoLoad: false,
            remoteSort: true,
            restful: true,
            url: adminBaseUrl + "repository/sample/ext/json",
            sortInfo: {
                field: 'id',
                direction: 'DESC'
            }
        });

        var defaultConfig = {
            labelWidth:160,
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
                    store:this.sampleStore,
                    loadMask:true,
                    columns: [
                        self.sampleSelModel,
                        {header: "id", dataIndex: 'id', sortable: true},
                        {header: "label", dataIndex: 'label', sortable: true},
                        {header: "class", dataIndex: 'sample_class__unicode', sortable: true}
                    ],
                    viewConfig:{
                        forceFit:true
                    },
                    sm: self.sampleSelModel,
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
                                        if (self.sampleSelModel.getCount() > 0) {
                                            var selections = self.sampleSelModel.getSelections();
                                            
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
                                                        run_id:self.runId,
                                                        sample_ids:ids.join(",")
                                                    },
                                                    asynchronous:true, 
                                                    evalJSON:'force',
                                                    onSuccess: function () {
                                                        self.sampleStore.load({ params: { run__id__exact: self.runId } });
                                                    }
                                                }
                                            );
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
                        self.deleteRun();
                    }
                },
                {
                    text:'Generate Worklist',
                    id:'generateWorklistButton',
                    handler:function() {
                        if (self.runId == 0) {
                            Ext.Msg.alert('Save Required', 'Before you can generate a worklist, this Run must be Saved');
                        } else {
                            window.open(wsBaseUrl + 'generate_worklist/' + self.runId, 'worklist');
                        }
                    }
                },
                { 
                    text:'Save Run',
                    handler:function() {
                        if (self.isValid()) {
                            if (self.runId == 0) {
                                //create new
                                values = {};
                                values.title = self.getComponent('title').getValue();
                                values.method_id = self.getComponent('method').getValue();
                                values.machine_id = self.getComponent('machine').getValue();
                                
                                MA.CRUDSomething('create/run/', values, MA.RunSaveCallback);
                            } else {
                                //update
                                values = {};
                                values.id = self.runId;
                                values.title = self.getComponent('title').getValue();
                                values.method_id = self.getComponent('method').getValue();
                                values.machine_id = self.getComponent('machine').getValue();
                                
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
        };

        config = Ext.apply(defaultConfig, config);

        MA.RunDetail.superclass.constructor.call(this, config);

        this.addEvents("delete");

        this.runId = 0;
    },
    clearRun: function () {
        this.createRun();
    },
    createRun: function () {
        this.runId = 0;

        this.getComponent("title").setValue("New Untitled Run");
        this.getComponent("method").clearValue();
        this.getComponent("machine").clearValue();

        this.sampleStore.load({ params: { run__id__exact: this.runId } });
    },
    deleteRun: function () {
        var self = this;

        if (this.runId == 0) {
            this.clearRun();
            this.fireEvent("delete", 0);
        } else {
            var agreed = window.confirm("Are you sure you wish to delete this Run?");
            if (agreed) {
                MA.CRUDSomething('delete/run/'+this.runId+'/', null, function () {
                    self.clearRun();
                    self.fireEvent("delete", self.runId);
                });
            }
        }
    },
    selectRun: function (record) {
        this.runId = record.data.id;

        this.getComponent("title").setValue(record.data.title);
        this.getComponent("method").setValue(record.data.method);
        this.getComponent("machine").setValue(record.data.machine);

        this.sampleStore.load({ params: { run__id__exact: this.runId } });
    },
});

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
        new MA.RunDetail({
            id:'runDetails',
            region:'center',
            bodyStyle:'padding:20px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
            listeners: {
                "delete": { fn: MA.RunDeleteCallback }
            }
        })
    ]
});
