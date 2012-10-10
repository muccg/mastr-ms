/**
 * madasRegistrationValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
MA.RegistrationValidatePassword = function (textfield, event) {
    var passEl = Ext.getCmp('registrationPassword');
    var confirmEl = Ext.getCmp('registrationConfirmPassword');
    var submitEl = Ext.getCmp('registrationSubmit');
    
    var passVal = Ext.getDom('registrationPassword').value;
    var confirmVal = Ext.getDom('registrationConfirmPassword').value;
    
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

MA.RegistrationCmp = 
{   id:'registration-container-panel', 
autoScroll:true,
items:[
       {  xtype:'form', 
       labelWidth: 100, // label settings here cascade unless overridden
       id:'registration-panel',
       url:MA.BaseUrl + 'registration/submit',
       method:'POST',
       frame:true,
       title: 'New Registration',
       bodyStyle:'padding:5px 5px 0',
       width: 380,
       style:'margin-left:30px;margin-top:20px;',
       defaults: {width: 230},
       defaultType: 'textfield',
       trackResetOnLoad: true,
       waitMsgTarget: true,
       
       items: [
               {
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
               fieldLabel: 'Email address',
               name: 'email',
               vtype: 'email',
               allowBlank:false
               },{
               fieldLabel: 'Password',
               name: 'password',
               id: 'registrationPassword',
               inputType: 'password',
               allowBlank:true
               },{
               fieldLabel: 'Confirm Password',
               inputType: 'password',
               id: 'registrationConfirmPassword',
               xtype: 'textfield',
               allowBlank:true,
               validator: MA.RegistrationValidatePassword
               },{
               fieldLabel: 'Office Phone (with area code)',
               name: 'telephoneNumber',
               allowBlank:false,
               xtype:'numberfield'
               },{
               fieldLabel: 'Home Phone (with area code)',
               name: 'homephone',
               allowBlank:true,
               xtype:'numberfield'
               },{
               fieldLabel: 'Position',
               name: 'title',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Department',
               name: 'dept',
               allowBlank:false,
               maskRe: /[^,=]/
               },{ 
               fieldLabel: 'Institute',
               name: 'institute',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
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
                                       value:'Australia (VIC)',
                                       triggerAction:'all',
                                       listWidth:230,
                                       store: countryStore
                                       })
               ],
       buttons: [
                 {
                 text: 'Cancel',
                 handler: function(){
                 Ext.getCmp('registration-panel').getForm().reset();
                 }
                 },
                 {
                 text: 'Submit',
                 id:'registrationSubmit',
                 handler: function(){
                    Ext.getCmp('registration-panel').getForm().submit({
                        successProperty: 'success',        
                        success: function (form, action) {
                            if (action.result.success === true) {
                                form.reset(); 
                                //display a success alert that auto-closes in 5 seconds
                                Ext.Msg.alert("Registration request sent successfully", "We will contact you via email or phone as soon as possible. Thank you for your inquiry.");
                                //load up the menu and next content area as declared in response
                                MA.ChangeMainContent(action.result.mainContentFunction);
                            } 
                        },
                        failure: function (form, action) {
                            //do nothing special. this gets called on validation failures and server errors
                            try {
                                if (action.result.msg === "User already exists") {
                                    alert('That email address is already registered. Perhaps try logging in, or use the "Forgot your password?" link from the Login page');
                                } else {
                                    alert('Error submitting form\n' + action.response.msg );
                                }
                            } catch (e) {
                                alert('Error submitting form, processing error:\n' + action.response );
                            }
                        }
                    });
                 }
                 }
                 ]
       }
       ]
};
