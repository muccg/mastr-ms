MA.TrackingSm = new Ext.grid.CheckboxSelectionModel({ width: 25 });

MA.SampleTrackingInit = function() {
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

    sampleLogStore.proxy.conn.url = wsBaseUrl + 'records/samplelog/sample__experiment__id/'+expId;
    sampleLogStore.load();
};

MA.SampleLogSuccess = function() {
    //something
    var expId = MA.CurrentExperimentId();
    
    sampleStore.proxy.conn.url = wsBaseUrl + 'recordsSamples/experiment__id/' + expId;
    sampleStore.load();
    
    sampleLogStore.load();
};

MA.SampleTracking = {
    title: 'sample tracking',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;background:transparent;',
    //layout:'fit',
    autoScroll:true,
    viewConfig: {
    forceFit: true,
    autoFill:true
    },
    items: [
            { 
            xtype:'fieldset', 
            bodyStyle:'padding:15px;background:transparent;padding-bottom:0px;',
            border:false,
            autoHeight:true,
            items: [
                    { xtype:'displayfield', fieldLabel:'experiment name', id:'trackingExperimentName'},
                    { xtype:'displayfield', fieldLabel:'comment', id:'trackingExperimentComment', width:400, height:40 },
                    { xtype:'displayfield', fieldLabel:'formal quote', id:'trackingFormalQuote' },
                    { xtype:'displayfield', fieldLabel:'organisation', id:'trackingOrg'},
                    { xtype:'displayfield', fieldLabel:'job number', id:'trackingJobNumber' }
                ]
            },
            {
            xtype:'grid',
            border: true,
            title:'samples',
            style: 'padding-left:3%;padding-right:3%;padding-bottom:10px;',
            height: 300,
            id:'sampleTracking',
            trackMouseOver: false,
            sm: MA.TrackingSm,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            tbar: {
                items: [
                    { xtype:'tbtext', text:'mark selected samples as ' },
                    { xtype: 'tbspacer', width: 15 },
                    { 
                        xtype: 'combo', 
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
                                                   data : [['Comment', 0],
                                                           ['Relocation', 1],
                                                           ['Method', 2]]
                                                   })
                        },
                    { xtype: 'tbspacer', width: 15 },
                    { xtype:'textfield', id:'sampleLogComment', width:200 },
                    { xtype: 'tbspacer', width: 15 },
                    { 
                        text:'save',
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
                      { header: "id", sortable:true, menuDisabled:true, dataIndex:'id' },
                      { header: "label", sortable:true, menuDisabled:true, dataIndex:'label' },
                      { header: "weight", sortable:true, menuDisabled:true, dataIndex:'weight' },
                      { header: "comment", sortable:true, menuDisabled:true, width:300, dataIndex:'comment' },
                      { header: "class", sortable:true, menuDisabled:true, dataIndex:'sample_class', renderer:renderClass },
                      { header: "last status", sortable:true, menuDisabled:true, width:300, dataIndex:'last_status' }
                      ],
            store: sampleStore
            },
            {
            xtype:'grid',
            border: true,
            title:'sample log',
            style: 'padding-left:3%;padding-right:3%;',
            height: 200,
            id:'sampleTrackingLog',
            trackMouseOver: false,
            viewConfig: {
            forceFit: true,
            autoFill:true
            },
            columns: [
                      { header: "id", sortable:true, menuDisabled:true, dataIndex:'id' },
                      { header: "date", sortable:true, menuDisabled:true, dataIndex:'changetimestamp' },
                      { header: "user", sortable:true, menuDisabled:true, width:300, dataIndex:'user', renderer:renderUser },
                      { header: "sample", sortable:true, menuDisabled:true, width:300, dataIndex:'sample' },
                      { header: "type", sortable:true, menuDisabled:true, dataIndex:'type', renderer:renderSampleLogType },
                      { header: "description", sortable:true, menuDisabled:true, dataIndex:'description' }
                      ],
            store: sampleLogStore
            }
            ]
};