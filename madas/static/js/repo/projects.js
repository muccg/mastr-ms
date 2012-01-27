
// These were defined in controller.js in repo

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
        paramString += encodeURIComponent(index) + '=' + encodeURIComponent(params[index]) + '&';
    }
    
    //TODO append the parameters to the url 
    var crudStore = new Ext.data.JsonStore( 
                                             {
                                             autoLoad: false,
                                             method:'GET',
                                             url: wsBaseUrl + remainderURL + paramString,
                                             listeners: {
                                                'load':callbackfn
                                             }
                                             });
    crudStore.load();
};



function ExperimentController() {
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

        var saver;
        var expId = self.currentId();
        var expName = Ext.getCmp("experimentName").getValue();
        var expDescription = Ext.getCmp("experimentDescription").getValue();
        var expComment = Ext.getCmp("experimentComment").getValue();
        var expFQuoteId = Ext.getCmp("formalQuote").getValue();
        if (expFQuoteId === null) {
            expFQuoteId = '';
        }
        var expStatus = Ext.getCmp('expFieldset').getComponent('status').getValue();
        if (expStatus === null) {
            expStatus = '';
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
            
            saver = new Ajax.Request(wsBaseUrl + 'create/experiment/?title='+encodeURIComponent(expName)+'&description='+encodeURIComponent(expDescription)+'&comment='+encodeURIComponent(expComment)+'&status_id=2&formal_quote_id='+encodeURIComponent(expFQuoteId)+'&job_number='+encodeURIComponent(expJobNumber)+'&project_id='+encodeURIComponent(MA.currentProjectId)+'&status_id='+encodeURIComponent(expStatus), 
                                                 { 
                                                 asynchronous:true, 
                                                 evalJSON:'force',
                                         onSuccess:     self.blurSuccess,
                                         onFailure:    MA.DSLoadException
                                         });
        } else {
            saver = new Ajax.Request(wsBaseUrl + 'update/experiment/'+expId+'/?title='+encodeURIComponent(expName)+'&description='+encodeURIComponent(expDescription)+'&comment='+encodeURIComponent(expComment)+'&status_id=2&formal_quote_id='+encodeURIComponent(expFQuoteId)+'&job_number='+encodeURIComponent(expJobNumber)+'&project_id='+encodeURIComponent(MA.currentProjectId)+'&status_id='+encodeURIComponent(expStatus), 
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

    this.updateSamplePreparationNotes = function(notes) {
        var expId = self.currentId();
        if (expId === 0) {
            return;
        }
        Ext.Ajax.request({
            url: wsBaseUrl + 'update/experiment/' + expId,
            params: {'sample_preparation_notes': notes },
            success: function(resp, opts) {
                self.mask.hide();
            },
            failure: function(resp, opts) {
                self.mask.hide();
                Ext.Msg.alert('Unexpected Error!', 'Unexpected error while trying to save Sample Preparation Notes');
            }
        });
        self.mask.show();

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
                                                massagedData[idx] = [data[idx].key, '#'+data[idx].key + '  ' + data[idx].value];
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

                                                 // and the ones on sample preparation page
                                                 var spnotes = Ext.getCmp('samplePreparationNotes');

                                                 
                                                 if (!namefield || !desc || !comment || !formalQuote || !jobNumber) {
                                                     return;
                                                 }
                                                 
                                                 namefield.setValue('');
                                                 desc.setValue('');
                                                 comment.setValue('');
                                                 formalQuote.clearValue();
                                                 jobNumber.setValue('');
                                                 Ext.getCmp('expFieldset').getComponent('status').setValue('');
                                                    
                                                 //tracking fields
                                                 tnamefield.setValue('');
                                                 tcomment.setValue('');
                                                 tformalQuote.setValue('');
                                                 tjobNumber.setValue('');

                                                 spnotes.setValue('');
    
                                                 var rs = response.responseJSON.rows;
                                                 
                                                 if (rs.length > 0) {
                                                     namefield.setValue(rs[0].title);
                                                     desc.setValue(rs[0].description);
                                                     comment.setValue(rs[0].comment);
                                                     formalQuote.setValue(rs[0].formal_quote);
                                                     jobNumber.setValue(rs[0].job_number);
                                                     
                                                     Ext.getCmp('expFieldset').getComponent('status').setValue(rs[0].status);
                                                     
                                                     //tracking fields
                                                     tnamefield.setValue(rs[0].title);
                                                     tcomment.setValue(rs[0].comment);
                                                     tformalQuote.setValue(rs[0].formal_quote);
                                                     tjobNumber.setValue(rs[0].job_number);

                                                     spnotes.setValue(rs[0].sample_preparation_notes);
                                                     //Set the project id so that the 'back to project' button works.
                                                     MA.currentProjectId = rs[0].project;
                                                 }
                                         
                                                 self.updateNav();
    
                                             }
                                         }
                                         );
    
        var changingExperiment = (self.currentId() != expId);
        self.setCurrentId(expId);
        
        MA.MenuHandler({ id:'experiment:view' });
    
        MA.skipBlur = true;
    
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
        
        MA.skipBlur = false;
        
        Ext.getCmp('center-panel').layout.setActiveItem('expProjTitle');
    };
    
    this.updateNav = function(index) {
        var en = Ext.getCmp("experimentName");
        var ds = Ext.StoreMgr.get("navDS");
        var et = Ext.getCmp("experimentTitle");
        var na = Ext.getCmp("expNav");
        
        if (na.getSelectionCount() === 0 || index !== null) {
            na.select(index,index,false);
        }
        
        var counter = 1;
        if (en.getValue() === '') {
            na.disable();
        } else {
            na.enable();
        }
                
        if (self.currentId() === 0) {
            et.setTitle('New Experiment');
        } else {
            et.setTitle('Experiment: '+en.getValue());
        }
    };
    
    this.createExperiment = function() {
        self.setCurrentId(0);
        var namefield = Ext.getCmp('experimentName');
        var statuscombo = namefield.ownerCt.getComponent('status');
        var desc = Ext.getCmp('experimentDescription');
        var comment = Ext.getCmp('experimentComment');
        var formalQuote = Ext.getCmp('formalQuote');
        var jobNumber = Ext.getCmp('jobNumber');
        var et = Ext.getCmp("experimentTitle");
        et.setTitle('New Experiment');
        
        namefield.setValue('');

        self.updateNav(0);       

        statuscombo.setValue(1);
        desc.setValue('');
        comment.setValue('');
        formalQuote.clearValue();
        jobNumber.setValue('');

        Ext.getCmp('center-panel').layout.setActiveItem('expProjTitle');
//        Ext.getCmp('expNav').getSelectionModel().selectFirstRow();
    };
    
    this.selectionChangeHandler = function(list, nodes) {
        var currItem;
        var blurFn;
        if (list.getSelectionCount() === 0) {
            return;
        }
     
        var index = list.getSelectedIndexes()[0];
        var r = list.getSelectedRecords()[0];

        if (Ext.currentExperimentNavItem == index) {
           return;
        }

        if (MA.skipBlur) {

            MA.Blur({'init':r.get("init"), 'index':index});
            MA.skipBlur = false;
        } else {
            currItem = Ext.StoreMgr.get("navDS").getAt(Ext.currentExperimentNavItem);
            blurFn = currItem.get("blur");
            if (blurFn !== null) {
                blurFn({'init':r.get("init"), 'index':index});
            }
        }
    };    


    this.initialSave = function() {
        MA.ExperimentController.blur({'init': MA.ExperimentController.updateNav, 'index': 0});
    };
}

MA.ExperimentController = new ExperimentController();

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
                id:'expFieldset',
                autoHeight:true,
                items: [
                    { xtype:'textfield', 
                      fieldLabel:'Experiment name', 
                      width:700, 
                      enableKeyEvents:true, 
                      id:'experimentName', 
                      allowBlank:false, 
                      listeners:{
                        'keydown':function(t, e){ 
                            MA.ExperimentController.updateNav(); 
                            return true; 
                        }, 
                        'keyup':function(t, e){ 
                            MA.ExperimentController.updateNav(); 
                            return true; 
                        },
                        'blur': function() {
                            MA.ExperimentController.initialSave(); 
                            return true; 
                        }
                      }
                    },
                    new Ext.form.ComboBox({
                            fieldLabel:'Status',
                            itemId:'status',
                            name:'status',
                            width:300,
                            editable:false,
                            forceSelection:true,
                            displayField:'value',
                            valueField:'key',
                            hiddenName:'status',
                            lazyRender:true,
                            allowBlank:false,
                            typeAhead:false,
                            triggerAction:'all',
                            listWidth:300,
                            store: expStatusComboStore
                        }),
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
id:'expProjTitle',
layout:'fit',
title:'Project',
tools: [
        {
        id:'left',
        qtip: "Back to the project",
        handler: function() {
        MA.LoadProject(MA.currentProjectId);
        }
        }
        ],
items:[
       {
       id:'experimentTitle',
       title:'New Experiment',
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
                                                                      [ "Access", MA.AccessInit, MA.Blur, false ],
                                                                      [ "Source", MA.BioSourceInit, MA.BioSourceBlur, false ],
                                                                      [ "Treatment", MA.TreatmentInit, MA.Blur, false ],
                                                                      [ "Sample Preparation", MA.SamplePrepInit, MA.Blur, false ],
                                                                      [ "Sample Classes", MA.ExperimentSamplesInit, MA.Blur, false ],
                                                                      [ "Samples", MA.ExperimentSamplesOnlyInit, MA.Blur, false ],
                                                                      [ "Sample Tracking", MA.SampleTrackingInit, MA.Blur, false ],
                                                                      [ "Runs", MA.ExperimentRunsInit, MA.Blur, false],
                                                                      [ "Files", MA.FilesInit, MA.Blur, false ]
                                                                      ]
                                                               }
                                                               )  
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
                      MA.Access,
                      MA.BioSource,
                      MA.Treatment,
                      MA.SamplePrep,
                      MA.ExperimentSamples,
                      MA.ExperimentSamplesOnly,
                      MA.SampleTracking,
                      MA.ExperimentRunListCmp,
                      MA.Files
                      ]
               }]
       }
       ]
};


// Original projects file follows ...




MA.ProjectList = Ext.extend(Ext.Panel, {
    constructor: function (config) {
        var self = this;

        var store = projectsListStore;
        if (config.store) {
            store = config.store;
        }

        var defaultConfig = {
            layout: "fit",
            items: [
                new Ext.grid.GridPanel({
                    itemId: "grid",
                    border: false,
                    tbar: [
                                    {
                                        text: "New Project",
                                        cls: "x-btn-text-icon",
                                        icon: "static/images/add.png",
                                        handler: function (b, e) {
                                            if (MA.CurrentUser.IsAdmin || MA.CurrentUser.IsMastrAdmin || MA.CurrentUser.IsProjectLeader) {
                                                // Toolbar.grid.ProjectList Panel
                                                this.ownerCt.ownerCt.ownerCt.createNewProject();
                                            } else {
                                                b.disable();
                                            }
                                        }
                                    }
                          ],
                    trackMouseOver: false,
                    plugins:[new Ext.ux.grid.Search({
                         mode:'local'
                        ,iconCls:false
                        ,dateFormat:'m/d/Y'
                        ,minLength:0
                        ,width:150
                        ,position:'top'
                    })],
                    selModel: new Ext.grid.RowSelectionModel({ singleSelect: true }),
                    viewConfig: {
                        forceFit: true,
                        autoFill: true
                    },
                    columns: [
                        { header: "ID", sortable: false, menuDisabled: true, dataIndex: "id", width: 50 },
                        { header: "Title", sortable: false, menuDisabled: true, dataIndex: "title" },
                        { header: "Client", sortable: false, menuDisabled: true, dataIndex: "client__unicode" },
                        { header: "Description", sortable: false, menuDisabled: true, dataIndex: "description", width: 300 }
                    ],
                    store: store,
                    listeners: {
                        "rowclick": function () {
                            self.fireEvent("click", this.getSelectionModel().getSelected().data.id);
                        },
                        "rowdblclick": function () {
                            self.fireEvent("dblclick", this.getSelectionModel().getSelected().data.id);
                        }
                    }
                })
            ]
        };

        config = Ext.apply(defaultConfig, config);

        /* Items that can be provided in the config that should apply to the
         * grid. */
        var keys = ["loadMask"];
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            if (config[key]) {
                config.items[0][key] = config[key];
            }
        }

        MA.ProjectList.superclass.constructor.call(this, config);
        this.addEvents("click", "dblclick", "delete");
    },
    getStore: function () {
        return this.getComponent("grid").getStore();
    },
    select: function (id) {
        var record = this.getStore().getById(id);
        this.getComponent("grid").getSelectionModel().selectRecords([record], false);
    }, 
    createNewProject: function () {
        MA.ChangeMainContent("project:new");
    }
});


MA.ProjectListCmp = new MA.ProjectList({
    title: 'Projects',
    region: 'center',
    cmargins: '0 0 0 0',
    collapsible: false,
    id:'projects-list',
    bodyStyle: 'padding:0px;',
    border:false,
    listeners: {
        dblclick: function (id) {
            MA.LoadProject(id);
        }
    }
});

MA.ProjectCmp = { 
    id:'projectCmpTitle',
    title:'New Project',
    layout:'border',
    forceLayout:true,
    deferredRender:false,
    defaults: {
        collapsible: false,
        bodyStyle: 'padding:15px;background-color:transparent;'
    },
    items: [{
        xtype: 'form',
        id:'project-form',
        border: false,
        region: 'north',
        width:720,
        autoHeight: true,
        title:'Project details',
        items: [ 
                { xtype:'textfield', fieldLabel:'Project title', width:700, id:'projectTitle', name:'title', allowBlank:false},
                { xtype:'textarea', fieldLabel:'Description', id:'projectDescription', width:700, height:100, name:'description' },
                new Ext.form.ComboBox({
                        fieldLabel:'Client',
                        id:'projectClientCombo',
                        name:'client',
                        width:700,
                        editable:false,
                        forceSelection:true,
                        displayField:'displayValue',
                        valueField:'id',
                        hiddenName:'client_id',
                        lazyRender:true,
                        allowBlank:false,
                        typeAhead:false,
                        triggerAction:'all',
                        listWidth:400,
                        store: clientsListStore,
                        itemSelector: 'div.search-item',
                        tpl:new Ext.XTemplate(
                        '<tpl for="."><div style="padding:8px;padding-top:5px;padding-bottom:5px;border-bottom:1px solid #ccc;" class="search-item">',
                        '{displayValue}<br /><span style="color:#666;">{organisationName}</span>',
                        '</div></tpl>'
                        )
                }),
                // this will hold the ',' joined ids of project managers on the project
                { xtype:'hidden', name: 'projectManagers' },
                {
                    fieldLabel:'Project managers',
                    width:525,
                    autoHeight:true,
                    bbar:[{
                        text: 'Add',
                        cls: 'x-btn-text-icon',
                        icon:'static/images/add.png',
                        id:'projManagersAddButton',
                        handler : function() {
                                //POP UP A WINDOW TO ASK WHICH USER TO ADD
                                var addWindow = new Ext.Window({
                                    title:'Add a Project Manager',
                                    width:380,
                                    height:130,
                                    minHeight:130,
                                    border:false,
                                    bodyStyle:'padding:20px;background-color:transparent;',
                                    x:290,
                                    y:250,
                                    layout:'vbox',
                                    modal:true,
                                    items:[
                                        new Ext.form.ComboBox({
                                                fieldLabel:'',
                                                labelWidth:50,
                                                itemId:'projManagerCombo',
                                                name:'projManager',
                                                width:300,
                                                editable:false,
                                                forceSelection:true,
                                                displayField:'value',
                                                valueField:'key',
                                                hiddenName:'projManagerId',
                                                lazyRender:true,
                                                allowBlank:false,
                                                typeAhead:false,
                                                triggerAction:'all',
                                                listWidth:300,
                                                store: maStaffComboStore
                                            })
                                    ],
                                    buttons:[
                                        {
                                            text:'Cancel',
                                            itemId:'cancel'
                                        },
                                        {
                                            text:'Add',
                                            itemId:'add'
                                        }
                                    ]
                                });
                                
                                addWindow.show();
                                
                                addWindow.buttons[0].on('click', function() { addWindow.close(); } );
                                addWindow.buttons[1].on('click', function() { 
                                    var id = addWindow.getComponent('projManagerCombo').getValue();
                                    var value = addWindow.getComponent('projManagerCombo').getRawValue();
                                    if (addWindow.getComponent('projManagerCombo').isValid()) {
                                        Ext.getCmp('projManagerList').getStore().add(new Ext.data.Record({'id':id, 'username':value})); 
                                        Ext.getCmp('projManagerList').refresh();
                                        addWindow.close(); 
                                    }
                                } );
                            }
                        },
                        {
                            text: 'Remove',
                            cls: 'x-btn-text-icon',
                            icon:'static/images/delete.png',
                            id:'projManagersRemoveButton',
                            handler : function(){
                                   //remove currently selected users
                                   var recs = Ext.getCmp('projManagerList').getSelectedRecords();
                                   for (i = 0; i < recs.length; i++) {
                                       var rec = recs[i];
                                       Ext.getCmp('projManagerList').getStore().remove(rec);
                                   }
                            }
                        }
                    ],
                    items:[{
                        xtype:'listview',
                        id:'projManagerList',
                        store: new Ext.data.ArrayStore({}),
                        height: 80,
                        loadingText:'Loading...',
                        columnSort:false,
                        columns: [{
                            header: "username", 
                            dataIndex: 'username', 
                            tpl: '<div style="padding:4px">{username}</div>'
                        }],
                        viewConfig:{
                            forceFit:true
                        },
                        singleSelect:true,
                        multiSelect:false,
                        hideHeaders:true,
                        style:'background:white;',
                        autoScroll:true,
                        reserveScrollOffset:true
                    }]
                }
        ],
        buttonAlign: 'left',
        buttons: [{
            text: 'Save',
            id:'projectSubmit',
            handler: function() {
                // collect the Project Manager ids and set them into a hidden field
                // so they get submitted on form.submit()
                var projManagerIds = Ext.getCmp('projManagerList').getStore().collect('id').join(',');
                Ext.getCmp('project-form').getForm().findField('projectManagers').setValue(projManagerIds);
                Ext.getCmp('project-form').getForm().submit({ 
                    url: wsBaseUrl + 'update/project/' + MA.currentProjectId,
                    successProperty: 'success',
                    success: function (form, action) {
                        if (action.result.success === true) {
                            MA.currentProjectId = action.result.rows[0].id;
                            Ext.Msg.alert("Project saved", "(this message will auto-close in 1 second)");
                            window.setTimeout(function() {Ext.Msg.hide();}, 1000);
                            Ext.getCmp('project-experiment-list').enable();
                            //load up the menu and next content area as declared in response
                            MA.ChangeMainContent(action.result.mainContentFunction);
                        }
                    },
                    failure: function (form, action) {
                        //do nothing special. this gets called on validation failures and server errors
                    }
                });
            }
        }]
    },{
            title: 'Experiments',
            region: 'center',
            cmargins: '0 0 0 0',
            collapsible: false,
            id:'project-experiment-list',
            bodyStyle: 'padding:0px;',
            layout:'fit',
            tbar: [{
                text: 'New Experiment',
                cls: 'x-btn-text-icon',
                icon:'static/images/add.png',
                handler : function(){
                        MA.MenuHandler({'id':'experiment:new'});
                    }
                },
                {
                text: 'Remove Experiment',
                cls: 'x-btn-text-icon',
                icon:'static/images/delete.png',
                handler : function(){
                   var grid = Ext.getCmp('project-experiments');
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
                   //console.log(delIds);
                   for (var i = 0; i < delIds.length; i++) {
                       MA.CRUDSomething('delete/experiment/'+delIds[i], {}, function() { experimentListStore.proxy.conn.url = wsBaseUrl + 'recordsExperiments/' + MA.currentProjectId;
                       experimentListStore.load(); });
                   }                        
                   }
                   
                }
            ],
            items: [
                {
                    xtype:'grid',
                    border: false,
                    id:'project-experiments',
                    trackMouseOver: false,
                    sm: new Ext.grid.RowSelectionModel( {singleSelect:true}),
                    view: new Ext.grid.GroupingView({
                        forceFit: true,
                        autoFill: true,
                        hideGroupedColumn: true
                    }),
                    columns: [
                        { header: "ID", sortable:false, menuDisabled:true, dataIndex:'id', width:50 },
                        { header: "Title", sortable:false, menuDisabled:true, dataIndex:'title' },
                        { header: "Principal", sortable:false, menuDisabled:true, dataIndex:'principal' },
                        { header: "Client", sortable:false, menuDisabled:true, dataIndex:'client' },
                        { header: "Description", sortable:false, menuDisabled:true, width:300, dataIndex:'description' },
                        { header: "Status", sortable:false, menuDisabled:true, dataIndex:'status_text' }
                    ],
                    store: experimentListStore,
                    listeners: {
                        'rowdblclick':function(el, ev) {
                            var sm = Ext.getCmp('project-experiments').getSelectionModel();
                            var rec = sm.getSelected();
                            MA.ExperimentController.loadExperiment(rec.data.id);
                        }
                    }
                }
            ]
        }
    ]
};

MA.LoadProject = function (projId) {
    projectsListStore.load();
    MA.currentProjectId = projId;
    
    Ext.getCmp('projectCmpTitle').setTitle('Loading project...');
    
    var projLoader = new Ajax.Request(wsBaseUrl + "recordsProject/" + projId, 
                                         { 
                                         asynchronous:true, 
                                         evalJSON:'force',
                                         onSuccess: function(response) {
                                                 var titlefield = Ext.getCmp('projectTitle');
                                                 var desc = Ext.getCmp('projectDescription');
                                                 var titleCmp = Ext.getCmp('projectCmpTitle');
                                                 var clientCmp = Ext.getCmp('projectClientCombo');
                                                 var projBarTitle = Ext.getCmp('expProjTitle');
                                                 //projBarTitle.setTitle('');

                                                 titleCmp.setTitle('');    
                                                 titlefield.setValue('');
                                                 desc.setValue('');
    
                                                 var rs = response.responseJSON.rows;

                                                 //enable or disable Add/Remove project managers based on access
                                                 var showAddRemove = false;
                                                 if (MA.CurrentUser.IsAdmin || MA.CurrentUser.IsMastrAdmin || MA.CurrentUser.IsProjectLeader) {
                                                     showAddRemove = true;
                                                 }

                                                 if (rs.length > 0) {
                                                     titleCmp.setTitle('Project: ' + rs[0].title);
                                                     //projBarTitle.setTitle('Project: ' + rs[0].title);
                                                     titlefield.setValue(rs[0].title);
                                                     desc.setValue(rs[0].description);
                                                     clientCmp.setValue(rs[0].client);
                                                                                                 
                                                     var pmList = Ext.getCmp('projManagerList');
                                                     var pmStore = pmList.getStore();
                                                     pmStore.removeAll(false);
                                                     for (i = 0; i < rs[0].managers.length; i++) {
                                                         val = rs[0].managers[i];
                                                         if (rs[0].managers[i].id == MA.CurrentUserId) {
                                                             showAddRemove = true;
                                                         }
                                                         pmStore.add(new Ext.data.Record(val));
                                                     }
                                                     
                                                 }
                                         
                                                 if (showAddRemove) {
                                                     Ext.getCmp("projManagersAddButton").enable();
                                                     Ext.getCmp("projManagersRemoveButton").enable();
                                                 } else {
                                                     Ext.getCmp("projManagersAddButton").disable();
                                                     Ext.getCmp("projManagersRemoveButton").disable();
                                                 }
                                             }
                                         }
                                         );
    
    experimentListStore.proxy.conn.url = wsBaseUrl + 'recordsExperiments/' + projId;
    experimentListStore.load();
  
    MA.MenuHandler({ id:'project:view' });
};
