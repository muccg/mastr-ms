var wsBaseUrl = MA.BaseUrl + "ws/";

MA.ComboRendererBackend = function(options) {
    var value = options.value;
    var combo = options.combo;

    var returnValue = value;
    var valueField = combo.valueField;
        
    var idx = combo.store.findBy(function(record) {
        if(record.get(valueField) == value) {
            returnValue = record.get(combo.displayField);
            return true;
        }
    });
    
    // This is our application specific and might need to be removed for your apps
    if(idx < 0 && value == 0) {
        returnValue = '';
    }
    
    return returnValue;
};

MA.ComboRenderer = function(combo) {
    return function(value, meta, record) {
        return MA.ComboRendererBackend({value: value, meta: meta, record: record, combo: combo});
    };
}



MA.RuleGeneratorDetailsCmp = {
    id: 'rule-generator-details',
    xtype: 'fieldset',
    columnWidth: 0.6,
    title: 'Rule generator details',
    labelWidth: 90,
    defaults: {border:false},
    defaultType: 'displayfield',
    autoHeight: true,
    bodyStyle: Ext.isIE ? 'padding:0 0 5px 15px;' : 'padding:10px 15px;',
    border: false,
    buttonAlign: 'left',
    style: {
        "margin-left": "10px", // when you add custom margin in IE 6...
        "margin-right": Ext.isIE6 ? (Ext.isStrict ? "-10px" : "-13px") : "0"  // you have to adjust for it somewhere else
    },
    displayRecord: function(rec) {
        Ext.getCmp("ruleGeneratorListCmp").getForm().loadRecord(rec);
        this.displayStartBlock(rec.data.startblock);
        this.displaySampleBlock(rec.data.sampleblock);
        this.displayEndBlock(rec.data.endblock);
        this.alterButton(rec);
    },
    alterButton: function(rec) {
        var but = Ext.getCmp('rulegenerator_state_button');
        var state = rec.get('state') 
        but.rulegen_prevstate = state;
        if ( (state == 'In Design') || (state == 'Disabled' ) )
        {
            but.setText('Enable Rule Generator');
            but.rulegen_state = 2; //enabled 
            but.rulegen_id = rec.get('id');
        }
        else if (state == 'Enabled')
        {
            but.setText('Disable Rule Generator');
            but.rulegen_state = 3; //disabled 
            but.rulegen_id = rec.get('id');
        }
    },
    displayStartBlock: function(startBlock) {
        var list= '<ol>';
        var item;
        for (var i = 0; i < startBlock.length; i++) {
            item = 'Add ' + startBlock[i].count + ' ' + startBlock[i].component;
            list += '<li>' + item  + '</li>';
        }
        list += '</ol>';
        this.getComponent('startblock').update(list);
    },
    displaySampleBlock: function(sampleBlock) {
        var list= '<ol>';
        var item;
        for (var i = 0; i < sampleBlock.length; i++) {
            item = 'Add ' + sampleBlock[i].count + ' ' + sampleBlock[i].component + ' for every ' + sampleBlock[i].sample_count + ' samples in ' + sampleBlock[i].order;
            list += '<li>' + item  + '</li>';
        }
        list += '</ol>';
        this.getComponent('sampleblock').update(list);
    },
    displayEndBlock: function(endBlock) {
        var list= '<ol>';
        var item;
        for (var i = 0; i < endBlock.length; i++) {
            item = 'Add ' + endBlock[i].count + ' ' + endBlock[i].component;
            list += '<li>' + item  + '</li>';
        }
        list += '</ol>';
        this.getComponent('endblock').update(list);
    },
    items: [{
            fieldLabel: 'Name',
            name: 'full_name'
        },{
            fieldLabel: 'State',
            name: 'state'
        },{
            fieldLabel: 'Accessible By',
            name: 'accessibility'
        },{
            fieldLabel: 'Start Block',
            itemId: 'startblock',
            xtype: 'panel'
        },{
            fieldLabel: 'Sample Block',
            itemId: 'sampleblock',
            xtype: 'panel'
        },{
            fieldLabel: 'End Block',
            itemId: 'endblock',
            xtype: 'panel'
        },{
            fieldLabel: 'Created By',
            name: 'created_by'
        }
    ],
    buttons: [{
            text:'Not Loaded',
            id: 'rulegenerator_state_button',
            sendUpdateRequest: function() {
                Ext.Ajax.request({
                        url: wsBaseUrl + 'edit_rule_generator',
                        method: 'POST',
                        params: {rulegen_id: this.rulegen_id, state: this.rulegen_state}, 
                        success:function(result, request){
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
                            Ext.getCmp('rulegeneratorGrid').store.reload();
                            Ext.getCmp('rulegeneratorGrid').getView().refresh();
                            var jsonData = Ext.util.JSON.decode(result.responseText)
                            if (jsonData.success){
                            }
                            else{
                                Ext.Msg.alert("Error", jsonData.msg);
                            }
                        },
                        failure: function(result, request){
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
                            Ext.Msg.alert("Operation failed");
                        } 
                });
            },
            handler: function(){
                if ( (typeof(this.rulegen_id) != 'undefined') &&
                     (typeof(this.rulegen_state) != 'undefined'))
                {
                    if (this.rulegen_prevstate === 'In Design') {
                        Ext.Msg.confirm("Are you sure?", 
                            "Once the Rule Generator has been enabled you won't be able to edit it anymore. Are you sure you want to enable the Rule Generator?", 
                            function(button) {
                                if (button === 'yes') {
                                    this.sendUpdateRequest();
                                }
                            }, this);               
                    } else {
                        this.sendUpdateRequest();
                    }
                }
            }
            } 
    ]
};

MA.RuleGeneratorListCmp = {
    id:'ruleGeneratorListCmp',
    layout:'column',
    xtype:'form',
    frame: 'true',
    bodyStyle: 'padding: 5px',
    onStoreLoad: function(){
                //refresh the details component
                var selModel = Ext.getCmp('rulegeneratorGrid').getSelectionModel();
                if (selModel.hasSelection()) {
                    var record = selModel.getSelected();
                    Ext.getCmp("rule-generator-details").displayRecord(record);
                } 
            },
    items: [
        {
            title:'Rule Generators',
            id:'rulegeneratorGrid',
            columnWidth: 0.4,
            layout: 'fit',
            height: 300,
            border: true,
            xtype:'grid',
            store: ruleGeneratorListStore,
            
            tbar: [{
                    text: 'Create New',
                    handler: function(b, ev) {
                        Ext.getCmp('ruleGeneratorCreateCmp').create();
                    }
                },{
                    xtype: 'tbseparator'
                },{
                    text: 'Create new Version',
                    handler: function(b, ev) {
                        var selModel = Ext.getCmp('rulegeneratorGrid').getSelectionModel();
                        var record;
                        if (!selModel.hasSelection()) {
                            Ext.Msg.alert('Nothing selected', 'Please select a Rule Generator first.');
                            return;
                        }
                        record = selModel.getSelected();
                        Ext.Ajax.request({
                            url: wsBaseUrl + 'create_new_version_of_rule_generator',
                            method: 'POST',
                            params: {'id': record.get('id')},
                            success:function(response, opts){
                                var newId = Ext.decode(response.responseText).new_id;

                                var store = Ext.getCmp('rulegeneratorGrid').getStore();
                                var selectFn = function() {
                                    selModel.selectRow(store.indexOfId(newId));
                                    Ext.getCmp('ruleGeneratorCreateCmp').edit(newId);
                                };
                                store.addListener('load', selectFn, this, {single:true});
                                store.reload();
                            },
                            failure: function(form, action){
                                Ext.Msg.alert("Error", "Couldn't create new version of Rule Generator");
                            }
                        });

                    }
                },{
                    xtype: 'tbseparator'
                },{
                    text: 'Clone',
                    handler: function(b, ev) {
                        var selModel = Ext.getCmp('rulegeneratorGrid').getSelectionModel();
                        var record;
                        if (!selModel.hasSelection()) {
                            Ext.Msg.alert('Nothing selected', 'Please select a Rule Generator first.');
                            return;
                        }
                        record = selModel.getSelected();
                        Ext.Ajax.request({
                            url: wsBaseUrl + 'clone_rule_generator',
                            method: 'POST',
                            params: {'id': record.get('id')},
                            success:function(response, opts){
                                var newId = Ext.decode(response.responseText).new_id;

                                var store = Ext.getCmp('rulegeneratorGrid').getStore();
                                var selectFn = function() {
                                    selModel.selectRow(store.indexOfId(newId));
                                    Ext.getCmp('ruleGeneratorCreateCmp').edit(newId);
                                };
                                store.addListener('load', selectFn, this, {single:true});
                                store.reload();
                            },
                            failure: function(form, action){
                                Ext.Msg.alert("Error", "Couldn't clone Rule Generator");
                            }
                        });

                    }
                },{
                    xtype: 'tbseparator'
                },{
                    text: 'Edit',
                    handler: function(b, ev) {
                        var selModel = Ext.getCmp('rulegeneratorGrid').getSelectionModel();
                        var record;
                        if (!selModel.hasSelection()) {
                            Ext.Msg.alert('Nothing selected', 'Please select the Rule Generator to edit first.');
                            return;
                        }
                        record = selModel.getSelected();
                        if (record.get('state') !== 'In Design') {
                            Ext.Msg.alert('Not Editable', 'Rule Generators are editable only while they are In Design. For changing Rule Generators that have been Enabled please consider using Create New Version.');
                            return;
                        }
                        Ext.getCmp('ruleGeneratorCreateCmp').edit(record.get('id'));
                    }
                }

            ], 
            columns: [
                  {header: 'Name', sortable:true, dataIndex: 'full_name'},
                  {header: 'State', sortable:true, dataIndex: 'state'},
                  {header: 'Accessible by', sortable:true, dataIndex: 'accessibility'},
                  {header: 'Created By', sortable:true, dataIndex: 'created_by'}
            ],
            viewConfig: {forceFit:true},
            sm: new Ext.grid.RowSelectionModel({
                    singleSelect: true,
                    listeners: {
                        rowselect: function(sm, row, rec) {
                            Ext.getCmp("rule-generator-details").displayRecord(rec);
                        }
                    }
            }),
            lazyRender:true,
            bbar:[{xtype:'tbspacer'}],
            },
        MA.RuleGeneratorDetailsCmp
        ]
};

ruleGeneratorListStore.on({
                    'load':{
                        fn: function(store, records, options){
                            MA.RuleGeneratorListCmp.onStoreLoad();
                        },
                        scope: this 
                    }});



var createRuleBlockComponent = function(idbasename, blockname, issampleblock){

    var create_block_store = function(){

    var fields = [{name: 'count', type: 'integer'},
                  {name: 'component', type: 'string'}
                 ];

    if (issampleblock){
        fields.push({name: 'every', type: 'integer'});
        fields.push({name: 'order', type: 'string'});
    }

    return new Ext.data.ArrayStore({
                    fields: fields
                }) 
    }


    var blockStore = create_block_store();
    var componentCombo = new Ext.form.ComboBox({ 
             editable: false,
             forceSelection: true,
             displayField: 'component',
             valueField: 'id',
             lazyRender: true,
             allowBlank: false,
             typeAhead: false,
             triggerAction: 'all',
             mode: 'local',
             store: ruleComponentStore
                            });

    var orderCombo = new Ext.form.ComboBox({ 
                 editable: false,
                 forceSelection: true,
                 displayField: 'order',
                 valueField: 'id',
                 lazyRender: true,
                 allowBlank: false,
                 typeAhead: false,
                 triggerAction: 'all',
                 mode: 'local',
                 store: new Ext.data.ArrayStore({fields: ['id', 'order'], 
                                                 data: [[1,'random'],[2, 'position']]}) //data comes from models.py 
                                                                                        //(RuleGeneratorSampleBlock)
                                });

    var columns = [
                    { header: 'Add', dataIndex: 'count', sortable: false, editor: new Ext.form.NumberField({editable:true, maxValue:99, minValue: 1, allowBlank:false}) },
                    { header: 'Components', dataIndex: 'component', sortable: false, editor: componentCombo, renderer:MA.ComboRenderer(componentCombo)} ];

     if (issampleblock){
        columns.push({header: 'Every', dataIndex: 'every', sortable: false, editor: new Ext.form.NumberField({editable:true, maxValue:99, minValue: 1, allowBlank:false})})
        columns.push({ header: 'Order', dataIndex: 'order', sortable: false, editor: orderCombo, renderer:MA.ComboRenderer(orderCombo)});
     }


    var blockgrid = {
                id: idbasename,
                fieldLabel: blockname,
                title: blockname,
                itemId: idbasename,
                name: idbasename,
                hiddenName: idbasename,
                xtype: 'grid',
                autoWidth: true,
                height: 300,
                //autoHeight: true,
                plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update', errorSummary:false})],
                sm: new Ext.grid.RowSelectionModel(),
                store: blockStore,
                columns: columns, //end columns
                viewConfig:{
                        forceFit:true,
                        autoFill:true
                    },
                autoScroll:true,
                reserveScrollOffset:true,
                moveSelectedRow: function(grid, direction) {
                    var record = grid.getSelectionModel().getSelected();
                    if (!record) {
                        return;
                    }
                    var index = grid.getStore().indexOf(record);
                    if (direction < 0) {
                        index--;
                        if (index < 0) {
                            return;
                        }
                    } else {
                        index++;
                        if (index >= grid.getStore().getCount()) {
                            return;
                        }
                    }
                    grid.getStore().remove(record);
                    grid.getStore().insert(index, record);
                    grid.getSelectionModel().selectRow(index, true);
                },
                bbar: [{
                        text: 'Add rule row',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-addrulebutton',
                        icon: 'static/images/add.png',
                        handler: function(btn, ev) {
                            blockStore.add( new blockStore.recordType({ count: 1,
                                component: 2, every: 1, order: 1}));

                        }
                       },
                       {
                        text: 'Remove rule row',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-removerulebutton',
                        icon: 'static/images/delete.png',
                        handler: function(btn, evt){
                            var thisgrid = Ext.getCmp(idbasename);
                            var selections = thisgrid.getSelectionModel().getSelections();
                            if (!Ext.isArray(selections)){
                                selections = [selections];
                            }

                            for (var index=0; index<selections.length; index++){
                                if (!Ext.isObject(selections[index])) {
                                    continue;
                                }
                                thisgrid.getStore().remove(selections[index]);
                            }
                        }
                       },{                       
                        text: 'Move rule up',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-moveuprulebutton',
                        icon: 'static/images/arrow-up.png',
                        handler: function(btn, evt){
                            var grid = Ext.getCmp(idbasename);
                            grid.moveSelectedRow(grid, -1);
                        }
                        },{                       
                        text: 'Move rule down',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-movedownrulebutton',
                        icon: 'static/images/arrow-down.png',
                        handler: function(btn, evt){
                            var grid = Ext.getCmp(idbasename);
                            grid.moveSelectedRow(grid, 1);
                        }
                       }

                ]
            }

        
        return blockgrid;
    };


// No map() in ExtJS? :(
function map(arr, map_fn) {
    var mapped_arr = []
    for (var i = 0; i < arr.length; i++) {
        mapped_arr.push(map_fn(arr[i]));
    }
    return mapped_arr;
}

MA.RuleGeneratorCreateCmp = new Ext.Window({
    id:'ruleGeneratorCreateCmp',
    title: 'Create new Rule Generator',
    closeAction: 'hide',
    bodyStyle: 'padding: 5px',
    width: 680,
    height: 550,
    modal:true,
    clearValues: function() {
        var theform = Ext.getCmp('ruleGeneratorCreateForm').getForm();
        theform.clearFields();
        Ext.getCmp('startblock').getStore().removeAll();
        Ext.getCmp('sampleblock').getStore().removeAll();
        Ext.getCmp('endblock').getStore().removeAll();
        theform.rulegen_id = null;
    },
    create: function() {
        this.clearValues();
        this.setTitle('Create new Rule Generator');
        MA.RuleGeneratorCreateCmp.show(); 
    },
    edit: function(rulegen_id) {
        this.clearValues();
        this.setTitle('Edit Rule Generator');
        Ext.Ajax.request({
            url: wsBaseUrl + 'get_rule_generator',
            method: 'GET',
            params: {'id': rulegen_id},
            success:function(response, opts){
                var rulegen = Ext.decode(response.responseText).rulegenerator;
                var theform = Ext.getCmp('ruleGeneratorCreateForm').getForm();
                var mapper_fn = function(rule) {return [rule.count, rule.component_id]; };
                var samplemapper_fn = function(rule) {return [rule.count, rule.component_id, rule.sample_count, rule.order_id]};
                theform.setValues(rulegen);
                theform.rulegen_id = rulegen_id; //set an id on the form so we know it is an edit
                if (rulegen.version) {
                    theform.findField('name').disable();
                } else {
                    theform.findField('name').enable();
                }
                Ext.getCmp('startblock').getStore().loadData(map(rulegen.startblock, mapper_fn));
                Ext.getCmp('sampleblock').getStore().loadData(map(rulegen.sampleblock, samplemapper_fn));
                Ext.getCmp('endblock').getStore().loadData(map(rulegen.endblock, mapper_fn));
                MA.RuleGeneratorCreateCmp.show(); 
            },
            failure: function(form, action){
                Ext.Msg.alert("Error", "Couldn't load details of Rule Generator");
            }
        });
    },
    items: [{
        bodyStyle: 'padding: 5px',
        id: 'ruleGeneratorCreateForm',
        xtype: 'form',
        url: wsBaseUrl + 'create_rule_generator',
        defaultType: 'textfield',
        buttonAlign: 'center',
        defaults: {labelWidth: 120, autoWidth:true, autoHeight:true},
        clearFields: function() {
            this.items.each(function(field) {
                    field.setRawValue('');
                });
            this.findField('accessibility_id').setValue(1);
        },
        items: [
            {
                fieldLabel: 'Name',
                name: 'name'
            },{
                fieldLabel: 'Version',
                name: 'version',
                xtype: 'displayfield'
            },{
                fieldLabel: 'Description',
                xtype: 'textarea',
                name: 'description'
            },{
                fieldLabel: 'Accessible by',
                name: 'accessibility_id',
                xtype: 'radiogroup',
                itemCls: 'x-check-group-alt',
                columns: 3,
                items: [
                    { boxLabel: 'Just Myself', name: 'accessibility_id', itemId: 'justMyself', inputValue: 1, checked: true },
                    { boxLabel: 'Everyone in my Node', name: 'accessibility_id', inputValue: 2 },
                    { boxLabel: 'Everyone', name: 'accessibility_id', inputValue: 3 }
                ]
            },{
                xtype:'tabpanel',
                activeItem:0,
                border:true,
                frame: true,
                anchor: '100%, 100%', //so anchoring works at lower level containers, and full height tabs
                defaults: { layout: 'form', labelWidth: 80, hideMode: 'offsets'},
                items: [
                    createRuleBlockComponent('startblock', 'Start Block', false),
                    createRuleBlockComponent('sampleblock', 'Sample Block', true),
                    createRuleBlockComponent('endblock', 'End Block', false)]

            } ],
        buttons: [{
                text: 'Save',
                
                formBind: true,
                disabled: false,
                handler: function(){
                    var theform = Ext.getCmp('ruleGeneratorCreateForm').getForm()

                    var get_grid_keyvals = function(gridid){
                        var retval = [];
                        var gridcmp = Ext.getCmp(gridid);
                        var store = gridcmp.getStore();
                        store.each(function(record) {
                                recobj = {};
                                for (var key in record.data){
                                    recobj[key] = record.get(key);
                                }
                                retval.push(recobj);
                            }, this);
                        return retval;
                    };

                    var formvalues = theform.getValues()

                    var formparams = {'name': formvalues.name, 
                                 'description': formvalues.description, 
                                 'accessibility': formvalues.accessibility_id, 
                                 'startblock':Ext.encode(get_grid_keyvals('startblock')), 
                                 'sampleblock': Ext.encode(get_grid_keyvals('sampleblock')), 
                                 'endblock':Ext.encode(get_grid_keyvals('endblock')), 
                                 };

                    var submiturl = 'create_rule_generator';
                    if ( (typeof(theform.rulegen_id)!='undefined') && (theform.rulegen_id != null) )
                    {
                        submiturl = 'edit_rule_generator';
                        formparams.rulegen_id = theform.rulegen_id;

                    }

                    Ext.Ajax.request({
                        url: wsBaseUrl + submiturl,
                        method: 'POST',
                        params: formparams, 
                        success:function(result, request){
                            Ext.getCmp('rulegeneratorGrid').store.reload();
                            Ext.getCmp('rulegeneratorGrid').getView().refresh();
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
                            var jsonData = Ext.util.JSON.decode(result.responseText)
                            if (jsonData.success){
                            }
                            else{
                                Ext.Msg.alert("Error", jsonData.msg);
                            }

                        },
                        failure: function(form, action){
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
                            Ext.Msg.alert("Operation failed");
                        } });
                        
                    }
                
                },
            {
                text: 'Cancel',
                handler: function(btn, ev) {
                    Ext.getCmp('ruleGeneratorCreateCmp').hide();
                }
            }
        ]
    }]
});



