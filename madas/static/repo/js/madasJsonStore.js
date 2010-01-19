MA.JsonStore = Ext.extend(Ext.data.Store, {

                                constructor: function(config){
                                MA.JsonStore.superclass.constructor.call(this, Ext.apply(config, {
                                                                                               reader: new MA.JsonReader(config)
                                                                                               }));
                                }
                                });
Ext.reg('madasjsonstore', MA.JsonStore);