Ext.madasExperimentSamplesInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    
    sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
    sampleClassStore.load();
};

Ext.madasSaveSampleRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.label = rec.data.label;
    bundledData.comment = rec.data.comment;
    
    Ext.madasSaveRowLiterals('sample', roweditor, bundledData, rec, i, function() { var scId = Ext.madasCurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId; sampleStore.load();});
};

Ext.madasExperimentSamples = {
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
                    sm: new Ext.grid.RowSelectionModel({
                                                       listeners:{'rowselect':function(sm, idx, rec) {
                                                       sampleStore.proxy.conn.url = wsBaseUrl + "records/sample/sample_class__id/" + rec.data.id;
                                                       sampleStore.load();
                                                       
                                                       Ext.madasCurrentSampleClassIdValue = rec.data.id;
                                                       
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
                                                       Ext.madasCurrentSampleClassIdValue = undefined;
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
                           Ext.madasCRUDSomething('sample_class_enable/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
                                                  sampleClassStore.load(); });
                           }
                           
                        }
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
                        { header: "id",  sortable:false, menuDisabled:true, dataIndex:"id" },
                        { header: "Class",  sortable:false, menuDisabled:true, dataIndex:"class_id" },
                              { header: "Treatment Variation",  sortable:false, menuDisabled:true, dataIndex:"treatments" },
                              { header: "Timeline",  sortable:false, menuDisabled:true, dataIndex:"timeline" },
                              { header: "Origin",  sortable:false, menuDisabled:true, dataIndex:"origin" },
                              { header: "Organ",  sortable:false, menuDisabled:true, dataIndex:"organ" },
                              { header: "Genotype",  sortable:false, menuDisabled:true, dataIndex:"genotype"}
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
                   Ext.madasCRUDSomething('create/sample/', {'sample_class_id':Ext.madasCurrentSampleClassId()}, function() { var scId = Ext.madasCurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId;
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
                   Ext.madasCRUDSomething('delete/sample/'+delIds[i], {}, function() { var scId = Ext.madasCurrentSampleClassId(); sampleStore.proxy.conn.url = wsBaseUrl + 'records/sample/sample_class__id/' + scId;
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
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveSampleRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
//                    autoHeight:true,
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    columns: [
                        { header: "id", sortable:false, menuDisabled:true, dataIndex:'id' },
                        { header: "label", sortable:false, menuDisabled:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                        { header: "comment", sortable:false, menuDisabled:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' }
                    ],
                    store: sampleStore
                }
            ]
        }
    ]
};