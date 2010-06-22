MA.AccessInit = function() {
    userStore.load({ params: { experiment__id__exact: MA.CurrentExperimentId() } });
};

MA.SaveAccessRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.experiment_id = MA.CurrentExperimentId();
    bundledData.user_id = rec.data.user;
    bundledData.type_id = rec.data.type;
    bundledData.additional_info = rec.data.additional_info;
    
    MA.SaveRowLiterals('userexperiment', roweditor, bundledData, rec, i, MA.AccessInit);
};

MA.Access = {
    baseCls: 'x-plain',
    border:'false',
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'involved users',
            region: 'center',
            bodyStyle:'padding:0px;background:transparent;',
            collapsible: false,
            layout:'fit',
            items: [
                {
                    xtype:'editorgrid',
                    border: false,
                    id:'involvedUsersGrid',
                    trackMouseOver: false,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveAccessRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    tbar: [
                        {
                            text: 'add user',
                            cls: 'x-btn-text-icon',
                            icon: 'static/repo/images/add.gif',
                            handler: function(){
                                    userStore.add(new Ext.data.Record({'user':'', 'type':'1', 'additional_info':''}));
                            }
                        },
                        {
                            text: 'remove user',
                            cls: 'x-btn-text-icon',
                            icon: 'static/repo/images/no.gif',
                            handler: function(){
                                var grid = Ext.getCmp('involvedUsersGrid');
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
                               
                                //'unnecessary' reload to remove rows without id's
                                MA.AccessInit();
                               
                                for (var i = 0; i < delIds.length; i++) {
                                    if (Ext.isDefined(delIds[i])) {
                                        MA.CRUDSomething('delete/userexperiment/'+delIds[i], {}, MA.AccessInit);
                                    }
                                }
                            }
                        }
                    ],
                    viewConfig: {
                        forceFit: true
                    },
                    columns: [
                        { header: "name", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:false,
                                forceSelection:true,
                                displayField:'value',
                                valueField:'key',
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: userComboStore
                            }), dataIndex: 'user', renderer:renderUser },
                        { header: "involvement", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox(
                            {
                                editable:false,
                                allowBlank:false,
                                forceSelection:true,
                                displayField:'value',
                                valueField:'key',
                                disableKeyFilter:true,
                                triggerAction:'all',
                                store: involvementComboStore
                            }
                            ),
                            dataIndex:'type', renderer:renderInvolvement
                        },
                        { header: "additional info", sortable:false, menuDisabled:true, editor:new Ext.form.TextField(), dataIndex:'additional_info' }
                    ],
                    store: userStore
                }
            ]
        }
    ]
};
