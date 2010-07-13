<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
    <head>
        <title>MASTR MS</title>

        <link rel="stylesheet" href="static/ext-3.2.1/resources/css/ext-all.css"/>
        <link rel="stylesheet" href="static/repo/main.css"/>
        <link rel="stylesheet" href="static/ext-3.2.1/examples/ux/css/RowEditor.css"/>
        <link rel="stylesheet" type="text/css" href="static/css/file-upload.css"/>


        <script src="static/repo/js/prototype.js" type="text/javascript"></script>
        <script src="static/repo/js/scriptaculous/scriptaculous.js" type="text/javascript"></script>
        <script src="static/ext-3.2.1/adapter/prototype/ext-prototype-adapter.js" type="text/javascript"></script>
        <script src="static/ext-3.2.1/ext-all.js"></script>
        <script src="static/repo/js/MARowEditor.js"></script>
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
        <script src="static/repo/js/GridSearch.js" type="text/javascript"></script>

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
        <script src="static/repo/js/runs.js" type="text/javascript"></script>
        <script src="static/repo/js/runlist.js" type="text/javascript"></script>
        <script src="static/repo/js/dashboard.js" type="text/javascript"></script>
        
        <script src="static/repo/js/controller.js" type="text/javascript"></script>
        <script src="static/repo/js/menu.js" type="text/javascript"></script>

        <script type="text/javascript">
            function callbacker(){
                MA.InitApplication('${ APP_SECURE_URL }', '${ username }', '${ mainContentFunction }', '${ params }');
            }
        </script>
    </head>
    <body onload="callbacker();">
        <div id="north">
            <div id="appTitle">MASTR MS</div>
            <div id="toolbar"></div>
        </div>

        <div style="position:relative;">
            <div id="loginDiv">
                <form id="loginForm" action="login/processLogin" method="POST">
                    <div class="x-form-item" id="hideUser">
                        <label class="x-form-item-label">Email address:</label>
                        <div class="x-form-element">
                            <input id="username" name="username">
                        </div>
                    </div>

                    <div class="x-form-clear-left"></div>

                    <div class="x-form-item" id="hidePass">
                        <label class="x-form-item-label">Password:</label>
                        <div class="x-form-element">
                            <input id="password" name="password" type="password">
                        </div>
                    </div>

                    <div class="x-form-clear-left"></div>

                    <input type="submit" value="Login" style="margin-left:200px;">
                </form>
            </div>
        </div>

        <div id="centerDiv"></div>

        <div id="south">
            <span id="revision">$Rev$</span>
            <a id="copyright" href="#">Copyright information</a>
        </div>

        <div id="copyright-information" class="x-hidden">
            <p style="padding-bottom: 1em">
                MASTR MS is &copy; 2010
                <a href="http://ccg.murdoch.edu.au/" target="_new">Centre for Comparative Genomics</a>.
            </p>

            <p>
                Some icons are licensed from the
                <a href="http://everaldo.com/crystal/" target="_new">Crystal Project</a>
                under the Lesser Generic Public License.
            </p>
        </div>

        <form id="hiddenForm"></form>

        <div id="loginOverlay">
            <div id="appLoad" class="x-panel">
                <div class="x-panel-tl">
                    <div class="x-panel-tr">
                        <div class="x-panel-tc">
                            <div class="x-panel-header x-unselectable">
                                MASTR MS
                            </div>
                        </div>
                    </div>
                </div>
                <div class="x-panel-bwrap">
                    <div class="x-panel-ml">
                        <div class="x-panel-mr">
                            <div class="x-panel-mc">
                                Loading...<br/>
                                <img src="static/ext-3.2.1/resources/images/default/shared/loading-balls.gif" width="41" height="9" />
                            </div>
                        </div>
                    </div>
                    <div class="x-panel-bl x-panel-nofooter">
                        <div class="x-panel-br">
                            <div class="x-panel-bc"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
