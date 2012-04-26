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

Ext.Ajax.on('requestexception', function(conn, response, options, e)
{
    if (response.status == 401)
    {
        //console.log("GLOBAL XHR error handler: Unauthenticated. Resetting user.");
        MA.ResetUser();
        MA.ChangeMainContent('login');
    }
    else if (response.status == 403)
    {
        //console.log("GLOBAL XHR error handler: Unauthorised.");
        MA.ChangeMainContent('notauthorized');
    }
    else
    {
        //console.log("GLOBAL XHR error handler: Uncaught response (" + response.status + ")");
    }
});

MA.reportError = function(type, errorMsg) {
    var fullMsg = 'Error Type: ' + type;
    fullMsg += '\nOccured at: ' + new Date();
    fullMsg += '\nUser: ' + MA.CurrentUser.Username;
    fullMsg += '\nUser Agent: ' + navigator.userAgent; 
    fullMsg += '\n' + errorMsg;
    MA.ErrorReportWindow.show(); 
    MA.ErrorReportForm.getForm().setValues({
        'notes': '',
        'details': fullMsg
    });
};

MA.dataProxyErrorHandler = function(proxy, type, action, options, response, error) {
    var message = '';
    if (type === 'response' && (response.status === 401 || response.status === 403)) {
        // HTTP Unauthorized and HTTP Forbidden responses aren't really errors
        // Global Handler will take care of these
        return;
    }
    message += "URL: " + Ext.encode(proxy.api[action].url);
    message += "\nType: " + Ext.encode(type);
    message += "\nResponse: " + Ext.encode(response);
    message += "\nError: " + Ext.encode(error);
    MA.reportError('DataProxy Exception', message);
};

Ext.data.DataProxy.on('exception', MA.dataProxyErrorHandler);

/*
Ext.data.DataProxy.on('exception', function(proxy, type, action, options, response, error) {
    var message = '';
    message += "URL: " + Ext.encode(proxy.api[action].url);
    message += "\nType: " + Ext.encode(type);
    message += "\nResponse: " + Ext.encode(response);
    message += "\nError: " + Ext.encode(error);
    MA.reportError('DataProxy Exception', message);
});
*/
MA.ErrorReportForm = new Ext.form.FormPanel({
        baseCls: 'x-plain',
        border: false,
        labelWidth: 150,
        url: MA.BaseUrl + 'ws/report_error',
        layout: {
            type: 'vbox',
            align: 'stretch'  // Child items are stretched to full width
        },
        items: [{
            xtype: 'displayfield',
            value: 'A system error occured. Please report it by clicking <b>Send</b> below.',
            style: { paddingTop: '10px', paddingBottom: '15px', textAlign: 'center', fontSize: 'larger' }
          },{
            plugins: [ Ext.ux.FieldLabeler ],
            name: 'notes',
            xtype: 'textarea',
            fieldLabel: 'Additional notes (optional)',
            height: 150
          },{
            plugins: [ Ext.ux.FieldLabeler ],
            name: 'details',
            readOnly: true,
            xtype: 'textarea', 
            fieldLabel: 'Details',
            height: 200
          }]
});
MA.ErrorReportWindow = new Ext.Window({
        title: 'System Error ',
        id: 'error-report-form',
        closeAction: 'hide',
        collapsible: false,
        maximizable: false,
        constrain: true,
        width: 750,
        height: 500,
        minWidth: 300,
        minHeight: 200,
        layout: 'fit',
        plain: true,
        bodyStyle: 'padding:5px;',
        buttonAlign: 'center',
        items: MA.ErrorReportForm,
        buttons: [{
            text: 'Send', handler: function(b, e) {
                MA.ErrorReportForm.getForm().submit({
                    success: function(form, action) {
                        MA.ErrorReportWindow.hide();
                        Ext.Msg.alert('Success', 'The error has been submitted. Thank you!');
                    },
                    failure: function(form, action) {
                        Ext.Msg.alert('Failure', "There's been an error while submitting the error. Please try again and/or consider reporting it by email (by copy-pasting the contents of the Details text area).");
                    }
                });

            }
        },{
            text: 'Cancel', handler: function(b, e) { b.ownerCt.ownerCt.hide(); }
        }]
    });


