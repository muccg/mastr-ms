Ext.madasGrowthInit = function() {
    var expId = Ext.madasCurrentExperimentId();
    var orgType = Ext.madasCurrentOrganismType();
    
    if (orgType == 3) {
        animalOriginStore.proxy.conn.url = wsBaseUrl + 'records/origindetails/source__experiment__id/' + expId;
        animalOriginStore.load();
        Ext.getCmp("animalOrigins").show();
        Ext.getCmp("growthConditions").hide();
    } else if (orgType == 2) {
        growthConditionStore.proxy.conn.url = wsBaseUrl + 'records/growthcondition/source__experiment__id/' + expId;
        growthConditionStore.load();
        Ext.getCmp("animalOrigins").hide();
        Ext.getCmp("growthConditions").show();
    } else {
        Ext.getCmp("animalOrigins").hide();
        Ext.getCmp("growthConditions").hide();
    }
}

Ext.madasSaveAnimalOriginRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['location_id'] = rec.data.location;
    bundledData['detailed_location'] = rec.data.detailed_location;
    bundledData['information'] = rec.data.information;
    
    Ext.madasSaveRowLiterals('origindetails', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); animalOriginStore.proxy.conn.url = wsBaseUrl + 'records/origindetails/source__experiment__id/' + expId; animalOriginStore.load();});
};

Ext.madasSaveGrowthConditionRow = function(roweditor, changes, rec, i) {
    var bundledData = {};
    
    bundledData['source_id'] = Ext.madasCurrentBioSourceId();
    bundledData['greenhouse_id'] = rec.data.greenhouse;
    bundledData['detailed_location'] = rec.data.detailed_location;
    bundledData['light_source_id'] = rec.data.light_source;
    bundledData['growing_place'] = rec.data.growing_place;
    bundledData['seeded_on'] = Ext.util.Format.date(rec.data.seeded_on, 'Y-m-d');
    bundledData['transplated_on'] = Ext.util.Format.date(rec.data.transplated_on, 'Y-m-d');
    bundledData['harvested_on'] = Ext.util.Format.date(rec.data.harvested_on, 'Y-m-d');
    bundledData['harvested_at'] = rec.data.harvested_at;
    bundledData['night_temp_cels'] = rec.data.night_temp_cels;
    bundledData['day_temp_cels'] = rec.data.day_temp_cels;
    bundledData['light_hrs_per_day'] = rec.data.light_hrs_per_day;
    bundledData['light_fluence'] = rec.data.light_fluence;
    bundledData['lamp_details'] = rec.data.lamp_details;
    
    Ext.madasSaveRowLiterals('growthcondition', roweditor, bundledData, rec, i, function() { var expId = Ext.madasCurrentExperimentId(); growthConditionStore.proxy.conn.url = wsBaseUrl + 'records/growthCondition/source__experiment__id/' + expId; growthConditionStore.load();});
};

Ext.madasGrowth = {
    baseCls: 'x-plain',
    border:false,
    frame:false,
    layout:'border',
    defaults: {
        bodyStyle:'padding:15px;background:transparent;'
    },
    items:[
        {
            title: 'growth',
            region: 'center',
            collapsible: false,
            autoScroll:true,
            layout:'form',
            minSize: 75,
            items: [ 
                { xtype:'editorgrid', 
                    id:'animalOrigins',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'animal origin',
                    width:500,
                    height:200,
                    border: true,
                    trackMouseOver: false,
//                    plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveAnimalOriginRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    viewConfig: {
                        forceFit: true,
                        autoFill:true
                    },
                    tbar: [{
                        text: 'add origin',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/add.gif',
                        handler : function(){
                            Ext.madasCRUDSomething('create/origindetails/', {'source_id':Ext.madasCurrentBioSourceId()}, function() { var expId = Ext.madasCurrentExperimentId(); animalOriginStore.proxy.conn.url = wsBaseUrl + 'records/origindetails/source__experiment__id/' + expId;
                                                  animalOriginStore.load(); });
                            }
                        },
                        {
                        text: 'remove origin',
                        cls: 'x-btn-text-icon',
                        icon:'static/repo/images/no.gif',
                        handler : function(){
                           var grid = Ext.getCmp('animalOrigins');
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
                           Ext.madasCRUDSomething('delete/origindetails/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); animalOriginStore.proxy.conn.url = wsBaseUrl + 'records/origindetails/source__experiment__id/' + expId;
                                                  animalOriginStore.load(); });
                           }                        }
                        }
                    ],
                    columns: [
                        { header: "location",  sortable:false, menuDisabled:true }
                    ],
                    store: animalOriginStore
                },
                    {
                    xtype:'editorgrid', 
                    id:'growthConditions',
                    style:'margin-top:10px;margin-bottom:10px;',
                    title:'plant growth conditions',
                    border: true,
                    height:200,
                    trackMouseOver: false,
                    //plugins: [new Ext.ux.grid.RowEditor({saveText: 'Update', errorSummary:false, listeners:{'afteredit':Ext.madasSaveGrowthConditionRow}})],
                    sm: new Ext.grid.RowSelectionModel(),
                    viewConfig: {
                    forceFit: true,
                    autoFill:true
                    },
                    tbar: [{
                           text: 'add growth condition',
                           cls: 'x-btn-text-icon',
                           icon:'static/repo/images/add.gif',
                           handler : function() {
                           growthConditionStore.add(new Ext.data.Record({'id':'', 'name':'', 'detailed_location':''}));
                            }
                           }, 
                           {
                           text: 'remove growth condition',
                           cls: 'x-btn-text-icon',
                           icon:'static/repo/images/no.gif',
                           handler : function(){
                           var grid = Ext.getCmp('growthConditions');
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
                           
                           var delCount = 0;
                           for (var i = 0; i < delIds.length; i++) {
                            if (Ext.isDefined(delIds[i]) && Ext.isNumber(delIds[i])) {
                               Ext.madasCRUDSomething('delete/growthcondition/'+delIds[i], {}, function() { var expId = Ext.madasCurrentExperimentId(); growthConditionStore.proxy.conn.url = wsBaseUrl + 'records/growthcondition/source__experiment__id/' + expId;
                                                      growthConditionStore.load(); });
                           delCount++;
                                }
                           }
                           if (delCount == 0) {
                           growthConditionStore.reload();
                           }
                           
                           }
                           }
                           ],
                    columns: [
                              { header: "greenhouse",  sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                                                                                                 editable:false,
                                                                                                                 forceSelection:true,
                                                                                                                 displayField:'value',
                                                                                                                 valueField:'key',
                                                                                                                 hiddenName:'tissue',
                                                                                                                 lazyRender:true,
                                                                                                                 allowBlank:false,
                                                                                                                 typeAhead:false,
                                                                                                                 triggerAction:'all',
                                                                                                                 listWidth:230,
                                                                                                                 store: locationComboStore
                                                                                                                       }), dataIndex:'greenhouse', renderer:renderLocation },
                              { header: "detailed location", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
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
                                                                                                                  store: plantDetailedLocationComboStore
                                                                                                                  }), dataIndex:'detailed_location'
                              },
                              { header: "growing place/media", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
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
                                                                                                                             store: plantGrowingPlaceComboStore
                                                                                                                             }), dataIndex:'growing_place'
                              },
                              { header: "seeding date", sortable:false, menuDisabled:true, editor:new Ext.form.DateField({
                                                                                                                               editable:true,
                                                                                                                               allowBlank:false,
                                                                                                                         format:'Y/m/d'
                                                                                                                        }), dataIndex:'seeded_on'
                              },
                              { header: "transplant date", sortable:false, menuDisabled:true, editor:new Ext.form.DateField({
                                                                                                                            editable:true,
                                                                                                                            allowBlank:false ,
                                                                                                                            format:'Y/m/d'                                                                                                                              }), dataIndex:'transplated_on'
                              },
                              { header: "harvest date", sortable:false, menuDisabled:true, editor:new Ext.form.DateField({
                                                                                                                         editable:true,
                                                                                                                         allowBlank:false  ,
                                                                                                                         format:'Y/m/d'                                                                                                                             }), dataIndex:'harvested_on'
                              },
                              { header: "harvest time", sortable:false, menuDisabled:true, editor:new Ext.form.TimeField({
                                                                                                                         editable:true,
                                                                                                                         allowBlank:false  ,
                                                                                                                         format:'H:i'                                                                                                                             }), dataIndex:'harvested_at'
                              },
                              { header: "night temp C", sortable:false, menuDisabled:true, editor:new Ext.form.NumberField({editable:true}), dataIndex:'night_temp_cels'
                              },
                              { header: "day temp C", sortable:false, menuDisabled:true, editor:new Ext.form.NumberField({editable:true}), dataIndex:'day_temp_cels'
                              },
                              
                              { header: "hrs of light/day", sortable:false, menuDisabled:true, editor:new Ext.form.NumberField({editable:true}), dataIndex:'light_hrs_per_day'
                              },
                              
                              { header: "light fluence", sortable:false, menuDisabled:true, editor:new Ext.form.NumberField({editable:true}), dataIndex:'light_fluence'
                              },
                              { header: "light source", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
                                                                                                                             editable:false,
                                                                                                                             forceSelection:true,
                                                                                                                             displayField:'value',
                                                                                                                             valueField:'key',
                                                                                                                             hiddenName:'tissue',
                                                                                                                             lazyRender:true,
                                                                                                                             allowBlank:false,
                                                                                                                             typeAhead:false,
                                                                                                                             triggerAction:'all',
                                                                                                                             listWidth:230,
                                                                                                                             store: lightSourceComboStore
                                                                                                                        }), dataIndex:'light_source', renderer:renderLightSource
                              },
                              { header: "lamp details", sortable:false, menuDisabled:true, editor:new Ext.form.ComboBox({
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
                                                                                                                        store: lampDetailsComboStore
                                                                                                                        }), dataIndex:'lamp_details'
                              }
                              ],
                    store: growthConditionStore
                    }
            ]
        }
    ]
};