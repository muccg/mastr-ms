<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <link rel="stylesheet" href="static/repo/ext-3.0.0/resources/css/ext-all.css"/>
    <link rel="stylesheet" href="static/repo/main.css"/>
    <link rel="stylesheet" href="static/repo/ext-3.0.0/examples/ux/css/RowEditor.css"/>
    <link rel="stylesheet" type="text/css" href="static/css/file-upload.css"/>

    <!-- <script type='text/javascript' src='http://getfirebug.com/releases/lite/1.2/firebug-lite-compressed.js'></script> -->

    <script src="static/repo/ext-3.0.0/adapter/ext/ext-base-debug.js" type="text/javascript"></script>
    <script src="static/repo/ext-3.0.0/ext-all-debug.js"></script>
    <script src="static/repo/ext-3.0.0/examples/ux/RowEditor.js"></script>
    <script type="text/javascript" src="static/js/FileUploadField.js"></script>


    <script>
    var baseUrl = '${ APP_SECURE_URL }';
    </script>

    <script src="static/repo/js/madasJsonReader.js" type="text/javascript"></script>
    <script src="static/repo/js/madasJsonStore.js" type="text/javascript"></script>

    <script src="static/repo/js/menucontroller.js" type="text/javascript"></script>
    <script src="static/repo/js/login.js" type="text/javascript"></script>
    <script src="static/repo/js/datastores.js" type="text/javascript"></script>

    <script src="static/repo/js/renderers.js" type="text/javascript"></script>
    <script src="static/repo/js/samples.js" type="text/javascript"></script>
    <script src="static/repo/js/biosource.js" type="text/javascript"></script>
    <script src="static/repo/js/growth.js" type="text/javascript"></script>
    <script src="static/repo/js/treatment.js" type="text/javascript"></script>
    <script src="static/repo/js/sampleprep.js" type="text/javascript"></script>
    <script src="static/repo/js/access.js" type="text/javascript"></script>
    <script src="static/repo/js/experimentlist.js" type="text/javascript"></script>
    <script src="static/repo/js/files.js" type="text/javascript"></script>
    
    <script src="static/repo/js/controller.js" type="text/javascript"></script>
    <script src="static/repo/js/menu.js" type="text/javascript"></script>

<script>
var callbackCount = 0;
function callbacker(){
    var username = document.getElementById('username').value;
    
    if (username == "" && callbackCount < 10) {
        //console.log("waiting...");
        callbackCount += 1;
        window.setTimeout("callbacker();", 100);
        return;
    }
    
    Ext.madasInitApplication();
    //'${ APP_SECURE_URL }', '${ username }', '${ mainContentFunction }', '${ params }');
    document.getElementById("appLoad").style.display = "none";
    document.getElementById("hidePass").style.display = "block";
    document.getElementById("hideUser").style.display = "block";
}
</script>

</head>
<body onLoad="callbacker();">

    <div id="north"><div id="appTitle">MASTR MS</div><div id="toolbar"></div></div>

<div style="position:relative;">
<div id="appLoad" style="display:none;z-index:1;position:absolute;left:0px;top:0px;width:400px;height:200px;background:white;padding:200px;"><img src="static/js/ext/resources/images/default/shared/large-loading.gif"> Loading...</div>
<div id="loginDiv">
<form id="loginForm" action="login/processLogin" method="POST">
<div class="x-form-item" id="hideUser"><label class="x-form-item-label">Email address:</label>
<div class="x-form-element">
<input id="username" name="username">
</div>
</div>
<div class="x-form-clear-left">
</div>
<div class="x-form-item" id="hidePass"><label class="x-form-item-label">Password:</label>
<div class="x-form-element">
<input id="password" name="password" type="password">
</div>
<div class="x-form-clear-left">
</div>
<input type="submit" value="Login" style="margin-left:200px;">
</form>
</div>
</div>

<div id="centerDiv"></div>

    <div id="south">(c) CCG 2008</div>
    <form id="hiddenForm"></form>
    <ul id="experiment-nav" class="x-hidden" onclick="javascript:Ext.madasActions['expDetails'];">
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expDetails" href="#">experiment details</a>
    	</li>
    	<li onclick="javascript:Ext.madasActions['expSamples'];">
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expSamples" href="#">samples/classes</a>
    	</li>
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expBioSource" href="#">biological source</a>
    	</li>
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expGrowth" href="#">growth</a>
    	</li>
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expTreat" href="#">treatment</a>
    	</li>
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expPrep" href="#">sample prep</a>
    	</li>
    	<li>
			<img src="static/repo/images/s.gif" class="icon-show-active"/>
    		<a id="expAccess" href="#">access</a>
    	</li>

    </ul>

</body>
</html>