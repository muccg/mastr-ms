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

MA.Dashboard.CreatePendingUserRequests = function() {
    var dataurl = MA.BaseUrl + "admin/adminrequests";
    var selectionModel = new Ext.grid.RowSelectionModel({ 
        singleSelect: true
    });
    var madasReader = new Ext.data.JsonReader({
            root: 'response.value.items',
            versionProperty: 'response.value.version',
            totalProperty: 'response.value.total_count'
        }, 
        [
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
        MA.ChangeMainContent('admin:useredit', username);
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
        items:[{
            xtype:'grid',
            border: false,
            autoScroll: true,
            stripeRows: true,
            height: 110,
            autoExpandColumn: 'username',
            ds: new Ext.data.Store({
                id: 'bSId',
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
            columns: [{
                    header: 'First Name',
                    sortable: true,
                    width: 100,
                    dataIndex: 'firstname'
                },{
                    header: 'Last Name',
                    sortable: true,
                    width: 100,
                    dataIndex: 'lastname'
                },{
                    id: 'username',
                    header: 'Username',
                    dataIndex: 'username'
                }
            ]
        }]
    });
   };

MA.Dashboard.CreateQuotesRequiringAttention = function() {
    var selectionModel = new Ext.grid.RowSelectionModel({ 
        singleSelect: true
    });
    var madasReader = new Ext.data.JsonReader({
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

    var dataurl = MA.BaseUrl + "quote/listNeedsAttention";
    var editQuote = function(quote_id) {
        MA.ChangeMainContent('quote:edit', [quote_id]);
    };
    var quoteEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editQuote(selectionModel.getSelected().data.id);
        }
    };

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'quoteEditBtn', text: 'Edit', handler: quoteEditHandler }
        ]
    });

    return new Ext.Panel({
        title:'Quotes Requiring Attention',
        style:'padding:20px 20px 0px 20px',
        id:'dashboard-quotes-requiring-attention',
        tbar: toolbar,
        init: function() {
            this.items.items[0].store.load();
        },
        items:[{
            xtype:'grid',
            border: false,
            autoScroll: true,
            stripeRows: true,
            height: 150,
            ds: new Ext.data.Store({
                id         : 'bSId',
                reader     : madasReader,
                sortInfo   : {field: 'requesttime', direction: 'DESC'},
                url        : dataurl
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
                            renderer: MA.Utils.GridCheckboxRenderer,
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

MA.Dashboard.CreateRecentProjects = function() {
    var selectionModel = new Ext.grid.RowSelectionModel({ 
        singleSelect: true
    });
    var madasReader = new Ext.data.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType: Ext.data.SortTypes.asInt },
            { name: 'title', sortType: Ext.data.SortTypes.asText },
            { name: 'client', sortType: Ext.data.SortTypes.asText }
        ]);

    var dataurl = MA.BaseUrl + "ws/recent_projects";
    var editProject = function(project_id) {
        MA.LoadProject(project_id);
    };
    var projectEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editProject(selectionModel.getSelected().data.id);
        }
    };

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'projectEditBtn', text: 'Edit', handler: projectEditHandler }
        ]
    });

    return new Ext.Panel({
        title:'Recent Projects',
        style:'padding:20px 20px 0px 20px',
        id:'dashboard-recent-projects',
        tbar: toolbar,
        init: function() {
            this.items.items[0].store.load();
        },
        items:[{
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
            listeners: {
                rowdblclick: function(grid, rowIndex, evt) {
                    var record = grid.store.getAt(rowIndex);
                    editProject(record.get('id'));
                }
            },
            columns: [{
                    header: 'ID',
                    sortable: true,
                    width: 40,
                    dataIndex: 'id'
                },{
                    header: 'Title',
                    width: 300,
                    dataIndex: 'title'
                },{
                    header: 'Client',
                    sortable: true,
                    width: 400,
                    dataIndex: 'client'
                }
            ]}
       ]
    });
   };



MA.Dashboard.CreateRecentExperiments = function() {
    var selectionModel = new Ext.grid.RowSelectionModel({ 
        singleSelect: true
    });
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
        MA.ExperimentController.loadExperiment(experiment_id);
    };
    var experimentEditHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            editExperiment(selectionModel.getSelected().data.id);
        }
    };
    
    MA.LoadMachineAndRuleGeneratorDatastores();

    var toolbar = new Ext.Toolbar({
        items   : [
            { id: 'experimentEditBtn', text: 'Edit', handler: experimentEditHandler }
        ]
    });

    return new Ext.Panel({
        title:'Recent Experiments',
        style:'padding:20px 20px 0px 20px',
        id:'dashboard-recent-experiments',
        tbar: toolbar,
        init: function() {
            this.items.items[0].store.load();
        },
        items:[{
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
            listeners: {
                rowdblclick: function(grid, rowIndex, evt) {
                    var record = grid.store.getAt(rowIndex);
                    editExperiment(record.get('id'));
                }
            },
            columns: [{
                    header: 'ID',
                    sortable: true,
                    width: 40,
                    dataIndex: 'id'
                },{
                    header: 'Title',
                    width: 300,
                    dataIndex: 'title'
                },{
                    header: 'Status',
                    sortable: true,
                    width: 100,
                    dataIndex: 'status'
                }
            ]}
       ]
    });
   };

MA.Dashboard.CreateRecentRuns = function() {
    var selectionModel = new Ext.grid.RowSelectionModel({ 
        singleSelect: true
    });
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



MA.Dashboard.CreateAvailableFiles = function() {
    var downloadClientFile = function(fileID) {
        window.location = MA.BaseUrl + "ws/downloadClientFile/" + fileID;
    };

    return new Ext.Panel({
        title:'Available files',
        style:'padding:20px 20px 0px 20px',
        id:'dashboard-available-files',
        tbar:[{
            xtype:'tbtext',
            text:'Click a filename to download'
        }],
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
                                       downloadClientFile(node.id);
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

MA.Dashboard.CreateToolbar = function() {
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


MA.Dashboard.CreateAdminDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.Dashboard.CreateToolbar(),
            MA.Dashboard.CreatePendingUserRequests(),
            MA.Dashboard.CreateQuotesRequiringAttention(),
            MA.Dashboard.CreateRecentProjects(),
            MA.Dashboard.CreateRecentExperiments()
        ]
    });
};

MA.Dashboard.CreateClientDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.Dashboard.CreateToolbar(),
            MA.Dashboard.CreateRecentExperiments(),
            MA.Dashboard.CreateAvailableFiles()
        ]
    });
};

MA.Dashboard.CreateStaffDashboard = function() {
    return new Ext.Container({
        id: 'dashboard-panel',
        autoScroll: true,
        init: function() {
            var i;
            for (i=0; i < this.items.length; i++) {
                this.items.items[i].init();
            }
        },
        items: [
            MA.Dashboard.CreateToolbar(),
            MA.Dashboard.CreateRecentProjects(),
            MA.Dashboard.CreateRecentExperiments(),
            MA.Dashboard.CreateRecentRuns()
        ]
    });
};


MA.Dashboard.Create = function() {
    if (!MA.CurrentUser.IsLoggedIn) {
        return;
    }
    MA.Dashboard.IsCreated = true;
    if (MA.CurrentUser.IsAdmin || MA.CurrentUser.IsNodeRep) {
        return MA.Dashboard.CreateAdminDashboard();
    } else if (MA.CurrentUser.IsClient) {
        return MA.Dashboard.CreateClientDashboard();
    } else {
        return MA.Dashboard.CreateStaffDashboard();
    }
};

MA.Dashboard.IsCreated = false;
MA.Dashboard.Init = function(){
    var dboard;
    if (!MA.Dashboard.IsCreated) {
        dboard = MA.Dashboard.Create();
        if (dboard !== undefined) {
            Ext.getCmp('center-panel').add(dboard);
        }
    }
    if (MA.Dashboard.IsCreated) {
        Ext.getCmp('dashboard-panel').init();
    }
};

