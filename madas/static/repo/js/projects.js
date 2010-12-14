MA.ProjectList = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var self = this;

        var store = projectsListStore;
        if (config.store) {
            store = config.store;
        }

        var defaultConfig = {
            layout: "fit",
            items: [
                new Ext.grid.GridPanel({
                    itemId: "grid",
                    border: false,
                    tbar: [
                                    {
                                        text: "New Project",
                                        cls: "x-btn-text-icon",
                                        icon: "static/repo/images/add.png",
                                        handler: function (b, e) {
                                            if (MA.IsAdmin || MA.IsNodeRep) {
                                                MA.MenuHandler({ "id": "project:new" });
                                            } else {
                                                b.disable();
                                            }
                                        }
                                    },
                                    {
                                        text: "Remove Project",
                                        cls: "x-btn-text-icon",
                                        icon: "static/repo/images/delete.png",
                                        handler: function (b, e) {
                                            if (MA.IsAdmin || MA.IsNodeRep) {
                                                var grid = self.getComponent("grid");
                                                var selections = grid.getSelectionModel().getSelections();
                        
                                                grid.getStore().remove(selections);
                                                self.fireEvent("delete", selections);
                                            } else {
                                                b.disable();
                                            }
                                        }
                                    }
                                ],
                    trackMouseOver: false,
                    plugins:[new Ext.ux.grid.Search({
                         mode:'local'
                        ,iconCls:false
                        ,dateFormat:'m/d/Y'
                        ,minLength:0
                        ,width:150
                        ,position:'top'
                    })],
                    selModel: new Ext.grid.RowSelectionModel({ singleSelect: true }),
                    viewConfig: {
                        forceFit: true,
                        autoFill: true
                    },
                    columns: [
                        { header: "ID", sortable: false, menuDisabled: true, dataIndex: "id", width: 50 },
                        { header: "Title", sortable: false, menuDisabled: true, dataIndex: "title" },
                        { header: "Client", sortable: false, menuDisabled: true, dataIndex: "client__unicode" },
                        { header: "Description", sortable: false, menuDisabled: true, dataIndex: "description", width: 300 }
                    ],
                    store: store,
                    listeners: {
                        "rowclick": function () {
                            self.fireEvent("click", this.getSelectionModel().getSelected().data.id);
                        },
                        "rowdblclick": function () {
                            self.fireEvent("dblclick", this.getSelectionModel().getSelected().data.id);
                        }
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        /* Items that can be provided in the config that should apply to the
         * grid. */
        var keys = ["loadMask"];
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            if (config[key]) {
                config.items[0][key] = config[key];
            }
        }

        MA.ProjectList.superclass.constructor.call(this, config);
        this.addEvents("click", "dblclick", "delete");
    },
    getStore: function () {
        return this.getComponent("grid").getStore();
    },
    select: function (id) {
        var record = this.getStore().getById(id);
        this.getComponent("grid").getSelectionModel().selectRecords([record], false);
    }
});


MA.ProjectListCmp = new MA.ProjectList({
    title: 'Projects',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'projects-list',
    bodyStyle: 'padding:0px;',
    listeners: {
        dblclick: function (id) {
            MA.LoadProject(id);
        }
    }
});

MA.ProjectCmp = { 
    id:'projectCmpTitle',
    title:'New Project',
    layout:'border',
    forceLayout:true,
    deferredRender:false,
    defaults: {
        collapsible: false,
        bodyStyle: 'padding:15px;background-color:transparent;'
    },
    items: [
        {
            region:'north',
            height:250,
            layout:'border',
            items: [
                {
                    border:false,
                    region:'center',
                    xtype: 'form',
                    collapsible: false,
                    id:'project-form',
                    bodyStyle: 'padding:8px;background-color:transparent',
                    width:850,
                    title:'Project details',
                    items: [ 
                        { xtype:'textfield', fieldLabel:'Project title', width:700, id:'projectTitle', name:'title', allowBlank:false},
                        { xtype:'textarea', fieldLabel:'Description', id:'projectDescription', width:700, height:100, name:'description' },
                        new Ext.form.ComboBox({
                                fieldLabel:'Client',
                                id:'projectClientCombo',
                                name:'client',
                                width:700,
                                editable:false,
                                forceSelection:true,
                                displayField:'username',
                                valueField:'id',
                                hiddenName:'client_id',
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: clientsListStore,
                                itemSelector: 'div.search-item',
                                tpl:new Ext.XTemplate(
                                '<tpl for="."><div style="padding:8px;padding-top:5px;padding-bottom:5px;border-bottom:1px solid #ccc;" class="search-item">',
                                '{username}<br /><span style="color:#666;">{first_name} {last_name}</span>',
                                '</div></tpl>'
                                )
                            })
                    ],
                    buttons: [
                        {
                             text: 'Save',
                             id:'projectSubmit',
                             handler: function(){
                                Ext.getCmp('project-form').getForm().submit(
                                    {   
                                        url: wsBaseUrl + 'update/project/' + MA.currentProjectId,
                                        successProperty: 'success',
                                        success: function (form, action) {
                                            if (action.result.success === true) {
                                                MA.currentProjectId = action.result.rows[0].id;
                                            
                                                //display a success alert that auto-closes in 1 second
                                                Ext.Msg.alert("Project saved", "(this message will auto-close in 1 second)");
                                                window.setTimeout(function () {
                                                    Ext.Msg.hide();
                                                }, 1000);
            
                                                Ext.getCmp('project-experiment-list').enable();
            
                                                //load up the menu and next content area as declared in response
                                                MA.ChangeMainContent(action.result.mainContentFunction);
                                            }
                                        },
                                        failure: function (form, action) {
                                            //do nothing special. this gets called on validation failures and server errors
                                        }
                                    });
                                }
                            }
                    ]
                },
                {
                    region:'east',
                    title:'Project managers',
                    width:200,
                    border:false,
                    tbar:[
                        {
                            text: 'Add',
                            cls: 'x-btn-text-icon',
                            icon:'static/repo/images/add.png',
                            id:'projManagersAddButton',
                            handler : function(){
                                //POP UP A WINDOW TO ASK WHICH USER TO ADD
                                var addWindow = new Ext.Window({
                                    title:'Add a Project Manager',
                                    width:280,
                                    height:130,
                                    minHeight:130,
                                    border:false,
                                    bodyStyle:'padding:20px;background-color:transparent;',
                                    x:290,
                                    y:250,
                                    layout:'vbox',
                                    modal:true,
                                    items:[
                                        new Ext.form.ComboBox({
                                                fieldLabel:'',
                                                labelWidth:50,
                                                itemId:'projManagerCombo',
                                                name:'projManager',
                                                width:200,
                                                editable:false,
                                                forceSelection:true,
                                                displayField:'value',
                                                valueField:'key',
                                                hiddenName:'projManagerId',
                                                lazyRender:true,
                                                allowBlank:false,
                                                typeAhead:false,
                                                triggerAction:'all',
                                                listWidth:200,
                                                store: userComboStore
                                            })
                                    ],
                                    buttons:[
                                        {
                                            text:'Cancel',
                                            itemId:'cancel'
                                        },
                                        {
                                            text:'Add',
                                            itemId:'add'
                                        }
                                    ]
                                });
                                
                                addWindow.show();
                                
                                addWindow.buttons[0].on('click', function() { addWindow.close(); } );
                                addWindow.buttons[1].on('click', function() { 
                                    if (addWindow.getComponent('projManagerCombo').isValid()) {
                                        MA.CRUDSomething('associate/project/manager/'+MA.currentProjectId+'/'+addWindow.getComponent('projManagerCombo').getValue()
                                        , {}, function (store, records) { 
                                            Ext.getCmp('projManagerList').getStore().removeAll();
                                            
                                            realRecords = records[0].data.managers;
                                            for (i = 0; i < realRecords.length; i++) {
                                                Ext.getCmp('projManagerList').getStore().add(new Ext.data.Record({'id':realRecords[i].id, 'username':realRecords[i].username})); 
                                            }
                                            Ext.getCmp('projManagerList').refresh();
                                            });
                                        addWindow.close(); 
                                    }
                                } );
                            }
                        },
                        {
                            text: 'Remove',
                            cls: 'x-btn-text-icon',
                            icon:'static/repo/images/delete.png',
                            id:'projManagersRemoveButton',
                            handler : function(){
                                   //remove currently selected users
                                   var recs = Ext.getCmp('projManagerList').getSelectedRecords();
                                   for (i = 0; i < recs.length; i++) {
                                       var rec = recs[i];
                                       MA.CRUDSomething('dissociate/project/manager/'+MA.currentProjectId+'/'+rec.data.id, {}, function () { Ext.getCmp('projManagerList').getStore().remove(rec); });
                                   }
                                   
                            }
                               
                        }
                    ],
                    items:[
                        {
                            xtype:'listview',
                            id:'projManagerList',
                            store:new Ext.data.ArrayStore({}),
                            loadingText:'Loading...',
                            columnSort:false,
                            columns: [
                                {header: "username", dataIndex: 'username', 
                                    tpl: '<div style="padding:4px">{username}</div>'}
                            ],
                            listeners:{
                            },
                            viewConfig:{
                                forceFit:true
                            },
                            singleSelect:true,
                            multiSelect:false,
                            hideHeaders:true,
                            style:'background:white;',
                            autoScroll:true,
                            reserveScrollOffset:true
                        }
                    ]
                }
            ]
        },
        {
            title: 'Experiments',
            region: 'center',
            cmargins: '0 0 0 0',
            collapsible: false,
            id:'project-experiment-list',
            bodyStyle: 'padding:0px;',
            layout:'fit',
//            disabled:true,
            tbar: [{
                text: 'New Experiment',
                cls: 'x-btn-text-icon',
                icon:'static/repo/images/add.png',
                handler : function(){
                        MA.MenuHandler({'id':'experiment:new'});
                    }
                },
                {
                text: 'Remove Experiment',
                cls: 'x-btn-text-icon',
                icon:'static/repo/images/delete.png',
                handler : function(){
                   var grid = Ext.getCmp('project-experiments');
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
                   //console.log(delIds);
                   for (var i = 0; i < delIds.length; i++) {
                       MA.CRUDSomething('delete/experiment/'+delIds[i], {}, function() { experimentListStore.proxy.conn.url = wsBaseUrl + 'recordsExperiments/' + MA.currentProjectId;
                       experimentListStore.load(); });
                   }                        
                   }
                   
                }
            ],
            items: [
                {
                    xtype:'grid',
                    border: false,
                    id:'project-experiments',
                    trackMouseOver: false,
                    sm: new Ext.grid.RowSelectionModel( {singleSelect:true}),
                    view: new Ext.grid.GroupingView({
                        forceFit: true,
                        autoFill: true,
                        hideGroupedColumn: true
                    }),
                    columns: [
                        { header: "ID", sortable:false, menuDisabled:true, dataIndex:'id', width:50 },
                        { header: "Title", sortable:false, menuDisabled:true, dataIndex:'title' },
                        { header: "Principal", sortable:false, menuDisabled:true, dataIndex:'principal' },
                        { header: "Client", sortable:false, menuDisabled:true, dataIndex:'client' },
                        { header: "Description", sortable:false, menuDisabled:true, width:300, dataIndex:'description' },
                        { header: "Status", sortable:false, menuDisabled:true, renderer:renderStatus, dataIndex:'status' }
                    ],
                    store: experimentListStore,
                    listeners: {
                        'rowdblclick':function(el, ev) {
                            var sm = Ext.getCmp('project-experiments').getSelectionModel();
                            var rec = sm.getSelected();
                            MA.ExperimentController.loadExperiment(rec.data.id);
                        }
                    }
                }
            ]
        }
    ]
};

MA.LoadProject = function (projId) {
    MA.currentProjectId = projId;
    
    Ext.getCmp('projectCmpTitle').setTitle('Loading project...');
    
    var projLoader = new Ajax.Request(wsBaseUrl + "records/project/id/" + projId, 
                                         { 
                                         asynchronous:true, 
                                         evalJSON:'force',
                                         onSuccess: function(response) {
                                                 var titlefield = Ext.getCmp('projectTitle');
                                                 var desc = Ext.getCmp('projectDescription');
                                                 var titleCmp = Ext.getCmp('projectCmpTitle');
                                                 var clientCmp = Ext.getCmp('projectClientCombo');
                                                 var projBarTitle = Ext.getCmp('expProjTitle');
                                                 projBarTitle.setTitle('');

                                                 titleCmp.setTitle('');    
                                                 titlefield.setValue('');
                                                 desc.setValue('');
    
                                                 var rs = response.responseJSON.rows;

                                                 //enable or disable Add/Remove project managers based on access
                                                 var showAddRemove = false;
                                                 if (MA.IsAdmin || MA.IsNodeRep) {
                                                     showAddRemove = true;
                                                 }

                                                 if (rs.length > 0) {
                                                     titleCmp.setTitle('Project: ' + rs[0].title);
                                                     projBarTitle.setTitle('Project: ' + rs[0].title);
                                                     titlefield.setValue(rs[0].title);
                                                     desc.setValue(rs[0].description);
                                                     clientCmp.setValue(rs[0].client);
                                                                                                 
                                                     var pmList = Ext.getCmp('projManagerList');
                                                     var pmStore = pmList.getStore();
                                                     pmStore.removeAll(false);
                                                     for (i = 0; i < rs[0].managers.length; i++) {
                                                         val = rs[0].managers[i];
                                                         if (rs[0].managers[i].id == MA.CurrentUserId) {
                                                             showAddRemove = true;
                                                         }
                                                         pmStore.add(new Ext.data.Record(val));
                                                     }
                                                     
                                                 }
                                         
                                                 if (showAddRemove) {
                                                     Ext.getCmp("projManagersAddButton").enable();
                                                     Ext.getCmp("projManagersRemoveButton").enable();
                                                 } else {
                                                     Ext.getCmp("projManagersAddButton").disable();
                                                     Ext.getCmp("projManagersRemoveButton").disable();
                                                 }
                                             }
                                         }
                                         );
    
    experimentListStore.proxy.conn.url = wsBaseUrl + 'recordsExperiments/' + projId;
    experimentListStore.load();
  
    MA.MenuHandler({ id:'project:view' });
};
