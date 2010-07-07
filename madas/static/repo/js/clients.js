MA.ClientsListCmp = {
    title: 'Clients',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'clients-list',
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [
        {
            text:'Samples for Selected Client',
            listeners: {
                'click':function(el, ev) {
                    var sm = Ext.getCmp('clients').getSelectionModel();
                    var rec = sm.getSelected();
                    MA.LoadClientSamples(rec.data.client);
                }
            }
        },
        {
            text:'Projects for Selected Client',
            listeners: {
                'click':function(el, ev) {
                    var sm = Ext.getCmp('clients').getSelectionModel();
                    var rec = sm.getSelected();
                    //MA.LoadClientSamples(rec.data.client);

                    projectsListStore.load({ params: { client__id__exact: rec.data.id } });

                    Ext.getCmp('center-panel').layout.setActiveItem('projects-list');
                }
            }
        },
        { xtype: "tbfill" },
        new MA.InlineSearch({
            width: 120,
            listeners: {
                clear: function () {
                    Ext.getCmp("clients").getStore().clearFilter();
                },
                search: function (term) {
                    term = term.toLowerCase();

                    Ext.getCmp("clients").getStore().filterBy(function (record, id) {
                        return (record.data.client.toLowerCase().indexOf(term) != -1);
                    });
                }
            }
        })
    ],
    items: [
        {
            xtype:'grid',
            border: false,
            id:'clients',
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
            store: clientsListStore
        }
    ]
};

MA.LoadClientSamples = function(id) {
    var scmp = clientSampleStore;
    
    scmp.proxy.conn.url = wsBaseUrl + 'recordsSamplesForClient/client/' + id;
    scmp.load();
    
    MA.MenuHandler({ id:'clients:samples' });
    
    Ext.getCmp('client-samples-list').setTitle('Samples by Client: '+id);
};

MA.ClientSamplesCmp = {
    title: 'Samples by Client',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'client-samples-list',
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [
    ],
    items: [
        {
            xtype:'grid',
            border: false,
            id:'clients-samples',
            trackMouseOver: false,
            sm: new Ext.grid.RowSelectionModel( {singleSelect:true} ),
            viewConfig: {
                forceFit: true,
                autoFill:true
            },
            view: new Ext.grid.GroupingView({
                loadMask : { msg : 'Please wait...' },
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
};
