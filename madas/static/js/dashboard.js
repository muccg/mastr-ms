/**
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


MA.DownloadClientFile = function(fileID) {
    window.location = MA.BaseUrl + "ws/downloadClientFile/" + fileID;
};

function clientFileActionRenderer(val) {
    return '<a href="#" onclick="MA.DownloadClientFile(\''+val+'\')">download</a>';
}

MA.DashboardCmp = { 
    id: 'dashboard-panel', 
    layout: 'fit', 
    title: 'Dashboard', 
    xtype: 'grid',
    style: 'padding:40px;',
    ds: new Ext.data.GroupingStore({
        id         : 'bSId',
        autoLoad   : true,
        sortInfo   : {field: 'filepath', direction: 'DESC'},
        url        : MA.BaseUrl + "ws/recordsClientFiles/",
        reader     : new Ext.data.JsonReader({
            root            : 'response.value.items',
            versionProperty : 'response.value.version',
            totalProperty   : 'response.value.total_count'
            }, [
                {
                     "type": "int", 
                     "name": "id"
                 }, 
                 {
                     "type": "auto", 
                     "name": "experiment"
                 }, 
                 {
                     "type": "string", 
                     "name": "experiment__unicode"
                 }, 
                 {
                     "type": "auto", 
                     "name": "filepath"
                 }, 
                 {
                     "type": "boolean", 
                     "name": "downloaded"
                 }, 
                 {
                     "type": "date", 
                     "name": "sharetimestamp"
                 }, 
                 {
                     "type": "auto", 
                     "name": "sharedby"
                 }, 
                 {
                     "type": "string", 
                     "name": "sharedby__unicode"
                 }
            ]),
        groupField : 'experiment__unicode'
        }),
    view: new Ext.grid.GroupingView({
        loadMask : { msg : 'Please wait...' },
        forceFit: true,
        groupTextTpl: ' {text}',
        hideGroupedColumn: true
        }),
    sm: new Ext.grid.RowSelectionModel({ singleSelect: true }),
    columns: [
        {header: 'Experiment', align : 'left', sortable: true, dataIndex: 'experiment__unicode' },
        {header: 'File', align : 'left', sortable: true, dataIndex: 'filepath' },
        {header: 'Shared by', align : 'left', sortable: true, dataIndex: 'sharedby__unicode' },
        {header: 'Actions', sortable:false, dataIndex: 'id', renderer: clientFileActionRenderer }
        ]
};