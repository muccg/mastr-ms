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
 
MA.UserEditInit = function () {

    var userEditCmp = Ext.getCmp('useredit-panel');   

    //fetch user details
    userEditCmp.load({url: MA.BaseUrl + 'user/userload', waitMsg:'Loading'});
    
    //attach validator that ext cannot deal with
    Ext.getCmp("userEditPassword").on('blur', MA.UserEditValidatePassword);
    Ext.getCmp("userEditConfirmPassword").on('blur', MA.UserEditValidatePassword);
    
    Ext.getCmp('userEditSubmit').enable();
    
    //allow the madas changeMainContent function to handle the rest from here
    return;
};

/**
 * madasAdminUserEditValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
MA.UserEditValidatePassword = function (textfield, event) {
    var passEl = Ext.getCmp('userEditPassword');
    var confirmEl = Ext.getCmp('userEditConfirmPassword');
    var submitEl = Ext.getCmp('userEditSubmit');
    
    var passVal = Ext.getDom('userEditPassword').value;
    var confirmVal = Ext.getDom('userEditConfirmPassword').value;

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

MA.UserEditCmp = {id:'useredit-container-panel', 
                layout:'absolute', 
                deferredRender:false,
                forceLayout:true,
                defaults: {
                    deferredRender:false,
                    forceLayout:true
                },
                items:[
                    {  xtype:'form', 
                    labelWidth: 100, // label settings here cascade unless overridden
                    id:'useredit-panel',
                    url:MA.BaseUrl + 'user/userSave',
                    method:'POST',
                    frame:true,
                    reader: new Ext.data.JsonReader({
                                                              root            : 'data',
                                                              //versionProperty : 'response.value.version',
                                                              //totalProperty   : 'response.value.total_count',
                                                              totalProperty   : 'totalRows',
                                                              successProperty : 'success',
                                                              fields: [
                                                                  { name: 'username', sortType : 'string' },
                                                                  { name: 'firstname', sortType : 'string' },
                                                                  { name: 'lastname', sortType : 'string' },
                                                                  { name: 'email', sortType : 'string' },
                                                                  { name: 'telephoneNumber', sortType : 'string' },
                                                                  { name: 'physicalDeliveryOfficeName', sortType : 'string' },
                                                                  { name: 'title', sortType : 'string' },
                                                                  { name: 'homephone', sortType : 'string' },
                                                                  { name: 'isAdmin', sortType : 'string' },
                                                                  { name: 'isNodeRep', sortType : 'string' },
                                                                  { name: 'node', sortType : 'string' },
                                                                  { name: 'status', sortType : 'string' },
                                                                  { name: 'dept', sortType : 'string' },
                                                                  { name: 'institute', sortType : 'string' },
                                                                  { name: 'address', sortType : 'string' },
                                                                  { name: 'supervisor', sortType : 'string' },
                                                                  { name: 'areaOfInterest', sortType : 'string' },
                                                                  { name: 'country', sortType : 'string' }
                                                                  ]}),
                    title: 'Edit My Details',
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
                            disabled:true
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
                            id: 'userEditPassword',
                            inputType: 'password',
                            allowBlank:true
                        },{
                            fieldLabel: 'Confirm Password',
                            inputType: 'password',
                            id: 'userEditConfirmPassword',
                            xtype: 'textfield',
                            allowBlank:true,
                            validator: MA.UserEditValidatePassword
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
                        }, {
                            fieldLabel: 'Node',
                            name: 'node',
                            disabled:true
                        },{
                            fieldLabel: 'Status',
                            name: 'status',
                            disabled:true
                        },{
                            fieldLabel: 'Department',
                            name: 'dept',
                            allowBlank:true,
                            maskRe: /[^,=]/
                        },{ 
                            fieldLabel: 'Institute',
                            name: 'institute',
                            allowBlank:true,
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
                            triggerAction:'all',
                            listWidth:230,
                            store: countryStore
                        })
                    ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp('useredit-panel').getForm().reset(); 
                            MA.ChangeMainContent('dashboard');
                            }
                        },{
                        text: 'Save',
                        id:'userEditSubmit',
                        handler: function(){
                            Ext.getCmp('useredit-panel').getForm().submit(
                                {   successProperty: 'success',        
                                    success: function (form, action) {
                                        if (action.result.success === true) {
                                            form.reset(); 
                                            
                                            //display a success alert that auto-closes in 5 seconds
                                            Ext.Msg.alert("User details saved successfully", "(this message will auto-close in 5 seconds)");
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
