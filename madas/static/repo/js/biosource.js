Ext.madasBioSourceInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    
    var orgType = Ext.madasCurrentOrganismType();
    //console.log("init for orgtype "+orgType);
    if (orgType == 4) {
        humanStore.proxy.conn.url = wsBaseUrl + 'records/human/experiment__id/' + expId;
        humanStore.load();
        Ext.getCmp("organismBioSourceHumanFieldset").show();
        Ext.getCmp("organismBioSourceAnimalFieldset").hide();
    }
    
    if (orgType == 3) {
        animalStore.proxy.conn.url = wsBaseUrl + 'records/animal/experiment__id/' + expId;
        animalStore.load();
        Ext.getCmp("organismBioSourceAnimalFieldset").show();
        Ext.getCmp("organismBioSourceHumanFieldset").hide();
    }
    
    if (orgType == 2) {
        Ext.getCmp("organismBioSourceAnimalFieldset").hide();
    }
    
    organStore.proxy.conn.url = wsBaseUrl + 'records/organ/source__experiment__id/' + expId;
    organStore.load();
    
    genotypeStore.proxy.conn.url = wsBaseUrl + 'records/genotype/source__experiment__id/' + expId;
    genotypeStore.load();
}

Ext.madasBioSourceBlur = function(invoker) {
    var expId = Ext.madasCurrentExperimentId();
    Ext.madasExperimentDeferredInvocation = invoker;

    if (Ext.madasCurrentOrganismType() == '4') { //human
        var humanGender = Ext.getCmp("humanGender").getValue();
        var humanDob = Ext.util.Format.date(Ext.getCmp("human_dob").getValue(), 'Y-m-d');
        var humanBmi = Ext.getCmp("human_bmi").getValue();
        var humanDiagnosis = Ext.getCmp("human_diagnosis").getValue();
        
        //hook up new load handler
        humanStore.on("load", Ext.madasBioSourceBlurSuccess);
        
        humanStore.proxy.conn.url = wsBaseUrl + 'update/human/'+escape(Ext.madasCurrentBioSourceId())+'/?sex_id='+escape(humanGender)+((humanDob === undefined || humanDob == '')?'':'&date_of_birth='+escape(humanDob))+((humanBmi === undefined || humanBmi == '')?'':'&bmi='+escape(humanBmi))+((humanDiagnosis === undefined || humanDiagnosis == '')?'':'&diagnosis='+escape(humanDiagnosis));
        humanStore.load();
    } else if (Ext.madasCurrentOrganismType() == '3') { //animal
        var animalGender = Ext.getCmp("animalGender").getValue();
        var animalAge = Ext.getCmp("animalAge").getValue();
        var animalParentalLine = Ext.getCmp("animalParentalLine").getRawValue();

        //hook up new load handler
        animalStore.on("load", Ext.madasBioSourceBlurSuccess);

        animalStore.proxy.conn.url = wsBaseUrl + 'update/human/'+escape(Ext.madasCurrentBioSourceId())+'/?sex_id='+escape(animalGender)+((animalAge === undefined || animalAge == '')?'':'&age='+escape(animalAge))+((animalParentalLine === undefined || animalParentalLine == '')?'':'&parental_line='+escape(animalParentalLine));
animalStore.load();
   } else {
        Ext.madasBioSourceBlurSuccess();
    }
}

Ext.madasBioSourceBlurSuccess = function() {
    experimentStore.un("load", Ext.madasBioSourceBlurSuccess);
    
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
    
    bundledData['name'] = rec.data.name;
    bundledData['tissue'] = rec.data.tissue;
    bundledData['cell_type'] = rec.data.cell_type;
    bundledData['subcellular_cell_type'] = rec.data.subcellular_cell_type;
    
    Ext.madasSaveRowLiterals('organ', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/source__experiment__id/' + expId; organStore.load();});
};

Ext.madasSaveGenotypeRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['name'] = rec.data.name;

    Ext.madasSaveRowLiterals('genotype', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); genotypeStore.proxy.conn.url = wsBaseUrl + 'records/genotype/source__experiment__id/' + expId; genotypeStore.load();});
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
                    { xtype:'fieldset', 
                    title:'animal info',
                    id:'organismBioSourceAnimalFieldset',
                    autoHeight:true,
                    //hidden:true,
                    items: [
                            
                        { xtype:'combo', 
                            fieldLabel:'gender',
                            id:'animalGender',
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
                            store: genderComboStore
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
                        store: genderComboStore
                        }, 
                        { xtype:'datefield', fieldLabel:'Date of birth', id:'human_dob', format:'d/m/Y'}, 
                        { xtype:'textfield', fieldLabel:'BMI', id:'human_bmi', maskRe:/^[0-9]*\.*[0-9]*$/ },
                        { xtype:'textfield', fieldLabel:'Diagnosis', id:'human_diagnosis' }
                        ]
                },
                { xtype:'editorgrid', 
                    id:'organs',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'organs',
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
                        text: 'add organ',
                        cls: 'x-btn-text-icon',
                        icon:'images/add.gif',
                        handler : function() {
                           Ext.madasCRUDSomething('create/organ/', {'source_id':Ext.madasCurrentBioSourceId()}, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/source__experiment__id/' + expId;
                                                  organStore.load(); });
                        }
                        }, 
                        {
                        text: 'remove organ',
                        cls: 'x-btn-text-icon',
                        icon:'images/no.gif',
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
                           Ext.madasCRUDSomething('delete/organ/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); organStore.proxy.conn.url = wsBaseUrl + 'records/organ/source__experiment__id/' + expId;
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
                        { header: "tissue", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                hiddenName:'tissue',
                                lazyRender:true,
                                allowBlank:true,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: tissueComboStore
                            }), dataIndex:'tissue'
                        },
                        { header: "cell type", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                hiddenName:'node',
                                lazyRender:true,
                                allowBlank:true,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: cellTypeComboStore
                            }),  dataIndex:"cell_type" },
                        { header: "subcellular cell type", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                editable:true,
                                forceSelection:false,
                                displayField:'value',
                                valueField:undefined,
                                hiddenName:'node',
                                lazyRender:true,
                                allowBlank:true,
                                typeAhead:false,
                                triggerAction:'all',
                                listWidth:230,
                                store: subcellularCellTypeComboStore
                            }), dataIndex:'subcellular_cell_type' }
                    ],
                    store: organStore
                },
                { xtype:'editorgrid', 
                    id:'genotypes',
                    border: true,
                    title:'genotypes',
                    trackMouseOver: false,
                    height:200,
                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveGenotypeRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    tbar: [{
                        text: 'add genotype',
                        cls: 'x-btn-text-icon',
                        icon:'images/add.gif',
                        handler : function(){
                           Ext.madasCRUDSomething('create/genotype/', {'source_id':Ext.madasCurrentBioSourceId()}, function() { var expId = Ext.madasCurrentExperimentId(); genotypeStore.proxy.conn.url = wsBaseUrl + 'records/genotype/source__experiment__id/' + expId;
                                                  genotypeStore.load(); });
                            }
                        },
                        {
                        text: 'remove genotype',
                        cls: 'x-btn-text-icon',
                        icon:'images/no.gif',
                        handler : function(){
                           var grid = Ext.getCmp('genotypes');
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
                           Ext.madasCRUDSomething('delete/genotype/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); genotypeStore.proxy.conn.url = wsBaseUrl + 'records/genotype/source__experiment__id/' + expId;
                                                  genotypeStore.load(); });
                           }
                        }
                        }
                    ],
                    columns: [
                        { header: "name", sortable:false, menuDisabled:true, 
                            editor:new Ext.form.ComboBox({
                                 editable:true,
                                 forceSelection:false,
                                 displayField:'value',
                                 valueField:undefined,
                                 hiddenName:'node',
                                 lazyRender:true,
                                 allowBlank:false,
                                 typeAhead:false,
                                 triggerAction:'all',
                                 listWidth:230,
                                 store: genotypeComboStore
                            }), 
                            dataIndex:'name'
                        }
                    ],
                    store: genotypeStore
                }
            ]
        }
    ]
};

