MA.Blur = function(invoker) {
    MA.ExperimentController.mask.show();

    if (invoker.index === -1) {
        Ext.getCmp("expContent").getLayout().setActiveItem(0);
    }

    invoker.init.call();
    Ext.getCmp("expContent").getLayout().setActiveItem(invoker.index); 
    Ext.currentExperimentNavItem = invoker.index;
    
    MA.ExperimentDeferredInvocation = {'init':MA.Null, 'index':-1};
    
    (function () {
        MA.ExperimentController.mask.hide();
    }).defer(500);
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
                                                'load':callbackfn,
                                                'exception':MA.DSLoadException}
                                             }
                                             );
    crudStore.load();
};

function _ExperimentController() {
    var self = this;

    this.init = function() {
        self.loadExperiment(self.currentId());
    };
    
    this.currentId = function() {
        if (!self._currentExpId) {
            return 0;
        }
        
        return self._currentExpId;
    };
    
    this.setCurrentId = function(newID) {
        self._currentExpId = newID;
    };
    
    this.blur = function(invoker) {
        var expId = self.currentId();
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
        
        if (!Ext.isDefined(expName) ||
            expName === "") {
            //seriously, this should never happen
            self.blurSuccess();
            return;
        }
        
        MA.ExperimentDeferredInvocation = invoker;
    
        if (expId === 0) {
            
            var saver = new Ajax.Request(wsBaseUrl + 'create/experiment/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber)+'&project_id='+escape(MA.currentProjectId), 
                                                 { 
                                                 asynchronous:true, 
                                                 evalJSON:'force',
                                         onSuccess:     self.blurSuccess,
                                         onFailure:    MA.DSLoadException
                                         });
        } else {
            var saver = new Ajax.Request(wsBaseUrl + 'update/experiment/'+expId+'/?title='+escape(expName)+'&description='+escape(expDescription)+'&comment='+escape(expComment)+'&status_id=2&formal_quote_id='+escape(expFQuoteId)+'&job_number='+escape(expJobNumber)+'&project_id='+escape(MA.currentProjectId), 
                                         { 
                                         asynchronous:true, 
                                         evalJSON:'force',
                                         onSuccess:     self.blurSuccess,
                                          onFailure:    MA.DSLoadException
                                         });
        }
        
        self.mask.show();
    };

    this.blurSuccess = function(response) {
        self.mask.hide();
    
        if (Ext.isDefined(response)) {
            if (!Ext.isDefined(response.responseJSON)) {
                Ext.Msg.alert('Error', 'An unexpected error has occurred. Your session may have timed out. Please reload your browser window.');
                return;
            }
            
            self.setCurrentId(response.responseJSON.rows[0].id);
        }
        
        var index = MA.ExperimentDeferredInvocation.index;
    
        if (index >= 0) {
            Ext.getCmp("expContent").getLayout().setActiveItem(index); 
            Ext.currentExperimentNavItem = index;
        }
    
        MA.ExperimentDeferredInvocation.init();
        
        MA.ExperimentDeferredInvocation = {'index':-1, 'init':MA.Null};
    };

    this.showFieldsets = function(organismType) {
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
            Ext.getCmp('organismFieldset').setTitle('Subtype');
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
    
    this.loadExperiment = function(expId) {
        
        var fquoLoader = new Ajax.Request(wsBaseUrl + 'populate_select/formalquote/id/toemail/', 
                                         { 
                                         asynchronous:true, 
                                         evalJSON:'force',
                                         onSuccess: function(response) {
                                             var fquoCombo = Ext.getCmp('formalQuote');
                                             var data = response.responseJSON.response.value.items;
                                             var massagedData = [];
                                             
                                             for (var idx = 0; idx < data.length; idx++) {
                                                massagedData[idx] = [data[idx]['key'], '#'+data[idx]['key']+'  '+data[idx]['value']];
                                             }
    
                                             //ensure that there is a blank entry
                                             massagedData.unshift(['','  none  ']);
                                             
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
    
                                                 //update the fields on the sample tracking page
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
                                                 formalQuote.clearValue();
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
                                         
                                                 self.updateNav();
    
                                             }
                                         }
                                         );
    
        var changingExperiment = (self.currentId() != expId);
        self.setCurrentId(expId);
        
        MA.MenuHandler({ id:'experiment:view' });
    
        // Eh, we'll check for IE 6 as well just in case.
        if ((Ext.isIE6 || Ext.isIE7) && changingExperiment) {
            /* This works around an apparent DOM manipulation timing bug in IE 7
             * where the multitude of calls required to deselect a pane in the
             * navigation and select the experiment details pane manages to confuse
             * it, as ExtJS will continue to make calls to manipulate elements that
             * are hidden, and things break. */
            
            self.mask.show();
    
            (function () {
                Ext.getCmp('expNav').select(0);
                self.mask.hide();
            }).defer(500);
        }
        else {
            Ext.getCmp('expContent').getLayout().setActiveItem(0);
        }
        
        Ext.getCmp('center-panel').layout.setActiveItem('experimentTitle');
    };
    
    this.updateNav = function(index) {
        var en = Ext.getCmp("experimentName");
        var ds = Ext.StoreMgr.get("navDS");
        var et = Ext.getCmp("experimentTitle");
        var na = Ext.getCmp("expNav");
        
        if (na.getSelectionCount() == 0 || index != null) {
            na.select(index,index,false);
        }
        
        var counter = 1;
        if (en.getValue() === '') {
            na.disable();
        } else {
            na.enable();
        }
                
        if (self.currentId() == 0) {
            et.setTitle('New Experiment');
        } else {
            et.setTitle('Experiment: '+en.getValue());
        }
    };
    
    this.createExperiment = function() {
        self.setCurrentId(0);
        var namefield = Ext.getCmp('experimentName');
        var desc = Ext.getCmp('experimentDescription');
        var comment = Ext.getCmp('experimentComment');
        var formalQuote = Ext.getCmp('formalQuote');
        var jobNumber = Ext.getCmp('jobNumber');
        var et = Ext.getCmp("experimentTitle");
        et.setTitle('New Experiment');
        
        namefield.setValue('');

        self.updateNav(0);       

        desc.setValue('');
        comment.setValue('');
        formalQuote.clearValue();
        jobNumber.setValue('');

        Ext.getCmp('center-panel').layout.setActiveItem('experimentTitle');
//        Ext.getCmp('expNav').getSelectionModel().selectFirstRow();
    };
    
    this.selectionChangeHandler = function(list, nodes) {
        if (list.getSelectionCount() == 0) {
            return;
        }
     
        var index = list.getSelectedIndexes()[0];
        var r = list.getSelectedRecords()[0];
    
        if (Ext.currentExperimentNavItem == index) {
           return;
        }
        
        var currItem = Ext.StoreMgr.get("navDS").getAt(Ext.currentExperimentNavItem);
        var blurFn = currItem.get("blur");
        if (blurFn !== null) {
            blurFn({'init':r.get("init"), 'index':index});
        }
    };    
};

MA.ExperimentController = new _ExperimentController();

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
            title: 'Experiment Details',
            region: 'center',
            collapsible: false,
            autoScroll:true,
            layout:'form',
            minSize: 75,
            items: [ 
                { xtype:'fieldset', 
                title:'Experiment',
                autoHeight:true,
                items: [
                    { xtype:'textfield', fieldLabel:'Experiment name', width:700, enableKeyEvents:true, id:'experimentName', allowBlank:false, listeners:{'keydown':function(t, e){ MA.ExperimentController.updateNav(); return true; }, 'keyup':function(t, e){ MA.ExperimentController.updateNav(); return true; }}},
                    { xtype:'textarea', fieldLabel:'Experiment overview/aim', id:'experimentDescription', width:700, height:100 },
                    { xtype:'textarea', fieldLabel:'Comment', id:'experimentComment', width:700, height:100 },
                        new Ext.form.ComboBox({
                                              width:300,
                                              fieldLabel:'Formal quote',
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
                        { xtype:'displayfield', fieldLabel:'Organisation', id:'expOrg', disabled:true},
                        { xtype:'textfield', fieldLabel:'Job number', id:'jobNumber' }
                    ]
                }
            ]
        }
    ]
};


MA.ExperimentCmp = { 
    id:'experimentTitle',
    title:'New Experiment',
    layout:'border',
    defaults: {
        collapsible: false,
        split: true,
        bodyStyle: 'padding:15px'
    },
    tools: [
        {
            id:'left',
            qtip: "Back to the project",
            handler: function() {
                MA.LoadProject(MA.currentProjectId);
            }
        }
    ],
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
        layout:'anchor',
        hideMode:'offsets',
        items: [
            {
                title: 'Navigation',
                frame: true,
                style:'background:white;',
                layout:'anchor',
                hideMode:'offsets',
                items: [
                    {
                        id: 'expNav',
                        baseCls: 'x-plain',
                        hideMode:'offsets',
                    	style:'background:white;',
                    	selectedClass:'ma-list-selected',
                        xtype:'listview', 
//                        border: false,
//                        trackMouseOver: false,
                        hideHeaders:true,
//                        syncFocus: false,
                        width:270,
//                        autoHeight:true,
                        singleSelect:true,
                        multiSelect:false,
                        listeners:{
                            "selectionchange": MA.ExperimentController.selectionChangeHandler,
                            "beforeselect":function(list, nodes, sel) {
                                return !list.disabled;
                            }
                        },
                        columns: [
                            { header: "Nav",  dataIndex:'nav', sortable:false, menuDisabled:true }
                        ],
                        store: new Ext.data.SimpleStore(
                            {
                                storeId:"navDS",
                                fields: ["nav", "init", "blur", "enabled"],
                                data: [ 
                                    [ "Experiment Details", MA.ExperimentController.init, MA.ExperimentController.blur, true ],
                                    [ "Source", MA.BioSourceInit, MA.BioSourceBlur, false ],
                                    [ "Treatment", MA.TreatmentInit, MA.Blur, false ],
                                    [ "Sample Preparation", MA.SamplePrepInit, MA.Blur, false ],
                                    [ "Sample Classes", MA.ExperimentSamplesInit, MA.Blur, false ],
                                    [ "Samples", MA.ExperimentSamplesOnlyInit, MA.Blur, false ],
                                    [ "Sample Tracking", MA.SampleTrackingInit, MA.Blur, false ],
                                    [ "Files", MA.FilesInit, MA.Blur, false ],
                                    [ "Access", MA.AccessInit, MA.Blur, false ]
                                ]
                            }
                          )  
                      }
                ]
            },
            {
            title: 'Current Run',
            frame: true,
            style:'background:white;margin-top:20px;',
            items: [
                {
                    xtype:'panel',
                    bodyStyle:'padding:4px;',
                    id:'runPanel',
                    items:[
                        {
                            xtype:'panel',
                            html:'Selected samples will be added to:'
                        },
                        {
                            xtype:'panel',
                            html:'New Untitled Run',
                            id:'currentRunTitle',
                            style:'font-weight:bold;padding:6px;'
                        },
                        {
                            xtype:'button',
                            text:'View',
                            handler:function(){MA.RunCmp.show();},
                            style: "margin-left: auto; margin-right: auto"
                        }
                    ]
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
        forceLayout:true,
        deferredRender:true,
        defaults: {
            forceLayout:true,
            deferredRender:true
        },
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


/**
 * madasInitApplication
 * initializes the main application interface and any required variables
 */
MA.InitApplication = function() {
    //various global settings for Ext
    Ext.BLANK_IMAGE_URL = 'static/ext-3.2.1/resources/images/default/s.gif';
    Ext.QuickTips.init();
    
    // turn on validation errors beside the field globally
    Ext.form.Field.prototype.msgTarget = 'side';
    
    var username = "";
    MA.MenuRender(username);

    MA.InitUI();
 
    // the loginOverlay must be removed or else the rest of the UI fails to render   
    MA.Authorize('dashboard:list', [], function () { Ext.get("loginOverlay").remove(); } );
};

MA.InitUI = function() {
   //the ViewPort defines the main layout for the entire Madas app
//   the center-panel component is the main area where content is switched in and out
//   if (Ext.getCmp('viewport')) {
//       return;
//   }
    
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
                layoutOnCardChange:true,
                activeItem:2,
                items: [MA.ExperimentCmp, MA.ExperimentListCmp, MA.LoginCmp, MA.ClientsListCmp, MA.ProjectListCmp, MA.ProjectCmp, MA.RunListCmp, MA.DashboardCmp]
            },
               new Ext.BoxComponent({
                                    region:'south',
                                    el: 'south',
                                    height:24
                                    })
            ]
    });

    Ext.get("copyright").addListener("click", function () {
        Ext.Msg.show({
            title: "Copyright Information",
            msg: document.getElementById("copyright-information").innerHTML,
            icon: Ext.Msg.INFO,
            buttons: Ext.Msg.OK,
            minWidth: 400
        });

        return false;
    });
    
    MA.ExperimentController.mask = new Ext.LoadMask("center-panel", {
        removeMask: true
    });
};


