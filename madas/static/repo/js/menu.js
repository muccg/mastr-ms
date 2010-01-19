MA.MenuRender = function(username) {

    var userText =  'User: '+username;

    var tb = new Ext.Toolbar(

        {
            id: 'toolbarA',
            items: [
                { xtype: 'tbbutton', text:'Login', id:'login', handler: MA.MenuHandler},
                { xtype: 'tbbutton', text:'Experiment', id:'experimentMenu', menu:{
                    items: [
                        {text:'New Experiment', id:'experiment:new', handler: MA.MenuHandler},
                        {text:'My Experiments', id:'experiment:my', handler: MA.MenuHandler}
                        ]
                    }
                },
//                { xtype: 'tbbutton', text:'Admin', id:'admin', menu:{
//                    items: [
//                        {text:'Admin Database', id:'admin:db', handler: MA.MenuHandler}
//                    ]
//                    }
//                },
//                { xtype: 'tbbutton', text:'Help', menu:{
//                    items: [
//                        {text:'Screencasts', id:'help:screencasts', menu: {
//                            items: [
//                                {text:'----------', id:'help:screencasts-quoterequest', handler: MA.MenuHandler}
//                                ]
//                            } 
//                        },
//                        {text:'Admin screencasts', id:'helpadmin:screencasts', menu: {
//                            items: [
//                                {text:'----------', id:'helpadmin:screencasts-authrequest', handler: MA.MenuHandler},
//                                {text:'----------', id:'helpadmin:screencasts-forwardquoterequest', handler: MA.MenuHandler},
//                                {text:'----------', id:'helpadmin:screencasts-forwardformal', handler: MA.MenuHandler},
//                                {text:'----------', id:'helpadmin:screencasts-replaceformal', handler: MA.MenuHandler}
//                                ]
//                            } 
//                        }
//                    ]
//                    }
//                },
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
        if (!MA.IsNodeRep) {
            //	        Ext.get('admin').hide();
//            Ext.getCmp('helpadmin:screencasts').disable();
        } else {
            //        	Ext.get('admin').show();
//            Ext.getCmp('helpadmin:screencasts').enable();
        }
    } else {
//        Ext.getCmp('admin:nodelist').enable();
//        Ext.get('admin').show();
//        Ext.getCmp('helpadmin:screencasts').enable();
    }

    //TEMP hide admin menu from all users
    //    Ext.get('admin').hide();

    
    Ext.get('login').hide();
    Ext.get('userMenu').show();
    Ext.get('experimentMenu').show();

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

    //    Ext.getCmp('helpadmin:screencasts').disable();

};

