//var wsBaseUrl = "http://boromir5.localdomain/madasrepo/ntakayama/ws/";
//var baseUrl = "/madas/ntakayama/repo/";
var wsBaseUrl = baseUrl + "ws/";
var storesNeededForRendering = [];

Ext.madasDSLoaded = function(ds, recs, opts) {
    storesNeededForRendering[ds.storeId] = 'loaded';
    ds.removeListener('load', Ext.madasDSLoaded);
    
    var allLoaded = true;
    for (index in storesNeededForRendering) {
        if (storesNeededForRendering[index] != 'loaded') {
            allLoaded = false;
        }
    }
    
    if (allLoaded && Ext.madasInitUI !== undefined) {
        Ext.madasInitUI();
    }
};

Ext.madasDSLoadException = function() {
    //console.log("load exception: "+this.storeId);
    
    storesNeededForRendering[this.storeId] = 'loaded';
    Ext.madasDSLoaded(this, null, null);
};

Ext.madasSaveRowLiterals = function(table, roweditor, changes, rec, i, callback) {
    if (rec.data.id === undefined || rec.data.id === "" || rec.data.id === 0) {
        Ext.madasCRUDSomething('create/' + table + '/', changes, callback);
    } else {
        Ext.madasCRUDSomething('update/' + table + '/' + rec.data.id + '/', changes, callback);
    }
};

Ext.madasCurrentExperimentId = function() {
    if (!Ext.madasCurrentExpId) {
        return 0;
    }
    
    return Ext.madasCurrentExpId;
};

Ext.madasCurrentBioSourceId = function() {
    if (biologicalSourceStore.getTotalCount() < 1) {
        return 0;
    }
    
    return biologicalSourceStore.getAt(0).get("id");
};

Ext.madasCurrentOrganismType = function() {
    return Ext.madasCurrentOrganismTypeValue;
};

Ext.madasCurrentAnimalId = function() {
    if (animalStore.getTotalCount() < 1) {
        return 0;
    }
    
    return animalStore.getAt(0).get("id");
};

Ext.madasCurrentTreatmentId = function() {
    if (Ext.madasCurrentTreatmentIdValue !== undefined) {
        return Ext.madasCurrentTreatmentIdValue;
    }
    
    return 0;
};

Ext.madasCurrentSampleClassId = function() {
    if (Ext.madasCurrentSampleClassIdValue !== undefined) {
        return Ext.madasCurrentSampleClassIdValue;
    }
    
    return 0;
};

// ---------- TABLE STORES ---------- (used for tables, entities)
var organStore = new Ext.madasJsonStore(
                        {
                            storeId: 'organism',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/organ/experiment__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var timelineStore = new Ext.madasJsonStore(
                        {
                            storeId: 'timeline',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/sampletimeline/experiment__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var treatmentStore = new Ext.madasJsonStore(
                        {
                            storeId: 'treatment',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/treatment/experiment__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var sopStore = new Ext.madasJsonStore(
                        {
                            storeId: 'sop',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/standardoperationprocedure/experiments__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var sopLookupStore = new Ext.madasJsonStore(
                        {
                            storeId: 'sopLookup',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/standardoperationprocedure/id__gte/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );

var userStore = new Ext.madasJsonStore(
                        {
                            storeId: 'user',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/userexperiment/experiment__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var experimentListStore = new Ext.madasJsonStore(
                        {
                            storeId: 'experimentList',
                            autoLoad: false,
                            url: wsBaseUrl + 'recordsExperiments',
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );
                    
var experimentStore = new Ext.data.ArrayStore({
                                             storeId:'experiment',
                                             fields: ['id', 'title', 'description', 'comment', 'status_id', 'created_on', 'client_id']
});

var sampleClassStore = new Ext.madasJsonStore(
                                             {
                                             storeId: 'sampleclass',
                                             autoLoad: false,
                                             url: wsBaseUrl + 'records/sampleclass/experiment__id/0',
                                             listeners: {'load':Ext.madasDSLoaded,
                                             'loadexception':Ext.madasDSLoadException}
                                             }
                                             );

var sampleStore = new Ext.madasJsonStore(
                                              {
                                              storeId: 'samples',
                                              autoLoad: false,
                                              url: wsBaseUrl + 'records/sample/sample_class__id/0',
                                              listeners: {'load':Ext.madasDSLoaded,
                                              'loadexception':Ext.madasDSLoadException}
                                              }
                                              );

var plantStore = new Ext.madasJsonStore(
                                          {
                                          storeId: 'plant',
                                          autoLoad: false,
                                          url: wsBaseUrl + 'records/plant/id/0',
                                          listeners: {'load':Ext.madasDSLoaded,
                                          'load':function(t, rs, o) {
                                              if (rs.length > 0) {
                                                  Ext.getCmp('development_stage').setValue(rs[0].data.development_stage);
                                              }
                                          },
                                          'loadexception':Ext.madasDSLoadException}
                                          }
                                          );
                    
var animalStore = new Ext.madasJsonStore(
                        {
                            storeId: 'animal',
                            autoLoad: false,
                            url: wsBaseUrl + 'records/animal/experiment__id/0',
                            listeners: {'load':Ext.madasDSLoaded,
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
                                        'loadexception':Ext.madasDSLoadException}
                            }
                    );

var humanStore = new Ext.madasJsonStore(
                                         {
                                         storeId: 'human',
                                         autoLoad: false,
                                         url: wsBaseUrl + 'records/human/experiment__id/0',
                                         listeners: {'load':Ext.madasDSLoaded,
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
                                         'loadexception':Ext.madasDSLoadException}
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
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );

var plantComboStore = new Ext.data.JsonStore(
                                                    {
                                                    storeId: 'plantCombo',
                                                    autoLoad: false,
                                                    url: wsBaseUrl + 'populate_select/plant/development_stage/',
                                                    root: 'response.value.items',
                                                    fields: ['value', 'key'],
                                                    listeners: {'load':Ext.madasDSLoaded,
                                                    'loadexception':Ext.madasDSLoadException}
                                                    }
                                                    );

var animalComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'animalCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/animal/parental_line/',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );

var organNameComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'organNameCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
var tissueComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'tissueCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/tissue',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
var cellTypeComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'celltypeCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/cell_type',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
var subcellularCellTypeComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'subcellularcelltypeCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/organ/subcellular_cell_type',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
                   
var plantGrowingPlaceComboStore = new Ext.data.JsonStore(
                                                             {
                                                             storeId: 'plantGrowingPlaceCombo',
                                                             autoLoad: false,
                                                             url: wsBaseUrl + 'populate_select/plant/id/location',
                                                             root: 'response.value.items',
                                                             fields: ['value', 'key'],
                                                             listeners: {'load':Ext.madasDSLoaded,
                                                             'loadexception':Ext.madasDSLoadException}
                                                             }
                                                             );
                    
var treatmentComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'treatmentCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/treatment/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );

var sopComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'sopCombo',
                            autoLoad: false,
                            url: wsBaseUrl + 'populate_select/standardoperationprocedure/id/label',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
var userComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'userCombo',
                            autoLoad: true,
                            url: wsBaseUrl + 'populate_select/user/id/username',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );
                    
var involvementComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'involvementCombo',
                            autoLoad: true,
                            url: wsBaseUrl + 'populate_select/userinvolvementtype/id/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':Ext.madasDSLoaded,
                                        'loadexception':Ext.madasDSLoadException}
                        }
                    );