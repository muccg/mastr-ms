MA.SamplePrepInit = function() {
    sopStore.load({ params: { experiments__id: MA.CurrentExperimentId() } });
};

MA.SaveSOPRow = function(changes) {
    
    if (changes.originalValue !== undefined && changes.originalValue !== "" && changes.originalValue !== null && changes.originalValue !== 0) {
        MA.CRUDSomething('dissociate/standardoperationprocedure/experiment/'+changes.value+'/'+MA.CurrentExperimentId(), {}, MA.Null);
    }
    MA.CRUDSomething('associate/standardoperationprocedure/experiment/'+changes.value+'/'+MA.CurrentExperimentId(), {}, MA.SamplePrepInit);
};

MA.RemoveSOPRow = function(rec) {
    if (rec !== undefined && rec.data !== undefined && rec.data.id !== undefined && rec.data.id !== '') {
        MA.CRUDSomething('dissociate/standardoperationprocedure/experiment/'+rec.data.id+'/'+MA.CurrentExperimentId(), {}, MA.SamplePrepInit);
    } else {
        sopStore.remove(rec);
    }
};

MA.SamplePrep = {
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
                        text: 'choose an SOP',
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
                                MA.RemoveSOPRow(selections[index]);
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
                    listeners: {'afteredit':function(e) { MA.SaveSOPRow(e); }},
                    store: sopStore
                }
//                },
//                { xtype: 'textfield', fieldLabel: 'weight' },
//                { xtype: 'checkbox', fieldLabel: 'dry weight?' }
            ]
        }
    ]
};
