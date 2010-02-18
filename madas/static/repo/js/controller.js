MA.ExperimentInit = function() {
    MA.LoadExperiment(MA.CurrentExperimentId());
};

MA.Blur = function(invoker) {
    invoker.init();
    
    Ext.getCmp("expContent").getLayout().setActiveItem(invoker.index); 
    Ext.currentExperimentNavItem = invoker.index;
    
    MA.ExperimentDeferredInvocation = {'init':MA.Null, 'index':-1};
};

MA.Null = function() {};

MA.CRUDSomething = function(remainderURL, params, callbackfn) {
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
                                                'load':MA.DSLoaded,
                                                'load':callbackfn,
                                                'loadexception':MA.DSLoadException}
                                             }
                                             );
    crudStore.load();
};

MA.ExperimentBlur = function(invoker) {
    var expId = MA.CurrentExperimentId();
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
    
    MA.ExperimentDeferredInvocation = invoker;

    if (expId === 0) {
        
        var saver = new Ajax.Request(wsBaseUrl + 'create/experiment/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber), 
                                             { 
                                             asynchronous:true, 
                                             evalJSON:'force',
                                     onSuccess:     MA.ExperimentBlurSuccess
                                     });
    } else {
        var saver = new Ajax.Request(wsBaseUrl + 'update/experiment/'+expId+'/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber), 
                                     { 
                                     asynchronous:true, 
                                     evalJSON:'force',
                                     onSuccess:     MA.ExperimentBlurSuccess
                                     });
    }
};

MA.ExperimentBlurSuccess = function(response) {
    if (Ext.isDefined(response)) {
        MA.CurrentExpId = response.responseJSON.rows[0].id;
    }
    
    var index = MA.ExperimentDeferredInvocation.index;

    if (index >= 0) {
        Ext.getCmp("expContent").getLayout().setActiveItem(index); 
        Ext.currentExperimentNavItem = index;
    }

    MA.ExperimentDeferredInvocation.init();
    
    MA.ExperimentDeferredInvocation = {'index':-1, 'init':MA.Null};
};

MA.ExperimentShowFieldsets = function(organismType) {
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

MA.LoadOrganismInfo = function(typeId, id) {
    if (typeId == 2) {//plant
        plantStore.proxy.conn.url = wsBaseUrl + 'records/plant/id/' + id;
        plantStore.load();
    }
};

MA.ExperimentDetails = {
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
                    { xtype:'textfield', fieldLabel:'experiment name', enableKeyEvents:true, id:'experimentName', allowBlank:false, listeners:{'keydown':function(t, e){ MA.UpdateNav(); return true; }, 'keyup':function(t, e){ MA.UpdateNav(); return true; }}},
                    { xtype:'textarea', fieldLabel:'description', id:'experimentDescription', width:700, height:100 },
                    { xtype:'textarea', fieldLabel:'comment', id:'experimentComment', width:700, height:100 },
                        new Ext.form.ComboBox({
                                              width:300,
                                              fieldLabel:'formal quote',
                                              id:'formalQuote', 
                                              editable:false,
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


MA.ExperimentCmp = { 
    id:'experimentTitle',
    title:'new experiment',
    layout:'border',
    defaults: {
        collapsible: false,
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
                                data: [ ["experiment details", MA.ExperimentInit, MA.ExperimentBlur, true], ["source", MA.BioSourceInit, MA.BioSourceBlur, false], ["treatment",MA.TreatmentInit, MA.Blur,false], ["sample prep",MA.SamplePrepInit, MA.Blur,false], ["sample classes", MA.ExperimentSamplesInit, MA.Blur, false], ["samples", MA.ExperimentSamplesOnlyInit, MA.Blur, false], ["sample tracking", MA.ExperimentSamplesOnlyInit, MA.Blur, false], ["files", MA.FilesInit, MA.Blur, false], ["access",MA.AccessInit, MA.Blur,false] ]
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
            MA.ExperimentDetails,
            MA.BioSource,
            MA.Treatment,
            MA.SamplePrep,
            MA.ExperimentSamples,
            MA.ExperimentSamplesOnly,
            MA.SampleTracking,
            MA.Files,
            MA.Access
        ]
    }]
};

MA.LoadExperiment = function(expId) {
    //if (expId == MA.CurrentExpId) {
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
                                            massagedData[idx] = [data[idx]['key'], '#'+data[idx]['key']+'  '+data[idx]['value']];
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

                                             //update the fields on the ssample tracking page
                                             var tnamefield = Ext.getCmp('trackingExperimentName');
                                             var tcomment = Ext.getCmp('trackingExperimentComment');
                                             var tformalQuote = Ext.getCmp('trackingFormalQuote');
                                             var tjobNumber = Ext.getCmp('trackingJobNumber');
                                             
                                             if (!namefield || !desc || !comment || !formalQuote || !jobNumber) {
                                                 return;
                                             }
                                             
                                             namefield.setValue('');
                                             desc.setValue('');
                                             comment.setValue('');
                                             formalQuote.setValue('');
                                             jobNumber.setValue('');
                                                
                                             //tracking fields
                                             tnamefield.setValue('');
                                             tcomment.setValue('');
                                             tformalQuote.setValue('');
                                             tjobNumber.setValue('');

                                             var rs = response.responseJSON.rows;
                                             
                                             if (rs.length > 0) {
                                                 namefield.setValue(rs[0].title);
                                                 desc.setValue(rs[0].description);
                                                 comment.setValue(rs[0].comment);
                                                 formalQuote.setValue(rs[0].formal_quote);
                                                 jobNumber.setValue(rs[0].job_number);
                                                 
                                                 //tracking fields
                                                 tnamefield.setValue(rs[0].title);
                                                 tcomment.setValue(rs[0].comment);
                                                 tformalQuote.setValue(rs[0].formal_quote);
                                                 tjobNumber.setValue(rs[0].job_number);
                                             }
                                     
                                             MA.UpdateNav();

                                         }
                                     }
                                     );
    
    MA.CurrentExpId = expId;
    
    MA.MenuHandler({ id:'experiment:view' });
    
    //Ext.getCmp('expContent').getLayout().setActiveItem(0);

    
};

/**
 * madasInitApplication
 * initializes the main application interface and any required variables
 */
MA.InitApplication = function() {
    //various global settings for Ext
    Ext.BLANK_IMAGE_URL = 'static/ext-3.1.0/resources/images/default/s.gif';
    Ext.QuickTips.init();
    
    // turn on validation errors beside the field globally
    Ext.form.Field.prototype.msgTarget = 'side';
    
    var username = "";
    MA.MenuRender(username);

    MA.InitUI();
    
    MA.Authorize('experiment:my', []);
};

MA.InitUI = function() {
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
                items: [MA.ExperimentCmp, MA.ExperimentListCmp, MA.LoginCmp]
            },
               new Ext.BoxComponent({
                                    region:'south',
                                    el: 'south',
                                    height:24
                                    })
            ]
    });
    
};

MA.UpdateNav = function() {
    var en = Ext.getCmp("experimentName");
    var ds = Ext.StoreMgr.get("navDS");
    var et = Ext.getCmp("experimentTitle");
    var counter = 1;
        
    for (counter = 1; counter <= 8; counter++) {
        ds.getAt(counter).set("enabled", (en.getValue() !== ''));
    }
    
    if (MA.CurrentExperimentId() == 0) {
        et.setTitle('new experiment');
    } else {
        et.setTitle('experiment: '+en.getValue());
    }
    
    Ext.getCmp("expNav").getView().refresh();
};