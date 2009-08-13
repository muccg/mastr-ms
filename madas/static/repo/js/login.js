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

Ext.madasLoginCmp = {id:'login-container-panel', 
layout:'absolute', 
items:[
       {  xtype:'form', 
       labelWidth: 75, // label settings here cascade unless overridden
       id:'login-panel',
       url:'login/processLogin',
       method:'POST',
       frame:true,
       title: 'Login',
       bodyStyle:'padding:5px 5px 0',
       width: 350,
       x: 200,
       y: 10,
       defaults: {width: 230},
       defaultType: 'textfield',
       
       items: [{
               xtype:'panel',
               el:"loginDiv"
               }
               ]}
       ]
};

Ext.madasNotAuthorizedCmp = { id: 'notauthorized-panel', title: 'Not Authorized', html: 'You are not authorized to access this page' };

/**
 * authorize
 * used to check if the user is still logged in, and if they can access the requested view
 */
Ext.madasAuthorize = function(requestedView, params) {
    if (requestedView == 'notauthorized')
        return Ext.madasChangeMainContent(requestedView, params);
    
    //the module we need to auth against is the first part of the requestedView
    //ie admin/adminrequest
    //we authorize against admin/authorize
    var viewSplit = requestedView.split(":");
    var module = viewSplit[0];
    
    var action = "";
    if (viewSplit.length > 1) {
        action = viewSplit[1];
    }
    
    //submit form
    var simple = new Ext.BasicForm('hiddenForm', {
                                   url:baseUrl+module+'/authorize',
                                   baseParams:{'subaction':action, 'params':Ext.util.JSON.encode(params)},
                                   method:'POST'
                                   });
    
    var submitOptions = {
    successProperty: 'success',        
    success: function (form, action) {
        //load up the menu and next content area as declared in response
        if (action.result.username) {
            Ext.getCmp('userMenu').setText('User: '+action.result.username);
            Ext.madasIsAdmin = action.result.isAdmin;
            Ext.madasIsNodeRep = action.result.isNodeRep;
            Ext.madasIsLoggedIn = true;
        }
        if (! action.result.authenticated) {
            Ext.madasIsAdmin = false;
            Ext.madasIsNodeRep = false;
            Ext.madasIsLoggedIn = false;
            Ext.getCmp('userMenu').setText('User: none');
        }
        Ext.madasChangeMainContent(action.result.mainContentFunction, action.result.params);
    },
    failure: function (form, action) {
        switch (action.failureType) {
            case Ext.form.Action.CLIENT_INVALID:
                Ext.Msg.alert('Failure', 'Form fields may not be submitted with invalid values');
                break;
            case Ext.form.Action.CONNECT_FAILURE:
                Ext.Msg.alert('Failure', 'Ajax communication failed');
                break;
            case Ext.form.Action.SERVER_INVALID:
                Ext.Msg.alert('Failure', action.result.msg);
        }
    }
    };

    simple.submit(submitOptions);
};


Ext.madasLoginInit = function(paramArray) {
    
    Ext.madasPostLoginParamArray = paramArray;
    
    Ext.getCmp('login-panel').getForm().reset();
    
};

Ext.madasLogoutInit = function(){
    
    var simple = new Ext.BasicForm('hiddenForm', {
                                   url:'login/processLogout',
                                   method:'POST'
                                   });
    
    var submitOptions = {
    successProperty: 'success',        
    success: function (form, action) {
        if (action.result.success === true) { 
            Ext.madasIsAdmin = false;
            Ext.getCmp('userMenu').setText('User: none');
            Ext.madasIsLoggedIn = false;
            
            Ext.Msg.alert('Successfully logged out', '(this dialog will auto-close in 3 seconds)');
            setTimeout('Ext.Msg.hide()', 3000);
            
            //load up the menu and next content area as declared in response
            Ext.madasChangeMainContent(action.result.mainContentFunction);
        } 
    },
    failure: function (form, action) {
        Ext.Msg.alert('Logout failure', '(this dialog will auto-close in 3 seconds)');
        setTimeout('Ext.Msg.hide()', 3000);
    }
    };
    
    simple.submit(submitOptions);
    
};
