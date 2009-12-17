Ext.madasTrackingSm = new Ext.grid.CheckboxSelectionModel({ width: 25 });

Ext.madasSampleLogSuccess = function() {
    //something
    var expId = Ext.madasCurrentExperimentId();
    
    sampleStore.proxy.conn.url = wsBaseUrl + 'recordsSamples/experiment__id/' + expId;
    sampleStore.load();
};

Ext.madasSampleTracking = {
    title: 'sample tracking',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    bodyStyle: 'padding:0px;background:transparent;',
    layout:'fit',
    items: [
            { 
            xtype:'fieldset', 
            bodyStyle:'padding:15px;background:transparent;',
            border:false,
            autoHeight:true,
            items: [
                    { xtype:'textfield', fieldLabel:'experiment name', id:'trackingExperimentName', disabled:true},
                    { xtype:'textarea', fieldLabel:'comment', id:'trackingExperimentComment', width:400, disabled:true },
                    { xtype:'textfield', fieldLabel:'formal quote', id:'trackingFormalQuote', disabled:true },
                    { xtype:'displayfield', fieldLabel:'organisation', id:'trackingOrg'},
                    { xtype:'textfield', fieldLabel:'job number', id:'trackingJobNumber', disabled:true }
                ]
            },
            {
            xtype:'grid',
            border: true,
            title:'samples',
            style: 'padding-left:3%;padding-right:3%;',
            height: 400,
            id:'sampleTracking',
            trackMouseOver: false,
            sm: Ext.madasTrackingSm,
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
                                if (Ext.madasTrackingSm.getCount() > 0) {
                                    var logType = Ext.getCmp('sampleLogType').getValue();
                                    var comment = Ext.getCmp('sampleLogComment').getValue();
                                    
                                    var selections = Ext.madasTrackingSm.getSelections();
                                    
                                    if (!Ext.isArray(selections)) {
                                        selections = [selections];
                                    }
                                    
                                    for (var idx in selections) {
                                        if (!Ext.isObject(selections[idx])) {
                                            continue;
                                        }
                                    
                                        var saver = new Ajax.Request(
                                            wsBaseUrl + 'create/samplelog/?type='+escape(logType)+'&description='+escape(comment)+'&sample_id='+escape(selections[idx].data.id), 
                                            { 
                                                asynchronous:true, 
                                                evalJSON:'force',
                                                onSuccess:     Ext.madasSampleLogSuccess
                                            });
                                    }
                                }
                            }
                        }
                    }
                ]
            },
            columns: [
                      Ext.madasTrackingSm,
                      { header: "id", sortable:true, menuDisabled:true, dataIndex:'id' },
                      { header: "label", sortable:true, menuDisabled:true, dataIndex:'label' },
                      { header: "weight", sortable:true, menuDisabled:true, dataIndex:'weight' },
                      { header: "comment", sortable:true, menuDisabled:true, width:300, dataIndex:'comment' },
                      { header: "class", sortable:true, menuDisabled:true, dataIndex:'sample_class', renderer:renderClass },
                      { header: "last status", sortable:true, menuDisabled:true, width:300, dataIndex:'last_status' }
                      ],
            store: sampleStore
            }
            ]
};