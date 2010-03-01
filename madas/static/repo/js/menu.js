MA.MenuRender = function(username) {

    var userText =  'User: '+username;

    var tb = new Ext.Toolbar(

        {
            id: 'toolbarA',
            items: [
                { xtype: 'tbbutton', text:'Login', id:'login', handler: MA.MenuHandler},
                { xtype: 'tbbutton', text:'Projects', id:'projectsMenu', menu:{
                    items: [
                        {text:'Projects List', id:'projects:list', handler: MA.MenuHandler}
                        ]
                    }
                },
                { xtype: 'tbbutton', text:'Experiment', id:'experimentMenu', menu:{
                    items: [
                        {text:'New Experiment', id:'experiment:new', handler: MA.MenuHandler},
                        {text:'My Experiments', id:'experiment:my', handler: MA.MenuHandler}
                        ]
                    }
                },
                { xtype: 'tbbutton', text:'Clients', id:'clientsMenu', menu:{
                    items: [
                        {text:'Clients List', id:'clients:list', handler: MA.MenuHandler}
                        ]
                    }
                },
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

    Ext.BLANK_IMAGE_URL = 'static/ext-3.1.0/resources/images/default/s.gif';

    //disable certain menu items if the user is not an admin
    if (!MA.IsAdmin) {
        Ext.getCmp('admin:nodelist').disable();
    }
    
    Ext.get('login').hide();
    Ext.get('userMenu').show();
    Ext.get('experimentMenu').show();
    Ext.get('clientsMenu').show();

};

MA.MenuHandler = function(item) {
    //we authorize every access to check for session timeout and authorization to specific pages
    
    MA.Authorize(item.id);
    
};

MA.MenuHide = function() {

    Ext.get('login').show();
    //    Ext.get('admin').hide();
    Ext.get('userMenu').hide();
    Ext.get('experimentMenu').hide();

    Ext.get('clientsMenu').hide();
    //    Ext.getCmp('helpadmin:screencasts').disable();

};

