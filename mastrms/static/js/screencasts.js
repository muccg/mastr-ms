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

MA.ScreencastsInit = function (vidFile) {
    var s = new SWFObject(MA.BaseUrl + "static/screencasts/flvplayer.swf","player","1280","740","7");
	s.addParam("allowfullscreen","true");
    s.addParam("wmode", "opaque");
	s.addVariable("file",vidFile);
	s.addVariable("width","1024");
	s.addVariable("height","762");
	s.addVariable("displayheight","762");
	s.addVariable("overstretch","fit");
	s.write("screencast-placeholder");

    //allow the madas changeMainContent function to handle the rest from here
    return;
};

MA.ScreencastsCmp = {
    id:'screencasts-container-panel', 
    layout:'absolute', 
    style:'z-index:0',
    deferredRender:false,
    forceLayout:true,
    items: [
        { html:'<p id="screencast-placeholder">You must have flash installed to view this screencast</p>'
        }
    ]
};
