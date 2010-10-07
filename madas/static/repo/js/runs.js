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
//        Ext.getCmp("runDetails").createRun();
    } else {
        var r = view.getSelectedRecords()[0];

        Ext.getCmp("runDetails").selectRun(r);
        Ext.getCmp('currentRunTitle').update(r.data.title);
    }
};

MA.RunSaveCallback = function(id) {
    Ext.getCmp('currentRunTitle').update(selectableRunStore.getById(id).data.title);
};

MA.RunDeleteCallback = function() {
    selectableRunStore.load();
    MA.ClearCurrentRun();
};

MA.ClearCurrentRun = function() {
    Ext.getCmp("runDetails").clearRun();
    Ext.getCmp('currentRunTitle').update("New Untitled Run");
};

// Create a component we can use both here and from the run list.
MA.RunDetail = Ext.extend(Ext.form.FormPanel, {
    constructor: function (config, mode) {
        var self = this;
        if (!Ext.isDefined(mode)) {
            mode = 'viewer';
            // viewer mode doesn't show samples to add
        }

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
            autoScroll:true,
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
                new Ext.form.Label({
                    fieldLabel: "Progress",
                    itemId: "progress",
                    style: "position: relative; top: 3px;",
                    text: ''
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
                    itemId:'samplesToAdd',
                    xtype:'grid',
                    width:310,
                    height:120,
                    store:this.pendingSampleStore,
                    loadMask:true,
                    columns: [
                        self.pendingSampleSelModel,
                        {header: "ID", dataIndex: 'id', sortable: true}
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
                                text:'Remove Samples',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/delete.png',
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
                    itemId:'samples',
                    height:120,
                    store:this.sampleStore,
                    loadMask:true,
                    columns: [
                        self.sampleSelModel,
                        {header: "ID", dataIndex: 'id', sortable: true},
                        {header: "Label", dataIndex: 'label', sortable: true},
                        {header: "Class", dataIndex: 'sample_class__unicode', sortable: true},
                       { header: "Seq", sortable:true, dataIndex:'sample_class_sequence' }
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
                                text:'Remove Samples',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/delete.png',
                                itemId:'removeBtn',
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
                },
                {
                    fieldLabel: 'Completed files',
                   xtype:'treepanel',
                   border: true,
                   autoScroll: true,
                   id:'runTree',
                   animate: true,
                   useArrows: true,
                   height:200,
                   dataUrl:wsBaseUrl + 'runFiles',
                   requestMethod:'GET',
                    tbar:[
                        {
                            xtype:'tbtext',
                            text:'Click a filename to download'
                        }
                    ],                   root: {
                       nodeType: 'async',
                       text: 'Files',
                       draggable: false,
                       id: 'runsRoot',
                       'metafile': true
                   },
                   selModel: new Ext.tree.DefaultSelectionModel(
                       { listeners:
                           {
                               selectionchange: function(sm, node) {
                                  if (node != null && !node.attributes.metafile) {
                                       window.location = wsBaseUrl + 'downloadRunFile?file=' + node.id + '&run_id=' + self.runId;
                                   }
                               }
                           }
                       }),
                   listeners:{
                        render: function() {
                            Ext.getCmp('runTree').getLoader().on("beforeload", function(treeLoader, node) {
                                treeLoader.baseParams.run = self.runId;
                                }, this);
                            Ext.getCmp('runTree').getRootNode().expand();
                        }
                    }
               }
            ],
            buttons:[
                {
                    text:'Delete Run',
                    itemId:'deleteButton',
                    handler:function() {
                        self.deleteRun();
                    }
                },
                {
                    text:'Generate Worklist',
                    disabled: true,
                    itemId:'generateWorklistButton',
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
                    itemId:'markCompleteButton',
                    disabled:true,
                    handler: function () {
                        var agreed = window.confirm("Are you sure you wish to mark this run as having been fully completed?");
                        if (agreed) {
                            Ext.Ajax.request({
                                url: wsBaseUrl + "mark_run_complete/" + self.runId,
                                success: function () {
                                    self.getComponent("state").setText(renderRunState(2));
                                    self.getComponent("progress").setText(renderRunProgress(1), false);
                                    self.fireEvent("save", self.runId);
                                }
                            });
                        }
                    }
                },
                { 
                    text:'Save Run',
                    handler:function() {
                        if (self.isValid()) {
                            var runSaveCallback = function (store, records, options) {
                                self.runId = records[0].data.id;
                                self.savePendingSamples();

                                self.getFooterToolbar().getComponent("generateWorklistButton").enable();
                                self.getFooterToolbar().getComponent("markCompleteButton").enable();

                                self.fireEvent("save", records[0].data.id);
                            };

                            var values = {};
                            values.title = self.getComponent('title').getValue();
                            values.method_id = self.getComponent('method').getValue();
                            values.machine_id = self.getComponent('machine').getValue();

                            if (self.runId == 0) {
                                //create new
                                MA.CRUDSomething('create/run/', values, runSaveCallback);
                            } else {
                                //update
                                values.id = self.runId;
                                
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
        
        if (mode == 'viewer') {
            this.remove("samplesToAdd");
            this.getComponent('samples').setHeight(200);
        } else {
            this.remove('runFiles');
        }
        
        self.setAutoScroll(true);
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
        this.getComponent("progress").setText(renderRunProgress(0), false);

        this.getComponent("title").setValue("New Untitled Run");
        this.getComponent("method").clearValue();
        this.getComponent("machine").clearValue();

        this.getFooterToolbar().getComponent("generateWorklistButton").disable();
        this.getFooterToolbar().getComponent("markCompleteButton").disable();
        this.getFooterToolbar().getComponent("deleteButton").disable();
        
        this.getComponent('samples').getBottomToolbar().getComponent('removeBtn').enable();

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
                        var message = "An error occurred while saving the "
                            + "sample list for this run. More detail may be "
                            + "available below:"
                            + "<br /><br />"
                            + response.responseText;

                        Ext.Msg.alert("Error", message);
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
        this.getComponent("progress").setText(renderRunProgress(null, null, record), false);
        this.getComponent("title").setValue(record.data.title);
        this.getComponent("method").setValue(record.data.method);
        this.getComponent("machine").setValue(record.data.machine);

        this.getFooterToolbar().getComponent("generateWorklistButton").enable();
        this.getFooterToolbar().getComponent("markCompleteButton").enable();
        this.getFooterToolbar().getComponent("deleteButton").enable();


        if (record.data.state == 2) {
            this.getFooterToolbar().getComponent("generateWorklistButton").disable();
            this.getFooterToolbar().getComponent("markCompleteButton").disable();
            this.getFooterToolbar().getComponent("deleteButton").disable();
        }
        
        if (record.data.state == 0) {
            this.getComponent('samples').getBottomToolbar().getComponent('removeBtn').enable();
        } else {
            this.getComponent('samples').getBottomToolbar().getComponent('removeBtn').disable();
        }
       
        this.sampleStore.load({ params: { run__id__exact: this.runId } });
        
        Ext.getCmp('runTree').getLoader().load(Ext.getCmp('runTree').getRootNode());
    }
});

MA.RunCmp = new Ext.Window({
    id:'runCmp',
    title:'Current Run',
    width:680,
    height:530,
    minHeight:530,
    x:170,
    y:50,
    closeAction:'hide',
    layout:'border',
    tbar: [{
        text: 'Create New',
        cls: 'x-btn-text-icon',
        icon:'static/repo/images/add.png',
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
            store:selectableRunStore,
            loadingText:'Loading...',
            columnSort:false,
            columns: [
	            {header: "Or select existing", dataIndex: 'title', 
	                tpl: '<div style="padding:4px"><b>{title}</b><br><div style="color:#666"><i>{method__unicode}<br>{creator__unicode}</i></div></div>'}
            ],
            listeners:{
                'selectionchange':MA.RunCmpRowSelect,
                'render': function() {
                    //register to be notified when the runstore loads so that we can update current sel
                    
                    selectableRunStore.addListener("load", function() {
                        var record = selectableRunStore.getById(Ext.getCmp('runDetails').runId);
                        if (record != null) {
                            var list = Ext.getCmp("runlistview");
                            list.refresh();
    
                            list.select(record);
                            list.getNode(record).scrollIntoView(list.innerBody.dom.parentNode);
                        } else {
                            MA.CreateNewRun();
                        }
                    });
                }
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
            autoScroll:true,
            region:'center',
            bodyStyle:'padding:20px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
            listeners: {
                "delete": MA.RunDeleteCallback,
                "save": function (id) {
                    selectableRunStore.load();
                    runStore.load();
                    MA.RunSaveCallback(id);
                }
            }
        }, 'editor')
    ]
});
