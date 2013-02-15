runListStore = new Ext.data.GroupingStore({
    groupField: "state",
    proxy: runStore.proxy,
    reader: runStore.reader,
    restful: true,
    remoteSort: false
});


MA.RunList = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var self = this;

        var defaultConfig = {
            layout: "fit",
            items: [
                new Ext.grid.GridPanel({
                    border: false,
                    itemId: "grid",
                    loadMask : true,
                    selModel: new Ext.grid.RowSelectionModel({ singleSelect: true }),
                    view: new Ext.grid.GroupingView({
                        forceFit: true,
                        autoFill: true,
                        hideGroupedColumn: true
                    }),
                    plugins:[new Ext.ux.grid.Search({
                         mode:'local'
                        ,iconCls:false
                        ,dateFormat:'m/d/Y'
                        ,minLength:0
                        ,width:150
                        ,position:'top'
                    })],
                    columns: [
                        { header: "ID", sortable: false, menuDisabled: true, dataIndex: "id", width: 50 },
                        { header: "Title", sortable: false, menuDisabled: true, dataIndex: "title" },
                        { header: "Method", sortable: false, menuDisabled: true, dataIndex: "method__unicode" },
                        { header: "Machine", sortable: false, menuDisabled: true, dataIndex: "machine__unicode" },
                        { header: "Creator", sortable: false, menuDisabled: true, dataIndex: "creator__unicode" },
                        { header: "Created On", sortable: false, menuDisabled: true, dataIndex: "created_on", renderer: renderDateTime },
                        { header: "Progress", sortable: false, menuDisabled: true, groupable: false, renderer: renderRunProgress },
                        { header: "State", sortable: false, menuDisabled: true, groupable: true, dataIndex: "state", renderer: renderRunState }
                    ],
                    store: runListStore,
                    tbar: [
                        {
                            text: "Remove Run",
                            cls: "x-btn-text-icon",
                            icon: "static/images/delete.png",
                            handler: function () {
                                var selModel = self.getComponent("grid").getSelectionModel();

                                if (selModel.hasSelection()) {
                                    var agreed = window.confirm("Are you sure you want to remove the selected run?");
                                    if (agreed) {
                                        var id = selModel.getSelected().data.id;
                                        MA.CRUDSomething("delete/run/"+id+"/", null, function () {
                                            self.getStore().reload();
                                            self.fireEvent("delete", id);
                                            
                                            //runStore.reload(); //BP:fixtimeouts
                                        });
                                    }
                                }
                            }
                        },
                        {
                            text: "Clone Run",
                            cls: "x-btn-text-icon",
                            icon: "static/images/add-to-run.png",
                            handler: function () {
                                var selModel = self.getComponent("grid").getSelectionModel();

                                if (selModel.hasSelection()) {
                                    var agreed = window.confirm("Are you sure you want to clone the selected run?");
                                    if (agreed) {
                                        var id = selModel.getSelected().data.id;
                                        var msg = Ext.Msg.wait("Cloning Run");
                                        var req = new Ajax.Request(wsBaseUrl + 'clone_run/' + encodeURIComponent(id),
                                                {
                                                    asynchronous:true,
                                                    evalJSON:'force',
                                                    onSuccess: function(response){
                                                        msg.hide();
                                                        console.log(response.responseJSON);
                                                        if (response.responseJSON.success !== true){
                                                            console.log('couldnt clone run');
                                                            Ext.Msg.alert("Error Cloning Run", response.responseJSON.message);
                                                        }
                                                        
                                                        self.getStore().reload();
                                                               },
                                                    onFailure: function(response){
                                                                
                                                        msg.hide();
                                                        Ext.Msg.alert("Communication Error", "Call to clone run failed.");
                                                        }
                                                });
                                        
                                    }
                                }
                            }
                        }
                    ],
                    listeners: {
//                        "rowclick": function () {
//                            self.fireEvent("click", this.getSelectionModel().getSelected().data.id);
//                        },
                        "rowdblclick": function () {
                            self.fireEvent("dblclick", this.getSelectionModel().getSelected().data.id);
                        }
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        MA.RunList.superclass.constructor.call(this, config);
        self.getComponent("grid").getSelectionModel().on('selectionchange', function(sm) { if (Ext.isDefined(self.getComponent("grid").getSelectionModel().getSelected())) { self.fireEvent("click", self.getComponent("grid").getSelectionModel().getSelected().data.id); } });

        self.addEvents("click", "dblclick", "delete");
    },
    getStore: function () {
        return this.getComponent("grid").getStore();
    },
    select: function (id) {
        var record = this.getStore().getById(id);
        this.getComponent("grid").getSelectionModel().selectRecords([record], false);
    }
});

MA.RunListCmp  = {
    title: "Runs",
    region: "center",
    cmargins: "0 0 0 0",
    border:false,
    collapsible: false,
    id: "runs-list",
    bodyStyle: "padding: 0",
    layout: "border",
    defaults: {
        split: true
    },
    items: [ new MA.RunList({
            border: false,
            id: "runs",
            region: "center",
            listeners: {
                click: function (id) {
                    var detail = Ext.getCmp("run-list-detail");
                    detail.selectRun(runListStore.getById(id));
                },
                "delete": function (id) {
                    var detail = Ext.getCmp("run-list-detail");
                    if (detail.runId == id) {
                        detail.clearRun();
                    }
                }
            }
        }),

        new Ext.Panel({
            region: "east",
            width: 520,
            border: false,
            bodyStyle: "background: #d0def0;",
            autoScroll:true,
            items: [
                new MA.RunDetail({
                    bodyStyle:'padding:10px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
                    border: false,
                    flex: 0,
                    id: "run-list-detail",
                    listeners: {
                        "delete": function () { runListStore.reload(); /*runStore.reload();*/ },
                        "save": function () { runListStore.reload(); /*runStore.reload();*/ }
                    }
                })
            ]
        })
    ] 
};
   
MA.ExperimentRunsInit = function() {
    Ext.getCmp('center-panel').layout.setActiveItem('experiment-runs-list');
    //Ext.getCmp('experiment-run-list-detail').clearRun();
    Ext.getCmp('experiment-runs-list').init();
};

MA.ExperimentRunListCmp = {
title: "Runs",
region: "center",
cmargins: "0 0 0 0",
collapsible: false,
id: "experiment-runs-list",
bodyStyle: "padding: 0",
layout: "border",
defaults: {
split: true
},
items: [
        new MA.RunList({
                       border: false,
                       id: "experimentruns",
                       region: "center",
                       listeners: {
                       click: function (id) {
                       var detail = Ext.getCmp("experiment-run-list-detail");
                       detail.selectRun(runListStore.getById(id));
                       },
                       "delete": function (id) {
                       var detail = Ext.getCmp("experiment-run-list-detail");
                       if (detail.runId == id) {
                       detail.clearRun();
                       }
                       }
                       },
                       store:experimentRunStore
                       }, mode='editor'),
        new Ext.Panel({
                      region: "east",
                      width: 520,
                      border: false,
                      bodyStyle: "background: #d0def0;",
                      autoScroll:true,
                      items: [
                              new MA.RunDetail({
                                               bodyStyle:'padding:10px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
                                               border: false,
                                               flex: 0,
                                               id: "experiment-run-list-detail",
                                               listeners: {
                                               "delete": function () { 
        //runListStore.proxy.conn.url = adminBaseUrl + "repository/run/ext/json?samples__experiment="+MA.ExperimentController.currentId();
runListStore.reload(); /*runStore.reload();*/ },
                                               "save": function () { 
        //runListStore.proxy.conn.url = adminBaseUrl + "repository/run/ext/json?samples__experiment="+MA.ExperimentController.currentId();
runListStore.reload(); /*runStore.reload();*/ }
                                               }
                                               }, {allowCreatingNewRun: true})
                              ]
                      })
        ],

    init: function() {
        var selectionModel = Ext.getCmp("experimentruns").getComponent("grid").getSelectionModel();
        var detailsPanel = Ext.getCmp('experiment-run-list-detail');
        var id;
        runListStore.load({'params': {'experiment__id': MA.ExperimentController.currentId()}});
        if (selectionModel.hasSelection()) {
            detailsPanel.selectRun(selectionModel.getSelected());
        } else {
            detailsPanel.clearRun();
        }
    }

};


MA.LoadRun = function (id) {
    Ext.getCmp("runs").select(id);
    Ext.getCmp("run-list-detail").selectRun(runListStore.getById(id));
    MA.MenuHandler({ id: "runs:list" });
};
