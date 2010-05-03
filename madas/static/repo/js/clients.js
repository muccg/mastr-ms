MA.ClientsListCmp = {
    title: 'clients',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'clients-list',
    bodyStyle: 'padding:0px;',
    layout:'fit',
    tbar: [
        { text:'samples for selected client',
          listeners: {
              'click':function(el, ev) {
                  var sm = Ext.getCmp('clients').getSelectionModel();
                  var rec = sm.getSelected();
                  MA.LoadClientSamples(rec.data.client);
              }
          }
        },
        { text:'projects for selected client',
          listeners: {
              'click':function(el, ev) {
                  var sm = Ext.getCmp('clients').getSelectionModel();
                  var rec = sm.getSelected();
//                  MA.LoadClientSamples(rec.data.client);

                  projectsListStore.proxy.conn.url = wsBaseUrl + 'records/project/client/' + rec.data.id;
                  projectsListStore.load();

                  Ext.getCmp('center-panel').layout.setActiveItem('projects-list');
              }
          }
        }
        
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
                      { header: "id", menuDisabled:true, dataIndex:'id', width:50 },
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
    
    Ext.getCmp('client-samples-list').setTitle('samples by client: '+id);
};

MA.ClientSamplesCmp = {
    title: 'samples by client',
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
                      { header: "id", sortable:true, dataIndex:'id' },
                      { header: "label", sortable:true, dataIndex:'label' },
                      { header: "weight", sortable:true, dataIndex:'weight' },
                      { header: "comment", sortable:false, sortable:true, width:300, dataIndex:'comment' },
                      { header: "last status", sortable:true, width:300, dataIndex:'last_status' },
                      { header: "experiment_id", dataIndex:'experiment_id' },
                      { header: "experiment_title", dataIndex:'experiment_title'},
                      { header: "sample class", dataIndex:'sample_class' }
            ],
            store: clientSampleStore
        }
    ]
};