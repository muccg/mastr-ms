MA.AccessInit = function() {
    userStore.load({ params: { experiment__id__exact: MA.ExperimentController.currentId() } });
};

MA.SaveAccessRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.experiment_id = MA.ExperimentController.currentId();
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
            title: 'Involved Users',
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
                    plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':MA.SaveAccessRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    tbar: [
                        {
                            text: 'Add User',
                            cls: 'x-btn-text-icon',
                            icon: 'static/images/add.png',
                            handler: function(){
                                    userStore.add(new Ext.data.Record({'user':'', 'type':'1', 'additional_info':''}));
                            }
                        },
                        {
                            text: 'Remove User',
                            cls: 'x-btn-text-icon',
                            icon: 'static/images/delete.png',
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
                        { header: "Name", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:false,
                                forceSelection:true,
                                displayField:'displayValue',
                                valueField:'id',
                                hiddenName:'client_id',
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: userListStore,
                                listeners: {
                                    'keyup': function(component, e) {
                                        MA.StoreFilter(component, e, 'name');
                                    }
                                },
                                itemSelector: 'div.search-item',
                                tpl:new Ext.XTemplate(
                                '<tpl for="."><div style="padding:8px;padding-top:5px;padding-bottom:5px;border-bottom:1px solid #ccc;" class="search-item">',
                                '{displayValue}<br /><span style="color:#666;">{organisationName}</span>',
                                '</div></tpl>')
                            }), dataIndex: 'user', renderer:renderUser },
                        { header: "Involvement", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox(
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
                        { header: "Additional Info", sortable:false, menuDisabled:true, editor:new Ext.form.TextField(), dataIndex:'additional_info' }
                    ],
                    store: userStore
                }
            ]
        }
    ]
};
