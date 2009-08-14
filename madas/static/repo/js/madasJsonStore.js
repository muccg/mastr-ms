Ext.madasJsonStore = Ext.extend(Ext.data.Store, {

                                constructor: function(config){
                                Ext.madasJsonStore.superclass.constructor.call(this, Ext.apply(config, {
                                                                                               reader: new Ext.madasJsonReader(config)
                                                                                               }));
                                }
                                });
Ext.reg('madasjsonstore', Ext.madasJsonStore);