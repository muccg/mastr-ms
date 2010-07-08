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
                                        handler: function () {
                                            MA.MenuHandler({ "id": "project:new" });
                                        }
                                    },
                                    {
                                        text: "Remove Project",
                                        cls: "x-btn-text-icon",
                                        icon: "static/repo/images/delete.png",
                                        handler: function () {
                                            var grid = self.getComponent("grid");
                                            var selections = grid.getSelectionModel().getSelections();
                    
                                            grid.getStore().remove(selections);
                                            self.fireEvent("delete", selections);
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
            items: [
                {
                    border:false,
                    xtype: 'form',
                    collapsible: false,
                    id:'project-form',
                    bodyStyle: 'background-color:transparent',
                    width:850,
                    items: [ 
                        { xtype:'fieldset', 
                        title:'Project Details',
                        bodyStyle: 'background-color:transparent',
                        autoHeight:true,
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
                                    displayField:'value',
                                    valueField:'key',
                                    hiddenName:'client_id',
                                    lazyRender:true,
                                    allowBlank:false,
                                    typeAhead:false,
                                    triggerAction:'all',
                                    listWidth:230,
                                    store: userComboStore
                                })
                            ]
                        }
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
                       MA.CRUDSomething('delete/experiment/'+delIds[i], {}, function() { experimentListStore.load(); });
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
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
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
                            MA.LoadExperiment(rec.data.id);
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

                                                 titleCmp.setTitle('');    
                                                 titlefield.setValue('');
                                                 desc.setValue('');
    
                                                 var rs = response.responseJSON.rows;

                                                 if (rs.length > 0) {
                                                     titleCmp.setTitle('Project: ' + rs[0].title);
                                                     titlefield.setValue(rs[0].title);
                                                     desc.setValue(rs[0].description);
                                                     clientCmp.setValue(rs[0].client);
                                                 }
                                         
                                             }
                                         }
                                         );
    
    experimentListStore.proxy.conn.url = wsBaseUrl + 'recordsExperiments/' + projId;
    experimentListStore.load();
    
    MA.MenuHandler({ id:'project:view' });
};
