<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <link rel="stylesheet" href="static/ext-3.1.0/resources/css/ext-all.css"/>
    <link rel="stylesheet" href="static/repo/main.css"/>
    <link rel="stylesheet" href="static/ext-3.1.0/examples/ux/css/RowEditor.css"/>
    <link rel="stylesheet" type="text/css" href="static/css/file-upload.css"/>

    <!-- <script type='text/javascript' src='http://getfirebug.com/releases/lite/1.2/firebug-lite-compressed.js'></script> -->

    <script src="static/repo/js/prototype.js" type="text/javascript"></script>
    <script src="static/repo/js/scriptaculous/scriptaculous.js" type="text/javascript"></script>
    <script src="static/ext-3.1.0/adapter/prototype/ext-prototype-adapter.js" type="text/javascript"></script>
<!--    <script src="static/ext-3.1.0/adapter/ext/ext-base-debug.js" type="text/javascript"></script>-->
    <script src="static/ext-3.1.0/ext-all-debug.js"></script>
    <script src="static/ext-3.1.0/examples/ux/RowEditor.js"></script>
    <script type="text/javascript" src="static/js/FileUploadField.js"></script>


    <script>
    Ext.ns('MA');
    var baseUrl = '${ APP_SECURE_URL }';
    </script>

<!--    <script src="static/repo/js/data.JsonReader.js" type="text/javascript"></script>-->
<!--    <script src="static/repo/js/madasJsonStore.js" type="text/javascript"></script>-->

    <script src="static/repo/js/menucontroller.js" type="text/javascript"></script>
    <script src="static/repo/js/login.js" type="text/javascript"></script>
    <script src="static/repo/js/datastores.js" type="text/javascript"></script>

    <script src="static/repo/js/renderers.js" type="text/javascript"></script>
    <script src="static/repo/js/samples.js" type="text/javascript"></script>
    <script src="static/repo/js/tracking.js" type="text/javascript"></script>
    <script src="static/repo/js/biosource.js" type="text/javascript"></script>
    <script src="static/repo/js/treatment.js" type="text/javascript"></script>
    <script src="static/repo/js/sampleprep.js" type="text/javascript"></script>
    <script src="static/repo/js/access.js" type="text/javascript"></script>
    <script src="static/repo/js/experimentlist.js" type="text/javascript"></script>
    <script src="static/repo/js/projects.js" type="text/javascript"></script>
    <script src="static/repo/js/clients.js" type="text/javascript"></script>
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
    
    MA.InitApplication();
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
<div id="appLoad" style="display:none;z-index:1;position:absolute;left:0px;top:0px;width:400px;height:200px;background:white;padding:200px;"><img src="static/ext-3.1.0/resources/images/default/shared/large-loading.gif"> Loading...</div>
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

    <div id="south">(c) CCG 2009</div>
    <form id="hiddenForm"></form>
    
    
    </body>
</html>
