//var wsBaseUrl = "http://boromir5.localdomain/madasrepo/ntakayama/ws/";
//var baseUrl = "/madas/ntakayama/repo/";
var wsBaseUrl = baseUrl + "ws/";
var storesNeededForRendering = [];

MA.DSLoaded = function(ds, recs, opts) {
    storesNeededForRendering[ds.storeId] = 'loaded';
    ds.removeListener('load', MA.DSLoaded);
    
    var allLoaded = true;
    for (index in storesNeededForRendering) {
        if (storesNeededForRendering[index] != 'loaded') {
            allLoaded = false;
        }
    }
    
    if (allLoaded && MA.InitUI !== undefined) {
        MA.InitUI();
    }
};

MA.DSLoadException = function() {
    //console.log("load exception: "+this.storeId);
    
    storesNeededForRendering[this.storeId] = 'loaded';
    MA.DSLoaded(this, null, null);
};

MA.SaveRowLiterals = function(table, roweditor, changes, rec, i, callback) {
    if (rec.data.id === undefined || rec.data.id === "" || rec.data.id === 0) {
        MA.CRUDSomething('create/' + table + '/', changes, callback);
    } else {
        MA.CRUDSomething('update/' + table + '/' + rec.data.id + '/', changes, callback);
    }
};

MA.CurrentExperimentId = function() {
    if (!MA.CurrentExpId) {
        return 0;
    }
    
    return MA.CurrentExpId;
};

MA.CurrentBioSourceId = function() {
    if (biologicalSourceStore.getTotalCount() < 1) {
        return 0;
    }
    
    return biologicalSourceStore.getAt(0).get("id");
};

MA.CurrentOrganismType = function() {
    return MA.CurrentOrganismTypeValue;
};

MA.CurrentAnimalId = function() {
    if (animalStore.getTotalCount() < 1) {
        return 0;
    }
    
    return animalStore.getAt(0).get("id");
};

MA.CurrentTreatmentId = function() {
    if (MA.CurrentTreatmentIdValue !== undefined) {
        return MA.CurrentTreatmentIdValue;
    }
    
    return 0;
};

MA.CurrentSampleClassId = function() {
    if (MA.CurrentSampleClassIdValue !== undefined) {
        return MA.CurrentSampleClassIdValue;
    }
    
    return 0;
};

// ---------- TABLE STORES ---------- (used for tables, entities)
var organStore = new Ext.data.JsonStore(
                        {
                            storeId: 'organism',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/organ/experiment__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                    
var timelineStore = new Ext.data.JsonStore(
                        {
                            storeId: 'timeline',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/sampletimeline/experiment__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                    
var treatmentStore = new Ext.data.JsonStore(
                        {
                            storeId: 'treatment',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/treatment/experiment__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                    
var sopStore = new Ext.data.JsonStore(
                        {
                            storeId: 'sop',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/standardoperationprocedure/experiments__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                    
var sopLookupStore = new Ext.data.JsonStore(
                        {
                            storeId: 'sopLookup',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/standardoperationprocedure/id__gte/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            }
                        }
                    );

var userStore = new Ext.data.JsonStore(
                        {
                            storeId: 'user',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/userexperiment/experiment__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            }
                        }
                    );
                    
var experimentListStore = new Ext.data.JsonStore(
                        {
                            storeId: 'experimentList',
                            autoLoad: false,
                            url: wsBaseUrl + 'recordsExperiments',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                                        },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                                    
                        }
                    );
                    
var clientsListStore = new Ext.data.JsonStore(
                        {
                            storeId: 'clientsList',
                            autoLoad: false,
                            url: wsBaseUrl + 'recordsClients',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                                        },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                                    
                        }
                    );
                    
var experimentStore = new Ext.data.ArrayStore({
                                             storeId:'experiment',
                                             fields: ['id', 'title', 'description', 'comment', 'status_id', 'created_on', 'client_id']
});

var sampleClassStore = new Ext.data.JsonStore(
                                             {
                                             storeId: 'sampleclass',
                                             autoLoad: false,
                                             url: wsBaseUrl + 'records/sampleclass/experiment__id/0',
                                             listeners: {'load':MA.DSLoaded,
                                             'loadexception':MA.DSLoadException
                                             },
                                             sortInfo: {
                                                 field: 'id',
                                                 direction: 'DESC'
                                             }
                                         }
                                             );

var sampleStore = new Ext.data.JsonStore(
                                              {
                                              storeId: 'samples',
                                              autoLoad: false,
                                              url: wsBaseUrl + 'records/sample/sample_class__id/0',
                                              listeners: {'load':MA.DSLoaded,
                                              'loadexception':MA.DSLoadException},
                                              sortInfo: {
                                                  field: 'id',
                                                  direction: 'DESC'
                                              }
                                              }
                                              );

var plantStore = new Ext.data.JsonStore(
                                          {
                                          storeId: 'plant',
                                          autoLoad: false,
                                          url: wsBaseUrl + 'records/plant/id/0',
                                          listeners: {'load':MA.DSLoaded,
                                          'load':function(t, rs, o) {
                                              if (rs.length > 0) {
                                                  Ext.getCmp('development_stage').setValue(rs[0].data.development_stage);
                                              }
                                          },
                                          'loadexception':MA.DSLoadException}
                                          }
                                          );
                    
var animalStore = new Ext.data.JsonStore(
                        {
                            storeId: 'animal',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/animal/experiment__id/0',
                            listeners: {'load':MA.DSLoaded,
                                        'load':function(t, rs, o) {
                                            Ext.getCmp('animalGender').clearValue();
                                            Ext.getCmp('animalAge').setValue('');
                                            Ext.getCmp('animalParentalLine').clearValue();
                                            
                                            if (rs.length > 0) {
                                                Ext.getCmp('animalGender').setValue(rs[0].data.sex);
                                                Ext.getCmp('animalAge').setValue(rs[0].data.age);
                                                Ext.getCmp('animalParentalLine').setValue(rs[0].data.parental_line);
                                            }
                                            
                                        },
                                        'loadexception':MA.DSLoadException}
                            }
                    );

var humanStore = new Ext.data.JsonStore(
                                         {
                                         storeId: 'human',
                                         autoLoad: false,
                                         url: wsBaseUrl + 'records/human/experiment__id/0',
                                         listeners: {'load':MA.DSLoaded,
                                         'load':function(t, rs, o) {
                                         Ext.getCmp('humanGender').clearValue();
                                         Ext.getCmp('human_dob').setValue('');
                                         Ext.getCmp('human_bmi').setValue('');
                                         Ext.getCmp('human_diagnosis').setValue('');
                                         
                                         if (rs.length > 0) {
                                         Ext.getCmp('humanGender').setValue(rs[0].data.sex);
                                         Ext.getCmp('human_dob').setValue(rs[0].data.date_of_birth);
                                         Ext.getCmp('human_bmi').setValue(rs[0].data.bmi);
                                         Ext.getCmp('human_diagnosis').setValue(rs[0].data.diagnosis);
                                         }
                                         
                                         },
                                         'loadexception':MA.DSLoadException}
                                         }
                                         );
                                        
// ---------- COMBO STORES ---------- (used for comboboxes)
var organismTypeComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'organismTypeCombo',
                            autoLoad: true,
                                                    method:'GET',
                            url: wsBaseUrl + 'populate_select/organismtype/id/name/',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );

var plantComboStore = new Ext.data.JsonStore(
                                                    {
                                                    storeId: 'plantCombo',
                                                    autoLoad: false,
                                                    url: wsBaseUrl + 'populate_select/plant/development_stage/',
                                                    root: 'response.value.items',
                                                    fields: ['value', 'key'],
                                                    listeners: {'load':MA.DSLoaded,
                                                    'loadexception':MA.DSLoadException}
                                                    }
                                                    );

var animalComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'animalCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/animal/parental_line/',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );

var organNameComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'organNameCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
var tissueComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'tissueCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/tissue',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
var cellTypeComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'celltypeCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/cell_type',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
var subcellularCellTypeComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'subcellularcelltypeCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/subcellular_cell_type',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
                   
var plantGrowingPlaceComboStore = new Ext.data.JsonStore(
                                                             {
                                                             storeId: 'plantGrowingPlaceCombo',
                                                             autoLoad: false,
                                                             url: wsBaseUrl + 'populate_select/plant/id/location',
                                                             root: 'response.value.items',
                                                             fields: ['value', 'key'],
                                                             listeners: {'load':MA.DSLoaded,
                                                             'loadexception':MA.DSLoadException}
                                                             }
                                                             );
                    
var treatmentComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'treatmentCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/treatment/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );

var sopComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'sopCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/standardoperationprocedure/id/label',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
var userComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'userCombo',
                            autoLoad: true,
                            url: wsBaseUrl + 'populate_select/user/id/username',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );
                    
var involvementComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'involvementCombo',
                            autoLoad: true,
                            url: wsBaseUrl + 'populate_select/userinvolvementtype/id/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException}
                        }
                    );