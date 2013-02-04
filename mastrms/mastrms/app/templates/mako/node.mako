<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}css/main.css"/>
<link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}css/jquery.treeview.css"/>
<script type="text/javascript" src="{{ STATIC_URL }}js/json2.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}js/jquery/jquery-1.5.1.min.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}js/jquery/jquery-ui-1.8.14.custom.min.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}js/jquery/jquery.cookie.js"></script>
<script type="text/javascript" src="{{ STATIC_URL }}js/jquery/jquery.treeview.js"></script>

<style type="text/css">
.missingchild { border: 2px solid #ffaaaa; -webkit-border-radius: 5px; -moz-border-radius: 5px; z-index: -1; }
</style>

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
    //console.log("Width:" + canvasEl.width);
    var cOffset = canvasJq.offset();
    var ctx = canvasEl.getContext("2d");
    ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);

    var drawlines = function(index, element){
        var li=$(element);
        //console.log("missing");
        if(li.attr("rel"))
        {
	    //console.log("rel");
            var srcelem;
            if (!(li.is(":visible"))){
                srcElem = li.parents(".closed")
            }
            else {
                srcElem = li;
            }


            var srcOffset=srcElem.offset();
            var srcMidHeight=srcElem.height()/2;
            var targetLi=$("#"+li.attr("rel"));

            if(targetLi.length)
            {
                //console.log("Found target");
                var trgOffset=targetLi.offset();
                var trgMidHeight=targetLi.height()/2;
                ctx.moveTo(srcOffset.left - cOffset.left, srcOffset.top - cOffset.top + srcMidHeight);
                ctx.lineTo(trgOffset.left + targetLi.width()/2 - cOffset.left, trgOffset.top - cOffset.top + trgMidHeight);
            }
        }
    }

    ctx.save()
    ctx.beginPath();
    ctx.strokeStyle = "#00FF00";
    presentfiles.each(function(index, element){
        drawlines(index, element);
    });
    ctx.stroke();
    ctx.closePath();
    ctx.restore()

    ctx.save()
    ctx.beginPath();
    ctx.strokeStyle = "#FF0000";
    missingfiles.each(function(index, element){
	drawlines(index, element);
    });
    ctx.stroke();
    ctx.closePath(); 
    ctx.restore();
}

function updatelines(){
    
    updateCanvas($("#canvas"), $(".present"), $(".missing") );
}

function updateFolders(){
    //var subs = $(".folder").children()
    //for (var fileindex = 0; fileindex<subs.length(); fileindex++){
    //    if 
    //}

    $(".missing").parent().parent().parent().addClass("missingchild");
}

$(document).ready(function(){
    // first example
    $("#clientfiles").treeview();
    $("#servercomplete").treeview();
    $("#serverincomplete").treeview();
    updatelines();
    updateFolders();


});


</script>

<%def name="header()">
</%def>
<head>
<body>
<div style="width:700px; margin-left:50px; padding:10px;">

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
                retstr += '<li id=\"%s\" class="closed" onclick="updatelines();"><span class=\"folder\">%s</span>' % (str(elem).upper().replace('-', '_').replace('.', '_'), str(elem))
                retstr += gendir(dirdict[elem])
                retstr += '</li>'
            else:
                if dirdict[elem] is not None and dirdict[elem][3]:
                    img = wh.url('/static/images/refresh.png')
                    statusclass = "present"
                else:
                    statusclass = "missing"
                    img = wh.url('/static/images/delete.png')
                retstr += '<li id=\"%s\"><span class=\"file %s\" rel="%s"><img src=\"%s\"></img>%s' % (elem+"dd", statusclass, elem.upper().replace('-', '_').replace('.', '_'), img, elem)
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
    <div>
    <strong>Last Error Result:</strong> ${clientstate.get('lastError', "Unable to retrieve last error")}
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
<div style= "padding-top:10px; padding-bottom:10px;">

</div>
<canvas id="canvas" style="width:1000px; height:3000px; position: absolute; top: 0px; left: 0px; z-index: -1;"></canvas>
</body>
</html>

