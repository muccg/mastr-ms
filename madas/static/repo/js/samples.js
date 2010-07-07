MA.ExperimentSamplesInit = function() {
    var expId = MA.CurrentExperimentId();
    
    sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
    sampleClassStore.load();
    
    sampleStore.removeAll();
};

MA.SampleLoadByExperiment = function () {
    sampleStore.load({ params: { experiment__id__exact: MA.CurrentExperimentId() } });
};

MA.SampleLoadBySampleClass = function () {
    sampleStore.load({ params: { sample_class__id__exact: MA.CurrentSampleClassId() } });
};

MA.SaveSampleRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    if (rec.data.weight == '') {
        rec.data.weight = '0.00';
    }
    
    bundledData.label = rec.data.label;
    bundledData.comment = rec.data.comment;
    bundledData.weight = rec.data.weight;
    
    MA.SaveRowLiterals('sample', roweditor, bundledData, rec, i, MA.SampleLoadBySampleClass);
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
            title: 'Sample Classes',
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
                    sm: new Ext.grid.RowSelectionModel({
                                                       listeners:{'rowselect':function(sm, idx, rec) {
                                                       MA.CurrentSampleClassIdValue = rec.data.id;
                                                       
                                                      MA.SampleLoadBySampleClass();
                                                       
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
                        text: 'Enable/Disable Sample Class',
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
                        { xtype: "tbseparator" },
                        {
                            text:'Create',
                            cls: 'x-btn-text-icon',
                            icon: 'static/repo/images/create-samples.png',
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
                                        MA.CRUDSomething('create/sample/', {'sample_class_id':selIds[i], 'experiment_id':MA.CurrentExperimentId()}, function() { var sm = Ext.getCmp('sampleClasses').getSelectionModel(); var selected = sm.getSelected(); sm.clearSelections(); sm.selectRecords([selected]);  MA.ExperimentSamplesInit(); });
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
                            html:' Samples for Selected Classes',
                            border:false,
                            bodyStyle:'background:transparent;padding:4px; color: #333'
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
                        { header: "ID", sortable:true, dataIndex:"id" },
                        { header: "Class", sortable:true, editor:new Ext.form.TextField(), dataIndex:"class_id" },
                        { header: "Samples", sortable:true, dataIndex:"count" },
                              { header: "Treatment Variation", sortable:true, dataIndex:"treatment" },
                              { header: "Timeline", sortable:true, dataIndex:"timeline" },
                              { header: "Organ", sortable:true, dataIndex:"organ" }
                      ],
                    store: sampleClassStore
                }
            ]
        },
        {
            title: 'Samples',
            region: 'center',
            cmargins: '0 0 0 0',
            collapsible: false,
            bodyStyle: 'padding:0px;',
            layout:'fit',
            tbar: [
                {
                    text: 'Add Sample',
                    cls: 'x-btn-text-icon',
                    disabled: true,
                    id: 'addsamplebutton',
                    icon: 'static/repo/images/add.png',
                    handler: function () {
                        MA.CRUDSomething('create/sample/', {
                            'sample_class_id': MA.CurrentSampleClassId(),
                            'experiment_id': MA.CurrentExperimentId()
                        }, function () {
                            MA.SampleLoadBySampleClass();
                            MA.ExperimentSamplesInit();
                        });
                    }
                },
                {
                    text: 'Remove Sample',
                    cls: 'x-btn-text-icon',
                    disabled: true,
                    id: 'removesamplebutton',
                    icon: 'static/repo/images/delete.png',
                    handler: function () {
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
                            MA.CRUDSomething("delete/sample/" + delIds[i], {}, function () {
                                MA.SampleLoadBySampleClass();
                                MA.ExperimentSamplesInit();
                            });
                        }
                    }
                },
                { xtype: "tbseparator" },
                {
                    text: 'Add Selected Samples to Run',
                    cls: 'x-btn-text-icon',
                    icon: 'static/repo/images/add-to-run.png',
                    handler: function() {
                        //save changes to selected entries
                        var grid = Ext.getCmp('samples');
                        var selections = grid.getSelectionModel().getSelections();
        
                        if (!Ext.isArray(selections)) {
                            selections = [selections];
                        }
        
                        if (selections.length > 0) {
                            
                            var ids = [];
                            for (var idx in selections) {
                                if (!Ext.isObject(selections[idx])) {
                                    continue;
                                }
                                
                                ids.push(selections[idx].data.id);
                            }
                            
                            Ext.getCmp("runDetails").addSample(ids);

                            MA.RunCmp.show();
                        }
                    }
                }
            ],
            items: [
                {
                    xtype:'grid',
                    border: false,
                    id:'samples',
                    loadMask:true,
                    trackMouseOver: false,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
//                    autoHeight:true,
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    columns: [
                        { header: "ID", sortable:true, dataIndex:'id' },
                        { header: "Label", sortable:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                          { header: "Weight", sortable:true, editor:new Ext.form.NumberField({editable:true, maxValue:9999.99}), dataIndex:'weight' },
                        { header: "Comment", sortable:false, sortable:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' }
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
    
    MA.SampleLoadByExperiment();
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
    
    MA.SaveRowLiterals('sample', roweditor, bundledData, rec, i, MA.SampleLoadByExperiment);
};

MA.ExperimentSamplesOnly = {
    title: 'Samples',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [
        {
            text: 'Add Sample',
            cls: 'x-btn-text-icon',
            id: 'addsamplesbutton',
            icon: 'static/repo/images/add.png',
            handler: function () {
                MA.CRUDSomething('create/sample/', {'experiment_id':MA.CurrentExperimentId()}, MA.SampleLoadByExperiment);
            }
        },
        {
            text: 'Remove Sample',
            cls: 'x-btn-text-icon',
            id: 'removesamplesbutton',
            icon: 'static/repo/images/delete.png',
            handler: function () {
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
                    MA.CRUDSomething("delete/sample/" + delIds[i], {}, MA.SampleLoadByExperiment);
                }
            }
        }
//           },
//           {
//               text: 'View Sample Log',
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
            xtype:'grid',
            border: false,
            id:'samplesOnly',
            trackMouseOver: false,
            loadMask:true,
            plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleOnlyRow}})],
            sm: new Ext.grid.RowSelectionModel(),
            //                    autoHeight:true,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            columns: [
                      { header: "ID", sortable:true, dataIndex:'id' },
                      { header: "Label", sortable:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                      { header: "Weight", sortable:true, editor:new Ext.form.NumberField({editable:true, maxValue:9999.99}), dataIndex:'weight' },
                      { header: "Comment", sortable:false, sortable:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' },
                      { header: "Class", sortable:true, dataIndex:'sample_class', editor:new Ext.form.ComboBox({
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
                      { header: "Last Status", sortable:true, width:300, dataIndex:'last_status' }
                      ],
            store: sampleStore
            }
            ]
};
