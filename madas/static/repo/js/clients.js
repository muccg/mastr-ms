MA.ClientsListCmp = {
    title: 'Clients',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'clients-list',
    bodyStyle: 'padding:0px;',
    layout:'border',
    defaults: {
        split: true
    },
    items: [
        {
            xtype:'grid',
            border: true,
            id:'clients',
            region: 'center',
            width: '50%',
//            trackMouseOver: false,
            sm: new Ext.grid.RowSelectionModel( {singleSelect:true} ),
            viewConfig: {
                forceFit: true,
                autoFill:true
            },
            columns: [
                      { header: "ID", menuDisabled:true, dataIndex:'id', width:50 },
                      { header: "Client", menuDisabled:true, dataIndex:'client' }
            ],
            store: clientsListStore,
            tbar: [
                { xtype: "tbfill" },
                new MA.InlineSearch({
                    filterFunction: function (record, term) {
                        term = term.toLowerCase();
                        return (record.data.client.toLowerCase().indexOf(term) != -1);
                    },
                    store: clientsListStore,
                    width: 120
                })
            ],
            listeners: {
                rowclick: function () {
                    var selModel = this.getSelectionModel();
                    var store = Ext.getCmp("client-project-list").getStore();

                    if (selModel.hasSelection()) {
                        var record = selModel.getSelected();
                        var clearFilter = function () {
                            this.clearFilter();
                        };

                        clientSampleStore.addListener("load", clearFilter, clientSampleStore, { single: true });
                        store.addListener("load", clearFilter, store, { single: true });

                        clientSampleStore.proxy.conn.url = wsBaseUrl + "recordsSamplesForClient/client/" + record.data.client;
                        clientSampleStore.load();

                        store.load({ params: { client__id__exact: record.data.id } });
                    }
                    else {
                        var rejectAll = function () {
                            return false;
                        };

                        clientSampleStore.filterBy(rejectAll);
                        store.filterBy(rejectAll);
                    }
                }
            }
        },
        {
            xtype: "panel",
            region: "east",
            width: "50%",
            border: false,
            layout: "border",
            defaults: {
                split: true
            },
            items: [
                new MA.ProjectList({
                    id: "client-project-list",
                    border: true,
                    region: "north",
                    height: 200,
                    title: "Client Projects",
                    loadMask: true,
                    store: new Ext.data.JsonStore({
                        autoLoad: false,
                        url: projectsListStore.url,
                        remoteSort: true,
                        restful: true,
                        writer: new Ext.data.JsonWriter({ encode: false }),
                        sortInfo: {
                            field: 'id',
                            direction: 'DESC'
                        }
                    })
                }),
                {
                    border: true,
                    title: "Client Samples",
                    xtype:'grid',
                    border: true,
                    region: "center",
                    id:'clients-samples',
                    trackMouseOver: false,
                    loadMask : true,
                    sm: new Ext.grid.RowSelectionModel( {singleSelect:true} ),
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    view: new Ext.grid.GroupingView({
                        loadMask : true,
                        forceFit: true,
                        groupTextTpl: '{[ values.rs[0].data["experiment_title"] ]} &nbsp;&nbsp;({[values.rs.length]} samples)',
                        hideGroupedColumn: true
                        }),
                    columns: [
                              { header: "ID", sortable:true, dataIndex:'id' },
                              { header: "Label", sortable:true, dataIndex:'label' },
                              { header: "Weight", sortable:true, dataIndex:'weight' },
                              { header: "Comment", sortable:false, sortable:true, width:300, dataIndex:'comment' },
                              { header: "Last Status", sortable:true, width:300, dataIndex:'last_status' },
                              { header: "Experiment ID", dataIndex:'experiment_id' },
                              { header: "Experiment Title", dataIndex:'experiment_title'},
                              { header: "Sample Class", dataIndex:'sample_class' }
                    ],
                    store: clientSampleStore
                }
            ]
        }
    ]
};
