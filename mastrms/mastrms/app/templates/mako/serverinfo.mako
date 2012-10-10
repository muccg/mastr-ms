<%def name="header()">
</%def>

<h2>Server info for request</h2>

<h3>request</h3>
<p>${str(type(request)).replace("<","&lt;").replace(">","&gt;")}</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num,item in enumerate(dir(request)):
<tr bgcolor="${'#f0f0f0' if num%2 else '#e0e0e0'}"><td>${item}</td><td>${ str(getattr(request,item)).replace("<","&lt;").replace(">","&gt;") }</td></tr>
%endfor
</table>

<h3>settings</h3>
<p>${str(type(s)).replace("<","&lt;").replace(">","&gt;")}</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num2,item2 in enumerate(dir(s)):
<tr bgcolor="${'#f0f0f0' if num2%2 else '#e0e0e0'}"><td>${item2}</td><td>${ str(getattr(s,item2)).replace("<","&lt;").replace(">","&gt;") }</td></tr>
%endfor
</table>

<h3>globals</h3>
<p>${str(type(g)).replace("<","&lt;").replace(">","&gt;")}</p>

<table numcols=2 cellpadding=3 cellspacing=0>
%for num3,item3 in enumerate(g.keys()):
<tr bgcolor="${'#f0f0f0' if num3%2 else '#e0e0e0'}"><td>${item3}</td><td>${ str(g[item3]).replace("<","&lt;").replace(">","&gt;") }</td></tr>
%endfor
</table>
