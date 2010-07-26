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

MA.EmailDisplayField = Ext.extend(Ext.form.DisplayField,  {
    setRawValue : function(v){
        if(this.htmlEncode){
            v = Ext.util.Format.htmlEncode(v);
        }
        return this.rendered ? (this.el.dom.innerHTML = (Ext.isEmpty(v) ? '' : '<a href="mailto:'+v+'">'+v+'</a>')) : (this.value = '<a href="mailto:'+v+'">'+v+'</a>');
    }
});

Ext.reg('emaildisplayfield', MA.EmailDisplayField);


 
MA.RequestQuoteInit = function () {
	var reqQuoCmp = Ext.getCmp('requestquote-panel');   

    //fetch user details
    reqQuoCmp.load({url: MA.BaseUrl + 'user/userload', waitMsg:'Loading'});

    //reqQuoCmp.doLayout();
    
    return;
};

MA.RequestQuoteCmp = 
    {   id:'requestquote-container-panel', 
        autoScroll:true,
        deferredRender:false,
        forceLayout:true,
        items:[
            {  xtype:'form', 
            labelWidth: 100, // label settings here cascade unless overridden
            id:'requestquote-panel',
            url:MA.BaseUrl + 'quote/sendRequest',
            method:'POST',
            frame:true,
            fileUpload: true,
            reader: new Ext.data.JsonReader({successProperty:'success', root: 'data'}, 
                                          [ {name: 'firstname', mapping: 'firstname'}, 
                                            {name: 'lastname', mapping: 'lastname'},
                                            {name: 'telephoneNumber', mapping: 'telephoneNumber'},
                                            {name: 'country', mapping: 'country'}
                                          ]),
            title: 'Make an Inquiry',
            bodyStyle:'padding:5px 5px 0',
            width: 380,
            style:'margin-left:30px;margin-top:20px;',
            defaults: {width: 230},
            defaultType: 'textfield',
            trackResetOnLoad: true,
            waitMsgTarget: true,
            
            items: [
                {
                    fieldLabel: 'Email address',
                    name: 'email',
                    vtype: 'email',
                    allowBlank:false
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
                    fieldLabel: 'Office Phone',
                    name: 'telephoneNumber',
                    allowBlank:false,
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
                }), new Ext.form.ComboBox({
                    fieldLabel: 'Send Request To',
                    id: 'quoteNode',
                    name: 'nodeDisplay',
                    editable:false,
                    forceSelection:true,
                    displayField:'name',
                    valueField:'submitValue',
                    hiddenName:'node',
                    lazyRender:true,
                    allowBlank:false,
                    typeAhead:false,
                    triggerAction:'all',
                    listWidth:230,
                    store: new Ext.data.JsonStore({
                        storeId:'sendToStore',
                        url: MA.BaseUrl + 'quote/listGroups',
                        root: 'response.value.items',
                        fields: ['name', 'submitValue']
                    })
                }),{
                    fieldLabel: 'Information Request Details',
                    name: 'details',
                    xtype: 'textarea',
                    allowBlank:false,
                    grow:true,
                    growMax:360
                },{
                        xtype: 'fileuploadfield',
                        id: 'quo-attach',
                        emptyText: '',
                        fieldLabel: 'Attach a File (optional)',
                        name: 'attachfile'
                } 
            ],
            buttons: [
                 {
                text: 'Cancel',
                handler: function(){
                    Ext.getCmp('requestquote-panel').getForm().reset();
                    }
                },
                {
                text: 'Send Request',
                id:'requestQuoteSubmit',
                handler: function(){
                    Ext.getCmp('requestquote-panel').getForm().submit(
                        {   successProperty: 'success',        
                            success: function (form, action) {
                                if (action.result.success === true) {
                                    form.reset(); 
                                    
                                    //display a success alert that auto-closes in 5 seconds
                                    Ext.Msg.alert("Request sent successfully", "We will contact you via email or phone as soon as possible. Thank you for your inquiry.");
                                    
                                    //load up the menu and next content area as declared in response
                                    MA.ChangeMainContent(action.result.mainContentFunction);
                                } 
                            },
                            failure: function (form, action) {
                                //do nothing special. this gets called on validation failures and server errors
                                alert('error submitting form\n' + action.response );
                            }
                        });
                    }
                }
                ]
            }
            ]
    };

MA.QuoteRequestListInit = function(){
        
    var dataurl = MA.BaseUrl + "quote/list";
        
    var madasReader = new MA.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType:'number' },
            { name: 'firstname', sortType : 'string' },
            { name: 'lastname', sortType : 'string' },
            { name: 'email', sortType : 'string' },
            { name: 'officephone', sortType : 'string' },
            { name: 'requesttime', sortType: 'date' },
            { name: 'completed', sortType: 'string' },
            { name: 'unread', sortType: 'string' }
        ]);
    
    var dataStore = new Ext.data.GroupingStore({
        id         : 'bSId',
        autoLoad   : true,
        reader     : madasReader,
        sortInfo   : {field: 'requesttime', direction: 'DESC'},
        url        : dataurl,
        groupField : 'completed'
        });
    var gridView = new Ext.grid.GroupingView({
        loadMask : { msg : 'Please wait...' },
        forceFit: true,
        groupTextTpl: '{[values.gvalue? "Completed" : "Requiring Attention"]} ({[values.rs.length]})',
        hideGroupedColumn: true
        });
    var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.Authorize('quote:edit', [selectionModel.getSelected().data['id']]);
        }
    };
    var topToolbar = new Ext.Toolbar({
            items   : [
                {  id: 'quoterequestsEditBtn', text: 'View/Edit', handler: editHandler, disabled: true }
            ]       
        });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var checkBoxRenderer = function (val){
        if(val == true){
            return '*';
        } else {
            return '';
        }
    }
    var colModel = new Ext.grid.ColumnModel([
        {header: 'ID', align : 'left', sortable: true, dataIndex: 'id', width:25 },
        {header: 'Unread', align:'center', sortable: true, dataIndex: 'unread', renderer: checkBoxRenderer, width:35 },
        {header: 'Completed', align:'center', sortable: true, dataIndex: 'completed', renderer: checkBoxRenderer, width:50 },
        {header: 'Email', width:185, align : 'left', sortable: true, dataIndex: 'email' },
        {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname' },
        {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname' },
        {header: 'Phone', align : 'left', sortable: true, dataIndex: 'officephone' },
        {header: 'Date Received', align:'left', sortable: true, dataIndex: 'requesttime'}
        ]);
    var grid = new Ext.grid.GridPanel({
        id             : 'quoterequests-panel',
        ds             : dataStore,
        enableDragDrop : false,
        enableColumnMove: false,
        cm             : colModel,
        sm             : selectionModel,
        loadMask       : { msg : 'Loading...' },
        view           : gridView,
        title          : 'Quote Requests',
        tbar           : topToolbar,
        trackMouseOver : false,
        plugins:[new Ext.ux.grid.Search({
             mode:'local'
            ,iconCls:false
            ,dateFormat:'m/d/Y'
            ,minLength:0
            ,width:150
            ,position:'top'
        })]
    });
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('quoterequestsEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);

};

MA.QuoteRequestEditInit = function (paramArray) {
    var id = paramArray[0];
    var quoteRequestEditCmp = Ext.getCmp('quoterequestedit-panel');
    var formalQuoteCmp = Ext.getCmp('formalquoteedit-panel');

    Ext.getCmp('quoterequestedit-panel').getForm().reset();
    Ext.getCmp('formalquoteedit-panel').getForm().reset();

    //fetch user details
    quoteRequestEditCmp.load({url: MA.BaseUrl + 'quote/load', params: {'qid': id}, waitMsg:'Loading'});
    formalQuoteCmp.load({url: MA.BaseUrl + 'quote/formalload', params: {'qid': id}, waitMsg:'Loading'});

    var quoteHistoryCmp = Ext.getCmp('qre-history');

    //fetch history
    quoteHistoryCmp.load({url:MA.BaseUrl + 'quote/history', params:{'qid':id}, callback:MA.RenderQuoteHistory, text:'Loading...'});

    //reload the combobox   
    if (Ext.StoreMgr.containsKey('redirectQuoteNodeDS')) {
        Ext.StoreMgr.get('redirectQuoteNodeDS').reload();
    }   

	Ext.getCmp('downloadattachbutton').disable();
	Ext.getCmp('downloadattachbutton').setText('looking for attachments...');

    //allow the madas changeMainContent function to handle the rest from here
    return;
};


MA.QuoteRequestEditLoaded = function () {
	if (Ext.getCmp('attachment').value == null || Ext.getCmp('attachment').value == '') {
		Ext.getCmp('downloadattachbutton').setText('no attachments');
		Ext.getCmp('downloadattachbutton').disable();
	} else {
		Ext.getCmp('downloadattachbutton').setText('Download '+Ext.getCmp('attachment').value);
		Ext.getCmp('downloadattachbutton').enable();
	}
	
	Ext.getCmp('qre-id').setValue(Ext.getCmp('qre-hidden-id').getValue());
}


MA.QuoteRequestEditCmp =
    {   id:'quoterequestedit-container-panel',
        autoScroll:true,
        layout:'column',
        deferredRender:false,
        forceLayout:true,
        items:[
            {  xtype:'form',
            labelWidth: 100, // label settings here cascade unless overridden
            id:'quoterequestedit-panel',
            url:MA.BaseUrl + 'quote/save',
            method:'POST',
            frame:true,
            deferredRender:false,
            reader: new Ext.data.JsonReader({successProperty:'success', root: 'data'}, 
                                          [ {name: 'id', mapping: 'id'}, 
                                            {name: 'tonode', mapping: 'tonode'},
                                            {name: 'details', mapping: 'details'},
                                            {name: 'requesttime', mapping: 'requesttime'},
                                            {name: 'firstname', mapping: 'firstname'},
                                            {name: 'lastname', mapping: 'lastname'},
                                            {name: 'officephone', mapping: 'officephone'},
                                            {name: 'completed', mapping: 'completed'},
                                            {name: 'email', mapping: 'email'},
                                            {name: 'attachment', mapping: 'attachment'}
                                          ]),
            title: 'Quote Request',
            bodyStyle:'padding:5px 5px 0',
            width: 380,
            style:'margin-left:30px;margin-top:20px;',
            defaults: {width: 230},
            defaultType: 'textfield',
//            trackResetOnLoad: true,
            waitMsgTarget: true,

            items: [
                {  
                    name: 'id',
                    id: 'qre-hidden-id',
                    xtype: 'hidden'
                },{
                    name: 'id',
                    id: 'qre-id',
                    fieldLabel:'Request ID',
                    xtype: 'displayfield'
                },{
                    fieldLabel: 'Email address',
                    name: 'email',
                    xtype: 'emaildisplayfield',
                    allowBlank:false,
                    id: 'qre-email'
                },{
                    fieldLabel: 'First name',
                    name: 'firstname',
                    allowBlank:false,
                    maskRe: /[^,=]/,
                    disabled: true,
                    id: 'qre-firstname'
                },{
                    fieldLabel: 'Last name',
                    name: 'lastname',
                    allowBlank:false,
                    maskRe: /[^,=]/,
                    disabled: true,
                    id: 'qre-lastname'
                },{
                    fieldLabel: 'Office Phone',
                    name: 'officephone',
                    allowBlank:false,
                    maskRe: /[^,=]/,
                    disabled: true,
                    id: 'qre-officephone'
                }, new Ext.form.ComboBox({
                    fieldLabel: 'Country',
                    name: 'countryDisplay',
                    editable:false,
                    forceSelection:true,
                    displayField:'displayLabel',
                    valueField:'submitValue',
                    hiddenName:'country',
                    lazyRender:true,
                    disabled:true,
                    typeAhead:false,
                    mode:'local',
                    triggerAction:'all',
                    listWidth:230,
                    store: countryStore
                }), new Ext.form.ComboBox({
                    fieldLabel: 'Send Request To',
                    id: 'redirectQuoteNode',
                    name: 'nodeDisplay',
                    editable:false,
                    forceSelection:true,
                    displayField:'name',
                    valueField:'submitValue',
                    hiddenName:'tonode',
                    lazyRender:true,
                    allowBlank:false,
                    typeAhead:false,
                    triggerAction:'all',
                    listWidth:230,
                    disabled: true,
                    store: new Ext.data.JsonStore({
                        storeId: 'redirectQuoteNodeDS',
                        url: MA.BaseUrl + 'quote/listGroups',
                        root: 'response.value.items',
                        fields: ['name', 'submitValue']
                    })
                }),{
                    fieldLabel: 'Details (readonly)',
                    name: 'details',
                    xtype: 'textarea',
                    allowBlank:true,
                    grow:true,
                    growMax:360,
                    //disabled: true,
                    readOnly: true,
                    id: 'qre-details'
                },{
                    fieldLabel: 'Completed',
                    name: 'completed',
                    xtype: 'checkbox',
                    inputValue: '1'
                },{
                    fieldLabel: 'Comment',
                    name: 'comment',
                    xtype: 'textarea',
                    allowBlank:false,
                    grow:true,
                    growMax:360
                },{  
                    name: 'attachment',
                    id: 'attachment',
                    inputType: 'hidden'
                },{
	            	xtype:'panel', 
	            	width: 350, 
	            	id: 'downloadattach',
	            	style:'padding-top:8px;padding-left:100px;padding-bottom:8px;', 
	            	items: [
	            		{
	            		xtype:'button',
	            		id:'downloadattachbutton',
	            		text:'Download Attachment',
	            		handler: function() {
	            				window.location = MA.BaseUrl + 'quote/downloadAttachment?quoterequestid=' + Ext.getCmp('qre-hidden-id').value;
	            			}
	            		}
	            	]
	            }
            ],
            buttons: [
                 {
                 text: 'Go Back',
                 handler: function(){
                        Ext.getCmp('quoterequestedit-panel').getForm().reset();
                        MA.QuoteEditVisualToggle(false);
                        MA.ChangeMainContent('quote:list');
                    }
                 },
                 {//this could be an Edit Details button, but functionality has been temporarily limited for practical purposes
                 text: 'Forward Request',
                 id: 'editQuoteRequestBtn',
                 handler: function() {
                    Ext.getCmp('cancelEditQuoteRequestBtn').show();
                    Ext.getCmp('editQuoteRequestBtn').hide();
                    //Ext.getCmp('qre-email').enable();
                    //Ext.getCmp('qre-firstname').enable();
                    //Ext.getCmp('qre-lastname').enable();
                    //Ext.getCmp('qre-officephone').enable();
                    Ext.getCmp('redirectQuoteNode').enable();
                    //Ext.getCmp('qre-details').enable();
                    }
                 },
                 {
                 text: 'Cancel Edit',
                 id: 'cancelEditQuoteRequestBtn',
                 hidden : true,
                 handler: function(){
                    Ext.getCmp('quoterequestedit-panel').getForm().reset();
                    MA.QuoteEditVisualToggle(false);
                    }
                 },
                 {
                 text: 'Save',
                 id:'requestQuoteSubmit',
                 handler: function(){
                    Ext.getCmp('quoterequestedit-panel').getForm().submit(
                        {   successProperty: 'success',
                            success: function (form, action) {
                                if (action.result.success === true) {
                                    form.reset();
    
                                    MA.QuoteEditVisualToggle(false);

                                    //display a success alert that auto-closes in 5 seconds
                                    Ext.Msg.alert("Quote Request Saved", "(this message will auto-close in 5 seconds)");
                                    setTimeout("Ext.Msg.hide()", 5000);

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
            },
            {
                title: 'Formal Quote',
                frame: true,
                bodyStyle:'padding:5px 5px 0',
                width: 380,
                style:'margin-left:30px;margin-top:20px;',
                xtype:'form',
                labelWidth: 100, // label settings here cascade unless overridden
                id:'formalquoteedit-panel',
                url:MA.BaseUrl + 'quote/formalsave',
                method:'POST',
                fileUpload: true,
                reader: new Ext.data.JsonReader({successProperty:'success', root: 'data', idProperty: 'quoterequestid'}, 
                                [
                                {name: 'quoterequestid', mapping: 'quoterequestid'},
                                {name: 'details', mapping: 'details'},
                                {name: 'fromemail', mapping: 'fromemail'},
                                {name: 'toemail', mapping: 'toemail'},
                                {name: 'tonode', mapping: 'tonode'},
                                {name: 'pdf', mapping: 'pdf'},
                                {name: 'fromname', mapping: 'fromname'},
                                {name: 'officePhone', mapping: 'officePhone'}
                                ]),
                defaults: {width: 230},
                defaultType: 'textfield',
//                trackResetOnLoad: true,
                waitMsgTarget: true,
    
                items: [
                    {  
                        name: 'quoterequestid',
                        id: 'fquo-qid',
                        inputType: 'hidden'
                    },{
                        fieldLabel: 'Email from',
                        name: 'fromemail',
                        vtype: 'fromemail',
                        allowBlank:false,
                        disabled:true,
                        id: 'fquo-email'
                    },{
                        fieldLabel: 'Current PDF',
                        name: 'details',
                        id: 'fquo-details',
                        allowBlank:false,
                        disabled: true
                    },{
                        xtype: 'fileuploadfield',
                        id: 'fquo-pdf',
                        emptyText: 'Select a PDF',
                        fieldLabel: 'Formal Quote File',
                        name: 'pdf'
                    } 
                ],
            buttons: [
                 {
                 text: 'Send Formal Quote',
                 id:'formalQuoteSubmit',
                 handler: function(){
                    if (Ext.getCmp('fquo-qid').getValue() === '') {
                        alert("sorry, there was an error with the page. please reload and try again");
                    } else {
                        Ext.getCmp('formalquoteedit-panel').getForm().submit(
                        {   successProperty: 'success',
                            success: function (form, action) {
                                if (action.result.success === true) {
                                    form.reset();
    
                                    //display a success alert that auto-closes in 5 seconds
                                    Ext.Msg.alert("Formal Quote Saved", "(this message will auto-close in 5 seconds)");
                                    setTimeout("Ext.Msg.hide()", 5000);

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
                }
                ]

            },
            {
                title: 'Quote History (newest first)',
                id: 'qre-history',
                frame: true,
                bodyStyle:'padding:5px 5px 0',
                width: 380,
                style:'margin-left:30px;margin-top:20px;'
            }
            ]
    };

MA.QuoteEditVisualToggle = function(editMode) {
    if (editMode === false) {
        Ext.getCmp('cancelEditQuoteRequestBtn').hide();
        Ext.getCmp('editQuoteRequestBtn').show();
        Ext.getCmp('qre-email').disable();
        Ext.getCmp('qre-firstname').disable();
        Ext.getCmp('qre-lastname').disable();
        Ext.getCmp('qre-officephone').disable();
        Ext.getCmp('redirectQuoteNode').disable();
        //Ext.getCmp('qre-details').disable();
    }
};

MA.RenderQuoteHistory = function(el, success, response, options) {
     var t = new Ext.XTemplate(
        '<tpl for="data">',
        '<div>',
            '<span style="float:left;color:#666666;">{changetimestamp}</span><span style="float:right;color:#666666;">{email}</span><br/>',
        '</div>',
        '<tpl if="completed != oldcompleted">',
        '<div>', 
            '<span style="float:right;">',
                '<tpl if="completed">quote marked as completed</tpl>',
                '<tpl if="!completed">completed flag cleared</tpl>',
            '</span><br/>',
        '</div>',    
        '</tpl>',
        '<div style="padding-top:4px;padding-bottom:8px;border-bottom:1px solid #7EADD9;">',
            '<div style="color:#999999;">Comment:</div>',
            '{comment}',
        '</div>',
        '</tpl>'
    );
    t.overwrite(el, Ext.util.JSON.decode(response.responseText));   
    
    window.setTimeout("MA.QuoteRequestEditLoaded()", 1000);
};

MA.QuoteRequestListAllInit = function(){
        
    var dataurl = MA.BaseUrl + "quote/listAll";
        
    var madasReader = new MA.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [
            { name: 'id', sortType:'number' },
            { name: 'firstname', sortType : 'string' },
            { name: 'lastname', sortType : 'string' },
            { name: 'email', sortType : 'string' },
            { name: 'officephone', sortType : 'string' },
            { name: 'requesttime', sortType: 'date' },
            { name: 'completed', sortType: 'string' },
            { name: 'unread', sortType: 'string' },
            { name: 'tonode', sortType: 'string' },
            { name: 'changetimestamp', sortType: 'date'}
        ]);
    
    var dataStore = new Ext.data.GroupingStore({
        id         : 'bSId',
        autoLoad   : true,
        reader     : madasReader,
        sortInfo   : {field: 'requesttime', direction: 'DESC'},
        url        : dataurl,
        groupField : 'tonode'
        });
    var gridView = new Ext.grid.GroupingView({
        loadMask : { msg : 'Please wait...' },
        forceFit: true,
        groupTextTpl: ' {[(values.gvalue.length == 0)? "Don\'t Know" : values.gvalue]}',
        hideGroupedColumn: true
        });
    /**var editHandler = function(el, ev) {
        if (selectionModel.hasSelection()) {
            MA.Authorize('quote:edit', [selectionModel.getSelected().data['id']]);
        }
    };*/
    var topToolbar = new Ext.Toolbar({
           /** items   : [
                {  id: 'quoterequestsallEditBtn', text: 'View/Edit', handler: editHandler, disabled: true }
            ] */      
        });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var checkBoxRenderer = function (val){
        if(val == true){
            return '*';
        } else {
            return '';
        }
    }
    var colModel = new Ext.grid.ColumnModel([
        {header: 'ID', align : 'left', sortable: true, dataIndex: 'id', width:25 },
        {header: 'Unread', align:'center', sortable: true, dataIndex: 'unread', renderer: checkBoxRenderer, width:35 },
        {header: 'Completed', align:'center', sortable: true, dataIndex: 'completed', renderer: checkBoxRenderer, width:50 },
        {header: 'Email', width:185, align : 'left', sortable: true, dataIndex: 'email' },
        {header: 'First Name', align : 'left', sortable: true, dataIndex: 'firstname' },
        {header: 'Last Name', align : 'left', sortable: true, dataIndex: 'lastname' },
        {header: 'Phone', align : 'left', sortable: true, dataIndex: 'officephone' },
        {header: 'Date Received', align:'left', sortable: true, dataIndex: 'requesttime'},
        {header: 'To Node', align:'left', sortable: true, dataIndex: 'tonode'},
        {header: 'Completion Date', align:'left', sortable: true, dataIndex: 'changetimestamp'}
        ]);
    var grid = new Ext.grid.GridPanel({
        id             : 'quoterequestsall-panel',
        ds             : dataStore,
        enableDragDrop : false,
        enableColumnMove: false,
        cm             : colModel,
        sm             : selectionModel,
        loadMask       : { msg : 'Loading...' },
        view           : gridView,
        title          : 'Quote Requests for All Nodes',
        tbar           : topToolbar,
        trackMouseOver : false,
        plugins:[new Ext.ux.grid.Search({
             mode:'local'
            ,iconCls:false
            ,dateFormat:'m/d/Y'
            ,minLength:0
            ,width:150
            ,position:'top'
        })]
    });
    /**
    selectionModel.on('selectionchange', function() { var editBtn = Ext.getCmp('quoterequestsallEditBtn'); if (selectionModel.hasSelection()) { editBtn.enable(); } else { editBtn.disable(); } } );
    grid.on('rowdblclick', editHandler);
    */
    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);

};


MA.FormalQuoteUserListInit = function(){
        
    var dataurl = MA.BaseUrl + "quote/listFormal";
        
    var madasReader = new MA.JsonReader({
        root            : 'response.value.items',
        versionProperty : 'response.value.version',
        totalProperty   : 'response.value.total_count'
        }, [//id, quoterequestid, details, created, fromemail, toemail, status
            { name: 'id', sortType:'number' },
            { name: 'quoterequestid', sortType : 'number' },
            { name: 'details', sortType : 'string' },
            { name: 'created', sortType : 'date' },
            { name: 'fromemail', sortType : 'string' },
            { name: 'toemail', sortType: 'string' },
            { name: 'status', sortType: 'string' }
        ]);
    
    var viewHandler = function(grid, rowIndex, e) {
        var selectionModel = grid.getSelectionModel();
    
        if (selectionModel.hasSelection() && selectionModel.getSelected().data['quoterequestid'] !== '') {
            MA.Authorize('quote:viewformal', {"qid" : selectionModel.getSelected().data['quoterequestid']});
        }
    };
    
    var dataStore = new Ext.data.GroupingStore({
        id         : 'bSId',
        autoLoad   : true,
        reader     : madasReader,
        sortInfo   : {field: 'created', direction: 'DESC'},
        url        : dataurl,
        groupField : 'status'
        });
    var gridView = new Ext.grid.GroupingView({
        loadMask : { msg : 'Please wait...' },
        forceFit: true,
//        groupTextTpl: ' {[(values.gvalue.length == 0)? "Don\'t Know" : values.gvalue]}',
        hideGroupedColumn: true
        });

    var topToolbar = new Ext.Toolbar({
            items   : [
                {  id: 'fquoListViewBtn', text: 'View', handler: viewHandler, disabled: true }
            ] 
        });
    var selectionModel = new Ext.grid.RowSelectionModel({ singleSelect: true });
    var checkBoxRenderer = function (val){
        if(val == true){
            return '*';
        } else {
            return '';
        }
    }
    var colModel = new Ext.grid.ColumnModel([
        {header: 'ID', align : 'left', sortable: true, dataIndex: 'id', width:25 },
        {header: 'QID', align : 'left', sortable: true, dataIndex: 'quoterequestid', width:25 },
        {header: 'From', align:'left', sortable: true, dataIndex: 'fromemail'},
         {header: 'To', align:'left', sortable: true, dataIndex: 'toemail'},
        {header: 'Details', align:'left', sortable: true, dataIndex: 'details'},
        {header: 'Status', align : 'left', sortable: true, dataIndex: 'status' },
        {header: 'Created', align : 'left', sortable: true, dataIndex: 'created' }
        ]);
    var grid = new Ext.grid.GridPanel({
        id             : 'fquolist-panel',
        ds             : dataStore,
        enableDragDrop : false,
        enableColumnMove: false,
        cm             : colModel,
        sm             : selectionModel,
        loadMask       : { msg : 'Loading...' },
        view           : gridView,
        title          : 'My Formal Quotes',
        tbar           : topToolbar,
        trackMouseOver : false,
        plugins:[new Ext.ux.grid.Search({
             mode:'local'
            ,iconCls:false
            ,dateFormat:'m/d/Y'
            ,minLength:0
            ,width:150
            ,position:'top'
        })]
    });
    selectionModel.on('selectionchange', function() { var viewBtn = Ext.getCmp('fquoListViewBtn'); if (selectionModel.hasSelection()) { viewBtn.enable(); } else { viewBtn.disable(); } } );
    grid.on('rowdblclick', viewHandler);

    //add this component to the center component
    var center = Ext.getCmp('center-panel');
    center.add(grid);

};



/**
 * madasFquoValidatePassword
 * we need to implement a custom validator because Ext cannot validate an empty field that has to be the same as another field
 */
MA.FquoValidatePassword = function (textfield, event) {
    var passEl = Ext.getCmp('fquoUserEditPassword');
    var confirmEl = Ext.getCmp('fquoUserEditConfirmPassword');
    var submitEl = Ext.getCmp('fquoAcceptButton');
    
    var passVal = Ext.getDom('fquoUserEditPassword').value;
    var confirmVal = Ext.getDom('fquoUserEditConfirmPassword').value;

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

MA.ViewFormalInit = function(paramArray){
    var id = paramArray["qid"];
    var quoteRequestEditCmp = Ext.getCmp('fquouserdetails-panel');
    var formalQuoteCmp = Ext.getCmp('formalquoteview-panel');

    //if node rep or admin, disable the user edit fields
    for (var i = 0; i < quoteRequestEditCmp.items.length; i++) {
        if (MA.IsNodeRep || MA.IsAdmin) {
            if (
                quoteRequestEditCmp.items.get(i).getId() != 'quov-hidden-id' &&
                quoteRequestEditCmp.items.get(i).getId() != 'quov-qid' &&
                quoteRequestEditCmp.items.get(i).getId() != 'fquoadminmode') {
                quoteRequestEditCmp.items.get(i).disable();
            }
        } else {
            quoteRequestEditCmp.items.get(i).enable();
        }
    }
    
    if (MA.IsNodeRep || MA.IsAdmin) {
        Ext.getCmp('fquoadminmode').show();
    } else {
        Ext.getCmp('fquoadminmode').hide();
    }
    
    //fetch user details
    quoteRequestEditCmp.load({url: MA.BaseUrl + 'quote/load', params: {'qid': id}, waitMsg:'Loading'});
    formalQuoteCmp.load({url: MA.BaseUrl + 'quote/formalload', params: {'qid': id}, waitMsg:'Loading'});

    //set the quote id
    Ext.getCmp('quov-hidden-id').setValue(id);
    Ext.getCmp('quov-qid').setValue(id);


};

MA.ViewFormalCmp = {   
    id:'viewformalquote-container-panel',
    autoScroll:true,
    layout:'column',
    bodyStyle:'padding:5px 5px 0px 0px',
    deferredRender:false,
    forceLayout:true,
    items:[
       {   xtype:'form', 
        labelWidth: 100, // label settings here cascade unless overridden
        id:'fquouserdetails-panel',
        url:MA.BaseUrl + 'quote/formalaccept',
        style:'margin-left:30px;margin-top:20px;',
        method:'POST',
        frame:true,
        width: 380,
        reader: new Ext.data.JsonReader({successProperty:'success', root: 'data'}, 
                                          [ {name: 'id', mapping: 'id'}, 
                                            {name: 'tonode', mapping: 'tonode'},
                                            {name: 'details', mapping: 'details'},
                                            {name: 'requesttime', mapping: 'requesttime'},
                                            {name: 'firstname', mapping: 'firstname'},
                                            {name: 'lastname', mapping: 'lastname'},
                                            {name: 'officephone', mapping: 'officephone'},
                                            {name: 'completed', mapping: 'completed'},
                                            {name: 'email', mapping: 'email'} 
                                          ]),
        title: 'Your details',
        bodyStyle:'padding:5px 5px 0',
        defaults: {width: 230},
        defaultType: 'textfield',
        trackResetOnLoad: true,
        waitMsgTarget: true,
        
        items: [
                { xtype:'panel',
                id:'fquoadminmode',
                width:350,
                style:'margin-bottom:10px;',
                frame:true,
                title:'Admin/node rep mode',
                html:'As you are logged in as an admin or node rep, you may Accept/Reject this formal quote on behalf of the user, but user edit fields have been disabled.'
                },
            
            {  
                name: 'id',
                id: 'quov-hidden-id',
                xtype: 'hidden'
            },{  
                name: 'id',
                id: 'quov-qid',
//                xtype:'displayfield',
                fieldLabel:'Request ID'
            },{
                fieldLabel: 'Email address',
                name: 'email',
                vtype: 'email',
                allowBlank:false,
                maskRe: /[^,=]/
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
                id: 'fquoUserEditPassword',
                inputType: 'password',
                allowBlank:true
            },{
                fieldLabel: 'Confirm Password',
                inputType: 'password',
                id: 'fquoUserEditConfirmPassword',
                xtype: 'textfield',
                allowBlank: true,
                validator: MA.FquoValidatePassword
            },{
                fieldLabel: 'Office',
                name: 'office',
                allowBlank:true,
                maskRe: /[^,=]/
            },{
                fieldLabel: 'Office Phone',
                name: 'officephone',
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
        buttons: [
            {
                text: 'Reject Quote',
                handler: function(){
                    //use a different form to submit to avoid validation requirements
                    var simple = new Ext.BasicForm('hiddenForm', {
                        url:MA.BaseUrl + 'quote/formalreject',
                        baseParams:{'qid':Ext.getCmp('quov-qid').getValue()},
                        method:'POST'
                        });
                
                    var submitOptions = {
                        successProperty: 'success',        
                        success: function (form, action) {
                            if (action.result.success === true) { 
                            
                                Ext.Msg.alert('Formal quote rejected', 'close this window when you are ready');
                                
                                //load up the menu and next content area as declared in response
                                MA.ChangeMainContent(action.result.mainContentFunction);
                            } 
                        },
                        failure: function (form, action) {
                        }
                    };
                
                    simple.submit(submitOptions);

                }
            },
            {
            text: 'Save Details and Accept Quote',
            id: 'fquoAcceptButton',
            handler: function(){
                Ext.getCmp('fquouserdetails-panel').getForm().submit(
                    {   successProperty: 'success',        
                        success: function (form, action) {
                            if (action.result.success === true) {
                                //display a success alert that auto-closes in 5 seconds
                                Ext.Msg.alert("You have accepted this formal quote. Thank you.", "An email has been sent to the node representative. We will contact you as soon as possible.");
                                
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
        },
        {
        title: 'Formal Quote',
        frame: true,
        bodyStyle:'padding:5px 5px 0',
        width: 380,
        style:'margin-left:30px;margin-top:20px;',
        xtype:'form',
        labelWidth: 100, // label settings here cascade unless overridden
        id:'formalquoteview-panel',
        reader: new Ext.data.JsonReader({successProperty:'success', root: 'data'}, 
                                        [
                                        {name: 'quoterequestid', mapping: 'quoterequestid'},
                                        {name: 'details', mapping: 'details'},
                                        {name: 'fromemail', mapping: 'fromemail'},
                                        {name: 'toemail', mapping: 'toemail'},
                                        {name: 'tonode', mapping: 'tonode'},
                                        {name: 'pdf', mapping: 'pdf'},
                                        {name: 'fromname', mapping: 'fromname'},
                                        {name: 'officePhone', mapping: 'officePhone'}
                                        ]),
        defaults: {width: 230},
        defaultType: 'textfield',
        trackResetOnLoad: true,
        waitMsgTarget: true,

        items: [
            {  
                name: 'quoterequestid',
                id: 'fquov-qid',
                inputType: 'hidden'
            },{
                fieldLabel: 'Email from',
                name: 'fromemail',
                vtype: 'fromemail',
                allowBlank:false,
                disabled:true,
                id: 'fquov-email'
            },{
                fieldLabel: 'Contact name',
                name: 'fromname',
                disabled:true,
                id: 'fquov-name'
            },{
                fieldLabel: 'MA Node',
                name: 'tonode',
                disabled:true,
                id: 'fquov-tonode'
            },{
                fieldLabel: 'Office Phone',
                name: 'officePhone',
                disabled:true,
                id: 'fquov-officePhone'
            },{
            	xtype:'panel', 
            	width: 350, 
            	style:'padding-top:8px;padding-left:120px;padding-bottom:8px;', 
            	items: [
            		{
            		xtype:'button',
            		text:'Download Quote PDF',
            		handler: function() {
            				window.location = MA.BaseUrl + 'quote/downloadPDF?quoterequestid=' + Ext.getCmp('fquov-qid').value;
            			}
            		}
            	]
            }

        ]
    }
    ]
};
