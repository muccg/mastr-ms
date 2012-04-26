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
MA.AdminRequestsInit = function(){
    
	var dataurl = MA.BaseUrl + "admin/adminrequests";
    
    var madasReader = new Ext.data.JsonReader({
                                              root            : 'response.value.items',
                                              versionProperty : 'response.value.version',
                                              totalProperty   : 'response.value.total_count'
                                              }, [
                                                  { name: 'username', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'firstname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'lastname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'email', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'telephoneNumber', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'physicalDeliveryOfficeName', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'title', sortType : Ext.data.SortTypes.asText }
                                                  ]);
    
    var dataStore = new Ext.data.Store({
                                       id         : 'bSId',
                                       autoLoad   : true,
                                       reader     : madasReader,
                                       sortInfo   : {field: 'username', direction: 'ASC'},
                                       url        : dataurl
                                       });
    var gridView = new Ext.grid.GridView({
                                         loadMask : { msg : 'Please wait...' },
                                         forceFit: true
                                         });
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.ChangeMainContent('admin:useredit', [selectionModel.getSelected().data['username']]);
        }
    };
    var topToolbar = new Ext.Toolbar({
                                     items   : [
                                                {  id: 'adminrequestsEditBtn', text: 'Edit', handler: editHandler, disabled: true }
                                                ]
                                     });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var colModel = new Ext.grid.ColumnModel([	
                                             {header: 'Username', width:185, align : 'left', sortable: true, dataIndex: 'username', sortable: true },
                                             {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname', sortable: true },
                                             {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname', sortable: true },
                                             {header: 'Phone', align : 'left', sortable: true, dataIndex: 'telephoneNumber', sortable: true },
                                             {header: 'Office', align : 'left', sortable: true, dataIndex: 'physicalDeliveryOfficeName', sortable: true },
                                             {header: 'Title', align : 'left', sortable: true, dataIndex: 'title', sortable: true }
                                             ]);
    var grid = new Ext.grid.GridPanel({
                                      id             : 'adminrequests-panel',
                                      ds             : dataStore,
                                      enableDragDrop : false,
                                      enableColumnMove: false,
                                      cm             : colModel,
                                      sm             : selectionModel,
                                      loadMask       : { msg : 'Loading...' },
                                      view           : gridView,
                                      title          : 'Administrator Requests',
                                      tbar           : topToolbar,
                                      trackMouseOver : false,
                                      plugins:[new Ext.ux.grid.Search({
                                                                      mode:'local',
                                                                      iconCls:false,
                                                                      dateFormat:'m/d/Y',
                                                                      minLength:0,
                                                                      width:150,
                                                                      position:'top'
                                                                      })]
                                      });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('adminrequestsEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);
    
};

MA.UserSearchInit = function(){
    
	var dataurl = MA.BaseUrl + "admin/usersearch";
    
    var madasReader = new Ext.data.JsonReader({
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
    
    var dataStore = new Ext.data.Store({
                                       id         : 'bSId',
                                       autoLoad   : true,
                                       reader     : madasReader,
                                       sortInfo   : {field: 'username', direction: 'ASC'},
                                       url        : dataurl
                                       });
    var gridView = new Ext.grid.GridView({
                                         loadMask : { msg : 'Please wait...' },
                                         forceFit: true
                                         });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var colModel = new Ext.grid.ColumnModel([	
                                             {header: 'Client?', width:35, sortable:true, dataIndex:'isClient', renderer: MA.Utils.GridCheckboxRenderer},
                                             {header: 'Username', width:185, align : 'left', sortable: true, dataIndex: 'username', sortable: true },
                                             {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname', sortable: true },
                                             {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname', sortable: true },
                                             {header: 'Phone', align : 'left', sortable: true, dataIndex: 'telephoneNumber', sortable: true },
                                             {header: 'Office', align : 'left', sortable: true, dataIndex: 'physicalDeliveryOfficeName', sortable: true },
                                             {header: 'Title', align : 'left', sortable: true, dataIndex: 'title', sortable: true }
                                             ]);
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.ChangeMainContent('admin:useredit', [selectionModel.getSelected().data['username']]);
        }
    };
    var topToolbar = new Ext.Toolbar({
                                     items   : [
                                                { id: 'usersearchEditBtn', text: 'Edit', handler: editHandler, disabled: true }
                                                ]
                                     });
    var grid = new Ext.grid.GridPanel({
                                      id             : 'usersearch-panel',
                                      ds             : dataStore,
                                      enableDragDrop : false,
                                      enableColumnMove: false,
                                      cm             : colModel,
                                      sm             : selectionModel,
                                      loadMask       : { msg : 'Loading...' },
                                      view           : gridView,
                                      title          : 'Active User Search',
                                      tbar           : topToolbar,
                                      trackMouseOver : false,
                                      plugins:[new Ext.ux.grid.Search({
                                                                      mode:'local',
                                                                      iconCls:false,
                                                                      dateFormat:'m/d/Y',
                                                                      minLength:0,
                                                                      width:150,
                                                                      position:'top'
                                                                      })]
                                      });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('usersearchEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);
    
};

MA.RejectedUserSearchInit = function(){
    
	var dataurl = MA.BaseUrl + "admin/rejectedUsersearch";
    
    var madasReader = new Ext.data.JsonReader({
                                              root            : 'response.value.items',
                                              versionProperty : 'response.value.version',
                                              totalProperty   : 'response.value.total_count'
                                              }, [
                                                  { name: 'username', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'firstname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'lastname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'email', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'telephoneNumber', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'physicalDeliveryOfficeName', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'title', sortType : Ext.data.SortTypes.asText }
                                                  ]);
    
    var dataStore = new Ext.data.Store({
                                       id         : 'bSId',
                                       autoLoad   : true,
                                       reader     : madasReader,
                                       sortInfo   : {field: 'username', direction: 'ASC'},
                                       url        : dataurl
                                       });
    var gridView = new Ext.grid.GridView({
                                         loadMask : { msg : 'Please wait...' },
                                         forceFit: true
                                         });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var colModel = new Ext.grid.ColumnModel([	
                                             {header: 'Username', width:185, align : 'left', sortable: true, dataIndex: 'username', sortable: true },
                                             {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname', sortable: true },
                                             {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname', sortable: true },
                                             {header: 'Phone', align : 'left', sortable: true, dataIndex: 'telephoneNumber', sortable: true },
                                             {header: 'Office', align : 'left', sortable: true, dataIndex: 'physicalDeliveryOfficeName', sortable: true },
                                             {header: 'Title', align : 'left', sortable: true, dataIndex: 'title', sortable: true }
                                             ]);
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.ChangeMainContent('admin:useredit', [selectionModel.getSelected().data['username']]);
        }
    };
    var topToolbar = new Ext.Toolbar({
                                     items   : [
                                                { id: 'rejectedusersearchEditBtn', text: 'Edit', handler: editHandler, disabled: true }
                                                ]
                                     });
    var grid = new Ext.grid.GridPanel({
                                      id             : 'rejectedusersearch-panel',
                                      ds             : dataStore,
                                      enableDragDrop : false,
                                      enableColumnMove: false,
                                      cm             : colModel,
                                      sm             : selectionModel,
                                      loadMask       : { msg : 'Loading...' },
                                      view           : gridView,
                                      title          : 'Rejected User Search',
                                      tbar           : topToolbar,
                                      trackMouseOver : false,
                                      plugins:[new Ext.ux.grid.Search({
                                                                      mode:'local',
                                                                      iconCls:false,
                                                                      dateFormat:'m/d/Y',
                                                                      minLength:0,
                                                                      width:150,
                                                                      position:'top'
                                                                      })]
                                      });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('rejectedusersearchEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);
    
};

MA.DeletedUserSearchInit = function(){
    
	var dataurl = MA.BaseUrl + "admin/deletedUsersearch";
    
    var madasReader = new Ext.data.JsonReader({
                                              root            : 'response.value.items',
                                              versionProperty : 'response.value.version',
                                              totalProperty   : 'response.value.total_count'
                                              }, [
                                                  { name: 'username', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'firstname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'lastname', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'email', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'telephoneNumber', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'physicalDeliveryOfficeName', sortType : Ext.data.SortTypes.asText },
                                                  { name: 'title', sortType : Ext.data.SortTypes.asText }
                                                  ]);
    
    var dataStore = new Ext.data.Store({
                                       id         : 'bSId',
                                       autoLoad   : true,
                                       reader     : madasReader,
                                       sortInfo   : {field: 'username', direction: 'ASC'},
                                       url        : dataurl
                                       });
    var gridView = new Ext.grid.GridView({
                                         loadMask : { msg : 'Please wait...' },
                                         forceFit: true
                                         });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var colModel = new Ext.grid.ColumnModel([	
                                             {header: 'Username', width:185, align : 'left', sortable: true, dataIndex: 'username', sortable: true },
                                             {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname', sortable: true },
                                             {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname', sortable: true },
                                             {header: 'Phone', align : 'left', sortable: true, dataIndex: 'telephoneNumber', sortable: true },
                                             {header: 'Office', align : 'left', sortable: true, dataIndex: 'physicalDeliveryOfficeName', sortable: true },
                                             {header: 'Title', align : 'left', sortable: true, dataIndex: 'title', sortable: true }
                                             ]);
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.ChangeMainContent('admin:useredit', [selectionModel.getSelected().data['username']]);
        }
    };
    var topToolbar = new Ext.Toolbar({
                                     items   : [
                                                { id: 'deletedusersearchEditBtn', text: 'Edit', handler: editHandler, disabled: true }
                                                ]
                                     });
    var grid = new Ext.grid.GridPanel({
                                      id             : 'deletedusersearch-panel',
                                      ds             : dataStore,
                                      enableDragDrop : false,
                                      enableColumnMove: false,
                                      cm             : colModel,
                                      sm             : selectionModel,
                                      loadMask       : { msg : 'Loading...' },
                                      view           : gridView,
                                      title          : 'Deleted User Search',
                                      tbar           : topToolbar,
                                      trackMouseOver : false,
                                      plugins:[new Ext.ux.grid.Search({
                                                                      mode:'local',
                                                                      iconCls:false,
                                                                      dateFormat:'m/d/Y',
                                                                      minLength:0,
                                                                      width:150,
                                                                      position:'top'
                                                                      })]
                                      });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('deletedusersearchEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);
    
};


MA.AdminUserEditInit = function (paramArray) {
    var username = paramArray[0];
    var adminUserEditCmp = Ext.getCmp('adminuseredit-panel');   
    var user = MA.CurrentUser;
    
    //fetch user details
    adminUserEditCmp.load({url: MA.BaseUrl + 'admin/userload', params: {'username': username}, waitMsg:'Loading'});
    
    //attach validator that ext cannot deal with
    Ext.getCmp("adminUserEditPassword").on('blur', MA.AdminUserEditValidatePassword);
    Ext.getCmp("adminUserEditConfirmPassword").on('blur', MA.AdminUserEditValidatePassword);
    
    Ext.getCmp('adminUserEditSubmit').enable();
    //Load the organisation store
    Ext.getCmp('adminUserEditOrganisation').store.load();

    Ext.getCmp('adminUserEditIsAdmin').setDisabled(!user.IsAdmin);
    Ext.getCmp('adminUserEditIsNodeRep').setDisabled(!(user.IsAdmin || user.IsNodeRep));
    Ext.getCmp('adminUserEditNode').setDisabled(!user.IsAdmin);
    Ext.getCmp('adminUserEditIsMastrAdmin').setDisabled(!(user.IsAdmin || user.IsMastrAdmin));
    Ext.getCmp('adminUserEditIsProjectLeader').setDisabled(!(user.IsAdmin || user.IsMastrAdmin || user.isProjectLeader));
    Ext.getCmp('adminUserEditIsMastrStaff').setDisabled(!(user.IsAdmin || user.IsMastrAdmin || user.isProjectLeader));
    
    //reload the combobox
    if (Ext.StoreMgr.containsKey('adminUserEditNodeDS')) {
        Ext.StoreMgr.get('adminUserEditNodeDS').reload();
    }
    
    //allow the madas changeMainContent function to handle the rest from here
    return;
};

/**
 * madasAdminUserEditValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
MA.AdminUserEditValidatePassword = function (textfield, event) {
    var passEl = Ext.getCmp('adminUserEditPassword');
    var confirmEl = Ext.getCmp('adminUserEditConfirmPassword');
    var submitEl = Ext.getCmp('adminUserEditSubmit');
    
    var passVal = Ext.getDom('adminUserEditPassword').value;
    var confirmVal = Ext.getDom('adminUserEditConfirmPassword').value;
    
    if (passVal == confirmVal) {
        confirmEl.clearInvalid();
        submitEl.enable();
        return true; 
    } else { 
        confirmEl.markInvalid('Password and Confirm Password must match');
        submitEl.disable();
        return false;
    }
};

MA.AdminUserEditCmp = {id:'adminuseredit-container-panel', 
    layout:'absolute', 
    autoScroll:true,
    deferredRender:false,
    forceLayout:true,
    defaults:{
        deferredRender:false,
        forceLayout:true
    },
    items:[
           {  xtype:'form', 
           labelWidth: 100, // label settings here cascade unless overridden
           id:'adminuseredit-panel',
           url:MA.BaseUrl + 'admin/userSave',
           method:'POST',
           frame:true,
           reader: new Ext.data.JsonReader({
                                                 root            : 'data',
                                                 idProperty      : 'username',
                                                 versionProperty : 'response.value.version',
                                                 totalProperty   : 'response.value.total_count',
                                                 successProperty : 'success'
                                                 }, [
                                                     { name: 'username', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'firstname', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'lastname', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'email', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'telephoneNumber', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'physicalDeliveryOfficeName', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'title', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'homephone', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'isAdmin', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'isNodeRep', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'isMastrAdmin', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'isProjectLeader', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'isMastrStaff', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'node', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'status', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'dept', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'institute', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'organisation', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'address', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'supervisor', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'areaOfInterest', sortType : Ext.data.SortTypes.asText },
                                                     { name: 'country', sortType : Ext.data.SortTypes.asText }
                                                     ]),
       title: 'Edit User',
       bodyStyle:'padding:5px 5px 0',
       width: 380,
       x: 50,
       y: 10,
       defaults: {width: 230},
       defaultType: 'textfield',
       trackResetOnLoad: true,
       waitMsgTarget: true,
       
       items: [
               {   name: 'originalEmail',
               inputType: 'hidden'
               },{
               fieldLabel: 'Email address',
               name: 'email',
               vtype: 'email',
               allowBlank:false,
               readOnly:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'First name',
               name: 'firstname',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Last name',
               name: 'lastname',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Password',
               name: 'password',
               id: 'adminUserEditPassword',
               inputType: 'password',
               allowBlank:true
               },{
               fieldLabel: 'Confirm Password',
               inputType: 'password',
               id: 'adminUserEditConfirmPassword',
               xtype: 'textfield',
               allowBlank: true,
               validator: MA.AdminUserEditValidatePassword
               },{
               fieldLabel: 'Office',
               name: 'physicalDeliveryOfficeName',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Office Phone',
               name: 'telephoneNumber',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Home Phone',
               name: 'homephone',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Position',
               name: 'title',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               xtype:'checkbox',
               id: 'adminUserEditIsAdmin',
               name: 'isAdmin',
               inputValue: 'true',
               fieldLabel: 'Administrator'
               },{
               xtype:'checkbox', 
               id: 'adminUserEditIsNodeRep',
               name: 'isNodeRep', 
               inputValue: 'true',
               fieldLabel: 'Node Rep'
               },{
               xtype:'checkbox',
               id: 'adminUserEditIsMastrAdmin',
               name: 'isMastrAdmin',
               inputValue: 'true',
               fieldLabel: 'Mastr Administrator'
               },{
               xtype:'checkbox',
               id: 'adminUserEditIsProjectLeader',
               name: 'isProjectLeader',
               inputValue: 'true',
               fieldLabel: 'Project Leader'
               },{
               xtype:'checkbox',
               id: 'adminUserEditIsMastrStaff',
               name: 'isMastrStaff',
               inputValue: 'true',
               fieldLabel: 'Mastr Staff'
               }, new Ext.form.ComboBox({
                                        fieldLabel: 'Node',
                                        id: 'adminUserEditNode',
                                        name: 'nodeDisplay',
                                        editable:false,
                                        forceSelection:true,
                                        displayField:'name',
                                        valueField:'submitValue',
                                        hiddenName:'node',
                                        lazyRender:true,
                                        typeAhead:false,
                                        triggerAction:'all',
                                        listWidth:230,
                                        store: new Ext.data.JsonStore({
                                                                      storeId: 'adminUserEditNodeDS',
                                                                      url: MA.BaseUrl + 'user/listAllNodes',
                                                                      root: 'response.value.items',
                                                                      fields: ['name', 'submitValue']
                                                                      })
                                        }), new Ext.form.ComboBox({
                                                                  fieldLabel: 'Status',
                                                                  name: 'statusDisplay',
                                                                  editable:false,
                                                                  forceSelection:true,
                                                                  displayField:'displayLabel',
                                                                  valueField:'submitValue',
                                                                  hiddenName:'status',
                                                                  lazyRender:true,
                                                                  typeAhead:false,
                                                                  mode:'local',
                                                                  triggerAction:'all',
                                                                  listWidth:230,
                                                                  store: new Ext.data.SimpleStore({
                                                          fields: ['submitValue', 'displayLabel'],
                                                          data : [['Pending','Pending'],
                                                                  ['User', 'Active'],
                                                                  ['Deleted','Deleted'],
                                                                  ['Rejected','Rejected']]
                                                          })
                                                                  }),{
               fieldLabel: 'Department',
               name: 'dept',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Institute',
               name: 'institute',
               allowBlank:true,
               maskRe: /[^,=]/
               },
               new Ext.form.ComboBox({
                                        fieldLabel: 'Organisation',
                                        id: 'adminUserEditOrganisation',
                                        name: 'orgDisplay',
                                        editable:false,
                                        forceSelection:true,
                                        displayField:'name',
                                        valueField:'id',
                                        hiddenName:'organisation',
                                        lazyRender:true,
                                        typeAhead:false,
                                        triggerAction:'all',
                                        listWidth:230,
                                        store: new Ext.data.JsonStore({
                                                                      autoLoad:false,
                                                                      storeId: 'organisationDS',
                                                                      url: MA.BaseUrl + 'admin/listOrganisations',
                                                                      root: 'response.value.items',
                                                                      fields: ['name', 'id']
                                                                      })
                                        }),
               {
               fieldLabel: 'Address',
               name: 'address',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Supervisor',
               name: 'supervisor',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Area of Interest',
               name: 'areaOfInterest',
               allowBlank:true,
               maskRe: /[^,=]/
               },new Ext.form.ComboBox({
                                       fieldLabel: 'Country',
                                       name: 'countryDisplay',
                                       editable:false,
                                       forceSelection:true,
                                       displayField:'displayLabel',
                                       valueField:'submitValue',
                                       hiddenName:'country',
                                       lazyRender:true,
                                       typeAhead:false,
                                       mode:'local',
                                       triggerAction:'all',
                                       listWidth:230,
                                       store: countryStore
                                       })                    ],
       buttons: [{
                 text: 'Cancel',
                 handler: function(){
                    Ext.getCmp('adminuseredit-panel').getForm().reset(); 
                    MA.ChangeMainContent(MA.CancelBackTarget);
                 }
                 },{
                 text: 'Save',
                 id: 'adminUserEditSubmit',
                 handler: function(){
                 Ext.getCmp('adminuseredit-panel').getForm().submit(
                                                                    {   successProperty: 'success',        
                                                                    success: function (form, action) {
                                                                    if (action.result.success === true) {
                                                                        form.reset(); 
                                                                    
                                                                        //display a success alert that auto-closes in 5 seconds
                                                                        Ext.Msg.alert("User details saved successfully", "(this message will auto-close in 5 seconds)");
                                                                        setTimeout(Ext.Msg.hide, 5000);
                                                                    
                                                                        //MA.ChangeMainContent(action.result.mainContentFunction);
                                                                        MA.ChangeMainContent(MA.CancelBackTarget);
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
};

//handles selection and loading of node details
MA.NodeManagementSelectionManager = function(selModel) { 
    if (selModel.hasSelection()) { 
        Ext.getCmp('nodedetails-name').setValue(selModel.getSelected().data['name']);
        Ext.getCmp('nodedetails-originalName').setValue(selModel.getSelected().data['name']);
        
        Ext.getCmp('nodedetails-panel').enable(); 
    } else { 
        //clear details when nothing is selected
        Ext.getCmp('nodedetails-name').setValue('');
        Ext.getCmp('nodedetails-originalName').setValue('');
        
        Ext.getCmp('nodedetails-panel').disable(); 
    } 
};

//clearing the form on a Cancel click
//reuse the same functionality as if the user had just clicked on a new item in the grid
MA.NodeManagementClearForm = function() {
    MA.NodeManagementSelectionManager(Ext.getCmp('nodeListGrid').getSelectionModel());
};

//handle the click on the 'add' tool button
MA.NodeManagementAddTool = function(event, toolEl, panel) {
    Ext.getCmp('nodeListGrid').getSelectionModel().clearSelections();
    
    Ext.getCmp('nodedetails-name').setValue('New node');
    Ext.getCmp('nodedetails-originalName').setValue('');
    
    Ext.getCmp('nodedetails-panel').enable();
};

//handle the click on the 'delete' tool button
MA.NodeManagementDeleteTool = function(event, toolEl, panel) {
    if (! Ext.getCmp('nodeListGrid').getSelectionModel().hasSelection()) {
        return false;
    }
    
    var nodename = Ext.getCmp('nodeListGrid').getSelectionModel().getSelected().data['name'];
    
    //only perform the deletion if the user confirms their action
    Ext.Msg.confirm('Confirm deletion', 'Are you sure you wish to delete the node: ' + nodename + ' ?', function(btn, text) {
                    if (btn == 'yes'){
                    
                    var nodename = Ext.getCmp('nodeListGrid').getSelectionModel().getSelected().data['name'];
                    
                    //execute the delete
                    //submit form   
                    var simple = new Ext.BasicForm('hiddenForm', {
                                                   url:MA.BaseUrl + 'admin/nodeDelete',
                                                   baseParams:{'name':nodename},
                                                   method:'POST'
                                                   });         
                    
                    var submitOptions = {   
                    successProperty: 'success',
                    success: function (form, action) {
                    //display a success alert that auto-closes in 5 seconds
                    Ext.Msg.alert("Node deleted successfully", "(this message will auto-close in 5 seconds)");
                    setTimeout(Ext.Msg.hide, 5000);
                    
                    //load up the menu and next content area as declared in response
                    MA.ChangeMainContent(action.result.mainContentFunction);
                    },
                    failure: function (form, action) {
                    //load up the menu and next content area as declared in response
                    MA.ChangeMainContent(action.result.mainContentFunction);
                    }
                    };
                    
                    simple.submit(submitOptions);
                    
                    
                    //clear the form, ready for future use
                    Ext.getCmp('nodeListGrid').getSelectionModel().clearSelections();
                    
                    Ext.getCmp('nodedetails-name').setValue('');
                    Ext.getCmp('nodedetails-originalName').setValue('');
                    
                    Ext.getCmp('nodedetails-panel').disable();
                    
                    }
                    });
    
};

//initialize node management grid and the event handlers
MA.NodeManagementInit = function() {
    Ext.getCmp('nodeListGrid').getStore().reload();
    
    //enable/disable the details panel when selection is changed (and load the details for the selected item)
    Ext.getCmp('nodeListGrid').getSelectionModel().on('selectionchange', MA.NodeManagementSelectionManager );
    
    //disable the node details panel by default
    Ext.getCmp('nodedetails-panel').disable();
};

//define the node details form
MA.NodeDetailsCmp = {
xtype:'form',
labelWidth: 100, // label settings here cascade unless overridden
id:'nodedetails-panel',
url:MA.BaseUrl + 'admin/nodesave',
region: 'center',
method:'POST',
reader: new Ext.data.JsonReader(),
bodyStyle: 'padding:10px;',
title: 'Node Details',
defaults: {width: 230},
defaultType: 'textfield',
trackResetOnLoad: true,
waitMsgTarget: true,
    
items: [
        {   name: 'originalName', id: 'nodedetails-originalName', xtype: 'hidden' },
        {   name: 'name', id: 'nodedetails-name', fieldLabel: 'Node Name', maskRe: /[^,=]/ }
        ],
buttons: [
          { text: 'Reset', handler: MA.NodeManagementClearForm },
        { text: 'Save', handler: function() { Ext.getCmp('nodedetails-panel').getForm().submit({   
                             successProperty: 'success',
                             success: function (form, action) {
                             if (action.result.success === true) {
                             //display a success alert that auto-closes in 5 seconds
                             Ext.Msg.alert("Node details saved successfully", "(this message will auto-close in 5 seconds)");
                             setTimeout(Ext.Msg.hide, 5000);
                             
                             //load up the menu and next content area as declared in response
                             MA.ChangeMainContent(action.result.mainContentFunction);
                             }
                             },
                             failure: function (form, action) {
                                Ext.Msg.alert("Error", action.result.msg);
                             }
                             });
          } }
          ]
};


MA.NodeManagementCmp = {
id:'nodeManagementCmp',
layout:'border',
items: [
        {
        title:'Node List',
        id:'nodeListGrid',
        region:'west',
        minWidth: 450,
        width: 450,
        split:true,
        xtype:'grid',
        tools: [
                { id: 'plus', qtip: 'Add a new node', handler: MA.NodeManagementAddTool },
                { id: 'minus', qtip: 'Delete currently selected node', handler: MA.NodeManagementDeleteTool }
                ],
        store: new Ext.data.JsonStore({
                                      url: MA.BaseUrl + 'user/listAllNodes',
                                      baseParams: { 'ignoreNone' : 'on' },
                                      root: 'response.value.items',
                                      fields: ['name', 'submitValue']
                                      }),
        columns: [
                  {header: 'Name', sortable:true, dataIndex: 'name'}
                  ],
        viewConfig: {
        forceFit:true
        },
        sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
        lazyRender:true,
        bbar:[{xtype:'tbspacer'}],
        plugins:[new Ext.ux.grid.Search({
                                        mode:'local',
                                        iconCls:false,
                                        dateFormat:'m/d/Y',
                                        minLength:0,
                                        width:150
                                        })]
        },
        MA.NodeDetailsCmp
        ]
};

//org management component ------------------------------------------------------------------------------------//

//handles selection and loading of org details
MA.OrgManagementSelectionManager = function(selModel) { 
    if (selModel.hasSelection()) { 
        Ext.getCmp('orgdetails-name').setValue(selModel.getSelected().data['name']);
        Ext.getCmp('orgdetails-id').setValue(selModel.getSelected().data['id']);
        Ext.getCmp('orgdetails-abn').setValue(selModel.getSelected().data['abn']);
        
        Ext.getCmp('orgdetails-panel').enable(); 
    } else { 
        //clear details when nothing is selected
        Ext.getCmp('orgdetails-name').setValue('');
        Ext.getCmp('orgdetails-id').setValue('');
        Ext.getCmp('orgdetails-abn').setValue('');
        
        Ext.getCmp('orgdetails-panel').disable(); 
    } 
};

//clearing the form on a Cancel click
//reuse the same functionality as if the user had just clicked on a new item in the grid
MA.OrgManagementClearForm = function() {
    MA.OrgManagementSelectionManager(Ext.getCmp('orgListGrid').getSelectionModel());
};

//handle the click on the 'add' tool button
MA.OrgManagementAddTool = function(event, toolEl, panel) {
    Ext.getCmp('orgListGrid').getSelectionModel().clearSelections();
    
    Ext.getCmp('orgdetails-name').setValue('New Organisation');
    Ext.getCmp('orgdetails-id').setValue('0');
    Ext.getCmp('orgdetails-abn').setValue('');
    
    Ext.getCmp('orgdetails-panel').enable();
};

//handle the click on the 'delete' tool button
MA.OrgManagementDeleteTool = function(event, toolEl, panel) {
    if (! Ext.getCmp('orgListGrid').getSelectionModel().hasSelection()) {
        return false;
    }
    
    var orgname = Ext.getCmp('orgListGrid').getSelectionModel().getSelected().data['name'];
    
    //only perform the deletion if the user confirms their action
    Ext.Msg.confirm('Confirm deletion', 'Are you sure you wish to delete the organisation: ' + orgname + ' ?', function(btn, text) {
                    if (btn == 'yes'){
                    
                    var orgid = Ext.getCmp('orgListGrid').getSelectionModel().getSelected().data['id'];
                    
                    //execute the delete
                    //submit form   
                    var simple = new Ext.BasicForm('hiddenForm', {
                                                   url:MA.BaseUrl + 'admin/orgDelete',
                                                   baseParams:{'id':orgid},
                                                   method:'POST'
                                                   });         
                    
                    var submitOptions = {   
                    successProperty: 'success',
                    success: function (form, action) {
                    //display a success alert that auto-closes in 5 seconds
                    Ext.getCmp('orgListGrid').getStore().reload();
                    Ext.Msg.alert("Organisation deleted successfully", "(this message will auto-close in 5 seconds)");
                    setTimeout(Ext.Msg.hide, 5000);
                    
                    //load up the menu and next content area as declared in response
                    MA.ChangeMainContent(action.result.mainContentFunction);
                    },
                    failure: function (form, action) {
                    //load up the menu and next content area as declared in response
                    MA.ChangeMainContent(action.result.mainContentFunction);
                    }
                    };
                    
                    simple.submit(submitOptions);
                    
                    
                    //clear the form, ready for future use
                    Ext.getCmp('orgListGrid').getSelectionModel().clearSelections();
                    
                    Ext.getCmp('orgdetails-name').setValue('');
                    Ext.getCmp('orgdetails-abn').setValue('');
                    Ext.getCmp('orgdetails-id').setValue('0');
                    
                    Ext.getCmp('orgdetails-panel').disable();
                    
                    }
                    });
    
};


//initialize org management grid and the event handlers
MA.OrgManagementInit = function() {
    Ext.getCmp('orgListGrid').getStore().reload();
    
    //enable/disable the details panel when selection is changed (and load the details for the selected item)
    Ext.getCmp('orgListGrid').getSelectionModel().on('selectionchange', MA.OrgManagementSelectionManager );
    
    //disable the node details panel by default
    Ext.getCmp('orgdetails-panel').disable();
};

//define the node details form
MA.OrgDetailsCmp = {
    xtype:'form',
    labelWidth: 100, // label settings here cascade unless overridden
    id:'orgdetails-panel',
    url:MA.BaseUrl + 'admin/orgsave',
    region: 'center',
    method:'POST',
    reader: new Ext.data.JsonReader(),
    bodyStyle: 'padding:10px;',
    title: 'Organisation Details',
    defaults: {width: 230},
    defaultType: 'textfield',
    trackResetOnLoad: true,
    waitMsgTarget: true,
        
    items: [
            {   name: 'id', id: 'orgdetails-id', xtype: 'hidden' },
            {   name: 'name', id: 'orgdetails-name', fieldLabel: 'Organisation Name', maskRe: /[^,=]/ },
            {   name: 'abn', id: 'orgdetails-abn', fieldLabel: 'ABN', maskRe: /[^,=]/ }
            ],
    buttons: [
              { text: 'Reset', handler: MA.OrgManagementClearForm },
              { text: 'Save', 
                  handler: function() { 
                      Ext.getCmp('orgdetails-panel').getForm().submit({   
                                        successProperty: 'success',
                                        success: function (form, action) {
                                        if (action.result.success === true) {
                                        //display a success alert that auto-closes in 5 seconds
                                        Ext.getCmp('orgListGrid').getStore().reload();
                                        Ext.Msg.alert("Organisation details saved successfully", "(this message will auto-close in 5 seconds)");
                                        setTimeout(Ext.Msg.hide, 5000);
                                        
                                        //load up the menu and next content area as declared in response
                                        MA.ChangeMainContent(action.result.mainContentFunction);
                                        }
                                        },
                                        failure: function (form, action) {
                                        //do nothing special. this gets called on validation failures and server errors
                                        }
                                        });
          } }
          ]
};

MA.OrgManagementCmp = {
    id:'orgManagementCmp',
    layout:'border',
    items: [
        {
        title:'Organisations List',
        id:'orgListGrid',
        region:'west',
        minWidth: 450,
        width: 450,
        split:true,
        xtype:'grid',
        tools: [
                { id: 'plus', qtip: 'Add a new organisation', handler: MA.OrgManagementAddTool },
                { id: 'minus', qtip: 'Delete currently selected organisation', handler: MA.OrgManagementDeleteTool }
                ],
        store: new Ext.data.JsonStore({
                                      url: MA.BaseUrl + 'admin/listOrganisations',
                                      baseParams: { 'ignoreNone' : 'on' },
                                      root: 'response.value.items',
                                      fields: ['name', 'submitValue']
                                      }),
        columns: [
                  {header: 'Name', sortable:true, dataIndex: 'name'}
                  ],
        viewConfig: {
        forceFit:true
        },
        sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
        lazyRender:true,
        bbar:[{xtype:'tbspacer'}],
        plugins:[new Ext.ux.grid.Search({
                                        mode:'local',
                                        iconCls:false,
                                        dateFormat:'m/d/Y',
                                        minLength:0,
                                        width:150
                                        })]
        },
        MA.OrgDetailsCmp
        ]
};
