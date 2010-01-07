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
 
Ext.madasUserEditInit = function () {

    var userEditCmp = Ext.getCmp('useredit-panel');   

    //fetch user details
    userEditCmp.load({url: Ext.madasBaseUrl + 'user/userload', waitMsg:'Loading'});
    
    //attach validator that ext cannot deal with
    Ext.getCmp("userEditPassword").on('blur', Ext.madasUserEditValidatePassword);
    Ext.getCmp("userEditConfirmPassword").on('blur', Ext.madasUserEditValidatePassword);
    
    Ext.getCmp('userEditSubmit').enable();
    
    //allow the madas changeMainContent function to handle the rest from here
    return;
};

/**
 * madasAdminUserEditValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
Ext.madasUserEditValidatePassword = function (textfield, event) {
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

Ext.madasUserEditCmp = {id:'useredit-container-panel', 
                layout:'absolute', 
                items:[
                    {  xtype:'form', 
                    labelWidth: 100, // label settings here cascade unless overridden
                    id:'useredit-panel',
                    url:Ext.madasBaseUrl + 'user/userSave',
                    method:'POST',
                    frame:true,
                    reader: new Ext.madasJsonReader(),
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
                            validator: Ext.madasUserEditValidatePassword
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
                            store: new Ext.data.SimpleStore({
                                fields: ['submitValue', 'displayLabel'],
                                data : [['Australia (ACT)', 'Australia (ACT)'],
                                        ['Australia (NSW)', 'Australia (NSW)'],
                                        ['Australia (NT)', 'Australia (NT)'],
                                        ['Australia (QLD)', 'Australia (QLD)'],
                                        ['Australia (SA)', 'Australia (SA)'],
                                        ['Australia (TAS)', 'Australia (TAS)'],
                                        ['Australia (VIC)', 'Australia (VIC)'],
                                        ['Australia (WA)', 'Australia (WA)'],
                                        ['United States of America', 'United States of America'],
                                        ['New Zealand', 'New Zealand'],
                                        ['Afganistan', 'Afghanistan'],
                                        ['Albania', 'Albania'],
                                        ['Algeria', 'Algeria'],
                                        ['American Samoa', 'American Samoa'],
                                        ['Andorra', 'Andorra'],
                                        ['Angola', 'Angola'],
                                        ['Anguilla', 'Anguilla'],
                                        ['Antigua & Barbuda', 'Antigua & Barbuda'],
                                        ['Argentina', 'Argentina'],
                                        ['Armenia', 'Armenia'],
                                        ['Aruba', 'Aruba'],
                                        ['Australia (ACT)', 'Australia (ACT)'],
                                        ['Australia (NSW)', 'Australia (NSW)'],
                                        ['Australia (NT)', 'Australia (NT)'],
                                        ['Australia (QLD)', 'Australia (QLD)'],
                                        ['Australia (SA)', 'Australia (SA)'],
                                        ['Australia (TAS)', 'Australia (TAS)'],
                                        ['Australia (VIC)', 'Australia (VIC)'],
                                        ['Australia (WA)', 'Australia (WA)'],
                                        ['Austria', 'Austria'],
                                        ['Azerbaijan', 'Azerbaijan'],
                                        ['Bahamas', 'Bahamas'],
                                        ['Bahrain', 'Bahrain'],
                                        ['Bangladesh', 'Bangladesh'],
                                        ['Barbados', 'Barbados'],
                                        ['Belarus', 'Belarus'],
                                        ['Belgium', 'Belgium'],
                                        ['Belize', 'Belize'],
                                        ['Benin', 'Benin'],
                                        ['Bermuda', 'Bermuda'],
                                        ['Bhutan', 'Bhutan'],
                                        ['Bolivia', 'Bolivia'],
                                        ['Bonaire', 'Bonaire'],
                                        ['Bosnia & Herzegovina', 'Bosnia & Herzegovina'],
                                        ['Botswana', 'Botswana'],
                                        ['Brazil', 'Brazil'],
                                        ['British Indian Ocean Ter', 'British Indian Ocean Ter'],
                                        ['Brunei', 'Brunei'],
                                        ['Bulgaria', 'Bulgaria'],
                                        ['Burkina Faso', 'Burkina Faso'],
                                        ['Burundi', 'Burundi'],
                                        ['Cambodia', 'Cambodia'],
                                        ['Cameroon', 'Cameroon'],
                                        ['Canada', 'Canada'],
                                        ['Canary Islands', 'Canary Islands'],
                                        ['Cape Verde', 'Cape Verde'],
                                        ['Cayman Islands', 'Cayman Islands'],
                                        ['Central African Republic', 'Central African Republic'],
                                        ['Chad', 'Chad'],
                                        ['Channel Islands', 'Channel Islands'],
                                        ['Chile', 'Chile'],
                                        ['China', 'China'],
                                        ['Christmas Island', 'Christmas Island'],
                                        ['Cocos Island', 'Cocos Island'],
                                        ['Colombia', 'Colombia'],
                                        ['Comoros', 'Comoros'],
                                        ['Congo', 'Congo'],
                                        ['Cook Islands', 'Cook Islands'],
                                        ['Costa Rica', 'Costa Rica'],
                                        ['Cote DIvoire', 'Cote DIvoire'],
                                        ['Croatia', 'Croatia'],
                                        ['Cuba', 'Cuba'],
                                        ['Curaco', 'Curacao'],
                                        ['Cyprus', 'Cyprus'],
                                        ['Czech Republic', 'Czech Republic'],
                                        ['Denmark', 'Denmark'],
                                        ['Djibouti', 'Djibouti'],
                                        ['Dominica', 'Dominica'],
                                        ['Dominican Republic', 'Dominican Republic'],
                                        ['East Timor', 'East Timor'],
                                        ['Ecuador', 'Ecuador'],
                                        ['Egypt', 'Egypt'],
                                        ['El Salvador', 'El Salvador'],
                                        ['Equatorial Guinea', 'Equatorial Guinea'],
                                        ['Eritrea', 'Eritrea'],
                                        ['Estonia', 'Estonia'],
                                        ['Ethiopia', 'Ethiopia'],
                                        ['Falkland Islands', 'Falkland Islands'],
                                        ['Faroe Islands', 'Faroe Islands'],
                                        ['Fiji', 'Fiji'],
                                        ['Finland', 'Finland'],
                                        ['France', 'France'],
                                        ['French Guiana', 'French Guiana'],
                                        ['French Polynesia', 'French Polynesia'],
                                        ['French Southern Ter', 'French Southern Ter'],
                                        ['Gabon', 'Gabon'],
                                        ['Gambia', 'Gambia'],
                                        ['Georgia', 'Georgia'],
                                        ['Germany', 'Germany'],
                                        ['Ghana', 'Ghana'],
                                        ['Gibraltar', 'Gibraltar'],
                                        ['Great Britain', 'Great Britain'],
                                        ['Greece', 'Greece'],
                                        ['Greenland', 'Greenland'],
                                        ['Grenada', 'Grenada'],
                                        ['Guadeloupe', 'Guadeloupe'],
                                        ['Guam', 'Guam'],
                                        ['Guatemala', 'Guatemala'],
                                        ['Guinea', 'Guinea'],
                                        ['Guyana', 'Guyana'],
                                        ['Haiti', 'Haiti'],
                                        ['Hawaii', 'Hawaii'],
                                        ['Honduras', 'Honduras'],
                                        ['Hong Kong', 'Hong Kong'],
                                        ['Hungary', 'Hungary'],
                                        ['Iceland', 'Iceland'],
                                        ['India', 'India'],
                                        ['Indonesia', 'Indonesia'],
                                        ['Iran', 'Iran'],
                                        ['Iraq', 'Iraq'],
                                        ['Ireland', 'Ireland'],
                                        ['Isle of Man', 'Isle of Man'],
                                        ['Israel', 'Israel'],
                                        ['Italy', 'Italy'],
                                        ['Jamaica', 'Jamaica'],
                                        ['Japan', 'Japan'],
                                        ['Jordan', 'Jordan'],
                                        ['Kazakhstan', 'Kazakhstan'],
                                        ['Kenya', 'Kenya'],
                                        ['Kiribati', 'Kiribati'],
                                        ['Korea North', 'Korea North'],
                                        ['Korea Sout', 'Korea South'],
                                        ['Kuwait', 'Kuwait'],
                                        ['Kyrgyzstan', 'Kyrgyzstan'],
                                        ['Laos', 'Laos'],
                                        ['Latvia', 'Latvia'],
                                        ['Lebanon', 'Lebanon'],
                                        ['Lesotho', 'Lesotho'],
                                        ['Liberia', 'Liberia'],
                                        ['Libya', 'Libya'],
                                        ['Liechtenstein', 'Liechtenstein'],
                                        ['Lithuania', 'Lithuania'],
                                        ['Luxembourg', 'Luxembourg'],
                                        ['Macau', 'Macau'],
                                        ['Macedonia', 'Macedonia'],
                                        ['Madagascar', 'Madagascar'],
                                        ['Malaysia', 'Malaysia'],
                                        ['Malawi', 'Malawi'],
                                        ['Maldives', 'Maldives'],
                                        ['Mali', 'Mali'],
                                        ['Malta', 'Malta'],
                                        ['Marshall Islands', 'Marshall Islands'],
                                        ['Martinique', 'Martinique'],
                                        ['Mauritania', 'Mauritania'],
                                        ['Mauritius', 'Mauritius'],
                                        ['Mayotte', 'Mayotte'],
                                        ['Mexico', 'Mexico'],
                                        ['Midway Islands', 'Midway Islands'],
                                        ['Moldova', 'Moldova'],
                                        ['Monaco', 'Monaco'],
                                        ['Mongolia', 'Mongolia'],
                                        ['Montserrat', 'Montserrat'],
                                        ['Morocco', 'Morocco'],
                                        ['Mozambique', 'Mozambique'],
                                        ['Myanmar', 'Myanmar'],
                                        ['Nambia', 'Nambia'],
                                        ['Nauru', 'Nauru'],
                                        ['Nepal', 'Nepal'],
                                        ['Netherland Antilles', 'Netherland Antilles'],
                                        ['Netherlands', 'Netherlands (Holland, Europe)'],
                                        ['Nevis', 'Nevis'],
                                        ['New Caledonia', 'New Caledonia'],
                                        ['New Zealand', 'New Zealand'],
                                        ['Nicaragua', 'Nicaragua'],
                                        ['Niger', 'Niger'],
                                        ['Nigeria', 'Nigeria'],
                                        ['Niue', 'Niue'],
                                        ['Norfolk Island', 'Norfolk Island'],
                                        ['Norway', 'Norway'],
                                        ['Oman', 'Oman'],
                                        ['Pakistan', 'Pakistan'],
                                        ['Palau Island', 'Palau Island'],
                                        ['Palestine', 'Palestine'],
                                        ['Panama', 'Panama'],
                                        ['Papua New Guinea', 'Papua New Guinea'],
                                        ['Paraguay', 'Paraguay'],
                                        ['Peru', 'Peru'],
                                        ['Phillipines', 'Philippines'],
                                        ['Pitcairn Island', 'Pitcairn Island'],
                                        ['Poland', 'Poland'],
                                        ['Portugal', 'Portugal'],
                                        ['Puerto Rico', 'Puerto Rico'],
                                        ['Qatar', 'Qatar'],
                                        ['Republic of Montenegro', 'Republic of Montenegro'],
                                        ['Republic of Serbia', 'Republic of Serbia'],
                                        ['Reunion', 'Reunion'],
                                        ['Romania', 'Romania'],
                                        ['Russia', 'Russia'],
                                        ['Rwanda', 'Rwanda'],
                                        ['St Barthelemy', 'St Barthelemy'],
                                        ['St Eustatius', 'St Eustatius'],
                                        ['St Helena', 'St Helena'],
                                        ['St Kitts-Nevis', 'St Kitts-Nevis'],
                                        ['St Lucia', 'St Lucia'],
                                        ['St Maarten', 'St Maarten'],
                                        ['St Pierre & Miquelon', 'St Pierre & Miquelon'],
                                        ['St Vincent & Grenadines', 'St Vincent & Grenadines'],
                                        ['Saipan', 'Saipan'],
                                        ['Samoa', 'Samoa'],
                                        ['Samoa American', 'Samoa American'],
                                        ['San Marino', 'San Marino'],
                                        ['Sao Tome & Principe', 'Sao Tome & Principe'],
                                        ['Saudi Arabia', 'Saudi Arabia'],
                                        ['Senegal', 'Senegal'],
                                        ['Seychelles', 'Seychelles'],
                                        ['Sierra Leone', 'Sierra Leone'],
                                        ['Singapore', 'Singapore'],
                                        ['Slovakia', 'Slovakia'],
                                        ['Slovenia', 'Slovenia'],
                                        ['Solomon Islands', 'Solomon Islands'],
                                        ['Somalia', 'Somalia'],
                                        ['South Africa', 'South Africa'],
                                        ['Spain', 'Spain'],
                                        ['Sri Lanka', 'Sri Lanka'],
                                        ['Sudan', 'Sudan'],
                                        ['Suriname', 'Suriname'],
                                        ['Swaziland', 'Swaziland'],
                                        ['Sweden', 'Sweden'],
                                        ['Switzerland', 'Switzerland'],
                                        ['Syria', 'Syria'],
                                        ['Tahiti', 'Tahiti'],
                                        ['Taiwan', 'Taiwan'],
                                        ['Tajikistan', 'Tajikistan'],
                                        ['Tanzania', 'Tanzania'],
                                        ['Thailand', 'Thailand'],
                                        ['Togo', 'Togo'],
                                        ['Tokelau', 'Tokelau'],
                                        ['Tonga', 'Tonga'],
                                        ['Trinidad & Tobago', 'Trinidad & Tobago'],
                                        ['Tunisia', 'Tunisia'],
                                        ['Turkey', 'Turkey'],
                                        ['Turkmenistan', 'Turkmenistan'],
                                        ['Turks & Caicos Is', 'Turks & Caicos Is'],
                                        ['Tuvalu', 'Tuvalu'],
                                        ['Uganda', 'Uganda'],
                                        ['Ukraine', 'Ukraine'],
                                        ['United Arab Erimates', 'United Arab Emirates'],
                                        ['United Kingdom', 'United Kingdom'],
                                        ['United States of America', 'United States of America'],
                                        ['Uraguay', 'Uruguay'],
                                        ['Uzbekistan', 'Uzbekistan'],
                                        ['Vanuatu', 'Vanuatu'],
                                        ['Vatican City State', 'Vatican City State'],
                                        ['Venezuela', 'Venezuela'],
                                        ['Vietnam', 'Vietnam'],
                                        ['Virgin Islands (Brit)', 'Virgin Islands (Brit)'],
                                        ['Virgin Islands (USA)', 'Virgin Islands (USA)'],
                                        ['Wake Island', 'Wake Island'],
                                        ['Wallis & Futana Is', 'Wallis & Futana Is'],
                                        ['Yemen', 'Yemen'],
                                        ['Zaire', 'Zaire'],
                                        ['Zambia', 'Zambia'],
                                        ['Zimbabwe', 'Zimbabwe']]
                            })
                        })
                    ],
                    buttons: [{
                        text: 'Cancel',
                        handler: function(){
                            Ext.getCmp('useredit-panel').getForm().reset(); 
                            Ext.madasAuthorize('dashboard');
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
