/**
 * This file is part of Madas.
 *
 * Madas is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Madas is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Madas.  If not, see <http://www.gnu.org/licenses/>.
 */



MA.DownloadClientFile = function(fileID) {
    window.location = MA.BaseUrl + "ws/downloadClientFile/" + fileID;
};

function clientFileActionRenderer(val) {
    return '<a href="#" onclick="MA.DownloadClientFile(\''+val+'\')">download</a>';
}

var selectionModel = new Ext.grid.RowSelectionModel({ 
    singleSelect: true
});

MA.DashboardCreatePendingUserRequests = function() {
    var dataurl = MA.BaseUrl + "admin/adminrequests";
    var madasReader = new MA.JsonReader({
                                              root            : 'response.value.items',
                                              versionProperty : 'response.value.version',
                                              totalProperty   : 'response.value.total_count'
                                              }, [
                                                  { name: 'isClient', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'username', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'firstname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'lastname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'email', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'telephoneNumber', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'physicalDeliveryOfficeName', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'title', sortType : Ext.data.SortTypes.asText }
                                                  ]);


    function editUser(username) {
        MA.Authorize('admin:useredit', username);
    }

    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editUser(selectionModel.getSelected().data.username);
        }
    };

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'userEditBtn', text: 'Edit', handler: editHandler }
        ]
    });

    return new Ext.Panel({

    title:'Pending User Requests',
    style:'padding:20px 20px 0px 20px',
    id:'dashboard-pending-user-requests',
    tbar: toolbar,
    init: function() {
        this.items.items[0].store.load();
    },
    items:[
                {
                    xtype:'grid',
                    border: false,
                    autoScroll: true,
                    stripeRows: true,
                    height: 110,
                    autoExpandColumn: 'username',
                    ds: new Ext.data.Store({
                        id         : 'bSId',
//                        autoLoad   : true,
                        reader     : madasReader,
                        sortInfo   : {field: 'lastname', direction: 'ASC'},
                        url        : dataurl
                    }),
                    sm: selectionModel,
                    listeners: {
                        rowdblclick: function(grid, rowIndex, evt) {
                            var record = grid.store.getAt(rowIndex);
                            editUser(record.get('username'));
                        }
                    },

                    columns: [
                        {
                            header: 'First Name',
                            sortable: true,
                            width: 100,
                            dataIndex: 'firstname'
                        },
                        {
                            header: 'Last Name',
                            sortable: true,
                            width: 100,
                            dataIndex: 'lastname'
                        },
                        {
                            id: 'username',
                            header: 'Username',
                            dataIndex: 'username'
                        }
                    ]
              }
       ]
    });
   };




                            
var checkBoxRenderer = function (val){
        if(val === true){
            return '*';
        } else {
            return '';
        }
};



MA.DashboardCreateQuotesRequiringAttention = function() {
    var madasReader2 = new Ext.data.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType: Ext.data.SortTypes.asInt },
            { name: 'firstname', sortType: Ext.data.SortTypes.asText },
            { name: 'lastname', sortType: Ext.data.SortTypes.asText },
            { name: 'email', sortType: Ext.data.SortTypes.asText },
            { name: 'officephone', sortType: Ext.data.SortTypes.asText },
            { name: 'requesttime', sortType: Ext.data.SortTypes.asDate },
            { name: 'completed', sortType: Ext.data.SortTypes.asText },
            { name: 'unread', sortType: Ext.data.SortTypes.asText },
            { name: 'details', sortType: Ext.data.SortTypes.asText},
            { name: 'tonode', sortType: Ext.data.SortTypes.asText},
            { name: 'country', sortType: Ext.data.SortTypes.asText}
        ]);

    var dataurl2 = MA.BaseUrl + "quote/listNeedsAttention";
    var editQuote = function(quote_id) {
        MA.Authorize('quote:edit', [quote_id]);
    };
    var quoteEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editQuote(selectionModel.getSelected().data.id);
        }
    };

    var toolbar2 = new Ext.Toolbar({
        items   : [
            { id: 'quoteEditBtn', text: 'Edit', handler: quoteEditHandler }
        ]
    });

    return new Ext.Panel({

    title:'Quotes Requiring Attention',
    style:'padding:20px 20px 0px 20px',
    id:'dashboard-quotes-requiring-attention',
    tbar: toolbar2,
    init: function() {
        this.items.items[0].store.load();
    },
    items:[
                {
                    xtype:'grid',
                    border: false,
                    autoScroll: true,
                    stripeRows: true,
                    height: 150,
                    ds: new Ext.data.Store({
                        id         : 'bSId',
//                        autoLoad   : true,
                        reader     : madasReader2,
                        sortInfo   : {field: 'requesttime', direction: 'DESC'},
                        url        : dataurl2
                    }),
                    sm: selectionModel,
                    listeners: {
                        rowdblclick: function(grid, rowIndex, evt) {
                            var record = grid.store.getAt(rowIndex);
                            editQuote(record.get('id'));
                        }
                    },

                    columns: [
                        {
                            header: 'ID',
                            sortable: true,
                            width: 40,
                            dataIndex: 'id'
                        },
                        {
                            header: 'Unread',
                            sortable: true,
                            width: 60,
                            renderer: checkBoxRenderer,
                            dataIndex: 'unread'
                        },
                        {
                            header: 'Email',
                            width: 185,
                            dataIndex: 'email'
                        },
                        {
                            header: 'First Name',
                            sortable: true,
                            width: 100,
                            dataIndex: 'firstname'
                        },
                        {
                            header: 'Last Name',
                            sortable: true,
                            width: 100,
                            dataIndex: 'lastname'
                        },
                        {
                            header: 'Node',
                            sortable: true,
                            width: 200,
                            dataIndex: 'tonode'
                        },
                        {
                            header: 'Date Received',
                            sortable: true,
                            width: 100,
                            dataIndex: 'requesttime'
                        }
                     ]
              }
       ]
    });
   };

MA.DashboardCreateRecentExperiments = function() {
    var madasReader = new Ext.data.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType: Ext.data.SortTypes.asInt },
            { name: 'title', sortType: Ext.data.SortTypes.asText },
            { name: 'status', sortType: Ext.data.SortTypes.asText }
        ]);

    var dataurl = MA.BaseUrl + "ws/recent_experiments";
    var editExperiment = function(experiment_id) {
        document.location = 'repo/experiment/view?id=' + experiment_id;
    };
    var experimentEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editExperiment(selectionModel.getSelected().data.id);
        }
    };

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'experimentEditBtn', text: 'Edit', handler: experimentEditHandler }
        ]
    });

    return new Ext.Panel({

    title:'Recent Experiments',
    style:'padding:20px 20px 0px 20px',
    id:'dashboard-recent-experiments',
    //tbar: toolbar,
    init: function() {
        this.items.items[0].store.load();
    },
    items:[
                {
                    xtype:'grid',
                    border: false,
                    autoScroll: true,
                    stripeRows: true,
                    height: 150,
                    ds: new Ext.data.Store({
                        id         : 'bSId',
                        reader     : madasReader,
                        url        : dataurl
                    }),
                    sm: selectionModel,
/*
                    listeners: {
                        rowdblclick: function(grid, rowIndex, evt) {
                            var record = grid.store.getAt(rowIndex);
                            editQuote(record.get('id'));
                        }
                    },
*/
                    columns: [
                        {
                            header: 'ID',
                            sortable: true,
                            width: 40,
                            dataIndex: 'id'
                        },
                        {
                            header: 'Title',
                            width: 300,
                            dataIndex: 'title'
                        },
                        {
                            header: 'Status',
                            sortable: true,
                            width: 100,
                            dataIndex: 'status'
                        }
                    ]
              }
       ]
    });
   };

MA.DashboardCreateRecentRuns = function() {
    var madasReader = new Ext.data.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType: Ext.data.SortTypes.asInt },
            { name: 'title', sortType: Ext.data.SortTypes.asText },
            { name: 'status', sortType: Ext.data.SortTypes.asText }
        ]);

    var dataurl = MA.BaseUrl + "ws/recent_runs";
    var editRun = function(run_id) {
        document.location = 'repo/run/view?id=' + run_id;
    };
    var runEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            runExperiment(selectionModel.getSelected().data.id);
        }
    };

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'runEditBtn', text: 'Edit', handler: runEditHandler }
        ]
    });

    return new Ext.Panel({

    title:'Recent Runs',
    style:'padding:20px 20px 0px 20px',
    id:'dashboard-recent-runs',
    //tbar: toolbar,
    init: function() {
        this.items.items[0].store.load();
    },
    items:[
                {
                    xtype:'grid',
                    border: false,
                    autoScroll: true,
                    stripeRows: true,
                    height: 150,
                    ds: new Ext.data.Store({
                        id         : 'bSId',
                        reader     : madasReader,
                        url        : dataurl
                    }),
                    sm: selectionModel,
/*
                    listeners: {
                        rowdblclick: function(grid, rowIndex, evt) {
                            var record = grid.store.getAt(rowIndex);
                            editQuote(record.get('id'));
                        }
                    },
*/
                    columns: [
                        {
                            header: 'ID',
                            sortable: true,
                            width: 40,
                            dataIndex: 'id'
                        },
                        {
                            header: 'Title',
                            width: 300,
                            dataIndex: 'title'
                        },
                        {
                            header: 'Method',
                            width: 200,
                            dataIndex: 'method'
                        },
                        {
                            header: 'Machine',
                            width: 300,
                            dataIndex: 'machine'
                        },
                        {
                            header: 'State',
                            sortable: true,
                            width: 100,
                            dataIndex: 'state'
                        }
                    ]
              }
       ]
    });
   };



MA.DashboardCreateAvailableFiles = function() {
    return new Ext.Panel({

    title:'Available files',
    style:'padding:20px 20px 0px 20px',
    id:'dashboard-available-files',
    tbar:[
        {
            xtype:'tbtext',
            text:'Click a filename to download'
        }
    ],
    init: function() {
    },
    items:[
                {
                   xtype:'treepanel',
                   border: false,
                   autoScroll: true,
                   animate: true,
                   useArrows: true,
                   dataUrl:MA.BaseUrl + 'ws/recordsClientFiles',
                   requestMethod:'GET',
                   root: {
                       nodeType: 'async',
                       text: 'Files',
                       draggable: false,
                       id: 'dashboardFilesRoot',
                       'metafile': true
                   },
                   selModel: new Ext.tree.DefaultSelectionModel(
                       { listeners:
                           {
                               selectionchange: function(sm, node) {
                                   if (node !== null && !node.attributes.metafile) {
                                       MA.DownloadClientFile(node.id);
                                   }
                               }
                           }
                       }),
                   listeners:{
                        render: function() {
                        }
                    }
               }
       ]
    });
   };

MA.DashboardCreateToolbar = function() {
    return {
        init: function() {},
        style: 'padding: 20px 20px 0px 20px',
        border: false,
        init: function() {
        },
        items: [{
            xtype: 'tbbutton',
            text: 'Refresh Dasboard Data',
            handler: function() {
                    var dashboard = Ext.getCmp('dashboard-panel');
                    dashboard.init();
                }    
            }]
    };
};


MA.DashboardCreateAdminDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        //    layout: 'column',
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.DashboardCreateToolbar(),
            MA.DashboardCreatePendingUserRequests(),
            MA.DashboardCreateQuotesRequiringAttention(),
            MA.DashboardCreateRecentExperiments()
        ]
    });
};

MA.DashboardCreateClientDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        //    layout: 'column',
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.DashboardCreateToolbar(),
            MA.DashboardCreateRecentExperiments(),
            MA.DashboardCreateAvailableFiles()
        ]
    });
};

MA.DashboardCreateStaffDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        //    layout: 'column',
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.DashboardCreateToolbar(),
            MA.DashboardCreateRecentExperiments(),
            MA.DashboardCreateRecentRuns()
        ]
    });
};


MA.DashboardCreateDashboard = function() {
    if (!MA.IsLoggedIn) {
        return MA.NotAuthorizedCmp;
    }
    if (MA.IsAdmin || MA.IsNodeRep) {
        return MA.DashboardCreateAdminDashboard();
    } else if (MA.IsClient) {
        return MA.DashboardCreateClientDashboard();
    } else {
        return MA.DashboardCreateStaffDashboard();
    }
};

MA.DashboardCreated = false;
MA.DashboardInit = function(){
    var dboard;
    if (!MA.DashboardCreated) {
        dboard = MA.DashboardCreateDashboard();
        Ext.getCmp('center-panel').add(dboard);
        MA.DashboardCreated = true;
    }
    Ext.getCmp('dashboard-panel').init();
};

