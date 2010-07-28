MA.TrackingSm = new Ext.grid.CheckboxSelectionModel({ width: 25 });

MA.SampleTrackingInit = function() {
    var expId = MA.ExperimentController.currentId();
    
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
    MA.SampleLogLoad();
    
//    Ext.getCmp('sampleTracking').tbar.setWidth(800);
//    Ext.getCmp('sampleTracking').topToolbar.setSize(800);
};

MA.SampleLogLoad = function () {
    sampleLogStore.load({ params: { sample__experiment__id__exact: MA.ExperimentController.currentId() } });
};

MA.SampleLogSuccess = function() {
    MA.SampleLoadByExperiment();
    MA.SampleLogLoad();
};

MA.SampleTracking = {
    title: 'Sample Tracking',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;background:transparent;',
    layout:'anchor',
    autoScroll:true,
    items: [
            { 
            xtype:'fieldset', 
            bodyStyle:'padding:15px;background:transparent;padding-bottom:0px;',
            border:false,
            autoHeight:true,
            items: [
                    { xtype:'displayfield', fieldLabel:'Experiment name', id:'trackingExperimentName'},
                    { xtype:'displayfield', fieldLabel:'Comment', id:'trackingExperimentComment', width:400, height:40 },
                    { xtype:'displayfield', fieldLabel:'Formal quote', id:'trackingFormalQuote' },
                    { xtype:'displayfield', fieldLabel:'Organisation', id:'trackingOrg'},
                    { xtype:'displayfield', fieldLabel:'Job number', id:'trackingJobNumber' }
                ]
            },
            {
            xtype:'grid',
            border: true,
            title:'Samples',
            style: 'padding-left:3%;padding-right:3%;padding-bottom:10px;',
            height: 300,
            id:'sampleTracking',
            trackMouseOver: false,
            sm: MA.TrackingSm,
            width:800,
//            collapsible:true,
//            collapsed:true,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            tbar: {
                items: [
                    { xtype:'tbtext', text:'Mark Selected Samples as ' },
                    { xtype: 'tbspacer', width: 15 },
                    { 
                        xtype: 'combo', width:120,
                        id:'sampleLogType',
                        name:'sampleLogTypeText',
                        forceSelection:true,
                        displayField:'value',
                        valueField:'key',
                        hiddenName:'sampleLogTypeValue',
                        value:'1',
                        mode:'local',
                        allowBlank:false,
                        editable:false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        store: new Ext.data.ArrayStore({
                                                   fields: ['value', 'key'],
                                                   data : [['Received', 0],
                                                           ['Stored', 1],
                                                           ['Prepared', 2],
                                                           ['Acquired', 3],
                                                           ['Data Processed', 4]]
                                                   })
                        },
                    { xtype: 'tbspacer', width: 115 },
                    { xtype:'textfield', id:'sampleLogComment', width:200 },
                    { xtype: 'tbspacer', width: 15 },
                    { 
                        text:'Save',
                        cls: 'x-btn-text-icon',
                        icon: 'static/repo/images/save.png',
                        listeners: {
                            'click': function(e) {
                                //save changes to selected entries
                                if (MA.TrackingSm.getCount() > 0) {
                                    var logType = Ext.getCmp('sampleLogType').getValue();
                                    var comment = Ext.getCmp('sampleLogComment').getValue();
                                    
                                    var selections = MA.TrackingSm.getSelections();
                                    
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
                                        wsBaseUrl + 'batchcreate/samplelog/?type='+escape(logType)+'&description='+escape(comment)+'&sample_ids='+escape(ids.join(",")), 
                                        { 
                                            asynchronous:true, 
                                            evalJSON:'force',
                                            onSuccess:     MA.SampleLogSuccess
                                        });
                                }
                            }
                        }
                    }
                ]
            },
            columns: [
                      MA.TrackingSm,
                      { header: "ID", sortable:true, menuDisabled:true, dataIndex:'id' },
                      { header: "Label", sortable:true, menuDisabled:true, dataIndex:'label' },
                      { header: "Weight", sortable:true, menuDisabled:true, dataIndex:'weight' },
                      { header: "Comment", sortable:true, menuDisabled:true, width:300, dataIndex:'comment' },
                      { header: "Class", sortable:true, menuDisabled:true, dataIndex:'sample_class', renderer:renderClass },
                      { header: "Last Status", sortable:true, menuDisabled:true, width:300, dataIndex:'last_status' }
                      ],
            store: sampleStore
            },
            {
            xtype:'grid',
            border: true,
            title:'Sample Log',
            style: 'padding-left:3%;padding-right:3%;',
            height: 200,
            width:800,
            id:'sampleTrackingLog',
            trackMouseOver: false,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            columns: [
                      { header: "ID", sortable:true, menuDisabled:true, dataIndex:'id' },
                      { header: "Date", sortable:true, menuDisabled:true, dataIndex:'changetimestamp' },
                      { header: "User", sortable:true, menuDisabled:true, width:300, dataIndex:'user', renderer:renderUser },
                      { header: "Sample", sortable:true, menuDisabled:true, width:300, dataIndex:'sample' },
                      { header: "Type", sortable:true, menuDisabled:true, dataIndex:'type', renderer:renderSampleLogType },
                      { header: "Description", sortable:true, menuDisabled:true, dataIndex:'description' }
                      ],
            store: sampleLogStore
            }
            ]
};
