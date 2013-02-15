# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349677863.3797929
_enable_loop = True
_template_filename = '/usr/local/src/mastrms/mastrms/templates/mako/index.mako'
_template_uri = 'index.mako'
_source_encoding = 'ascii'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        username = context.get('username', UNDEFINED)
        mainContentFunction = context.get('mainContentFunction', UNDEFINED)
        APP_SECURE_URL = context.get('APP_SECURE_URL', UNDEFINED)
        params = context.get('params', UNDEFINED)
        wh = context.get('wh', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n<head>\n<!--\n * This file is part of Madas.\n *\n * Madas is free software: you can redistribute it and/or modify\n * it under the terms of the GNU General Public License as published by\n * the Free Software Foundation, either version 3 of the License, or\n * (at your option) any later version.\n *\n * Madas is distributed in the hope that it will be useful,\n * but WITHOUT ANY WARRANTY; without even the implied warranty of\n * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n * GNU General Public License for more details.\n *\n * You should have received a copy of the GNU General Public License\n * along with Madas.  If not, see <http://www.gnu.org/licenses/>.\n *\n -->\n    <title>MA LIMS</title>\n\n<link rel="shortcut icon" href="/favicon.ico" />\n<link rel="stylesheet" href="')
        # SOURCE LINE 24
        __M_writer(unicode(wh.url('/static/ext-3.4.0/resources/css/ext-all.css')))
        __M_writer(u'"/>\n<link rel="stylesheet" type="text/css" href="')
        # SOURCE LINE 25
        __M_writer(unicode(wh.url('/static/css/main.css')))
        __M_writer(u'"/>\n<link rel="stylesheet" href="')
        # SOURCE LINE 26
        __M_writer(unicode(wh.url('/static/css/RowEditor.css')))
        __M_writer(u'"/>\n<link rel="stylesheet" type="text/css" href="')
        # SOURCE LINE 27
        __M_writer(unicode(wh.url('/static/css/file-upload.css')))
        __M_writer(u'"/>\n<!--\n<script type="text/javascript" src="')
        # SOURCE LINE 29
        __M_writer(unicode(wh.url('/static/js/repo/scriptaculous/scriptaculous.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 30
        __M_writer(unicode(wh.url('/static/js/repo/prototype.js')))
        __M_writer(u'"></script>\n<script src="')
        # SOURCE LINE 31
        __M_writer(unicode(wh.url('/static/ext-3.4.0/adapter/ext/ext-base.js')))
        __M_writer(u'" type="text/javascript"></script>\n<script src="')
        # SOURCE LINE 32
        __M_writer(unicode(wh.url('/static/ext-3.4.0/adapter/prototype/ext-prototype-adapter.js')))
        __M_writer(u'" type="text/javascript"></script>\n<script src="')
        # SOURCE LINE 33
        __M_writer(unicode(wh.url('/static/ext-3.3.0/ext-all.js')))
        __M_writer(u'"></script>\n-->\n<script type="text/javascript" src="')
        # SOURCE LINE 35
        __M_writer(unicode(wh.url('/static/js/repo/prototype.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 36
        __M_writer(unicode(wh.url('/static/js/repo/scriptaculous/scriptaculous.js')))
        __M_writer(u'"></script>\n<script src="')
        # SOURCE LINE 37
        __M_writer(unicode(wh.url('/static/ext-3.4.0/adapter/ext/ext-base-debug.js')))
        __M_writer(u'" type="text/javascript"></script>\n<!--<script src="')
        # SOURCE LINE 38
        __M_writer(unicode(wh.url('/static/ext-3.4.0/adapter/ext/ext-base.js')))
        __M_writer(u'" type="text/javascript"></script>-->\n<script src="')
        # SOURCE LINE 39
        __M_writer(unicode(wh.url('/static/ext-3.4.0/ext-all-debug.js')))
        __M_writer(u'"></script>\n<!--<script src="')
        # SOURCE LINE 40
        __M_writer(unicode(wh.url('/static/ext-3.4.0/ext-all.js')))
        __M_writer(u'"></script>-->\n<script type="text/javascript" src="')
        # SOURCE LINE 41
        __M_writer(unicode(wh.url('/static/js/repo/DisplayField.js')))
        __M_writer(u'"></script>\n\n<!-- setup variable -->\n<script>\nExt.ns(\'MA\', \'MA.Dashboard\', \'MA.Utils\');\nMA.BaseUrl = \'')
        # SOURCE LINE 46
        __M_writer(unicode( APP_SECURE_URL ))
        __M_writer(u'\';\nif(Ext.isIE6 || Ext.isIE7 || Ext.isAir){ Ext.BLANK_IMAGE_URL = "')
        # SOURCE LINE 47
        __M_writer(unicode(wh.url('/static/images/default/s.gif')))
        __M_writer(u'"; }\n</script>\n\n<!-- Madas scripts -->\n<script type="text/javascript" src="')
        # SOURCE LINE 51
        __M_writer(unicode(wh.url('/static/js/FieldLabeler.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 52
        __M_writer(unicode(wh.url('/static/js/utils.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 53
        __M_writer(unicode(wh.url('/static/js/global.js')))
        __M_writer(u'"></script>\n\n<script type="text/javascript" src="')
        # SOURCE LINE 55
        __M_writer(unicode(wh.url('/static/js/json2.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 56
        __M_writer(unicode(wh.url('/static/js/repo/datastores.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 57
        __M_writer(unicode(wh.url('/static/js/repo/renderers.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 58
        __M_writer(unicode(wh.url('/static/js/repo/GridSearch.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 59
        __M_writer(unicode(wh.url('/static/js/repo/MARowEditor.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 60
        __M_writer(unicode(wh.url('/static/js/FileUploadField.js')))
        __M_writer(u'"></script>\n\n\n\n<script type="text/javascript" src="')
        # SOURCE LINE 64
        __M_writer(unicode(wh.url('/static/js/repo/samples.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 65
        __M_writer(unicode(wh.url('/static/js/repo/tracking.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 66
        __M_writer(unicode(wh.url('/static/js/repo/biosource.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 67
        __M_writer(unicode(wh.url('/static/js/repo/treatment.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 68
        __M_writer(unicode(wh.url('/static/js/repo/sampleprep.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 69
        __M_writer(unicode(wh.url('/static/js/repo/access.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 70
        __M_writer(unicode(wh.url('/static/js/repo/files.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 71
        __M_writer(unicode(wh.url('/static/js/repo/runs.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 72
        __M_writer(unicode(wh.url('/static/js/repo/runlist.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 73
        __M_writer(unicode(wh.url('/static/js/repo/rulegenerators.js')))
        __M_writer(u'"></script>\n\n<script type="text/javascript" src="')
        # SOURCE LINE 75
        __M_writer(unicode(wh.url('/static/js/repo/projects.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 76
        __M_writer(unicode(wh.url('/static/js/repo/clients.js')))
        __M_writer(u'"></script>\n\n<script type="text/javascript" src="')
        # SOURCE LINE 78
        __M_writer(unicode(wh.url('/static/js/datastores.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 79
        __M_writer(unicode(wh.url('/static/js/menu.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 80
        __M_writer(unicode(wh.url('/static/js/registration.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 81
        __M_writer(unicode(wh.url('/static/js/login.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 82
        __M_writer(unicode(wh.url('/static/js/controller.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 83
        __M_writer(unicode(wh.url('/static/js/dashboard.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 84
        __M_writer(unicode(wh.url('/static/js/admin.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 85
        __M_writer(unicode(wh.url('/static/js/user.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 86
        __M_writer(unicode(wh.url('/static/js/quote.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 87
        __M_writer(unicode(wh.url('/static/js/swfobject.js')))
        __M_writer(u'"></script>\n<script type="text/javascript" src="')
        # SOURCE LINE 88
        __M_writer(unicode(wh.url('/static/js/screencasts.js')))
        __M_writer(u'"></script>\n<script>\nvar callbackCount = 0;\nfunction callbacker(){\n    var username = document.getElementById(\'username\').value;\n    \n    if (username == "" && callbackCount < 5) {\n        //console.log("waiting...");\n        callbackCount += 1;\n        window.setTimeout("callbacker();", 100);\n        return;\n    }\n    \n    MA.InitApplication(\'')
        # SOURCE LINE 101
        __M_writer(unicode( APP_SECURE_URL ))
        __M_writer(u"', '")
        __M_writer(unicode( username ))
        __M_writer(u"', '")
        __M_writer(unicode( mainContentFunction ))
        __M_writer(u"', '")
        __M_writer(unicode( params ))
        __M_writer(u'\');\n    document.getElementById("appLoad").style.display = "none";\n    //document.getElementById(\'loginDiv\').style.display = \'none\';\n}\n</script>\n\n</head>\n<body onLoad="callbacker();">\n\n<div id="north"><div id="appTitle">MA LIMS</div><div id="toolbar"></div></div>\n\n<div id="south">(c) CCG 2009-2012</div>\n\n\n<div style="position:relative;">\n<div id="appLoad" style="z-index:1;position:absolute;left:0px;top:0px;width:400px;height:200px;background:white;padding:200px;"><img src="')
        # SOURCE LINE 116
        __M_writer(unicode(wh.url('static/ext-3.4.0/resources/images/default/shared/large-loading.gif')))
        __M_writer(u'"> Loading...</div>\n<div id="loginDiv" style="width:300;">\n<form id="loginForm" action="')
        # SOURCE LINE 118
        __M_writer(unicode(wh.url('/login/processLogin')))
        __M_writer(u'" method="POST">\n<label class="x-form-item-label">Email address:</label>\n<div class="x-form-element" style="margin-top:-10px;">\n<input id="username" name="username">\n</div>\n<div class="x-form-clear-left">\n</div>\n<label class="x-form-item-label">Password:</label>\n<div class="x-form-element" style="margin-top:-10px;">\n<input id="password" name="password" type="password">\n</div>\n<div class="x-form-clear-left">\n</div>\n<input type="submit" value="Login" style="margin-left:200px;">\n</form>\n</div>\n\n<div id="centerDiv"></div>\n\n\n\n<form id="hiddenForm"></form>\n\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


