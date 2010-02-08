MA.TreatmentInit = function() {
    var expId = MA.CurrentExperimentId();
    
    timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/experiment__id/' + expId;
    timelineStore.load();

    treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/experiment__id/' + expId;
    treatmentStore.load();
};

MA.SaveTimelineRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.taken_on = Ext.util.Format.date(rec.data.taken_on, 'Y-m-d');
    bundledData.taken_at = rec.data.taken_at;
    
    MA.SaveRowLiterals('sampletimeline', roweditor, bundledData, rec, i, function() { var expId = MA.CurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/experiment__id/' + expId; timelineStore.load();});
};

MA.SaveTreatmentRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.name = rec.data.name;
    bundledData.type_id = rec.data.type;
    bundledData.description = rec.data.description;
    
    MA.SaveRowLiterals('treatment', roweditor, bundledData, rec, i, function() { var expId = MA.CurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/experiment__id/' + expId; treatmentStore.load();});
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
                items: [
                    { xtype:'editorgrid', 
                            id:'dates',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'dates',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveTimelineRow}})],
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
                                    MA.CRUDSomething('create/sampletimeline/', {'experiment_id':MA.CurrentExperimentId()}, function() { var expId = MA.CurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/experiment__id/' + expId;
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
                                   //console.log(delIds);
                                   for (var i = 0; i < delIds.length; i++) {
                                   MA.CRUDSomething('delete/sampletimeline/'+delIds[i], {}, function() { var expId = MA.CurrentExperimentId(); timelineStore.proxy.conn.url = wsBaseUrl + 'records/sampletimeline/experiment__id/' + expId;
                                                          timelineStore.load(); });
                                   }                        }
                                   }
                            ],
                            columns: [
                                      { header: "date sample taken",  sortable:false, menuDisabled:true, editor:new Ext.form.DateField({
                                                   editable:true,
                                                   allowBlank:false,
                                                   initDate: new Date(),
                                                   format:'Y/m/d'
                                                   }), dataIndex:'taken_on' },
                                      { header: "time sample taken",  sortable:false, menuDisabled:true, editor:new Ext.form.TimeField({
                                                   editable:true,
                                                   allowBlank:false,
                                                   initDate: new Date(),
                                                   minValue: '0:00',
                                                   maxValue: '23:59',
                                                   increment: 1,
                                                   format:'H:i'
                                                   }), dataIndex:'taken_at' }
                            ],
                            store: timelineStore
                        }
                    ]
                },
                { xtype:'fieldset', 
                title:'treatments',
                autoHeight:true,

                items: [
                    { xtype:'editorgrid', 
                            id:'othertreat',
                            style:'margin-top:10px;margin-bottom:10px;',
                            title:'other treatments',
                            width:500,
                            height:200,
                            border: true,
                            trackMouseOver: false,
                            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveTreatmentRow}})],
                            sm: new Ext.grid.RowSelectionModel(),
                            store:treatmentStore,
                            viewConfig: {
                                forceFit: true,
                                autoFill:true
                            },
                            tbar: [{
                                text: 'add treatment',
                                cls: 'x-btn-text-icon',
                                icon:'static/repo/images/add.gif',
                                handler : function(){
                                   MA.CRUDSomething('create/treatment/', {'experiment_id':MA.CurrentExperimentId(), 'name':'Unknown'}, function() { var expId = MA.CurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/experiment__id/' + expId;
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
                                   MA.CRUDSomething('delete/treatment/'+delIds[i], {}, function() { var expId = MA.CurrentExperimentId(); treatmentStore.proxy.conn.url = wsBaseUrl + 'records/treatment/experiment__id/' + expId;
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
                            }), dataIndex:'name' }]
                      }
                    ]
                }
            ]
        }
    ]
};