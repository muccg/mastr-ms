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

Ext.madasScreencastsInit = function (vidFile) {
    var s = new SWFObject(Ext.madasBaseUrl + "static/screencasts/flvplayer.swf","player","1280","740","7");
	s.addParam("allowfullscreen","true");
	s.addVariable("file",vidFile);
	s.addVariable("width","1024");
	s.addVariable("height","762");
	s.addVariable("displayheight","762");
	s.addVariable("overstretch","fit");
	s.write("screencast-placeholder");

    //allow the madas changeMainContent function to handle the rest from here
    return;
};

Ext.madasScreencastsCmp = {
    id:'screencasts-container-panel', 
    layout:'absolute', 
    items: [
        { html:'<p id="screencast-placeholder">You must have flash installed to view this screencast</p>'
        }
    ]
};
