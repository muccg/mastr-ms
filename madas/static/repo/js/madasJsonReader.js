/*
 * MA.JsonReader
 * 
 * extending the JsonReader to pick up additional info such as authenticated, authorized, etc.
 *
 * This file is part of Madas.
 *
 * Madas is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Madas is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Madas.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 * madasAjaxMetadataProcess
 * look at the other headers in the header of an ajax request for a livegrid or other Object
 * assessing whether the user has timed-out or is not authorized to perform that action
 */
MA.AjaxMetadataProcess = function(ajaxData) {
    
    //look for specific sentinel values in the json
    //var authenticated = ajaxData.response.value.authenticated;
    //var authorized = ajaxData.response.value.authorized;
    var authenticated = ajaxData.authenticated;
    var authorized = ajaxData.authorized;
    
    if (authenticated != 1) {
        //trigger the login page
        MA.IsLoggedIn = false;
        MA.IsAdmin = false;
        Ext.getCmp('userMenu').setText('User: none');
        
        MA.ChangeMainContent('login');
        //return false to tell the JsonReader to abort
        return false;
    }
    
    if (authorized != 1) {
        //trigger a notauthorized page
        MA.ChangeMainContent('notauthorized');
        //return false to tell the JsonReader to abort
        return false;
    }
    
    return true;
    
}



MA.JsonReader = function(meta, recordType){
    MA.JsonReader.superclass.constructor.call(this, meta, recordType);
};


Ext.extend(MA.JsonReader, Ext.data.JsonReader, {
    
    /**
     * @cfg {String} versionProperty Name of the property from which to retrieve the 
     *                               version of the data repository this reader parses 
     *                               the reponse from
     */   

    read : function(response){
        var json = response.responseText;
        var ob = eval("("+json+")");
        if(!ob) {
            throw {message: "JsonReader.read: Json object not found"};
        }
        if(ob.metaData){
            delete this.ef;
            this.meta = ob.metaData;
            this.recordType = Ext.data.Record.create(ob.metaData.fields);
            this.onMetaChange(this.meta, this.recordType, ob);
        }
        return this.readRecords(ob);
    },

    /**
     * Create a data block containing Ext.data.Records from a JSON object.
     * @param {Object} o An object which contains an Array of row objects in the property specified
     * in the config as 'root, and optionally a property, specified in the config as 'totalProperty'
     * which contains the total size of the dataset.
     * @return {Object} data A data block which is used by an Ext.data.Store object as
     * a cache of Ext.data.Records.
     */
    readRecords : function(oc)
    {
        // o is the ajax response, already evald
        //we pass on to the generic AJAX metadata processor to intercept 
        var aaPass = MA.AjaxMetadataProcess(oc);
        if (aaPass) {
            //from here below is a copy-and-paste of the Ext standard code
        
            /**
             * After any data loads, the raw JSON data is available for further custom processing.  If no data is
             * loaded or there is a load exception this property will be undefined.
             * @type Object
             */
            this.jsonData = oc;
            var s = this.meta, Record = this.recordType,
                f = Record.prototype.fields, fi = f.items, fl = f.length;
    
    //      Generate extraction functions for the totalProperty, the root, the id, and for each field
            if (!this.ef) {
                if(s.totalProperty) {
                        this.getTotal = this.getJsonAccessor(s.totalProperty);
                    }
                    if(s.successProperty) {
                        this.getSuccess = this.getJsonAccessor(s.successProperty);
                    }
                    this.getRoot = s.root ? this.getJsonAccessor(s.root) : function(p){return p;};
                    if (s.id) {
                            var g = this.getJsonAccessor(s.id);
                            this.getId = function(rec) {
                                    var r = g(rec);
                                    return (r === undefined || r === "") ? null : r;
                            };
                    } else {
                            this.getId = function(){return null;};
                    }
                this.ef = [];
                for(var i = 0; i < fl; i++){
                    f = fi[i];
                    var map = (f.mapping !== undefined && f.mapping !== null) ? f.mapping : f.name;
                    this.ef[i] = this.getJsonAccessor(map);
                }
            }
    
            var root = this.getRoot(oc), c = root.length, totalRecords = c, success = true;
            if(s.totalProperty){
                var v = parseInt(this.getTotal(oc), 10);
                if(!isNaN(v)){
                    totalRecords = v;
                }
            }
            if(s.successProperty){
                var v = this.getSuccess(oc);
                if(v === false || v === 'false'){
                    success = false;
                }
            }
            var records = [];
            for(var i = 0; i < c; i++){
                    var n = root[i];
                var values = {};
                var id = this.getId(n);
                for(var j = 0; j < fl; j++){
                    f = fi[j];
                var v = this.ef[j](n);
                values[f.name] = f.convert((v !== undefined) ? v : f.defaultValue);
                }
                var record = new Record(values, id);
                record.json = n;
                records[i] = record;
            }
            return {
                success : success,
                records : records,
                totalRecords : totalRecords
            };    
            
        } else {
           return { success : false, records : [], totalRecords : 0 };
        } 
    }
    
});
