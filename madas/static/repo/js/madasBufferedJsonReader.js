/*
 * Ext.ux.data.MadasBufferedJsonReader
 * 
 * extending the BufferedJsonReader to pick up additional info such as authenticated, authorized, etc.
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

Ext.namespace('Ext.ux.data');


Ext.ux.data.MadasBufferedJsonReader = function(meta, recordType){
    
    Ext.ux.data.MadasBufferedJsonReader.superclass.constructor.call(this, meta, recordType);
};


Ext.extend(Ext.ux.data.MadasBufferedJsonReader, Ext.ux.data.BufferedJsonReader, {
    
    /**
     * @cfg {String} versionProperty Name of the property from which to retrieve the 
     *                               version of the data repository this reader parses 
     *                               the reponse from
     */   

    

    /**
     * Create a data block containing Ext.data.Records from a JSON object.
     * @param {Object} o An object which contains an Array of row objects in the property specified
     * in the config as 'root, and optionally a property, specified in the config as 'totalProperty'
     * which contains the total size of the dataset.
     * @return {Object} data A data block which is used by an Ext.data.Store object as
     * a cache of Ext.data.Records.
     */
    readRecords : function(o)
    {
        // o is the ajax response, already evald
        //we pass on to the generic AJAX metadata processor to intercept 

        var aaPass = Ext.madasAjaxMetadataProcess(o);
        
        if (aaPass) {
            var s = this.meta;
            
            if(!this.ef && s.versionProperty) {
                this.getVersion = this.getJsonAccessor(s.versionProperty);
            }
            
            // shorten for future calls
            if (!this.__readRecords) {
                this.__readRecords = Ext.ux.data.BufferedJsonReader.superclass.readRecords;
            }
            
            var intercept = this.__readRecords.call(this, o);
            
            
            if (s.versionProperty) {
                var v = this.getVersion(o);
                intercept.version = (v === undefined || v === "") ? null : v;
            }
    
            
            return intercept;
        } else {
            return null;
        } 
    }
    
});
