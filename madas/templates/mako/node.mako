<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<link rel="stylesheet" type="text/css" href="${wh.url('/static/css/main.css')}"/>
<link rel="stylesheet" type="text/css" href="${wh.url('/static/css/jquery.treeview.css')}"/>
<script type="text/javascript" src="${wh.url('/static/js/json2.js')}"></script>
<script type="text/javascript" src="${wh.url('/static/js/jquery-1.5.1.min.js')}"></script>
<script type="text/javascript" src="${wh.url('/static/js/jquery-ui-1.8.14.custom.min.js')}"></script>
<script type="text/javascript" src="${wh.url('/static/js/jquery.cookie.js')}"></script>
<script type="text/javascript" src="${wh.url('/static/js/jquery.treeview.js')}"></script>

<script>
var pos = 0;
var serverlogfilename = "";

function sendRequest(url,callback,postData) {
	var req = createXMLHTTPObject();
	if (!req) return;
	var method = (postData) ? "POST" : "GET";
	req.open(method,url,true);
	req.setRequestHeader('User-Agent','XMLHTTP/1.0');
	if (postData)
		req.setRequestHeader('Content-type','application/x-www-form-urlencoded');
	req.onreadystatechange = function () {
		if (req.readyState != 4) return;
		if (req.status != 200 && req.status != 304) {
//			alert('HTTP error ' + req.status);
			return;
		}
		callback(req);
	}
	if (req.readyState == 4) return;
	req.send(postData);
}

var XMLHttpFactories = [
	function () {return new XMLHttpRequest()},
	function () {return new ActiveXObject("Msxml2.XMLHTTP")},
	function () {return new ActiveXObject("Msxml3.XMLHTTP")},
	function () {return new ActiveXObject("Microsoft.XMLHTTP")}
];

function createXMLHTTPObject() {
	var xmlhttp = false;
	for (var i=0;i<XMLHttpFactories.length;i++) {
		try {
			xmlhttp = XMLHttpFactories[i]();
		}
		catch (e) {
			continue;
		}
		break;
	}
	return xmlhttp;
}


function updateCanvas(canvasJq, presentfiles, missingfiles){
    var canvasEl = canvasJq[0];
    canvasEl.width=canvasJq.width();
    canvasEl.height=canvasJq.height();
    console.log("Width:" + canvasEl.width);
    var cOffset = canvasJq.offset();
    var ctx = canvasEl.getContext("2d");
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);
    ctx.beginPath();

    var drawlines = function(index, element){
        var li=$(element);
        if(li.attr("rel"))
        {
            //console.log("rel was" + li.attr("rel"));
            //var srcOffset=li.offset();
            var srcOffset=li.position();
            var srcMidHeight=li.height()/2;
            console.log("Looking for #" + li.attr("rel"));
            var targetLi=$("#"+li.attr("rel"));

            if(targetLi.length)
            {
                console.log("Found target");
                //var trgOffset=targetLi.offset();
                var trgOffset=targetLi.position();
                var trgMidHeight=li.height()/2;
                
                console.log("srcOffset:" + srcOffset + ", trgOffset: " + trgOffset);
                ctx.moveTo(srcOffset.left - cOffset.left, srcOffset.top - cOffset.top + srcMidHeight);
                ctx.lineTo(trgOffset.left - cOffset.left, trgOffset.top - cOffset.top + trgMidHeight);
                //console.log("Move to:" + srcOffset.left - cOffset.left + "," +  srcOffset.top - cOffset.top + srcMidHeight )
            }
        }
    }

    $('.file').each(function(index, element){
        drawlines(index, element);
    });
    ctx.stroke();
    ctx.closePath();
}


$(document).ready(function(){
    // first example
    $("#clientfiles").treeview();
    $("#servercomplete").treeview();
    $("#serverincomplete").treeview();

    updateCanvas($("#canvas"), $(".file") );

});


</script>

<%def name="header()">
</%def>
<head>
<body>
<div style="width:700px; margin-left:50px; padding:10px">
<!--generate file structure html !-->
<% 
    def gendir(dirdict):
        # This function generates HTML needed by the treeview plugin
        # for jQuery.
        # It has to deal with the special case of the formatting of the 
        # input dict, where current path is in the key
        # called '/' (ignored), and directory contents is in the dir
        # called '.'
        retstr = "<ul>"
        for elem in dirdict:
            if elem == '/':
                pass
            
            elif elem == '.':
                retstr += gendir(dirdict[elem])
            
            elif isinstance(dirdict[elem], dict):
                retstr += '<li id=\"%s\" class="closed"><span class=\"folder\">%s</span>' % (str(elem).upper().replace('-', '_').replace('.', '_'), str(elem).upper())
                #retstr += '<li id=\"%s\"><span class=\"folder\">%s</span>' % (str(elem).upper().replace('-', '_').replace('.', '_'), str(elem).upper())
                retstr += gendir(dirdict[elem])
                retstr += '</li>'
            else:
                if dirdict[elem] is not None and dirdict[elem][3]:
                    img = wh.url('/static/images/refresh.png')
                else:
                    img = wh.url('/static/images/delete.png')
                retstr += '<li id=\"%s\"><span class=\"file\" rel="%s"><img src=\"%s\"></img>%s' % (elem+"dd", elem.replace('-', '_').replace('.', '_'), img, elem)
                retstr += '</span></li>'
        retstr += '</ul>'
        return retstr
%>

<div style="width:45%; float: left; margin: 7px;">
<h2>Client Details</h2></br></br>
    <div >
    <strong>Client Node Path:</strong>${clientstate['organisation']}.${clientstate['sitename']}.${clientstate['station']}
    </div>
    <div>
    <strong>Last Requested Sync:</strong> ${clientstate['lastSyncAttempt']} <em>(${timediff.seconds//3600}h ${ (timediff.seconds%3600)//60}m ${timediff.seconds%60}s ago)</em>
    </div>
    <strong>Client Files:</strong>
    <ul id="clientfiles" class="filetree">
        ${ gendir(clientstate['files']) }
    </ul>
</div>

<div style = "width: 45%; float: right; margin: 7px;">
<h2>Server Details</h2></br></br>
   <div>
    <strong>Default data path:</strong> ${nodeclient.default_data_path}
   </div>
   <div>
    <strong>Default username:</strong> ${nodeclient.username}
   </div>
   <div>
    <strong>Default hostname:</strong> ${nodeclient.hostname}
   </div>
   <div>
    <strong>Rsync flags:</strong> ${nodeclient.flags}
   </div>

    <div>
        <strong> Expected complete</strong> (${ len(expectedfiles['complete']) } runs)
        <ul id='servercomplete' class="filetree">
            ${ gendir(expectedfiles['complete']) }
        </ul>
    </div>
    <div>
        <strong> Expected incomplete</strong> (${ len(expectedfiles['incomplete']) } runs)
        <ul id='serverincomplete' class="filetree">
            ${ gendir(expectedfiles['incomplete']) }
        </ul>
    </div>
</div>
<!--
<ul id="browser" class="filetree">
		<li><span class="folder">Folder 1</span>
			<ul>
				<li><span class="file">Item 1.1</span></li>
			</ul>
		</li>
		<li><span class="folder">Folder 2</span>
			<ul>
				<li><span class="folder">Subfolder 2.1</span>
					<ul id="folder21">
						<li><span class="file">File 2.1.1</span></li>
						<li><span class="file">File 2.1.2</span></li>
					</ul>
				</li>
				<li><span class="file">File 2.2</span></li>
			</ul>
		</li>
		<li class="closed"><span class="folder">Folder 3 (closed at start)</span>
			<ul>
				<li><span class="file">File 3.1</span></li>
			</ul>
		</li>
		<li><span class="file">File 4</span></li>
	</ul>
<div style= "padding-top:10px; padding-bottom:10px;">
-->

</div>
<canvas id="canvas" style="width:800px; height:800px; position: absolute; z-index:-1;"></canvas>
</body>
</html>

