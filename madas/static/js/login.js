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

Ext.madasLoginExecute = function(paramArray){
                            Ext.getCmp('login-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            //Ext.Msg.alert ('Result: ' + action.result.toString())
                                            form.reset(); 
                                            //load up the menu and next content area as declared in response
                                            if (action.result.username) {
                                                Ext.getCmp('userMenu').setText('User: '+action.result.username);
                                            }
                                            
                                            var resultContent = action.result.mainContentFunction;
                                            var params = action.result.params;
                                            if (Ext.madasPostLoginParamArray) {
                                                resultContent = Ext.madasPostLoginParamArray[0];
                                                params = Ext.madasPostLoginParamArray[1];
                                            }
                                            
                                            Ext.madasAuthorize(resultContent, params);
                                        } 
                                    },
                                    failure: function (form, action) {
                                        Ext.Msg.alert('Login failure', '(this dialog will auto-close in 3 seconds)');
                                        setTimeout('Ext.Msg.hide()', 3000);
                                    }
                                });
                        };
                        
Ext.madasForgotPasswordExecute = function(){
                            Ext.getCmp('forgot-password-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            form.reset(); 
                                            //load up the menu and next content area as declared in response
                                            Ext.madasChangeMainContent(action.result.mainContentFunction, action.result.params);
                                        } 
                                    },
                                    failure: function (form, action) {
                                        Ext.Msg.alert('Submit failure', '(this dialog will auto-close in 3 seconds)');
                                        setTimeout('Ext.Msg.hide()', 3000);
                                    }
                                });
                        };

Ext.madasRequestQuoteButtonHandler = function() {
    //Ext.madasAuthorize('quote:request');
    Ext.madasChangeMainContent('quote:request');
};

Ext.madasLoginCmp = {id:'login-container-panel', 
                layout:'absolute', 
                items:[
                       { xtype:'panel',
                       frame:true,
                       title:'',
                       bodyStyle:'padding:5px 5px 0',
                       width:350,
                       x: 50,
                       y:10,
                       items: [{
                               xtype:'panel',
                               html:'Welcome to the <a href="http://www.metabolomics.net.au/">Metabolomics Australia</a> User and Quote Management System. This site allows existing and prospective clients of Metabolomics Australia to obtain a quote for accessing the many services offered my Metabolomics Australia.                               <p> <br>                              To make an inquiry about any of the services offered by Metabolomics Australia, clients are encouraged to fill out an online inquiry form by clicking the "Make an Inquiry" button, below.                               <p> <br>                              Existing clients can login to the website using the form to the right, or if required request a new password by <a href="#" onclick="Ext.madasAuthorize(\'login:forgotpassword\')">clicking here</a>.<br><br>'
                               },
                               {
                               xtype:'button',
                               text:'Make an Inquiry',
                               style:'margin-left:200px;',
                               handler:Ext.madasRequestQuoteButtonHandler
                               }
                               ]
                       },
                    
                    {  xtype:'form', 
                    labelWidth: 75, // label settings here cascade unless overridden
                    id:'login-panel',
                    url:Ext.madasBaseUrl + 'login/processLogin',
                    method:'POST',
                    frame:true,
                    title: 'Login',
                    bodyStyle:'padding:5px 5px 0',
                    width: 350,
                    x: 430,
                    y: 10,
                    defaults: {width: 230},
                    defaultType: 'textfield',
                    
                    items: [{
                            xtype:'panel',
                            el:"loginDiv"
                        },
                        {xtype:'panel', width: 350, style:'padding-top:4px;padding-left:80px;', html: '<a href="/madas-registration/">Click here</a> to register for an account' },
                        {xtype:'panel', width: 350, style:'padding-top:4px;padding-left:80px;', html: '<a href="#" onclick="Ext.madasAuthorize(\'login:forgotpassword\')">Forgot your password?</a>' }
                    ]}
                    ]
                };
                
/**
 * madasForgotPassword
 */
Ext.madasForgotPasswordCmp = {id:'forgot-password-container-panel', 
                layout:'absolute', 
                items:[
                    {  xtype:'form', 
                    labelWidth: 75, // label settings here cascade unless overridden
                    id:'forgot-password-panel',
                    url:Ext.madasBaseUrl + 'login/processForgotPassword',
                    method:'POST',
                    frame:true,
                    title: 'Forgot Password',
                    bodyStyle:'padding:5px 5px 0',
                    width: 350,
                    x: 50,
                    y: 10,
                    defaults: {width: 230},
                    defaultType: 'textfield',
                    
                    items: [{
                            fieldLabel: 'Email address',
                            name: 'username',
                            //vtype: 'email',
                            allowBlank:false
                            }
                        ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp('forgot-password-panel').getForm().reset(); 
                            Ext.madasAuthorize('login');
                            }
                        },{
                        text: 'Submit',
                        handler: Ext.madasForgotPasswordExecute
                        }
                        ]}
                    ],
                    keys: [{key: [10,13], fn: Ext.madasForgotPasswordExecute}]
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
        url:Ext.madasBaseUrl + module+'/authorize',
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
            //load up the menu and next content area as declared in response
            //alert(action.response.responseText);
            Ext.madasChangeMainContent(action.result.mainContentFunction, action.result.params);
        }
    };

    simple.submit(submitOptions);
};


Ext.madasLoginInit = function(paramArray) {
    
    Ext.madasPostLoginParamArray = paramArray;
    
    Ext.getCmp('login-panel').getForm().reset();
    
};

Ext.madasForgotPasswordInit = function() {
    
    Ext.getCmp('forgot-password-panel').getForm().reset();
    
};

Ext.madasLogoutInit = function(){

    var simple = new Ext.BasicForm('hiddenForm', {
        url:Ext.madasBaseUrl + 'login/processLogout',
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

/**
 * madasResetPasswordValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
Ext.madasResetPasswordValidatePassword = function (textfield, event) {
    var passEl = Ext.getCmp('resetPasswordPassword');
    var confirmEl = Ext.getCmp('resetPasswordConfirmPassword');
    var submitEl = Ext.getCmp('resetPasswordSubmit');
    
    var passVal = Ext.getDom('resetPasswordPassword').value;
    var confirmVal = Ext.getDom('resetPasswordConfirmPassword').value;

    if (passVal == confirmVal) {
        confirmEl.clearInvalid();
        submitEl.enable();
        return true; 
    } else { 
        confirmEl.markInvalid('Password and Confirm Password must match');
        submitEl.disable();
        return false;
    };
};

Ext.madasResetPasswordInit = function() {

    var resetPasswordCmp = Ext.getCmp('resetpassword-panel');   

    //fetch details for this request
    resetPasswordCmp.load({url: Ext.madasBaseUrl + 'login/populateResetPasswordForm', waitMsg:'Loading'});
    
    //attach validator that ext cannot deal with
    Ext.getCmp("resetPasswordPassword").on('blur', Ext.madasResetPasswordValidatePassword);
    Ext.getCmp("resetPasswordConfirmPassword").on('blur', Ext.madasResetPasswordValidatePassword);
    
    Ext.getCmp('resetPasswordSubmit').disable();

    
};

Ext.madasResetPasswordCmp = {id:'resetpassword-container-panel', 
                layout:'absolute', 
                items:[
                    {  xtype:'form', 
                    labelWidth: 100, // label settings here cascade unless overridden
                    id:'resetpassword-panel',
                    url:Ext.madasBaseUrl + 'login/processResetPassword',
                    method:'POST',
                    frame:true,
                    reader: Ext.madasJsonReader,
                    title: 'Reset Password',
                    bodyStyle:'padding:5px 5px 0',
                    width: 380,
                    x: 50,
                    y: 10,
                    defaults: {width: 230},
                    defaultType: 'textfield',
                    trackResetOnLoad: true,
                    waitMsgTarget: true,
                    
                    items: [
                        {   name: 'email',
                            inputType: 'hidden'
                        },{
                            name: 'validationKey',
                            inputType: 'hidden'
                        },{
                            fieldLabel: 'Password',
                            name: 'password',
                            id: 'resetPasswordPassword',
                            inputType: 'password',
                            allowBlank:true
                        },{
                            fieldLabel: 'Confirm Password',
                            inputType: 'password',
                            id: 'resetPasswordConfirmPassword',
                            xtype: 'textfield',
                            allowBlank:true,
                            validator: Ext.madasResetPasswordValidatePassword
                        }
                    ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp('resetpassword-panel').getForm().reset(); 
                            Ext.madasAuthorize('login');
                            }
                        },{
                        text: 'Save',
                        id:'resetPasswordSubmit',
                        handler: function(){
                            Ext.getCmp('resetpassword-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            form.reset(); 
                                            
                                            //display a success alert that auto-closes in 5 seconds
                                            Ext.Msg.alert("Password reset successfully", "(this message will auto-close in 5 seconds)");
                                            setTimeout("Ext.Msg.hide()", 5000);
                                            
                                            //load up the menu and next content area as declared in response
                                            Ext.madasChangeMainContent(action.result.mainContentFunction);
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
