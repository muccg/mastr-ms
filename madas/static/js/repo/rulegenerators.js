var wsBaseUrl = MA.BaseUrl + "ws/";

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
            text:'Disable Rule Generator'
        }
    ]
};

MA.RuleGeneratorListCmp = {
    id:'ruleGeneratorListCmp',
    layout:'column',
    xtype:'form',
    frame: 'true',
    bodyStyle: 'padding: 5px',
    items: [
        {
            title:'Rule Generators',
            id:'rulegeneratorGrid',
            columnWidth: 0.4,
            layout: 'fit',
            height: 300,
            border: true,
            xtype:'grid',
            /*
            tools: [
                { id: 'plus', qtip: 'Add a new node', handler: MA.NodeManagementAddTool },
                { id: 'minus', qtip: 'Delete currently selected node', handler: MA.NodeManagementDeleteTool }
            ],
            */
            store: ruleGeneratorListStore, 
            tbar: [{
                    text: 'Create New',
                    handler: function(b, ev) {
                        Ext.getCmp('ruleGeneratorCreateCmp').show();
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


var create_block_store = function(){
    return new Ext.data.ArrayStore({
                    fields: [
                        {name: 'count'},
                        {name: 'component', type:'integer'}
                    ]//,
                    //data: [ [1,1],[1,2],[1,3], [1,4], [1,5]]
                }) 
    }

var createRuleBlockComponent = function(idbasename, blockname){
    
    var blockStore = create_block_store();

    return {
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
                plugins: [new Ext.ux.grid.MARowEditor({saveText: 'Update'})],
                sm: new Ext.grid.RowSelectionModel(),
                store: blockStore,
                columns: [
                    { header: 'Add', dataIndex: 'count', sortable: false, editor: new Ext.form.NumberField({editable:true, maxValue:99, minValue: 1, allowBlank:false}) },
                    { header: 'Components', dataIndex: 'component', sortable: false, editor: new Ext.form.ComboBox({ 
     editable: false,
     forceSelection: true,
     displayField: 'component',
     valueField: 'id',
     lazyRender: true,
     allowBlank: false,
     typeAhead: false,
     triggerAction: 'all',
     mode: 'remote',
     store: ruleComponentStore
                    }), //end combobox part of header
     renderer:renderClass                
     } ], //end columns
                viewConfig:{
                        forceFit:true,
                        autoFill:true
                    },
                autoScroll:true,
                reserveScrollOffset:true,
                bbar: [{
                        text: 'Add rule row',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-addrulebutton',
                        icon: 'static/images/add.png',
                        handler: function(btn, ev) {
                            blockStore.add( new blockStore.recordType({ count: 1,
                                component: 2}));

                        }
                       },
                       {
                        text: 'Remove rule row',
                        cls: 'x-btn-text-icon',
                        id: idbasename + '-removerulebutton',
                        icon: 'static/images/delete.png',

                        handler: function(btn, evt){
                            alert("Todo!");
                        }
                       }
                ]
            }

        
    };

MA.RuleGeneratorCreateCmp = new Ext.Window({
    id:'ruleGeneratorCreateCmp',
    title: 'Create new Rule Generator',
    closeAction: 'hide',
    bodyStyle: 'padding: 5px',
    width: 680,
    height: 530,
    modal:true,
    items: [{
        bodyStyle: 'padding: 5px',
        id: 'ruleGeneratorCreateForm',
        xtype: 'form',
        url: wsBaseUrl + 'create_rule_generator',
        defaultType: 'textfield',
        buttonAlign: 'center',
        defaults: {labelWidth: 120, autoWidth:true, autoHeight:true},
        items: [
            {
                fieldLabel: 'Name',
                name: 'name'
            },{
                fieldLabel: 'Description',
                xtype: 'textarea',
                name: 'description'
            },{
                fieldLabel: 'Accessible by',
                xtype: 'radiogroup',
                itemCls: 'x-check-group-alt',
                columns: 3,
                items: [
                    { boxLabel: 'Just Myself', name: 'accessibility', inputValue: 1, checked: true },
                    { boxLabel: 'Everyone in my Node', name: 'accessibility', inputValue: 2 },
                    { boxLabel: 'Everyone', name: 'accessibility', inputValue: 3 }
                ]
            },{
                xtype:'tabpanel',
                //activeItem:0,
                border:true,
                frame: true,
                anchor: '100%, 100%', //so anchoring works at lower level containers, and full height tabs
                deferredRender: false, //submit fields from all tabs, not just active one.
                defaults: { layout: 'form', labelWidth: 80, hideMode: 'offsets'},
                items: [
                    createRuleBlockComponent('startblock', 'Start Block'),
                    createRuleBlockComponent('sampleblock', 'Sample Block'),
                    createRuleBlockComponent('endblock', 'End Block')]

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
                        gridcmp.getSelectionModel().selectAll()
                        var sels = gridcmp.getSelectionModel().getSelections();
                        for (i=0; i < sels.length; i++){
                            retval.push({count:sels[i].get('count'), component: sels[i].get('component')});
                        }
                        return retval;
                    };

                    var formvalues = theform.getValues()

                    Ext.Ajax.request({
                        url: wsBaseUrl + 'create_rule_generator',
                        method: 'POST',
                        params: {'name': formvalues.name, 
                                 'description': formvalues.description, 
                                 'accessibility': formvalues.accessibility, 
                                 'startblock':Ext.encode(get_grid_keyvals('startblock')), 
                                 'sampleblock': Ext.encode(get_grid_keyvals('sampleblock')), 
                                 'endblock':Ext.encode(get_grid_keyvals('endblock')), 
                                 },
                        success:function(form, action){
                            console.log('Create rule gen succeeded');
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
                        },
                        failure: function(form, action){
                            console.log('Create rule gen failed');
                            Ext.getCmp('ruleGeneratorCreateCmp').hide();
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



