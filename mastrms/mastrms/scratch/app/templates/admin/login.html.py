# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349769489.6535931
_enable_loop = True
_template_filename = u'/usr/local/webapps/mastrms/virtualenv/lib/python2.6/site-packages/Mango_py-1.3.1_ccg1_3-py2.6.egg/django/contrib/admin/templates/mako/admin/login.html'
_template_uri = 'admin/login.html'
_source_encoding = 'ascii'
_exports = ['block_breadcrumbs', 'block_content', 'block_bodyclass', 'block_stylesheet', 'block_content_title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.ModuleNamespace(u'admin', context._clean_inheritance_tokens(), callables=None, calling_uri=_template_uri, module=u'django.contrib.admin.templatetags.adminmedia')
    context.namespaces[(__name__, u'admin')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'admin/base_site.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n\n')
        # SOURCE LINE 4
        __M_writer(unicode(self.block_stylesheet()))
        __M_writer(u'\n\n')
        # SOURCE LINE 6
        __M_writer(unicode(self.block_bodyclass()))
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        __M_writer(unicode(self.block_content_title()))
        __M_writer(u'\n\n')
        # SOURCE LINE 10
        __M_writer(unicode(self.block_breadcrumbs()))
        __M_writer(u'\n\n')
        # SOURCE LINE 12
        __M_writer(unicode(self.block_content()))
        # SOURCE LINE 38
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_breadcrumbs(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        app_path = context.get('app_path', UNDEFINED)
        csrf_token = context.get('csrf_token', UNDEFINED)
        error_message = context.get('error_message', UNDEFINED)
        csrf_tag = context.get('csrf_tag', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n\n')
        # SOURCE LINE 14
        if error_message:
            # SOURCE LINE 15
            __M_writer(u'\n<p class="errornote">')
            # SOURCE LINE 16
            __M_writer(unicode(error_message))
            __M_writer(u'</p>\n\n')
        # SOURCE LINE 19
        __M_writer(u'\n<div id="content-main">\n<form action="')
        # SOURCE LINE 21
        __M_writer(unicode(app_path))
        __M_writer(u'" method="post" id="login-form">')
        __M_writer(unicode( csrf_tag(csrf_token) ))
        __M_writer(u'\n  <div class="form-row">\n    <label for="id_username">')
        # SOURCE LINE 23
        __M_writer(unicode(trans('Username:')))
        __M_writer(u'</label> <input type="text" name="username" id="id_username" />\n  </div>\n  <div class="form-row">\n    <label for="id_password">')
        # SOURCE LINE 26
        __M_writer(unicode(trans('Password:')))
        __M_writer(u'</label> <input type="password" name="password" id="id_password" />\n    <input type="hidden" name="this_is_the_login_form" value="1" />\n  </div>\n  <div class="submit-row">\n    <label>&nbsp;</label><input type="submit" value="')
        # SOURCE LINE 30
        __M_writer(unicode(trans('Log in')))
        __M_writer(u'" />\n  </div>\n</form>\n\n<script type="text/javascript">\ndocument.getElementById(\'id_username\').focus()\n</script>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_bodyclass(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'login')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_stylesheet(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(unicode(admin_media_prefix()))
        __M_writer(u'css/login.css')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


