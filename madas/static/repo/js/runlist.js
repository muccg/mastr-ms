runListStore = new Ext.data.GroupingStore({
    groupField: "state",
    proxy: runStore.proxy,
    reader: runStore.reader,
    restful: true,
    remoteSort: false
});


MA.RunListCmp = {
    title: "runs",
    region: "center",
    cmargins: "0 0 0 0",
    collapsible: false,
    id: "runs-list",
    bodyStyle: "padding: 0",
    layout: "border",
    defaults: {
        split: true
    },
    items: [
        new Ext.grid.GridPanel({
            border: false,
            region: "center",
            id: "runs",
            selModel: new Ext.grid.RowSelectionModel({ singleSelect: true }),
            view: new Ext.grid.GroupingView({
                forceFit: true,
                autoFill: true,
                hideGroupedColumn: true
            }),
            columns: [
                { header: "id", sortable: false, menuDisabled: true, dataIndex: "id" },
                { header: "title", sortable: false, menuDisabled: true, dataIndex: "title" },
                { header: "method", sortable: false, menuDisabled: true, dataIndex: "method__unicode" },
                { header: "machine", sortable: false, menuDisabled: true, dataIndex: "machine__unicode" },
                { header: "creator", sortable: false, menuDisabled: true, dataIndex: "creator__unicode" },
                { header: "created_on", sortable: false, menuDisabled: true, dataIndex: "created_on", renderer: renderDateTime },
                { header: "progress", sortable: false, menuDisabled: true, groupable: false, renderer: renderRunProgress },
                { header: "state", sortable: false, menuDisabled: true, groupable: true, dataIndex: "state", renderer: renderRunState }
            ],
            store: runListStore,
            listeners: {
                "rowclick": function () {
                    var detail = Ext.getCmp("run-list-detail");

                    detail.selectRun(Ext.getCmp("runs").getSelectionModel().getSelected());
                }
            }
        }),
        new Ext.Panel({
            region: "east",
            width: 520,
            border: false,
            bodyStyle: "background: #d0def0;",
            items: [
                new MA.RunDetail({
                    bodyStyle:'padding:10px;background:transparent;border-top:none;border-bottom:none;border-right:none;',
                    border: false,
                    flex: 0,
                    id: "run-list-detail",
                    listeners: {
                        "delete": function () { runListStore.reload(); },
                        "save": function () { runListStore.reload(); }
                    }
                })
            ]
        })
    ]
};
