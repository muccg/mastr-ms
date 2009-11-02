Ext.madasMenuRender = function(username) {

    var userText =  'User: '+username;

    var tb = new Ext.Toolbar(

        {
            id: 'toolbar',
            items: [
                { xtype: 'tbbutton', text:'Login', id:'login', handler: Ext.madasMenuHandler},
                { xtype: 'tbbutton', text:'Dashboard', id:'dashboard', handler: Ext.madasMenuHandler},
                { xtype: 'tbbutton', text:'Admin', id:'admin', menu:{
                    items: [
                        {text:'Admin Requests', id:'admin:adminrequests', handler: Ext.madasMenuHandler},
                        {text:'Active User Search', id:'admin:usersearch', handler: Ext.madasMenuHandler},
                        {text:'Rejected User Search', id:'admin:rejectedUsersearch', handler: Ext.madasMenuHandler},
                        {text:'Deleted User Search', id:'admin:deletedUsersearch', handler: Ext.madasMenuHandler},
                        new Ext.menu.Separator(),
                        {text:'Node Management', id:'admin:nodelist', handler: Ext.madasMenuHandler}
                    ]
                    }
                },
                { xtype: 'tbbutton', text:'Quotes', menu:{
                    items: [
                        {text:'Make an Inquiry', id:'quote:request', handler: Ext.madasMenuHandler},
                        {text:'View Quote Requests', id:'quote:list', handler: Ext.madasMenuHandler},
                        {text:'My Formal Quotes', id:'quote:listFormal', handler: Ext.madasMenuHandler},
                        {text:'Overview List', id:'quote:listAll', handler: Ext.madasMenuHandler}
                    ]
                    }
                },
                { xtype: 'tbbutton', text:'Help', menu:{
                    items: [
                            {text:'Screencasts', id:'help:screencasts', menu: {
                            items: [
                                    {text:'Requesting a Quote', id:'help:screencasts-quoterequest', handler: Ext.madasMenuHandler}
                                    ]
                            } 
                            },
                            {text:'Admin screencasts', id:'helpadmin:screencasts', menu: {
                            items: [
                                    {text:'Accepting/rejecting users', id:'helpadmin:screencasts-authrequest', handler: Ext.madasMenuHandler},
                                    {text:'Forwarding a Quote Request', id:'helpadmin:screencasts-forwardquoterequest', handler: Ext.madasMenuHandler},
                                    {text:'Sending a Formal Quote', id:'helpadmin:screencasts-forwardformal', handler: Ext.madasMenuHandler},
                                    {text:'Replacing a Formal Quote', id:'helpadmin:screencasts-replaceformal', handler: Ext.madasMenuHandler}
                                    ]
                            } 
                            },
                            {text:'Contact Us', id:'help:contactus', handler: Ext.madasMenuHandler }
                            ]
                    }
                },
                    
                { xtype: 'tbfill'},
                { xtype: 'tbbutton', text:userText, id: 'userMenu', menu:{
                    items: [
                        {text:'Logout', id:'login:processLogout', handler: Ext.madasLogoutHandler},
                        {text:'My Account', id:'user:myaccount', handler: Ext.madasMenuHandler}
                    ]
                    }
                }
            ]
        }

    );
    tb.render('toolbar');

}

Ext.madasMenuEnsure = function() {
    if (Ext.madasIsLoggedIn) 
        Ext.madasMenuShow();
    else 
        Ext.madasMenuHide();
}

Ext.madasMenuShow = function() {

    Ext.BLANK_IMAGE_URL = Ext.madasBaseUrl + 'static/js/ext/resources/images/default/s.gif';

    //disable certain menu items if the user is not an admin
    if (!Ext.madasIsAdmin) {
        Ext.getCmp('admin:nodelist').disable();
        if (!Ext.madasIsNodeRep) {
	        Ext.get('admin').hide();
            Ext.getCmp('helpadmin:screencasts').disable();
        }
        else {
        	Ext.get('admin').show();
            Ext.getCmp('helpadmin:screencasts').enable();
        }
    } else {
        Ext.getCmp('admin:nodelist').enable();
        Ext.get('admin').show();
        Ext.getCmp('helpadmin:screencasts').enable();
    }

    Ext.get('login').hide();
    Ext.get('dashboard').show();
    Ext.get('userMenu').show();
    Ext.getCmp('quote:list').show();
    Ext.getCmp('quote:listAll').show();
    Ext.getCmp('quote:listFormal').show();

}

Ext.madasMenuHandler = function(item) {
    //we authorize every access to check for session timeout and authorization to specific pages
    if (item.id.substr(0,4) == "help") {
        Ext.madasChangeMainContent(item.id);
    } else {
        Ext.madasAuthorize(item.id);
    }
}

Ext.madasLogoutHandler = function() {
    window.location = "login/processLogout";
}

Ext.madasMenuHide = function() {

    Ext.get('login').show();
    Ext.get('dashboard').hide();
    Ext.get('admin').hide();
    Ext.get('userMenu').hide();
    Ext.getCmp('quote:list').hide();
    Ext.getCmp('quote:listAll').hide();
    Ext.getCmp('quote:listFormal').hide();
    Ext.getCmp('helpadmin:screencasts').disable();
}

