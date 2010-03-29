MA.ExperimentSamplesInit = function() {
    var expId = MA.CurrentExperimentId();
    
    sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
    sampleClassStore.load();
    
    sampleStore.removeAll();
};

MA.SaveSampleRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    if (rec.data.weight == '') {
        rec.data.weight = '0.00';
    }
    
    bundledData.label = rec.data.label;
    bundledData.comment = rec.data.comment;
    bundledData.weight = rec.data.weight;
    
    MA.SaveRowLiterals('sample', roweditor, bundledData, rec, i, function() { var scId = MA.CurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId; sampleStore.load();});
};

MA.SaveSampleClassRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.class_id = rec.data.class_id;

    MA.SaveRowLiterals('sampleclass', roweditor, bundledData, rec, i, MA.ExperimentSamplesInit);
};

MA.ExperimentSamples = {
    baseCls: 'x-plain',
    border:'false',
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'sample classes',
            region: 'north',
            bodyStyle:'padding:0px;background:transparent;',
            collapsible: false,
            layout:'fit',
            height:200,
            split: true,
            minSize: 155,
            items: [
                {
                    xtype:'grid',
                    border: false,
                    id:'sampleClasses',
                    trackMouseOver: false,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleClassRow}})],
                    sm: new Ext.grid.RowSelectionModel({
                                                       listeners:{'rowselect':function(sm, idx, rec) {
                                                       sampleStore.proxy.conn.url = wsBaseUrl + "records/sample/sample_class__id/" + rec.data.id;
                                                       sampleStore.load();
                                                       
                                                       MA.CurrentSampleClassIdValue = rec.data.id;
                                                       
                                                       var grid = Ext.getCmp("samples");
                                                       grid.enable();
                                                       Ext.getCmp('addsamplebutton').enable();
                                                       Ext.getCmp('removesamplebutton').enable();
                                                       },
                                                       'selectionchange':{buffer:10, fn:function(sm) {
                                                       var grid;
                                                       if (! sm.hasSelection()) {
                                                            grid = Ext.getCmp("samples");
                                                       grid.disable();
                                                       Ext.getCmp('addsamplebutton').disable();
                                                       Ext.getCmp('removesamplebutton').disable();
                                                       MA.CurrentSampleClassIdValue = undefined;
                                                       }
                                                       }}                        }
                    }),
                    tbar: [{
                        text: 'enable/disable sample class',
                        handler : function(){
                           var grid = Ext.getCmp('sampleClasses');
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
                           MA.CRUDSomething('sample_class_enable/'+delIds[i], {}, function() { var expId = MA.CurrentExperimentId(); sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
                                                  sampleClassStore.load(); });
                           }
                           
                        }
                        },
                        {
                            text:' create ',
                            handler: function() {
                                var reps = Ext.getCmp('replicateField').getValue();
                                
                                var grid = Ext.getCmp('sampleClasses');
                                var selIds = []; 
                                
                                var selections = grid.getSelectionModel().getSelections();
                                if (!Ext.isArray(selections)) {
                                    selections = [selections];
                                }
                                
                                for (var index = 0; index < selections.length; index++) {
                                    if (!Ext.isObject(selections[index])) {
                                        continue;
                                    }
                                    
                                    selIds.push(selections[index].data.id);
                                }
                                
                                for (var i = 0; i < selIds.length; i++) {
                                    for (var j = 0; j < reps; j++) {
                                        MA.CRUDSomething('create/sample/', {'sample_class_id':selIds[i], 'experiment_id':MA.CurrentExperimentId()}, function() { var sm = Ext.getCmp('sampleClasses').getSelectionModel(); var selected = sm.getSelected(); sm.clearSelections(); sm.selectRecords([selected]); });
                                    }
                                }
                            }
                        },
                        {
                            xtype:'numberfield',
                            id:'replicateField',
                            value:'6',
                            width:28
                        },
                        {
                            xtype:'panel',
                            html:' samples for selected classes ',
                            border:false,
                            bodyStyle:'background:transparent;padding:4px;'
                        }
                    ],
                    viewConfig: {
                        forceFit: true,
                        autoFill:true,
                        getRowClass : function (row, index) { 
                            var cls = ''; 
                            var data = row.data;
                            //console.log(data);
                            if (data.enabled) { 
                                cls = ''; 
                            } else {
                                cls = 'x-row-gray'; 
                            }//end switch 
                            return cls; 
                        }
                    },
                    columns: [
                        { header: "id", sortable:true, dataIndex:"id" },
                        { header: "Class", sortable:true, editor:new Ext.form.TextField(), dataIndex:"class_id" },
                              { header: "Treatment Variation", sortable:true, dataIndex:"treatment" },
                              { header: "Timeline", sortable:true, dataIndex:"timeline" },
                              { header: "Origin", sortable:true, dataIndex:"origin" },
                              { header: "Organ", sortable:true, dataIndex:"organ" }
                      ],
                    store: sampleClassStore
                }
            ]
        },
        {
            title: 'samples',
            region: 'center',
            cmargins: '0 0 0 0',
            collapsible: false,
            bodyStyle: 'padding:0px;',
            layout:'fit',
            tbar: [{
                text: 'add sample',
                cls: 'x-btn-text-icon',
                   disabled:true,
                   id:'addsamplebutton',
                icon:'static/repo/images/add.gif',
                handler : function(){
                   MA.CRUDSomething('create/sample/', {'sample_class_id':MA.CurrentSampleClassId(), 'experiment_id':MA.CurrentExperimentId()}, function() { var scId = MA.CurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId;
                                          sampleStore.load(); });
                   }
                },
                {
                text: 'remove sample',
                cls: 'x-btn-text-icon',
                   disabled:true,
                   id:'removesamplebutton',
                icon:'static/repo/images/no.gif',
                handler : function(){
                   var grid = Ext.getCmp('samples');
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
                   MA.CRUDSomething('delete/sample/'+delIds[i], {}, function() { var scId = MA.CurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId;
                                          sampleStore.load(); });
                   }                        }
                }
            ],
            items: [
                {
                    xtype:'editorgrid',
                    border: false,
                    id:'samples',
                    trackMouseOver: false,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
//                    autoHeight:true,
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    columns: [
                        { header: "id", sortable:true, dataIndex:'id' },
                        { header: "label", sortable:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                          { header: "weight", sortable:true, editor:new Ext.form.NumberField({editable:true, maxValue:9999.99}), dataIndex:'weight' },
                        { header: "comment", sortable:false, sortable:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' }
                    ],
                    store: sampleStore
                }
            ]
        }
    ]
};

MA.ExperimentSamplesOnlyInit = function() {
    var expId = MA.CurrentExperimentId();
    
    var classLoader = new Ajax.Request(wsBaseUrl + 'populate_select/sampleclass/id/class_id/experiment__id/'+escape(expId), 
                                     { 
                                     asynchronous:false, 
                                     evalJSON:'force',
                                     onSuccess: function(response) {
                                         var classComboStore = Ext.StoreMgr.get('classCombo');
                                         var data = response.responseJSON.response.value.items;
                                         var massagedData = [];

                                         for (var idx in data) {
                                             massagedData[idx] = [data[idx]['key'], data[idx]['value']];
                                         }
                                         
                                         classComboStore.loadData(massagedData);
                                         }
                                     }
                                     );
    
    sampleStore.proxy.conn.url = wsBaseUrl + 'recordsSamples/experiment__id/' + expId;
    sampleStore.load();
};

MA.SaveSampleOnlyRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.label = rec.data.label;
    bundledData.comment = rec.data.comment;
    if (rec.data.weight == '') {
        rec.data.weight = '0.00';
    }
    bundledData.weight = rec.data.weight;
    bundledData.sample_class_id = rec.data.sample_class;
    
    MA.SaveRowLiterals('sample', roweditor, bundledData, rec, i, function() { var eId = MA.CurrentExperimentId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/experiment__id/' + eId;
                             sampleStore.load();});
};

MA.ExperimentSamplesOnly = {
    title: 'samples',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [{
           text: 'add sample',
           cls: 'x-btn-text-icon',
           id:'addsamplesbutton',
           icon:'static/repo/images/add.gif',
           handler : function(){
           MA.CRUDSomething('create/sample/', {'experiment_id':MA.CurrentExperimentId()}, function() { var eId = MA.CurrentExperimentId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/experiment__id/' + eId;
                                  sampleStore.load(); });
           }
           },
           {
           text: 'remove sample',
           cls: 'x-btn-text-icon',
           id:'removesamplesbutton',
           icon:'static/repo/images/no.gif',
           handler : function(){
           var grid = Ext.getCmp('samplesOnly');
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
           MA.CRUDSomething('delete/sample/'+delIds[i], {}, function() { var eId = MA.CurrentExperimentId(); sampleStore.proxy.conn.url = wsBaseUrl + 'recordsSamples/experiment__id/' + eId;
                                  sampleStore.load(); });
           }                        }
           }
//           },
//           {
//               text: 'view sample log',
//               cls: 'x-btn-text-icon',
//               id:'viewsamplelogbutton',
//               icon:'static/repo/images/s.gif',
//               handler : function(){
//                   var grid = Ext.getCmp('samplesOnly');
//                   var delIds = []; 
//                   
//                   var selections = grid.getSelectionModel().getSelections();
//                   if (!Ext.isArray(selections)) {
//                       selections = [selections];
//                   }
//                   
//                   for (var index = 0; index < selections.length; index++) {
//                       if (!Ext.isObject(selections[index])) {
//                           continue;
//                       }
//                       
//                       delIds.push(selections[index].data.id);
//                   }
//                   
//                   for (var i = 0; i < delIds.length; i++) {
        //           MA.CRUDSomething('delete/sample/'+delIds[i], {}, function() { var eId = MA.CurrentExperimentId(); sampleStore.proxy.conn.url = wsBaseUrl + 'recordsSamples/experiment__id/' + eId;
        //                                  sampleStore.load(); });
//                   }
//               }
//           }
           ],
    items: [
            {
            xtype:'editorgrid',
            border: false,
            id:'samplesOnly',
            trackMouseOver: false,
            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleOnlyRow}})],
            sm: new Ext.grid.RowSelectionModel(),
            //                    autoHeight:true,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            columns: [
                      { header: "id", sortable:true, dataIndex:'id' },
                      { header: "label", sortable:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                      { header: "weight", sortable:true, editor:new Ext.form.NumberField({editable:true, maxValue:9999.99}), dataIndex:'weight' },
                      { header: "comment", sortable:false, sortable:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' },
                      { header: "class", sortable:true, dataIndex:'sample_class', editor:new Ext.form.ComboBox({
                               editable:true,
                               forceSelection:false,
                               displayField:'value',
                               valueField:'key',
                               lazyRender:true,
                               allowBlank:true,
                               typeAhead:false,
                               triggerAction:'all',
                               listWidth:230,
                               mode:'local',
                               store: new Ext.data.ArrayStore({storeId:'classCombo', fields: ['key', 'value']})                               }),
                      renderer:renderClass },
                      { header: "last status", sortable:true, width:300, dataIndex:'last_status' }
                      ],
            store: sampleStore
            }
            ]
};