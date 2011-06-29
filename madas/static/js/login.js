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

MA.ResetUser = function()
{
    MA.CurrentUser = {
        IsAdmin: false,
        IsNodeRep: false,
        IsClient: false,
        IsStaff: false,
        IsLoggedIn: false,
        Username: "",
        // Mastr MS membership
        IsMastrAdmin: false,
        IsProjectLeader: false, 
        IsMastrStaff: false
    };
}

MA.LoginExecute = function(paramArray){
                            Ext.getCmp('login-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        var resultContent;
                                        var params;
                                        if (action.result.success === true) {
                                            //console.log("Login Execute: "  + action.result.toString());
                                            form.reset(); 
                                            //load up the menu and next content area as declared in response
                                            if (action.result.username) {
                                                Ext.getCmp('userMenu').setText('User: aaa '+action.result.username);
                                            }
                                            
                                            resultContent = action.result.mainContentFunction;
                                            params = action.result.params;
                                            if (MA.PostLoginParamArray) {
                                                resultContent = MA.PostLoginParamArray[0];
                                                params = MA.PostLoginParamArray[1];
                                            }
                                            
                                            MA.ChangeMainContent(resultContent, params);
                                        } 
                                    },
                                    failure: function (form, action) {
                                        Ext.Msg.alert('Login failure', '(this dialog will auto-close in 3 seconds)');
                                        setTimeout(Ext.Msg.hide, 3000);
                                    }
                                });
                        };
                        
MA.ForgotPasswordExecute = function(){
                            Ext.getCmp('forgot-password-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            form.reset(); 
                                            //load up the menu and next content area as declared in response
                                            MA.ChangeMainContent(action.result.mainContentFunction, action.result.params);
                                        } 
                                    },
                                    failure: function (form, action) {
                                        Ext.Msg.alert('Submit failure', '(this dialog will auto-close in 3 seconds)');
                                        setTimeout(Ext.Msg.hide, 3000);
                                    }
                                });
                        };

MA.RequestQuoteButtonHandler = function() {
    MA.ChangeMainContent('quote:request');
};

MA.LoginCmp = {id:'login-container-panel', 
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
                               html:'Welcome to the <a href="http://www.metabolomics.net.au/">Metabolomics Australia</a> User and Quote Management System. This site allows existing and prospective clients of Metabolomics Australia to obtain a quote for accessing the many services offered my Metabolomics Australia.                               <p> <br>                              To make an inquiry about any of the services offered by Metabolomics Australia, clients are encouraged to fill out an online inquiry form by clicking the "Make an Inquiry" button, below.                               <p> <br>                              Existing clients can login to the website using the form to the right, or if required request a new password by <a href="#" onclick="MA.ChangeMainContent(\'login:forgotpassword\')">clicking here</a>.<br><br>'
                               },
                               {
                               xtype:'button',
                               text:'Make an Inquiry',
                               style:'margin-left:200px;',
                               handler:MA.RequestQuoteButtonHandler
                               }
                               ]
                       },
                    
                    {  xtype:'form', 
                    labelWidth: 75, // label settings here cascade unless overridden
                    id:'login-panel',
                    url:MA.BaseUrl + 'login/processLogin',
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
                            {xtype:'panel', width: 350, style:'padding-top:4px;padding-left:80px;', html: '<a href="#" onclick="MA.ChangeMainContent(\'registration\')">Click here</a> to register for an account' },
                        {xtype:'panel', width: 350, style:'padding-top:4px;padding-left:80px;', html: '<a href="#" onclick="MA.ChangeMainContent(\'login:forgotpassword\')">Forgot your password?</a>' }
                    ]}
                    ]
                };
                
/**
 * madasForgotPassword
 */
MA.ForgotPasswordCmp = {id:'forgot-password-container-panel', 
                layout:'absolute', 
                items:[
                    {  xtype:'form', 
                    labelWidth: 75, // label settings here cascade unless overridden
                    id:'forgot-password-panel',
                    url:MA.BaseUrl + 'login/processForgotPassword',
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
                            MA.ChangeMainContent('login');
                            }
                        },{
                        text: 'Submit',
                        handler: MA.ForgotPasswordExecute
                        }
                        ]}
                    ],
                    keys: [{key: [10,13], fn: MA.ForgotPasswordExecute}]
                };
                
MA.NotAuthorizedCmp = { id: 'notauthorized-panel', title: 'Not Authorized', html: 'You are not authorized to access this page' };

MA.GetUserInfo = function(callback) {
    //console.log("Called GetUserInfo");
    var simplereq = Ext.Ajax.request({
            url:MA.BaseUrl+'userinfo',
            success: function(response) {
                   //console.log(this);
                   MA.CurrentUser = Ext.decode(response.responseText);
                   if (callback !== undefined) {
                        callback();
                   }
            },
            failure: function() {
                   //console.log('Failed to get userinfo');
                   MA.ResetUser();
            },
    });
};

MA.LoginInit = function(paramArray) {
    
    MA.PostLoginParamArray = paramArray;
    
    document.getElementById('loginDiv').style.display = 'block';
    Ext.getCmp('login-panel').getForm().reset();
    
};

MA.ForgotPasswordInit = function() {
    
    Ext.getCmp('forgot-password-panel').getForm().reset();
    
};

MA.LogoutInit = function(){

    var simple = new Ext.BasicForm('hiddenForm', {
        url:MA.BaseUrl + 'login/processLogout',
        method:'POST'
        });

    var submitOptions = {
        successProperty: 'success',        
        success: function (form, action) {
            if (action.result.success === true) { 
                MA.CurrentUser.IsAdmin = false;
                Ext.getCmp('userMenu').setText('User: none');
                MA.CurrentUser.IsLoggedIn = false;
            
                Ext.Msg.alert('Successfully logged out', '(this dialog will auto-close in 3 seconds)');
                setTimeout(Ext.Msg.hide, 3000);
            
                //load up the menu and next content area as declared in response
                MA.ChangeMainContent(action.result.mainContentFunction);
            } 
        },
        failure: function (form, action) {
            Ext.Msg.alert('Logout failure', '(this dialog will auto-close in 3 seconds)');
            setTimeout(Ext.Msg.hide, 3000);
        }
    };

    simple.submit(submitOptions);

};

/**
 * madasResetPasswordValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
MA.ResetPasswordValidatePassword = function (textfield, event) {
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
    }
};

MA.ResetPasswordInit = function() {

    var resetPasswordCmp = Ext.getCmp('resetpassword-panel');   

    //fetch details for this request
    resetPasswordCmp.load({url: MA.BaseUrl + 'login/populateResetPasswordForm', waitMsg:'Loading'});
    
    //attach validator that ext cannot deal with
    Ext.getCmp("resetPasswordPassword").on('blur', MA.ResetPasswordValidatePassword);
    Ext.getCmp("resetPasswordConfirmPassword").on('blur', MA.ResetPasswordValidatePassword);
    
    Ext.getCmp('resetPasswordSubmit').disable();

    
};

MA.ResetPasswordCmp = {id:'resetpassword-container-panel', 
                layout:'absolute',
                forceLayout:true,
                deferredRender:false, 
                items:[
                    {  xtype:'form', 
                    labelWidth: 100, // label settings here cascade unless overridden
                    id:'resetpassword-panel',
                    url:MA.BaseUrl + 'login/processResetPassword',
                    method:'POST',
                    frame:true,
                    forceLayout:true,
                    deferredRender:false, 
                    reader: new Ext.data.JsonReader({
                                  root            : 'response.value.items',
                                  versionProperty : 'response.value.version',
                                  totalProperty   : 'response.value.total_count'
                                  }, [{ name: 'email', sortType:'string' },
                                  {name: 'validationKey', sortType:'string'}]),
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
                            validator: MA.ResetPasswordValidatePassword
                        }
                    ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp('resetpassword-panel').getForm().reset(); 
                            MA.ChangeMainContent('login');
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
                                            setTimeout(Ext.Msg.hide, 5000);
                                            
                                            //load up the menu and next content area as declared in response
                                            MA.ChangeMainContent(action.result.mainContentFunction);
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
