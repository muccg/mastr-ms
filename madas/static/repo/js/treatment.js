Ext.madasTreatmentInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    
    timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/source__experiment__id/' + expId;
    timelineStore.load();

    treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/source__experiment__id/' + expId;
    treatmentStore.load();
}

Ext.madasSaveTimelineRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['taken_on'] = Ext.util.Format.date(rec.data.taken_on, 'Y-m-d');
    bundledData['taken_at'] = rec.data.taken_at;
    
    Ext.madasSaveRowLiterals('sampletimeline', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/source__experiment__id/' + expId; timelineStore.load();});
};

Ext.madasSaveTreatmentRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['name'] = rec.data.name;
    bundledData['type_id'] = rec.data.type;
    bundledData['description'] = rec.data.description;
    
    Ext.madasSaveRowLiterals('treatment', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/source__experiment__id/' + expId; treatmentStore.load();});
};

Ext.madasSaveTreatmentVariationRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['name'] = rec.data.name;
    
    Ext.madasSaveRowLiterals('treatmentvariation', roweditor, bundledData, rec, i, function() { var treatId = Ext.madasCurrentTreatmentId(); treatmentVariationStore.proxy.conn.url = wsBaseUrl + 'records/treatmentvariation/treatment__id/' + treatId; treatmentVariationStore.load();});
};

Ext.madasTreatment = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'treatment',
            region: 'center',
            collapsible: false,
            layout:'form',
            autoScroll:true,
            minSize: 75,
            items: [ 
                { xtype:'fieldset', 
                title:'timeline',
                autoHeight:true,
//                collapsible:true,
//                checkboxToggle:true,
//                collapsed:true,
                items: [
                    { xtype:'editorgrid', 
                            id:'dates',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'dates',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveTimelineRow}})],
                            sm: new Ext.grid.RowSelectionModel(),
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            tbar: [{
                                text: 'add date',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/add.gif',
                                handler : function(){
                                    Ext.madasCRUDSomething('create/sampletimeline/', {'source_id':Ext.madasCurrentBioSourceId()}, function() { var expId = Ext.madasCurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/source__experiment__id/' + expId;
                                                          timelineStore.load(); });
                                    }
                                },
                                {
                                text: 'remove date',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/no.gif',
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
                                   console.log(delIds);
                                   for (var i = 0; i < delIds.length; i++) {
                                   Ext.madasCRUDSomething('delete/sampletimeline/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/source__experiment__id/' + expId;
                                                          timelineStore.load(); });
                                   }                        }
                                   }
                            ],
                            columns: [
                                      { header: "date sample taken",  sortable:false, menuDisabled:true, editor:new Ext.form.DateField({
                                                                                                                                       editable:true,
                                                                                                                                       allowBlank:false,
                                                                                                                                       format:'Y/m/d'
                                                                                                                                       }), dataIndex:'taken_on' },
                                      { header: "time sample taken",  sortable:false, menuDisabled:true, editor:new Ext.form.TimeField({
                                                                                                                                       editable:true,
                                                                                                                                       allowBlank:false,
                                                                                                                                       format:'H:m'
                                                                                                                                       }), dataIndex:'taken_at' }
                            ],
                            store: timelineStore
                        }
                    ]
                },
                { xtype:'fieldset', 
                title:'treatments',
                autoHeight:true,
//                collapsible:true,
//                checkboxToggle:true,
//                collapsed:true,
                items: [
                    { xtype:'editorgrid', 
                            id:'othertreat',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'other treatments',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveTreatmentRow}})],
                            sm: new Ext.grid.RowSelectionModel({
                               singleSelect:true,
                                listeners:{
                                    'rowselect':function(sm, idx, rec) {
                                        treatmentVariationStore.proxy.conn.url = wsBaseUrl + "records/treatmentvariation/treatment__id/" + rec.data.id;
                                        Ext.madasCurrentTreatmentIdValue = rec.data.id;
                                        treatmentVariationStore.load();
                                        
                                        var grid = Ext.getCmp("specifictreat");
                                        grid.enable();
                                        grid.expand(true);
                                    },
                                    'selectionchange':{buffer:10, fn:function(sm) {
                                        if (! sm.hasSelection()) {
                                            var grid = Ext.getCmp("specifictreat");
                                            grid.disable();
                                            grid.collapse(true);
                                        }
                                    }}

                                }
                            }),
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            tbar: [{
                                text: 'add treatment',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/add.gif',
                                handler : function(){
                                   Ext.madasCRUDSomething('create/treatment/', {'source_id':Ext.madasCurrentBioSourceId()}, function() { var expId = Ext.madasCurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/source__experiment__id/' + expId;
                                                          treatmentStore.load(); });
                                   }
                                },
                                {
                                text: 'remove treatment',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/no.gif',
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
                                   Ext.madasCRUDSomething('delete/treatment/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/source__experiment__id/' + expId;
                                                          treatmentStore.load(); });
                                   }
                                }
                                }
                            ],
                            columns: [
                                { header: "name",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: treatmentComboStore
                            }), dataIndex:'name' },
                            { header: "type",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:false,
                                forceSelection:true,
                                displayField:'value',
                                valueField:'key',
                                hiddenName:'node',
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: treatmentTypeComboStore
                            }), dataIndex:'type', renderer:renderTreatmentType },
                                { header: "description", sortable:false, menuDisabled:true, editor:new Ext.form.TextField({}), dataIndex:'description' }
                            ],
                            store: treatmentStore
                        },
                        { xtype:'editorgrid', 
                            id:'specifictreat',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'specific treatments',
                            collapsible:true,
                            collapsed:true,
                            width:500,
                            height:200,
                            disabled:true,
                            border: true,
                            trackMouseOver: false,
                        plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'validateedit':function() { return true; }, 'afteredit':Ext.madasSaveTreatmentVariationRow}})],
                            sm: new Ext.grid.RowSelectionModel(),
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            tbar: [{
                                text: 'add specific treatment',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/add.gif',
                                handler : function(){
                                   Ext.madasCRUDSomething('create/treatmentvariation/', {'treatment_id':Ext.madasCurrentTreatmentId()}, function() { var treatId = Ext.madasCurrentTreatmentId(); treatmentVariationStore.proxy.conn.url = wsBaseUrl + 'records/treatmentvariation/treatment__id/' + treatId;
                                                          treatmentVariationStore.load(); });
                                   }
                                },
                                {
                                text: 'remove specific treatment',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/no.gif',
                                handler : function(){
                                   var grid = Ext.getCmp('specifictreat');
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
                                   Ext.madasCRUDSomething('delete/treatmentvariation/'+delIds[i], {}, function() { var treatId = Ext.madasCurrentTreatmentId(); treatmentVariationStore.proxy.conn.url = wsBaseUrl + 'records/treatmentvariation/treatment__id/' + treatId;
                                                          treatmentVariationStore.load(); });
                                   }
                                   }
                                }
                            ],
                            columns: [
                                      { header: "variation",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                                                                                                              editable:true,
                                                                                                                              forceSelection:false,
                                                                                                                              displayField:'value',
                                                                                                                              valueField:undefined,
                                                                                                                              lazyRender:true,
                                                                                                                              allowBlank:false,
                                                                                                                              typeAhead:false,
                                                                                                                              triggerAction:'all',
                                                                                                                              listWidth:230,
                                                                                                                              store: treatmentVariationComboStore
                                                                                                                              }), dataIndex:'name' }
                            ],
                            store: treatmentVariationStore
                        }
                    ]
                }
            ]
        }
    ]
};