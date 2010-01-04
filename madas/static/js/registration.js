/**
 * madasRegistrationValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
Ext.madasRegistrationValidatePassword = function (textfield, event) {
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

Ext.madasRegistrationCmp = 
{   id:'registration-container-panel', 
autoScroll:true,
items:[
       {  xtype:'form', 
       labelWidth: 100, // label settings here cascade unless overridden
       id:'registration-panel',
       url:Ext.madasBaseUrl + 'registration/submit',
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
               validator: Ext.madasRegistrationValidatePassword
               },{
               fieldLabel: 'Office Phone (with area code)',
               name: 'telephoneNumber',
               allowBlank:false,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Home Phone (with area code)',
               name: 'homephone',
               allowBlank:true,
               maskRe: /[^,=]/
               },{
               fieldLabel: 'Position',
               name: 'title',
               allowBlank:true,
               maskRe: /[^,=]/
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
                                       value:'Australia (VIC)',
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
                                                                               ['United Arab Emirates', 'United Arab Emirates'],
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
                 Ext.getCmp('registration-panel').getForm().submit(
                                                                   {   successProperty: 'success',        
                                                                   success: function (form, action) {
                                                                   if (action.result.success === true) {
                                                                   form.reset(); 
                                                                   
                                                                   //display a success alert that auto-closes in 5 seconds
                                                                   Ext.Msg.alert("Registration request sent successfully", "We will contact you via email or phone as soon as possible. Thank you for your inquiry.");
                                                                   
                                                                   //load up the menu and next content area as declared in response
                                                                   Ext.madasChangeMainContent(action.result.mainContentFunction);
                                                                   } 
                                                                   },
                                                                   failure: function (form, action) {
                                                                   //do nothing special. this gets called on validation failures and server errors
                                                                   try {
                                                                   if (action.result.mainContentFunction == "error:existingRegistration") {
                                                                   alert('That email address is already registered. Perhaps try logging in, or use the "Forgot your password?" link from the Login page');
                                                                   } else {
                                                                   alert('error submitting form\n' + action.response );
                                                                   }
                                                                   } catch (e) {
                                                                   alert('error submitting form, processing error:\n' + action.response );
                                                                   }
                                                                   }
                                                                   });
                 }
                 }
                 ]
       }
       ]
};
