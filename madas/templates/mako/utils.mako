<link rel="stylesheet" type="text/css" href="/static/css/main.css"/>
<%def name="header()">
</%def>

<div style="width:700px; margin-left:50px; padding:10px">
<h2>MDatasync Utils</h2></br></br>

<div style= "padding-top:10px; padding-bottom:10px;">
<h3>Submitted Logs</h3>
<p>Number of Logs: ${len(logslist)}</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num2,logname in enumerate(logslist):
    <tr bgcolor="${'#f0f0f0' if num2%2 else '#e0e0e0'}"><td>${logname}</td><td><a href=${wh.url("/sync/files/synclogs/${logname}")}>${ logname }</td></tr>
%endfor
</table>
</div>

<div style= "padding-top:10px; padding-bottom:10px;">
<h3>Submitted Screenshots</h3>
<p>Number of Screenshots: ${len(shotslist) }</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num3,shotname in enumerate(shotslist):
    <tr bgcolor="${'#f0f0f0' if num3%2 else '#e0e0e0'}"><td>${shotname}</td><td><a href=${wh.url("/sync/files/synclogs/${shotname}")}>${ shotname }</a></td></tr>
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
</div>

