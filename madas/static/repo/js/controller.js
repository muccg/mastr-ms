Ext.madasExperimentInit = function() {
    if (Ext.madasDenyReInit) { return; }
        
    Ext.madasDenyReInit = true;
    var expId = Ext.madasCurrentExperimentId();

    //hide/show relevant fieldsets
    Ext.madasExperimentShowFieldsets();
    
    biologicalSourceStore.proxy.conn.url = wsBaseUrl + 'records/biologicalsource/experiment__id/' + expId;
    biologicalSourceStore.load();
    Ext.getCmp("expNav").getView().refresh();
    Ext.madasDenyReInit = false;
    
    Ext.madasUpdateNav();
};

Ext.madasBlur = function(invoker) {
    invoker.init();
    
    Ext.getCmp("expContent").getLayout().setActiveItem(invoker.index); 
    Ext.currentExperimentNavItem = invoker.index;
    
    Ext.madasExperimentDeferredInvocation = {'init':Ext.madasNull, 'index':-1};
};

Ext.madasNull = function() {};

Ext.madasCRUDSomething = function(remainderURL, params, callbackfn) {
    var paramString = '?';
    
    for (var index in params) {
        paramString += escape(index) + '=' + escape(params[index]) + '&';
    }
    
    //TODO append the parameters to the url 
    var crudStore = new Ext.data.JsonStore( 
                                             {
                                             autoLoad: false,
                                             url: wsBaseUrl + remainderURL + paramString,
                                             listeners: {
                                                'load':Ext.madasDSLoaded,
                                                'load':callbackfn,
                                                'loadexception':Ext.madasDSLoadException}
                                             }
                                             );
    crudStore.load();
};

Ext.madasExperimentBlur = function(invoker) {
    var expId = Ext.madasCurrentExperimentId();
    var expName = Ext.getCmp("experimentName").getValue();
    var expDescription = Ext.getCmp("experimentDescription").getValue();
    var expComment = Ext.getCmp("experimentComment").getValue();
    
    Ext.madasExperimentDeferredInvocation = invoker;

    if (expId == 0 && expName != "") {
        
        //unhook the default load handler
        experimentStore.un("load", Ext.madasExperimentReload);
        //hook up new load handler
        experimentStore.on("load", Ext.madasSyncBiologicalSource);
        
        experimentStore.proxy.conn.url = wsBaseUrl + 'create/experiment/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2';
        experimentStore.load();
    } else {
        //unhook the default load handler
        experimentStore.un("load", Ext.madasExperimentReload);
        //hook up new load handler
        experimentStore.on("load", Ext.madasSyncBiologicalSource);
        
        experimentStore.proxy.conn.url = wsBaseUrl + 'update/experiment/'+expId+'/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2';
        experimentStore.load();
    
        Ext.madasExperimentBlurSuccess();
    }
};

Ext.madasExperimentBlurSuccess = function() {
    experimentStore.un("load", Ext.madasExperimentBlurSuccess);
    
    var index = Ext.madasExperimentDeferredInvocation.index;

    if (index >= 0) {
        Ext.getCmp("expContent").getLayout().setActiveItem(index); 
        Ext.currentExperimentNavItem = index;
    }

    Ext.madasExperimentDeferredInvocation.init();
    
    Ext.madasExperimentDeferredInvocation = {'index':-1, 'init':Ext.madasNull};
};

Ext.madasSyncBiologicalSource = function() {
    var organismId = Ext.getCmp("speciesfield").getValue();
    var expId = Ext.madasCurrentExperimentId();
    var loadedBioSource = null;
    var organismType = Ext.getCmp("organismType").getValue();
    var table = 'biologicalsource';
    var additionalValues = '';
    //console.log("sync bio");
    
    if (biologicalSourceStore.getTotalCount() > 0) {
        loadedBioSource = biologicalSourceStore.getAt(0).get("id");
    }

    //plant 2
    if (Ext.getCmp("organismType").getValue() == "2") {
        table = "plant";
        additionalValues = '&development_stage='+escape(Ext.getCmp('development_stage').getValue());
    }
    
    //animal 3
    if (Ext.getCmp("organismType").getValue() == "3") {
        table = "animal";
        additionalValues = "&sex_id=1";
    }
    
    //human 4
    if (Ext.getCmp("organismType").getValue() == "4") {
        table = "human";
        additionalValues = "&sex_id=1";
    }

    biologicalSourceStore.on("load", Ext.madasExperimentBlurSuccess);
    biologicalSourceStore.on("load", function() {biologicalSourceStore.on("load", Ext.madasExperimentBlurSuccess);});
    
    if (loadedBioSource === null && organismId != '') {
        //save the species details

        biologicalSourceStore.proxy.conn.url = wsBaseUrl + 'create/' + table + '/?organism_id='+escape(organismId)+'&experiment_id='+escape(expId)+additionalValues;
        biologicalSourceStore.load();
    } else if (loadedBioSource !== null && organismId != '') {
        //save the species details
        
        biologicalSourceStore.proxy.conn.url = wsBaseUrl + 'update/' + table + '/'+loadedBioSource+'/?organism_id='+escape(organismId)+'&experiment_id='+escape(expId)+additionalValues;
        biologicalSourceStore.load();
    }
    
    //rehook original callback handler
    experimentStore.un("load", Ext.madasSyncBiologicalSource);
    experimentStore.on("load", Ext.madasExperimentReload);
};

Ext.madasExperimentShowFieldsets = function(organismType) {
    Ext.getCmp('organismFieldset').hide();
    Ext.getCmp('plantFieldset').hide();
    Ext.getCmp('rankfield').hide();
    Ext.getCmp('upperrankfield').setVisible(false);
    Ext.getCmp('ncbifield').setVisible(false);
    
    if (organismType === undefined) 
        return;
    
    if (organismType > 4) {  //4 here refers to food & beverage, or synthetic compound. everything else is an organism
        Ext.getCmp('rankfield').hide();
        Ext.getCmp('organismFieldset').setTitle('subtype');
        Ext.getCmp('upperrankfield').setVisible(false);
        Ext.getCmp('ncbifield').setVisible(false);
    } else {
        Ext.getCmp('organismFieldset').show();
        Ext.getCmp('rankfield').show();
        Ext.getCmp('upperrankfield').setVisible(true);
        Ext.getCmp('ncbifield').setVisible(true);
        
    }
    
    if (organismType != 2) {
        Ext.getCmp("plantFieldset").hide();
    } else {
        Ext.getCmp("plantFieldset").show();
    }
    
    Ext.getCmp('speciesfield').enable();
};

Ext.madasLoadOrganismInfo = function(typeId, id) {
    if (typeId == 2) {//plant
        plantStore.proxy.conn.url = wsBaseUrl + 'records/plant/id/' + id;
        plantStore.load();
    }
};

Ext.madasExperimentDetails = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'experiment details',
            region: 'center',
            collapsible: false,
            autoScroll:true,
            layout:'form',
            minSize: 75,
            items: [ 
                { xtype:'fieldset', 
                title:'experiment',
                autoHeight:true,
                items: [
                    { xtype:'textfield', fieldLabel:'experiment name', enableKeyEvents:true, id:'experimentName', allowBlank:false, listeners:{'keydown':function(t, e){ Ext.madasUpdateNav(); return true; }, 'keyup':function(t, e){ Ext.madasUpdateNav(); return true; }}},
                    { xtype:'textarea', fieldLabel:'description', id:'experimentDescription', width:400 },
                    { xtype:'textarea', fieldLabel:'comment', id:'experimentComment', width:400 }
                    ]
                },
                    { xtype:'fieldset',
                    title:'source type',
                    autoheight:true,
                    items: [
                            { xtype:'combo', 
                            fieldLabel:'type',
                            editable:false,
                            id:'organismType',
                            forceSelection:true,
                            displayField:'value',
                            valueField:'key',
                            hiddenName:'organismtype',
                            lazyRender:true,
                            allowBlank:false,
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:230,
                            store: organismTypeComboStore,
                            listeners:{'select':function(f, r, i) {
                            if (r === undefined || r.data.key === undefined) {
                            return;
                            }
                            
                            Ext.madasCurrentOrganismTypeValue = r.data.key;
                            
                            organismComboStore = new Ext.data.JsonStore(
                                                   {
                                                   storeId: 'organismCombo',
                                                   autoLoad: true,
                                                   url: wsBaseUrl + 'populate_select/organism/id/name/type/' + r.data.key,
                                                   root: 'response.value.items',
                                                   fields: ['value', 'key'],
                                                   listeners: {'load':Ext.madasDSLoaded,
                                                   'load':function(){
                                                   if (Ext.getCmp('speciesfield')) {
                                                   Ext.getCmp('speciesfield').setValue(Ext.getCmp('speciesfield').getValue());
                                                   }
                                                   },
                                                   'loadexception':Ext.madasDSLoadException}
                                                   }
                                                   );
                            
                            Ext.getCmp('speciesfield').bindStore(organismComboStore);
                            Ext.getCmp('speciesfield').clearValue();
                            Ext.getCmp('rankfield').setValue("");
                            Ext.getCmp('upperrankfield').setValue("");
                            Ext.getCmp('ncbifield').setValue("");
                            
                            Ext.madasExperimentShowFieldsets(r.data.key); 
                            }}
                            }
                        ]
                    },
                { xtype:'fieldset', 
                title:'specific info',
                id:'organismFieldset',
                autoHeight:true,
                //hidden:true,
                items: [
                    
                    { xtype:'combo', 
                        fieldLabel:'specific type',
                        id:'speciesfield',
                        editable:false,
                        disabled:true,
                        forceSelection:true,
                        displayField:'value',
                        valueField:'key',
                        hiddenName:'species',
                        lazyRender:true,
                        allowBlank:false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:230,
                        store: organismComboStore,
                        listeners:{'select':function(f, r, i) {
                            organismStore.proxy.conn.url = wsBaseUrl + "records/organism/id/" + r.data.key;
                            organismStore.load();

                            Ext.madasUpdateNav();

                        }}
                    },
                    { xtype:'textfield', 
                        fieldLabel:'rank',
                        id:'rankfield',
                        readOnly:true,
                        style:'background:transparent;'
                        },
                    { xtype:'textfield', 
                        fieldLabel:'upper rank',
                        id:'upperrankfield',
                        readOnly:true,
                        style:'background:transparent;'
                        },
                    { xtype:'textfield', 
                        fieldLabel:'NCBI ID',
                        id:'ncbifield',
                        readOnly:true,
                        style:'background:transparent;'
                        }
                    ]
                },
                    { xtype:'fieldset', 
                    title:'plant info',
                    id:'plantFieldset',
                    autoHeight:true,
                    //hidden:true,
                    items: [
                            
                            { xtype:'combo', 
                            fieldLabel:'development stage',
                            id:'development_stage',
                            editable:true,
                            forceSelection:false,
                            displayField:'value',
                            valueField:undefined,
                            lazyRender:true,
                            allowBlank:false,
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:230,
                            store: plantComboStore
                            }
                        ]
                    }
            ]
        }
    ]
};


Ext.madasExperimentCmp = { 
    id:'experimentTitle',
    title:'new experiment',
    layout:'border',
    defaults: {
        collapsible: true,
        split: true,
        bodyStyle: 'padding:15px'
    },
    items: [{
        region:'west',
        margins: '5 0 0 0',
        cmargins: '5 5 0 0',
        width: 175,
        minSize: 100,
        maxSize: 250,
        border: false,
        baseCls: 'x-plain',
        bodyStyle: 'padding:0px;padding-left:5px;',
        items: [
            {
                title: 'navigation',
                frame: true,
                style:'background:white;',
                items: [
                    {
                        id: 'expNav',
                    	baseCls:'x-plain',
                        xtype:'grid', 
                        border: false,
                        trackMouseOver: false,
                        hideHeaders:true,
                        syncFocus: false,
                        width:270,
                        autoHeight:true,
                        sm: new Ext.grid.RowSelectionModel(
                            {
                                singleSelect:true,
                                listeners:{
                                    "rowselect":function(sm, index, r) { 
                                        if (Ext.currentExperimentNavItem == index) {
                                           return;
                                        }
                                        
                                        var currItem = Ext.StoreMgr.get("navDS").getAt(Ext.currentExperimentNavItem);
                                        var blurFn = currItem.get("blur");
                                        if (blurFn !== null) {
                                            blurFn({'init':r.get("init"), 'index':index});
                                        }
                                    },
                                    "beforerowselect":function(sm, ri, ke, r) {
                                        if (!r.data.enabled) {
                                            return false;
                                        }
                                    }
                                }
                            } 
                        ),
                        viewConfig: {
                            forceFit: true,
                            autoFill:true,
                            scrollOffset:0
                        },
                        columns: [
                            { header: "nav",  sortable:false, menuDisabled:true, renderer: renderNavItem }
                        ],
                        store: new Ext.data.SimpleStore(
                            {
                                storeId:"navDS",
                                fields: ["nav", "init", "blur", "enabled"],
                                data: [ ["experiment details", Ext.madasExperimentInit, Ext.madasExperimentBlur, true], ["samples/classes", Ext.madasExperimentSamplesInit, Ext.madasBlur, false], ["source", Ext.madasBioSourceInit, Ext.madasBioSourceBlur, false], ["growth",Ext.madasGrowthInit, Ext.madasBlur,false], ["treatment",Ext.madasTreatmentInit, Ext.madasBlur,false], ["sample prep",Ext.madasSamplePrepInit, Ext.madasBlur,false], ["files", Ext.madasFilesInit, Ext.madasBlur, false], ["access",Ext.madasAccessInit, Ext.madasBlur,false] ],
                            }
                        ),
                        listeners:{"render":function(a){window.setTimeout("Ext.getCmp('expNav').getSelectionModel().selectFirstRow();", 500);}}
                      }
                ]
            }
        ]
    },{
        id: 'expContent',
        collapsible: false,
        region:'center',
        border: false,
        margins: '5 0 0 0',
        layout:'card',
        activeItem:0,
        bodyStyle:'padding:0px;',
        items:[
            Ext.madasExperimentDetails,
            Ext.madasExperimentSamples,
            Ext.madasBioSource,
            Ext.madasGrowth,
            Ext.madasTreatment,
            Ext.madasSamplePrep,
            Ext.madasFiles,
            Ext.madasAccess
        ]
    }]
};

Ext.madasLoadExperiment = function(expId) {
    Ext.getCmp('speciesfield').disable();

    experimentStore.proxy.conn.url = wsBaseUrl + "records/experiment/id/" + expId;
    experimentStore.load();
    
    Ext.madasMenuHandler({ id:'experiment:view' });
};

/**
 * madasInitApplication
 * initializes the main application interface and any required variables
 */
Ext.madasInitApplication = function() {
    //various global settings for Ext
    Ext.BLANK_IMAGE_URL = 'static/repo/ext-3.0.0/resources/images/default/s.gif';
    Ext.QuickTips.init();
    
    // turn on validation errors beside the field globally
    Ext.form.Field.prototype.msgTarget = 'side';
    
    var username = "";
    Ext.madasMenuRender(username);

    Ext.madasInitUI();
    
    Ext.madasAuthorize('experiment:my', []);
};

Ext.madasInitUI = function() {
   //the ViewPort defines the main layout for the entire Madas app
   //the center-panel component is the main area where content is switched in and out
   if (Ext.getCmp('viewport')) {
       return;
   }
    
    Ext.currentExperimentNavItem = 0;
   
   var viewport = new Ext.Viewport({
        layout:'border',
        id:'viewport',
        items:[
            new Ext.BoxComponent({
                region:'north',
                el: 'north',
                height:54
            }),
            {
                region:'center',
                id:'center-panel',
                layout: 'card',
                activeItem:2,
                items: [Ext.madasExperimentCmp, Ext.madasExperimentListCmp, Ext.madasLoginCmp]
            },
               new Ext.BoxComponent({
                                    region:'south',
                                    el: 'south',
                                    height:24
                                    })
            ]
    });
    
};

Ext.madasUpdateNav = function() {
    var en = Ext.getCmp("experimentName");
    var ot = Ext.getCmp("speciesfield");
    var ds = Ext.StoreMgr.get("navDS");
    var et = Ext.getCmp("experimentTitle");
    var counter = 1;
    //console.log(ot.isValid() + " " + ot.getValue());
    var valid = ot.isValid();
    if (valid) {
        valid = (ot.getValue() == "")?false:true;
    }
        
    for (counter = 1; counter <= 7; counter++) {
        ds.getAt(counter).set("enabled", (en.getValue() != '' && valid));
    }
    
    if (en.getValue() == '') {
        et.setTitle('new experiment');
    } else {
        et.setTitle('experiment: '+en.getValue());
    }
    
    Ext.getCmp("expNav").getView().refresh();
//    en.focus();
};