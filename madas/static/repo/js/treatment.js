MA.TreatmentInit = function() {
    MA.TimelineLoad();
    MA.TreatmentLoad();
};

MA.TimelineLoad = function () {
    timelineStore.load({ params: { experiment__id__exact: MA.ExperimentController.currentId() } });
};

MA.TreatmentLoad = function () {
    treatmentStore.load({ params: { experiment__id__exact: MA.ExperimentController.currentId() } });
};

MA.SaveTimelineRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.timeline = rec.data.timeline;
    bundledData.abbreviation = rec.data.abbreviation;
    
    MA.SaveRowLiterals('sampletimeline', roweditor, bundledData, rec, i, MA.TimelineLoad);
};

MA.SaveTreatmentRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.name = rec.data.name;
    bundledData.type_id = rec.data.type;
    bundledData.description = rec.data.description;
    bundledData.abbreviation = rec.data.abbreviation;
    
    MA.SaveRowLiterals('treatment', roweditor, bundledData, rec, i, MA.TreatmentLoad);
};

MA.Treatment = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'Treatment',
            region: 'center',
            collapsible: false,
            layout:'form',
            autoScroll:true,
            minSize: 75,
            items: [ 
                { xtype:'fieldset', 
                title:'Timeline',
                autoHeight:true,
                items: [
                    { xtype:'editorgrid', 
                            id:'dates',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'Timeline',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveTimelineRow}})],
                            sm: new Ext.grid.RowSelectionModel(),
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            bbar: [
                                {
                                    text:'Create',
                                    cls: 'x-btn-text-icon',
                                    icon: 'static/repo/images/create-samples.png',
                                    handler: function() {
                                        var reps = Ext.getCmp('timelineReplicateField').getValue();
                                        
                                        var grid = Ext.getCmp('dates');

                                        for (var i = 0; i < parseInt(reps); i++) {
                                            MA.CRUDSomething('create/sampletimeline/', {
                                                'experiment_id': MA.ExperimentController.currentId(),
                                                'timeline': '00:00'
                                            }, MA.TimelineLoad);
                                        }
                                    }
                                },
                                {
                                    xtype:'numberfield',
                                    id:'timelineReplicateField',
                                    value:'1',
                                    width:28
                                },
                                {
                                    xtype:'panel',
                                    html:' new timeline entries',
                                    border:false,
                                    bodyStyle:'background:transparent;padding:4px; color: #333'
                                }
                            ],
                            tbar: [
                                {
                                    text: 'Add Time',
                                    cls: 'x-btn-text-icon',
                                    icon:'static/repo/images/add.png',
                                    handler : function(){
                                        MA.CRUDSomething('create/sampletimeline/', {
                                            'experiment_id': MA.ExperimentController.currentId(),
                                            'timeline': '00:00'
                                        }, MA.TimelineLoad);
                                    }
                                },
                                {
                                    text: 'Remove Time',
                                    cls: 'x-btn-text-icon',
                                    icon:'static/repo/images/delete.png',
                                    handler : function(){
                                        var grid = Ext.getCmp('dates');
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
                                            MA.CRUDSomething('delete/sampletimeline/'+delIds[i], {}, MA.TimelineLoad);
                                        }
                                    }
                                }
                            ],
                            columns: [
                                      { header: "Timeline",  sortable:false, menuDisabled:true, dataIndex:'timeline', editor: new Ext.form.TextField({allowBlank:false}) },
                                      { header: "Abbrev", sortable:false, menuDisabled:true, editor:new Ext.form.TextField({ allowBlank:true }), dataIndex:'abbreviation'
                                      }
                            ],
                            store: timelineStore
                        }
                    ]
                },
                { xtype:'fieldset', 
                title:'Treatments',
                autoHeight:true,

                items: [
                    { xtype:'editorgrid', 
                            id:'othertreat',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'Treatments',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:true, listeners:{'afteredit':MA.SaveTreatmentRow}})],
                            sm: new Ext.grid.RowSelectionModel(),
                            store:treatmentStore,
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            tbar: [
                                {
                                    text: 'Add Treatment',
                                    cls: 'x-btn-text-icon',
                                    icon:'static/repo/images/add.png',
                                    handler : function(){
                                        MA.CRUDSomething('create/treatment/', {
                                            'experiment_id': MA.ExperimentController.currentId(),
                                            'name': 'Unknown'
                                        }, MA.TreatmentLoad);
                                    }
                                },
                                {
                                    text: 'Remove Treatment',
                                    cls: 'x-btn-text-icon',
                                    icon:'static/repo/images/delete.png',
                                    handler : function(){
                                        var grid = Ext.getCmp('othertreat');
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
                                            MA.CRUDSomething('delete/treatment/'+delIds[i], {}, MA.TreatmentLoad);
                                        }
                                    }
                                }
                            ],
                            columns: [
                                { header: "Name",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                lazyRender:true,
                                name:'bullshot',
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'query',
                                listWidth:230,
                                store: treatmentComboStore,
                                enableKeyEvents: true,
                                scope: this,
                                listeners: {
                                    
                                    expand: function(combo) {                                
                                       // Since ExtJS combobox doesn't allow selection at -1  --> we pick -2 :)
                                        this.select(-2, false);                    
                                    },
                                    
                                    beforequery: function() {
                                        this.collapse();                
                                    },
                                    
                                    keydown: function(field, e) {                
                                        if(e.getKey() == 9) {    // When pressing 'Tab'
                                            this.collapse();    
                                        }
                                    }
                                    
                                } 
                            }), dataIndex:'name' },
                            { header: "Abbrev", sortable:false, menuDisabled:true, editor:new Ext.form.TextField({ allowBlank:true }), dataIndex:'abbreviation'
                            }
                            ]
                      }
                    ]
                }
            ]
        }
    ]
};
