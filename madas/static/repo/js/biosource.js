Ext.madasBioSourceInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    
    var loader = new Ajax.Request(wsBaseUrl + 'records/biologicalsource/experiment__id/'+expId, 
                                 { 
                                 asynchronous:true, 
                                 evalJSON:'force',
                                 onSuccess:     Ext.madasBioLoadSuccess
                                 });
    
    var orgType = Ext.madasCurrentOrganismType();
    //console.log("init for orgtype "+orgType);
    if (orgType == 4) {
        humanStore.proxy.conn.url = wsBaseUrl + 'records/human/experiment__id/' + expId;
        humanStore.load();
        Ext.getCmp("organismBioSourceHumanFieldset").show();
        Ext.getCmp("organismBioSourceAnimalFieldset").hide();
    } else if (orgType == 3) {
        animalStore.proxy.conn.url = wsBaseUrl + 'records/animal/experiment__id/' + expId;
        animalStore.load();
        Ext.getCmp("organismBioSourceAnimalFieldset").show();
        Ext.getCmp("organismBioSourceHumanFieldset").hide();
    } else if (orgType == 2) {
        Ext.getCmp("organismBioSourceHumanFieldset").hide();
        Ext.getCmp("organismBioSourceAnimalFieldset").hide();
    } else {
        Ext.getCmp("organismBioSourceAnimalFieldset").hide();
        Ext.getCmp("organismBioSourceHumanFieldset").hide();
    }
    
    organStore.proxy.conn.url = wsBaseUrl + 'records/organ/experiment__id/' + expId;
    organStore.load();

};

Ext.madasBioLoadSuccess = function(response) {
    Ext,madasCurrentSingleSourceId = response.responseJSON.rows[0].id;
    Ext.getCmp('sourceType').setValue( response.responseJSON.rows[0].type );
    Ext.getCmp('sourceInfo').setValue( response.responseJSON.rows[0].information );
    Ext.getCmp('sourceNCBI').setValue( response.responseJSON.rows[0].ncbi_id );
};

Ext.madasBioSourceBlur = function(invoker) {
    var expId = Ext.madasCurrentExperimentId();
    Ext.madasExperimentDeferredInvocation = invoker;
    var humanGender, humanDob, humanBmi, humanDiagnosis, animalGender, animalAge, animalParentalLine;
    var sourceType, sourceInfo, sourceNCBI;
    
    sourceType = Ext.getCmp('sourceType').getValue();
    sourceInfo = Ext.getCmp('sourceInfo').getValue();
    sourceNCBI = Ext.getCmp('sourceNCBI').getValue();
    
    //TODO process new form field elements
    if (Ext.madasCurrentOrganismType() == '4') { //human
    } else if (Ext.madasCurrentOrganismType() == '3') { //animal
    } else {
    }

    //this request should ask the server to rejig the single biosource that we currently permit
    var saver = new Ajax.Request(wsBaseUrl + 'updateSingleSource/'+expId+'/?type='+escape(sourceType)+'&information='+escape(sourceInfo)+'&ncbi_id='+escape(sourceNCBI), 
                                 { 
                                 asynchronous:true, 
                                 evalJSON:'force',
                                 onSuccess:     Ext.madasBioSourceBlurSuccess
                                 });
};

Ext.madasSourceTypeSelect = function() {
    //display the appropriate fieldset
};

Ext.madasBioSourceBlurSuccess = function() {
    
    var index = Ext.madasExperimentDeferredInvocation.index;
    
    if (index >= 0) {
        Ext.getCmp("expContent").getLayout().setActiveItem(index); 
        Ext.currentExperimentNavItem = index;
    }

    Ext.madasExperimentDeferredInvocation.init();
    
    Ext.madasExperimentDeferredInvocation = {'index':-1, 'init':Ext.madasNull};
};

Ext.madasSaveOrganRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData.name = rec.data.name;
    bundledData.detail = rec.data.detail;
    
    Ext.madasSaveRowLiterals('organ', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/experiment__id/' + expId; organStore.load();});
};

Ext.madasBioSource = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
           title: 'source details',
            region: 'center',
            collapsible: false,
            layout:'form',
            autoScroll:true,
            minSize: 75,
            items: [
                    { 
                        xtype: 'combo', 
                        fieldLabel:'source type',
                        id:'sourceType',
                        name:'typeText',
                        editable:false,
                        forceSelection:true,
                        displayField:'value',
                        valueField:'key',
                        hiddenName:'sourceTypeValue',
                        lazyRender:true,
                        value:'Microbial',
                        mode:'local',
                        allowBlank:false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        store: new Ext.data.ArrayStore({
                                                   fields: ['value', 'key'],
                                                   data : [['Microbial', 1],
                                                           ['Plant', 2],
                                                           ['Animal', 3],
                                                           ['Human', 4]]
                                                   }),
                        listeners: {
                            'select': Ext.madasSourceTypeSelect
                        }
                    },
                    {
                        fieldLabel:'information',
                        id:'sourceInfo',
                        xtype:'textfield'
                    },
                    {
                        fieldLabel:'ncbi id',
                        id:'sourceNCBI',
                        xtype:'textfield'
                    },
                    { xtype:'fieldset', 
                    title:'animal info',
                    id:'organismBioSourceAnimalFieldset',
                    autoHeight:true,
                    //hidden:true,
                    items: [
                            
                        { xtype:'combo', 
                            fieldLabel:'gender',
                            id:'animalGender',
                            name:'genderText',
                            editable:false,
                            forceSelection:true,
                            displayField:'value',
                            valueField:'key',
                            hiddenName:'gender',
                            lazyRender:true,
                            allowBlank:false,
                            mode:'local',
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:230,
                            store: new Ext.data.ArrayStore({
                                                            fields: ['value', 'key'],
                                                            data : [['Male', 'M'],
                                                                    ['Female', 'F'],
                                                                    ['Unknown', 'U']]
                                                            })
                        }, 
                        { xtype:'textfield', fieldLabel:'age', id:'animalAge', maskRe:/^[0-9]*$/}, 
                        { xtype:'combo', 
                            fieldLabel:'parental line',
                            editable:true,
                            id:'animalParentalLine',
                            displayField:'value',
                            valueField:'key',
                            forceSelection:false,
                            hiddenName:'node',
                            lazyRender:true,
                            allowBlank:true,
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:230,
                            store: animalComboStore    
                        }
                    ]
                },
                { xtype:'fieldset', 
                title:'human info',
                id:'organismBioSourceHumanFieldset',
                autoHeight:true,
                //hidden:true,
                items: [
                        
                        { xtype:'combo', 
                        fieldLabel:'gender',
                        id:'humanGender',
                        editable:false,
                        forceSelection:true,
                        displayField:'value',
                        valueField:'key',
                        hiddenName:'node',
                        lazyRender:true,
                        allowBlank:false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        store: new Ext.data.ArrayStore({
                                                       fields: ['value', 'key'],
                                                       data : [['Male', 'M'],
                                                               ['Female', 'F'],
                                                               ['Unknown', 'U']]
                                                       })
                        
                        }, 
                        { xtype:'datefield', fieldLabel:'Date of birth', id:'human_dob', format:'d/m/Y'}, 
                        { xtype:'textfield', fieldLabel:'BMI', id:'human_bmi', maskRe:/^[0-9]*\.*[0-9]*$/ },
                        { xtype:'textfield', fieldLabel:'Diagnosis', id:'human_diagnosis' }
                        ]
                },
                { xtype:'grid', 
                    id:'organs',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'organs/parts',
                    border: true,
                    height:200,
                    trackMouseOver: false,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveOrganRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    tbar: [{
                        text: 'add organ/part',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/add.gif',
                        handler : function() {
                           Ext.madasCRUDSomething('create/organ/', {'experiment_id':Ext.madasCurrentExperimentId()}, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/experiment__id/' + expId;
                                                  organStore.load(); });
                        }
                        }, 
                        {
                        text: 'remove organ/part',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/no.gif',
                        handler : function(){
                            var grid = Ext.getCmp('organs');
                            var delIds = []; 
                           
                            var selections = grid.getSelectionModel().getSelections();
                            if (!Ext.isArray(selections)) {
                                selections = [selections];
                            }
                           
                           for (var index = 0; index < selections.length; index++) {
                                if (!Ext.isObject(selections[index])) {
                                    continue;
                                }
                           
                                delIds.push(selections[index].data.id);
                            }

                           for (var i = 0; i < delIds.length; i++) {
                           Ext.madasCRUDSomething('delete/organ/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/experiment__id/' + expId;
                                                  organStore.load(); });
                            }
                        }
                        }
                    ],
                    columns: [
                        { header: "name",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                hiddenName:'tissue',
                                lazyRender:true,
                                allowBlank:false,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: organNameComboStore
                            }), dataIndex:'name' },
                        { header: "detail", sortable:false, menuDisabled:true, editor:new Ext.form.TextField({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                hiddenName:'detailValue',
                                lazyRender:true,
                                allowBlank:true,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                            }), dataIndex:'detail'
                        }
                    ],
                    store: organStore
                }
            ]
        }
    ]
};

