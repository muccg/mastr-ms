MA.MenuRender = function(username) {

    var userText =  'User: '+username;

    var tb = new Ext.Toolbar(

        {
            id: 'toolbarA',
            items: [
                { xtype: 'tbbutton', text:'Login', id:'login', handler: MA.MenuHandler},
                { xtype: 'tbbutton', text:'Dashboard', id:'dashboard:list', handler: MA.MenuHandler},
                { xtype: 'tbspacer', width: 5 },
                { xtype: 'tbbutton', text:'Projects', id:'projects:list', handler: MA.MenuHandler},
                { xtype: 'tbspacer', width: 5 },
                { xtype: 'tbbutton', text:'Clients', id:'clients:list', handler: MA.MenuHandler},
                { xtype: 'tbspacer', width: 5 },
                { xtype: 'tbbutton', text:'Runs', id:'runs:list', handler: MA.MenuHandler},
                { xtype: 'tbfill'},
                { xtype: 'tbbutton', text:userText, id: 'userMenu', menu:{
                    items: [
                        {text:'Logout', id:'login:processLogout', handler: MA.MenuHandler}
                    ]
                    }
                }
            ]
        }

    );
    tb.render('toolbar');

};

MA.MenuEnsure = function() {
    if (MA.IsLoggedIn) {
        MA.MenuShow();
    } else {
        MA.MenuHide();
    }
};

MA.MenuShow = function() {

    Ext.BLANK_IMAGE_URL = 'static/ext-3.3.0/resources/images/default/s.gif';

    //disable certain menu items if the user is not an admin
    if (!MA.IsAdmin) {
        Ext.getCmp('admin:nodelist').disable();
    }
    
    Ext.get('login').hide();
    Ext.get('dashboard:list').show();
    Ext.get('userMenu').show();
    Ext.get('clients:list').show();
    Ext.get('projects:list').show();
    Ext.get('runs:list').show();

};

MA.MenuHandler = function(item) {
    //we authorize every access to check for session timeout and authorization to specific pages
    
    MA.Authorize(item.id);
    
};

MA.MenuHide = function() {

    Ext.get('login').show();
    //    Ext.get('admin').hide();
    Ext.get('dashboard:list').hide();
    Ext.get('userMenu').hide();

    Ext.get('clients:list').hide();
    //    Ext.getCmp('helpadmin:screencasts').disable();
    Ext.get('projects:list').hide();
    Ext.get("runs:list").hide();

};

