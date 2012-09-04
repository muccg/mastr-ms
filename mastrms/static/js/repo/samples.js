MA.ExperimentSamplesInit = function() {
    var expId = MA.ExperimentController.currentId();
    
    sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
    sampleClassStore.load();
    
    sampleStore.removeAll();
    randomisableSampleStore.removeAll();
};

MA.SampleLoadByExperiment = function (randomise) {
    var params = { experiment__id__exact: MA.ExperimentController.currentId() };
    if (typeof(randomise) !== 'undefined' && randomise === true) {
        params.randomise = true;
    }
    randomisableSampleStore.load({ params: params});
    // lastOptions will be used again when sorting by header click etc. so we 
    // have to remove randomise or all consequent responses will be randomised
    var lastOptions = randomisableSampleStore.lastOptions;
    delete lastOptions.params.randomise;
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
                    loadMask:true,
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
                    tbar: [
                        {
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
                               MA.CRUDSomething('sample_class_enable/'+delIds[i], {}, function() { var expId = MA.ExperimentController.currentId(); sampleClassStore.proxy.conn.url = wsBaseUrl + 'recreate_sample_classes/' + expId;
                                                      sampleClassStore.load(); });
                               }
                               
                            }
                        }
                    ],
                    bbar: [
                        {
                            text:'Create',
                            cls: 'x-btn-text-icon',
                            icon: 'static/images/create-samples.png',
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
                                    MA.CRUDSomething('createSamples/', {'sample_class_id':selIds[i], 'experiment_id':MA.ExperimentController.currentId(), 'replicates':reps}, function() { var sm = Ext.getCmp('sampleClasses').getSelectionModel(); var selected = sm.getSelected(); sm.clearSelections(); sm.selectRecords([selected]);  MA.ExperimentSamplesInit(); });
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
                    icon: 'static/images/add.png',
                    handler: function () {
                        MA.CRUDSomething('create/sample/', {
                            'sample_class_id': MA.CurrentSampleClassId(),
                            'experiment_id': MA.ExperimentController.currentId()
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
                    icon: 'static/images/delete.png',
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
                    icon: 'static/images/add-to-run.png',
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
                            
                            Ext.getCmp("runDetails").clearSamples();
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
                    plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
//                    autoHeight:true,
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    columns: [
                        { header: "ID", sortable:true, dataIndex:'id' },
                        { header: "Seq", sortable:true, dataIndex:'sample_class_sequence' },
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
    var expId = MA.ExperimentController.currentId();
    
    var classLoader = new Ajax.Request(wsBaseUrl + 'populate_select/sampleclass/id/class_id/experiment__id/'+encodeURIComponent(expId), 
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

MA.SampleCSVUploadForm = new Ext.Window({
    title: 'Upload CSV of Samples',
    closeAction:'hide',
    width:300,
    height:200,
    minHeight:200,
    minWidth:300,
    id:'sampleCSVUploadWindow',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    
    items:[
        {
            id:'sampleCSVUpload',
            xtype:'form',
            fileUpload: true,
            url: wsBaseUrl + 'uploadSampleCSV',
            waitTitle: 'Uploading...',
            border:false,
            items:[
                { 
                    xtype: 'hidden',
                    name: 'experiment_id',
                    itemId: 'expIdField'
                },
                {
                    xtype: 'panel',
                    border: false,
                    bodyStyle:'padding:15px;background:transparent;',
                    html: 'Uploaded CSVs must be of the format:<br><br><code>label,weight,comment</code><br><br>'
                },
                {
                    xtype: 'fileuploadfield',
                    itemId: 'samplecsvupload',
                    emptyText: '',
                    fieldLabel: 'File',
                    name: 'samplecsv'
                }
            ]
        }
    ],
    buttons: [
        {
            text: 'Upload',
            itemId:'csvUploadBtn',
            handler: function(){
                Ext.getCmp('sampleCSVUpload').getComponent('expIdField').setValue( MA.ExperimentController.currentId() );
            
                Ext.getCmp('sampleCSVUpload').getForm().submit(
                    {   
                        successProperty: 'success',        
                        success: function (form, action) {
                            if (action.result.success === true) {
                                form.reset(); 
                                MA.ExperimentSamplesOnlyInit();
                                Ext.getCmp('sampleCSVUploadWindow').hide();
                            } 
                        },
                        failure: function (form, action) {
                            //do nothing special. this gets called on validation failures and server errors
                            MA.ExperimentSamplesOnlyInit();
                            alert('Error processing CSV. Some lines were not imported as they did not seem to be formatted properly. Some samples may have been imported successfully.');
                        }
                    }
                );
            }
        }
    ]
});

var createSampleCSV = function(records){
    var csvtext = "<html><head></head><body>";
    var fields = [];
    if (records.length > 0)
    {
        var header = "# "
        //first write the header
        var r = records[0];
        for (var propname in r){
            fields.push(propname);
            header += propname + ", ";
        }
        
        csvtext += header + "</br>";

        for (var count=0; count < records.length; count++)
        {
            line = ""
            for (var fieldindex=0; fieldindex<fields.length; fieldindex++){
                line += records[count][fields[fieldindex]];
                if (fieldindex < fields.length-1){
                    line += ","
                }
            }
            csvtext += line + "</br>";       
        }
    }

    csvtext += "</body></html>";

    return csvtext;
};

var exportCSV = function(records){
    var csvtext = createSampleCSV(records);
    var expWindow = window.open('', '', 'width=600, height=600');
    var doc = expWindow.document;
    doc.open('text/html', true);
    doc.charset='utf-8';
    doc.write(csvtext);
    doc.close();
    //var fileName='experiment.csv';
    //doc.execCommand("SaveAs", null, fileName);
    

};


MA.ExperimentSamplesOnly = {
    id: 'samplesOnlyPanel',
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
            icon: 'static/images/add.png',
            handler: function () {
                MA.CRUDSomething('create/sample/', {'experiment_id':MA.ExperimentController.currentId()}, MA.SampleLoadByExperiment);
            }
        },
        {
            text: 'Remove Sample',
            cls: 'x-btn-text-icon',
            id: 'removesamplesbutton',
            icon: 'static/images/delete.png',
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
        },
        { xtype: "tbseparator" },
        {
            text: 'Upload CSV file',
            cls: 'x-btn-text-icon',
            id: 'uploadsamplesbutton',
            icon: 'static/images/add.png',
            handler: function () {
                MA.SampleCSVUploadForm.show();
            }
        },
        {
            text: 'Download CSV file',
            cls: 'x-btn-text-icon',
            id: 'downloadsamplesbutton',
            icon: 'static/images/arrow-down.png',
            handler: function () {
                var grid = Ext.getCmp('samplesOnly');
                var gridstore = grid.getStore();
                records = []
                gridstore.each(function(record){
                    //console.log("Record: " + record.id + "," + record.sample_id + "," + record.sample_class);
                    records.push(record.data)
                });

                    exportCSV(records);
                }
        },
        { xtype: "tbseparator" },
        {
            text: 'Add Selected Samples to Run',
            cls: 'x-btn-text-icon',
            icon: 'static/images/add-to-run.png',
            handler: function() {
                //save changes to selected entries
                var grid = Ext.getCmp('samplesOnly');
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
                    
                    Ext.getCmp("runDetails").clearSamples();
                    Ext.getCmp("runDetails").addSample(ids);
        
                    MA.RunCmp.show();
                }
            }
        },
        { xtype: "tbseparator" },
        {
            text: 'Randomise Samples',
            cls: 'x-btn-text-icon',
            icon: 'static/images/refresh.png',
            handler: function() {
                var grid = Ext.getCmp('samplesOnly');
                var sm = grid.getSelectionModel();
                sm.clearSelections();
                MA.SampleLoadByExperiment(true);
            }
        }
    ],
    items: [
            {
            xtype:'grid',
            border: false,
            id:'samplesOnly',
            trackMouseOver: false,
            loadMask:true,
            plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveSampleOnlyRow}})],
            sm: new Ext.grid.RowSelectionModel(),
            //                    autoHeight:true,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            columns: [
                      new Ext.grid.RowNumberer(),
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
                      { header: "Seq", sortable:false, dataIndex:'sample_class_sequence' },
                      { header: "Label", sortable:true, editor:new Ext.form.TextField(), dataIndex:'label' },
                      { header: "Weight", sortable:true, editor:new Ext.form.NumberField({editable:true, maxValue:9999.99}), dataIndex:'weight' },
                      { header: "Comment", sortable:true, sortable:true, width:300, editor:new Ext.form.TextField(), dataIndex:'comment' },
                      { header: "Last Status", sortable:true, width:300, dataIndex:'last_status' },
                      { header: "ID", sortable:true, dataIndex:'id' }
                      ],
            store: randomisableSampleStore
            }
            ]
};
