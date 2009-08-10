Ext.madasSamplePrepInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    
    sopStore.proxy.conn.url = wsBaseUrl + 'records/standardoperationprocedure/experiments__id/' + expId;
    sopStore.load();
}

Ext.madasSaveSOPRow = function(changes) {
    
    if (changes.originalValue !== undefined && changes.originalValue != "" && changes.originalValue !== null && changes.originalValue != 0) {
        Ext.madasCRUDSomething('dissociate/standardoperationprocedure/experiment/'+changes.value+'/'+Ext.madasCurrentExperimentId(), {}, Ext.madasNull);
    }
    Ext.madasCRUDSomething('associate/standardoperationprocedure/experiment/'+changes.value+'/'+Ext.madasCurrentExperimentId(), {}, Ext.madasSamplePrepInit);
};

Ext.madasRemoveSOPRow = function(rec) {
    if (rec !== undefined && rec.data !== undefined && rec.data.id !== undefined && rec.data.id !== '') {
        Ext.madasCRUDSomething('dissociate/standardoperationprocedure/experiment/'+rec.data.id+'/'+Ext.madasCurrentExperimentId(), {}, Ext.madasSamplePrepInit);
    } else {
        sopStore.remove(rec);
    }
};

Ext.madasSamplePrep = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'sample preparation',
            region: 'center',
            collapsible: false,
            autoScroll:true,
            layout:'form',
            minSize: 75,
            items: [ 
                { xtype:'editorgrid', 
                    id:'standop',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'standard operating procedures used',
                    width:500,
                    height:200,
                    border: true,
                    trackMouseOver: false,
                    sm: new Ext.grid.RowSelectionModel(),
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    tbar: [{
                        text: 'add SOP',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/add.gif',
                        handler : function(){
                                sopStore.add(new Ext.data.Record({'id':'', 'description':''}));
                            }
                        },
                        {
                        text: 'remove SOP',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/no.gif',
                        handler : function(){
                            var grid = Ext.getCmp('standop');
                            var store = Ext.StoreMgr.get('sopStore');
                            
                            var selections = grid.getSelectionModel().getSelections();
                            
                            for (var index in selections) {
                                Ext.madasRemoveSOPRow(selections[index]);
                            }
                        }
                        }
                    ],
                    columns: [
                        { header: "SOP",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:false,
                                forceSelection:true,
                                displayField:'value',
                                valueField:'key',
                                lazyRender:true, 
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: sopComboStore,
                                listeners:{'selectionchange':function() { }}
                            }), dataIndex:'id', renderer: renderSOPLabel },
                        { header: "description", sortable:false, menuDisabled:true, dataIndex:'id', renderer: renderSOPDescription }
                    ],
                    listeners: {'afteredit':function(e) { Ext.madasSaveSOPRow(e); }},
                    store: sopStore
                }
//                },
//                { xtype: 'textfield', fieldLabel: 'weight' },
//                { xtype: 'checkbox', fieldLabel: 'dry weight?' }
            ]
        }
    ]
};
