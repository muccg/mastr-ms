//var wsBaseUrl = "http://boromir5.localdomain/madasrepo/ntakayama/ws/";
//var baseUrl = "/madas/ntakayama/repo/";
var adminBaseUrl = baseUrl + "repoadmin/";
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
    
//    if (allLoaded && MA.InitUI !== undefined) {
//        MA.InitUI();
//    }
};

MA.DSLoadIgnoreException = function() { MA.DSLoaded(this, null, null); };

MA.DSLoadException = function(status, text, c, d, e) {
    var title = "Network Error";
    if (status !== undefined) {
        title = "Error";
    }
    
    if (text === undefined) {
        text = "An unidentified error occurred, please try again. (Code: "+status+")";
    } else if (Ext.isObject(text)) {
        if (c.status == 200) {
            text = "Session timeout occurred.";
        } else {
            text = "An error occurred, code: "+c.status+" message: "+c.statusText;
        }
    }
    
    Ext.Msg.alert(title, text);
    
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
                            url: adminBaseUrl + "repository/organ/ext/json",
                            remoteSort: true,
                            restful: true,
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
                            url: adminBaseUrl + "repository/sampletimeline/ext/json",
                            remoteSort: true,
                            restful: true,
                            listeners: {'load': function(store, records, options) {
                                        },
                                'exception': function(proxy, type, action, options, response, arg) {
                                            //console.log('exception');
                                        }
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
                            url: adminBaseUrl + "repository/treatment/ext/json",
                            remoteSort: true,
                            restful: true,
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
                            url: adminBaseUrl + "repository/standardoperationprocedure/ext/json",
                            remoteSort: true,
                            restful: true,
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
                            autoLoad: true,
                            url: adminBaseUrl + "repository/standardoperationprocedure/ext/json",
                            remoteSort: true,
                            restful: true,
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadIgnoreException
                            }
                        }
                    );

var userStore = new Ext.data.JsonStore(
                        {
                            storeId: 'user',
                            autoLoad: false,
                            url: adminBaseUrl + "repository/userexperiment/ext/json",
                            remoteSort: true,
                            restful: true,
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                            }
                        }
                    );
                    
/* By rights, this should use the ExtJsonInterface, but because
 * recordsExperiments does some magic to fill in the principal, for now I'm
 * just going to hack the appropriate row filtering into repository.wsviews and
 * come back to this at a later stage. */
var experimentListStore = new Ext.data.GroupingStore(
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
                            },
                            reader:new Ext.data.JsonReader({}),
                            groupField:'status'      
                        }
                    );

//store:runRelatedExperimentStore
var runRelatedExperimentStore = new Ext.data.JsonStore(
{
    storeId: 'runRelatedExperimentStore',
    autoLoad: false,
    url: wsBaseUrl + 'recordsExperiments',
    listeners: {'load':MA.DSLoaded,
        'loadexception':MA.DSLoadException
    },
    sortInfo: {
        field: 'id',
        direction: 'DESC'
    },
    reader:new Ext.data.JsonReader({})     
}
);

var projectsListStore = new Ext.data.JsonStore(
                        {
                            storeId: 'projectList',
                            autoLoad: false,
                            url: adminBaseUrl + 'repository/project/ext/json',
                            remoteSort: true,
                            restful: true,
                            writer: new Ext.data.JsonWriter({ encode: false }),
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
                            autoLoad: true,
                            url: wsBaseUrl + 'recordsClientList',
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadException
                                        },
                            sortInfo: {
                                field: 'username',
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
                                              url: adminBaseUrl + 'repository/sample/ext/json',
                                              remoteSort: true,
                                              restful: true,
                                              listeners: {'load':MA.DSLoaded,
                                              'loadexception':MA.DSLoadException},
                                              sortInfo: {
                                                  field: 'id',
                                                  direction: 'DESC'
                                              }
                                              }
                                              );
                                              
var sampleLogStore = new Ext.data.JsonStore(
                                              {
                                              storeId: 'samplelogs',
                                              autoLoad: false,
                                              url: adminBaseUrl + 'repository/samplelog/ext/json',
                                              remoteSort: true,
                                              restful: true,
                                              listeners: {'load':MA.DSLoaded,
                                              'loadexception':MA.DSLoadException},
                                              sortInfo: {
                                                  field: 'id',
                                                  direction: 'DESC'
                                              }
                                              }
                                              );

var clientSampleStore = new Ext.data.GroupingStore(
                                              {
                                              storeId: 'clientsamples',
                                              autoLoad: false,
                                              url: wsBaseUrl + 'recordsSamplesForClient/client/',
                                              root: 'rows',
                                              totalProperty: 'results',
                                              id: 'id',
                                              fields: ['id','experiment_id','experiment_title','label','weight','comment','sample_class','last_status'],
                                              reader:new Ext.data.JsonReader({}),
                                              sortInfo: {
                                                  field: 'id',
                                                  direction: 'DESC'
                                              },
                                              groupField:'experiment_id'
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

var experimentRunStore = new Ext.data.JsonStore(
                                                {
                                                storeId: 'experimentRunStore',
                                                autoLoad: true,
                                                url: adminBaseUrl + "repository/run/ext/json",
                                                restful: true,
                                                listeners: {'load':MA.DSLoaded,
                                                'loadexception':MA.DSLoadIgnoreException
                                                },
                                                sortInfo: {
                                                field: 'id',
                                                direction: 'DESC'
                                                }
                                                }
                                                );

var selectableRunStore = new Ext.data.JsonStore(
                        {
                            storeId: 'run',
                            autoLoad: true,
                            url: adminBaseUrl + "repository/run/ext/json?state=0",
                            restful: true,
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadIgnoreException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                                         
var runStore = new Ext.data.JsonStore(
                        {
                            storeId: 'run',
                            autoLoad: true,
                            url: adminBaseUrl + "repository/run/ext/json",
                            restful: true,
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadIgnoreException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );
                    
var runSampleStore = new Ext.data.JsonStore(
                        {
                            storeId: 'runsamples',
                            autoLoad: true,
                            url: adminBaseUrl + "repository/sample/ext/json?run__id__exact=0",
                            restful: true,
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadIgnoreException
                            },
                            sortInfo: {
                                field: 'id',
                                direction: 'DESC'
                            }
                        }
                    );

var machineStore = new Ext.data.JsonStore(
{
    storeId: 'machineStore',
    autoLoad: true,
    url: adminBaseUrl + 'mdatasync_server/nodeclient/ext/json',
    restful: false,
    listeners: {'load':MA.DSLoaded,
        'loadexception':MA.DSLoadIgnoreException
    },
    sortInfo: {
        field: 'id',
        direction: 'DESC'
    }
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
                                        'loadexception':MA.DSLoadIgnoreException}
                        }
                    );

var plantComboStore = new Ext.data.JsonStore(
                                                    {
                                                    storeId: 'plantCombo',
                                                    autoLoad: false,
                                                    url: wsBaseUrl + 'populate_select/plantinfo/development_stage/',
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
                            url: wsBaseUrl + 'populate_select/animalinfo/parental_line/',
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
                                        'loadexception':MA.DSLoadIgnoreException}
                        }
                    );

var clientComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'clientCombo',
                            autoLoad: true,
                            url: adminBaseUrl + "auth/user/ext/json?run__id__exact=0",
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                            'loadexception':MA.DSLoadIgnoreException}
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
                                        'loadexception':MA.DSLoadIgnoreException}
                        }
                    );
                    
var expStatusComboStore = new Ext.data.JsonStore(
                        {
                            storeId: 'expStatusCombo',
                            autoLoad: true,
                            url: wsBaseUrl + 'populate_select/experimentstatus/id/name',
                            root: 'response.value.items',
                            fields: ['value', 'key'],
                            listeners: {'load':MA.DSLoaded,
                                        'loadexception':MA.DSLoadIgnoreException}
                        }
                    );

var methodStore = new Ext.data.JsonStore({
    autoLoad:true,
    storeId:'methodStore',
    url: wsBaseUrl + 'populate_select/instrumentmethod/id/title/',
    root: 'response.value.items',
    fields: ['key', 'value']
});