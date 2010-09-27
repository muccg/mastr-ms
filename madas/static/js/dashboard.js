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
    title:'Available files',
    style:'padding:40px',
    tbar:[
        {
            xtype:'tbtext',
            text:'Click a filename to download (folders cannot be downloaded)'
        }
    ],
    items:[
                {
                   xtype:'treepanel',
                   border: false,
                   autoScroll: true,
                   animate: true,
                   useArrows: true,
                   dataUrl:MA.BaseUrl + 'ws/recordsClientFiles',
                   requestMethod:'GET',
                   root: {
                       nodeType: 'async',
                       text: 'Files',
                       draggable: false,
                       id: 'dashboardFilesRoot'
                   },
                   selModel: new Ext.tree.DefaultSelectionModel(
                       { listeners:
                           {
                               selectionchange: function(sm, node) {
                                   if (node != null && node.isLeaf()) {
                                       MA.DownloadClientFile(node.id);
                                   }
                               }
                           }
                       }),
                   listeners:{
                        render: function() {
                        }
                    }
               }
       ]
   };