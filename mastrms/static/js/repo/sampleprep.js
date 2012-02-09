MA.SamplePrepInit = function() {
    sopStore.load({ params: { experiments__id: MA.ExperimentController.currentId() } });
};

MA.SaveSOPRow = function(changes) {
    
    if (changes.originalValue !== undefined && changes.originalValue !== "" && changes.originalValue !== null && changes.originalValue !== 0) {
        MA.CRUDSomething('dissociate/standardoperationprocedure/experiment/'+changes.value+'/'+MA.ExperimentController.currentId(), {}, MA.Null);
    }
    MA.CRUDSomething('associate/standardoperationprocedure/experiment/'+changes.value+'/'+MA.ExperimentController.currentId(), {}, MA.SamplePrepInit);
};

MA.RemoveSOPRow = function(rec) {
    if (rec !== undefined && rec.data !== undefined && rec.data.id !== undefined && rec.data.id !== '') {
        MA.CRUDSomething('dissociate/standardoperationprocedure/experiment/'+rec.data.id+'/'+MA.ExperimentController.currentId(), {}, MA.SamplePrepInit);
    } else {
        sopStore.remove(rec);
    }
};

MA.DownloadSOPFile = function(sopID) {
    window.open(wsBaseUrl + "downloadSOPFileById/" + sopID);
};

function sopFileActionRenderer(val) {
    return '<a href="#" onclick="MA.DownloadSOPFile(\''+val+'\')">download</a>';
}

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
            title: 'Sample Preparation',
            region: 'center',
            collapsible: false,
            autoScroll:true,
            layout:'form',
            labelAlign: 'top',
            minSize: 75,
            items: [ 
                { xtype:'editorgrid', 
                    id:'standop',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'Standard Operating Procedures Used',
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
                        text: 'Choose a SOP',
                        cls: 'x-btn-text-icon',
                        icon:'static/images/add.png',
                        handler : function(){
                                sopStore.add(new Ext.data.Record({'id':'', 'description':''}));
                            }
                        },
                        {
                        text: 'Remove SOP',
                        cls: 'x-btn-text-icon',
                        icon:'static/images/delete.png',
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
                        { header: "Description", sortable:false, menuDisabled:true, dataIndex:'id', renderer: renderSOPDescription },
                        { header: "View", sortable:false, menuDisabled:false, dataIndex:'id', renderer: sopFileActionRenderer }
                    ],
                    listeners: {'afteredit':function(e) { MA.SaveSOPRow(e); }},
                    store: sopStore
                },{
                    id: 'samplePreparationNotes',
                    xtype: 'textarea',
                    fieldLabel: 'Notes',
                    autoScroll: true,
                    maxLength: 2000,
                    width: 500,
                    height: 200,
                    listeners: {
                        'change': function(field, newValue, oldValue) {
                            if (field.isValid()) {
                                MA.ExperimentController.updateSamplePreparationNotes(newValue);
                            }
                         } 
                    }
                }
                

//                },
//                { xtype: 'textfield', fieldLabel: 'Weight' },
//                { xtype: 'checkbox', fieldLabel: 'Dry weight?' }
            ]
        }
    ]
};
