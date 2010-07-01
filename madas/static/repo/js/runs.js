//run.js needs to manage a few things
//the list of runs
//the current run being manipulated
//the current samples in the run being manipulated

MA.CreateNewRun = function() {
    Ext.getCmp('runlistview').clearSelections();

    Ext.getCmp("runDetails").createRun();
    
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

MA.RunCmpRowSelect = function(view, nodes) {
    if (nodes.length == 0) {
        Ext.getCmp("runDetails").createRun();
    } else {
        var r = view.getSelectedRecords()[0];

        Ext.getCmp("runDetails").selectRun(r);
        Ext.getCmp('currentRunTitle').update(r.data.title);
    }
};

MA.RunSaveCallback = function(id) {
    Ext.getCmp('currentRunTitle').update(runStore.getById(id).data.title);
};

MA.RunDeleteCallback = function() {
    MA.ClearCurrentRun();
};

MA.ClearCurrentRun = function() {
    Ext.getCmp("runDetails").clearRun();
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

// Create a component we can use both here and from the run list.
MA.RunDetail = Ext.extend(Ext.form.FormPanel, {
    constructor: function (config) {
        var self = this;

        this.pendingSampleSelModel = new Ext.grid.CheckboxSelectionModel({ width: 25 });
        this.sampleSelModel = new Ext.grid.CheckboxSelectionModel({ width: 25 });

        this.pendingSampleFields = [
            { name: "id", type: "int" }
        ];

        this.pendingSampleStore = new Ext.data.ArrayStore({
            fields: this.pendingSampleFields,
            idIndex: 0,
            sortInfo: {
                field: "id",
                direction: "DESC"
            }
        });

        this.PendingSampleRecord = Ext.data.Record.create(this.pendingSampleFields);

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
                new Ext.form.Label({
                    fieldLabel: "State",
                    itemId: "state",
                    style: "position: relative; top: 3px;",
                    text: renderRunState(0)
                }),
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
                    width: 200,
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
                    width: 200,
                    store: machineStore
                }),
                {
                    fieldLabel:'Samples to Add',
                    xtype:'grid',
                    width:310,
                    height:120,
                    store:this.pendingSampleStore,
                    loadMask:true,
                    columns: [
                        self.pendingSampleSelModel,
                        {header: "id", dataIndex: 'id', sortable: true}
                    ],
                    viewConfig:{
                        forceFit:true
                    },
                    sm: self.pendingSampleSelModel,
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
                                        if (self.pendingSampleSelModel.getCount() > 0) {
                                            var selections = self.pendingSampleSelModel.getSelections();
                                            
                                            if (!Ext.isArray(selections)) {
                                                selections = [selections];
                                            }
                                            
                                            var ids = [];
                                            for (var idx in selections) {
                                                if (!Ext.isObject(selections[idx])) {
                                                    continue;
                                                }

                                                self.pendingSampleStore.remove(selections[idx]);
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                },
                {
                    fieldLabel:'Samples',
                    xtype:'grid',
                    width:310,
                    height:120,
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
                    text: "Mark Complete",
                    handler: function () {
                        Ext.Ajax.request({
                            url: wsBaseUrl + "mark_run_complete/" + self.runId,
                            success: function () {
                                self.getComponent("state").setText(renderRunState(2));
                                self.fireEvent("save", self.runId);
                            }
                        });
                    }
                },
                { 
                    text:'Save Run',
                    handler:function() {
                        if (self.isValid()) {
                            var runSaveCallback = function (store, records, options) {
                                self.runId = records[0].data.id;
                                self.savePendingSamples();

                                self.fireEvent("save", records[0].data.id);
                            };

                            if (self.runId == 0) {
                                //create new
                                if (self.pendingSampleStore.getCount() == 0) {
                                    Ext.Msg.alert("Warning", "You cannot create a run without samples. Please select some samples and try again.");
                                    return;
                                }

                                values = {};
                                values.title = self.getComponent('title').getValue();
                                values.method_id = self.getComponent('method').getValue();
                                values.machine_id = self.getComponent('machine').getValue();
                                
                                MA.CRUDSomething('create/run/', values, runSaveCallback);
                            } else {
                                //update
                                values = {};
                                values.id = self.runId;
                                values.title = self.getComponent('title').getValue();
                                values.method_id = self.getComponent('method').getValue();
                                values.machine_id = self.getComponent('machine').getValue();
                                
                                MA.CRUDSomething('update/run/'+values.id+'/', values, runSaveCallback);
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

        this.addEvents("delete", "save", "save-samples");

        this.pendingSampleStore.removeAll();
        this.runId = 0;
    },
    addSample: function (id) {
        if (Ext.isArray(id)) {
            for (var i = 0; i < id.length; i++) {
                this.addSample(id[i]);
            }
            return;
        }

        this.pendingSampleStore.add(new this.PendingSampleRecord({ id: id }, id));
    },
    clearRun: function () {
        this.createRun();
    },
    createRun: function () {
        this.runId = 0;
        this.pendingSampleStore.removeAll();

        this.getComponent("state").setText(renderRunState(0));
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
    savePendingSamples: function () {
        if (this.pendingSampleStore.getCount() > 0) {
            if (this.runId) {
                var self = this;

                var ids = [];
                this.pendingSampleStore.each(function (record) {
                    ids.push(record.data.id);
                });

                Ext.Ajax.request({
                    url: wsBaseUrl + "add_samples_to_run/",
                    method: "POST",
                    params: {
                        run_id: this.runId,
                        sample_ids: ids.join(",")
                    },
                    success: function () {
                        self.pendingSampleStore.removeAll();
                        self.sampleStore.load({ params: { run__id__exact: self.runId } });
                        self.fireEvent("save-samples");
                    },
                    failure: function (response, options) {
                        Ext.Msg.alert("Error", "An error occurred while saving the sample list for this run.");
                    }
                });
            }
            else {
                throw new Error("Pending samples can only be saved if a run has already been created.");
            }
        }
    },
    selectRun: function (record) {
        this.runId = record.data.id;
        this.pendingSampleStore.removeAll();

        this.getComponent("state").setText(renderRunState(record.data.state));
        this.getComponent("title").setValue(record.data.title);
        this.getComponent("method").setValue(record.data.method);
        this.getComponent("machine").setValue(record.data.machine);

        this.sampleStore.load({ params: { run__id__exact: this.runId } });
    }
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
                "delete": MA.RunDeleteCallback,
                "save": function (id) {
                    runStore.load();
                    MA.RunSaveCallback(id);
                }
            }
        })
    ]
});
