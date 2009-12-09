Ext.madasExperimentInit = function() {
    Ext.madasLoadExperiment(Ext.madasCurrentExperimentId());
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
                                           method:'GET',
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
    var expFQuoteId = Ext.getCmp("formalQuote").getValue();
    if (expFQuoteId === null) {
        expFQuoteId = '';
    }
    var expJobNumber = Ext.getCmp("jobNumber").getValue();
    if (expJobNumber === null) {
        expJobNumber = '';
    }
    
    Ext.madasExperimentDeferredInvocation = invoker;

    if (expId === 0) {
        
        var saver = new Ajax.Request(wsBaseUrl + 'create/experiment/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber), 
                                             { 
                                             asynchronous:true, 
                                             evalJSON:'force',
                                     onSuccess:     Ext.madasExperimentBlurSuccess
                                     });
    } else {
        var saver = new Ajax.Request(wsBaseUrl + 'update/experiment/'+expId+'/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber), 
                                     { 
                                     asynchronous:true, 
                                     evalJSON:'force',
                                     onSuccess:     Ext.madasExperimentBlurSuccess
                                     });
    }
};

Ext.madasExperimentBlurSuccess = function(response) {
    if (Ext.isDefined(response)) {
        Ext.madasCurrentExpId = response.responseJSON.rows[0].id;
    }
    
    var index = Ext.madasExperimentDeferredInvocation.index;

    if (index >= 0) {
        Ext.getCmp("expContent").getLayout().setActiveItem(index); 
        Ext.currentExperimentNavItem = index;
    }

    Ext.madasExperimentDeferredInvocation.init();
    
    Ext.madasExperimentDeferredInvocation = {'index':-1, 'init':Ext.madasNull};
};

Ext.madasExperimentShowFieldsets = function(organismType) {
    Ext.getCmp('organismFieldset').hide();
    Ext.getCmp('plantFieldset').hide();
    Ext.getCmp('rankfield').hide();
    Ext.getCmp('upperrankfield').setVisible(false);
    Ext.getCmp('ncbifield').setVisible(false);
    
    if (organismType === undefined) {
        return;
    }
    
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
                    { xtype:'textarea', fieldLabel:'comment', id:'experimentComment', width:400 },
                        new Ext.form.ComboBox({
                                              width:300,
                                              fieldLabel:'formal quote',
                                              id:'formalQuote', 
                                              editable:true,
                                              forceSelection:true,
                                              displayField:'value',
                                              valueField:'key',
                                              hiddenName:'formalQuoteValue',
                                              lazyRender:true,
                                              allowBlank:true,
                                              typeAhead:false,
                                              triggerAction:'all',
                                              listWidth:300,
                                              mode:'local',
                                              store: new Ext.data.ArrayStore({fields: ['key', 'value']})
                                              }),
                        { xtype:'displayfield', fieldLabel:'organisation', id:'expOrg', disabled:true},
                        { xtype:'textfield', fieldLabel:'job number', id:'jobNumber' }
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
                                data: [ ["experiment details", Ext.madasExperimentInit, Ext.madasExperimentBlur, true], ["source", Ext.madasBioSourceInit, Ext.madasBioSourceBlur, false], ["treatment",Ext.madasTreatmentInit, Ext.madasBlur,false], ["sample prep",Ext.madasSamplePrepInit, Ext.madasBlur,false], ["sample classes", Ext.madasExperimentSamplesInit, Ext.madasBlur, false], ["samples", Ext.madasExperimentSamplesOnlyInit, Ext.madasBlur, false], ["files", Ext.madasFilesInit, Ext.madasBlur, false], ["access",Ext.madasAccessInit, Ext.madasBlur,false] ]
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
            Ext.madasBioSource,
            Ext.madasTreatment,
            Ext.madasSamplePrep,
            Ext.madasExperimentSamples,
            Ext.madasExperimentSamplesOnly,
            Ext.madasFiles,
            Ext.madasAccess
        ]
    }]
};

Ext.madasLoadExperiment = function(expId) {
    //if (expId == Ext.madasCurrentExpId) {
//        return;
//    }
    
    var fquoLoader = new Ajax.Request(wsBaseUrl + 'populate_select/formalquote/id/toemail/', 
                                     { 
                                     asynchronous:true, 
                                     evalJSON:'force',
                                     onSuccess: function(response) {
                                         var fquoCombo = Ext.getCmp('formalQuote');
                                         var data = response.responseJSON.response.value.items;
                                         var massagedData = [];

                                         for (var idx in data) {
                                             massagedData[idx] = [data[idx]['key'], data[idx]['value']];
                                         }
                                         
                                         fquoCombo.getStore().loadData(massagedData);
                                         
                                         fquoCombo.setValue(fquoCombo.getValue());
                                         }
                                     }
                                     );
    
    var expLoader = new Ajax.Request(wsBaseUrl + "records/experiment/id/" + expId, 
                                     { 
                                     asynchronous:true, 
                                     evalJSON:'force',
                                     onSuccess: function(response) {
                                             var namefield = Ext.getCmp('experimentName');
                                             var desc = Ext.getCmp('experimentDescription');
                                             var comment = Ext.getCmp('experimentComment');
                                             var formalQuote = Ext.getCmp('formalQuote');
                                             var jobNumber = Ext.getCmp('jobNumber');
                                             
                                             if (!namefield || !desc || !comment || !formalQuote || !jobNumber) {
                                                 return;
                                             }
                                             
                                             namefield.setValue('');
                                             desc.setValue('');
                                             comment.setValue('');
                                             formalQuote.setValue('');
                                             jobNumber.setValue('');
                                     
                                             var rs = response.responseJSON.rows;
                                             
                                             if (rs.length > 0) {
                                                 namefield.setValue(rs[0].title);
                                                 desc.setValue(rs[0].description);
                                                 comment.setValue(rs[0].comment);
                                                 formalQuote.setValue(rs[0].formal_quote);
                                                 jobNumber.setValue(rs[0].job_number);
                                             }
                                     
                                             Ext.madasUpdateNav();

                                         }
                                     }
                                     );
    
    Ext.madasCurrentExpId = expId;
    
    Ext.madasMenuHandler({ id:'experiment:view' });
    
    Ext.getCmp('expContent').getLayout().setActiveItem(0);

    
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
    var ds = Ext.StoreMgr.get("navDS");
    var et = Ext.getCmp("experimentTitle");
    var counter = 1;
        
    for (counter = 1; counter <= 7; counter++) {
        ds.getAt(counter).set("enabled", (en.getValue() !== ''));
    }
    
    if (en.getValue() === '') {
        et.setTitle('new experiment');
    } else {
        et.setTitle('experiment: '+en.getValue());
    }
    
    Ext.getCmp("expNav").getView().refresh();
};