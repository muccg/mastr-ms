<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>

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
</script>

<script type="text/javascript" src="${wh.url('/static/js/json2.js')}"></script>
<link rel="stylesheet" type="text/css" href="${wh.url('/static/css/main.css')}"/>
<%def name="header()">
</%def>
<head>
<body>
<div style="width:700px; margin-left:50px; padding:10px">
<h2>MDatasync Utils</h2></br></br>

<div style= "padding-top:10px; padding-bottom:10px;">
<h3>Submitted Logs</h3>
<p>Number of Logs: ${len(clientlogslist)}</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num2,logname in enumerate(clientlogslist):
    <tr bgcolor="${'#f0f0f0' if num2%2 else '#e0e0e0'}"><td>${logname}</td><td><a href="${wh.url("/sync/files/synclogs/")}${logname}">${ logname }</td></tr>
%endfor
</table>
</div>

<div style= "padding-top:10px; padding-bottom:10px;">
<h3>Submitted Screenshots</h3>
<p>Number of Screenshots: ${len(shotslist) }</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num3,shotname in enumerate(shotslist):
    <tr bgcolor="${'#f0f0f0' if num3%2 else '#e0e0e0'}"><td>${shotname}</td><td><a href="${wh.url("/sync/files/synclogs/")}${shotname}">${ shotname }</a></td></tr>
%endfor
</table>
</div>
<div style= "padding-top:10px; padding-bottom:10px;">
<h3>Server Logging Level</h3>
<%
bgcol="blue"
%>
%if len(message) > 0:
%   if success:
<%        bgcol="green"%>
%   else:
<%        bgcol="red"%>
%   endif
    <div style="background-color:${bgcol}; width:100%px; color:white;">
        ${message}
    </div>
%endif
<p>Current Level: ${str(currentLogLevel)}</p>

<form action="" method="post">
    <select name="loglevel">
%for i in range(len(levelnames)):
    <option value="${levelvalues[i]}">${levelnames[i]} (${levelvalues[i]})</option>
%endfor
    </select>
    <input type="submit" value="Change" />
</form>
</div>

<script>
    function handleTail(req)
    {
        var writeroot = document.getElementById('Logcontents');
        var dataobj = JSON.parse(req.responseText);
        writeroot.innerHTML += dataobj.data;
        pos = dataobj.position;
    };
</script>

<p>Tail Log</p>
<form name='serverlogform'>
    <select name="serverlog">
%for index, serverlogname in enumerate(serverloglist):
        <option value="${serverlogname}">${serverlogname}</option>
%endfor
    </select>
</form>    


<p><input type="button" value="Tail" onclick="sendRequest('/sync/taillog/'+ getServerLogfilename() +'/50/' + pos.toString() + '/', handleTail);"></p>

<div id='Logcontents' style="height: 400px; overflow:auto;"></div>
<script>

    function getServerLogfilename()
    {
        var selectedserverlogfilename = serverlogform.serverlog.options[serverlogform.serverlog.selectedIndex].value;
        if (selectedserverlogfilename != serverlogfilename)
        {
            //clear the div
            var writeroot2 = document.getElementById('Logcontents');
            writeroot2.innerHTML = "";
            serverlogfilename = selectedserverlogfilename;
            pos = 0;
        }
        return selectedserverlogfilename;
    }    
</script>

</div>
</body>
</html>

