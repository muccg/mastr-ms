# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349756344.076242
_enable_loop = True
_template_filename = u'/usr/local/src/mastrms/mastrms/app/templates/mako/admin/base.html'
_template_uri = u'admin/base.html'
_source_encoding = 'ascii'
_exports = ['block_extrahead', 'block_breadcrumbs', 'block_bodyclass', 'block_stylesheet', 'block_content_title', 'block_stylesheet_rtl', 'block_content', 'block_coltype', 'block_title', 'block_footer', 'block_branding', 'block_nav_global', 'block_blockbots', 'block_sidebar', 'block_pretitle', 'block_userlinks', 'block_extrastyle']


# SOURCE LINE 8

import django.core.urlresolvers as resolvers


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 7
    ns = runtime.ModuleNamespace(u'admin', context._clean_inheritance_tokens(), callables=None, calling_uri=_template_uri, module=u'django.contrib.admin.templatetags.adminmedia')
    context.namespaces[(__name__, u'admin')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        is_popup = context.get('is_popup', UNDEFINED)
        messages = context.get('messages', UNDEFINED)
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        next = context.get('next', UNDEFINED)
        escapejs = context.get('escapejs', UNDEFINED)
        force_escape = context.get('force_escape', UNDEFINED)
        user = context.get('user', UNDEFINED)
        LANGUAGE_CODE = context.get('LANGUAGE_CODE', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        LANGUAGE_BIDI = context.get('LANGUAGE_BIDI', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" lang="')
        # SOURCE LINE 2
        __M_writer(unicode(LANGUAGE_CODE))
        __M_writer(u'" xml:lang="')
        __M_writer(unicode(LANGUAGE_CODE))
        __M_writer(u'" \n')
        # SOURCE LINE 3
        if LANGUAGE_BIDI:
            # SOURCE LINE 4
            __M_writer(u'dir="rtl"\n')
        # SOURCE LINE 6
        __M_writer(u'>\n')
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 10
        __M_writer(u'\n<head>\n')
        # SOURCE LINE 12
        __M_writer(u'\n<title>')
        # SOURCE LINE 13
        __M_writer(unicode(self.block_title()))
        __M_writer(u'</title>\n')
        # SOURCE LINE 14
        __M_writer(u'\n')
        # SOURCE LINE 15
        __M_writer(u'\n<link rel="stylesheet" type="text/css" href="')
        # SOURCE LINE 16
        __M_writer(unicode(self.block_stylesheet()))
        __M_writer(u'" />\n<link rel="stylesheet" type="text/css" href="')
        # SOURCE LINE 17
        __M_writer(unicode(next.block_stylesheet()))
        __M_writer(u'" />\n  \n<!--[if lte IE 7]><link rel="stylesheet" type="text/css" href="{% block stylesheet_ie %}{% load adminmedia %}{% admin_media_prefix %}css/ie.css{% endblock %}" /><![endif]--> \n')
        # SOURCE LINE 20
        if LANGUAGE_BIDI:
            # SOURCE LINE 21
            __M_writer(u'<link rel="stylesheet" type="text/css" href="')
            __M_writer(unicode(self.block_stylesheet_rtl()))
            __M_writer(u'" />\n')
        # SOURCE LINE 23
        __M_writer(u'<script type="text/javascript">window.__admin_media_prefix__ = "')
        __M_writer(unicode( escapejs( admin_media_prefix() ) ))
        __M_writer(u'";</script>\n<!-- STYLES -->\n')
        # SOURCE LINE 25
        __M_writer(unicode(self.block_extrastyle()))
        __M_writer(u'\n')
        # SOURCE LINE 26
        __M_writer(unicode(self.block_extrahead()))
        __M_writer(u'\n')
        # SOURCE LINE 27
        __M_writer(unicode(self.block_blockbots()))
        __M_writer(u'\n</head>\n\n\n<body class="\n')
        # SOURCE LINE 32
        if is_popup:
            # SOURCE LINE 33
            __M_writer(u'popup \n')
        # SOURCE LINE 35
        __M_writer(unicode(self.block_bodyclass()))
        __M_writer(u'">\n\n<!-- Container -->\n<div id="container">\n\n    \n')
        # SOURCE LINE 41
        if not is_popup:
            # SOURCE LINE 42
            __M_writer(u'\n    <!-- Header -->\n    <div id="header">\n        <div id="branding">\n        ')
            # SOURCE LINE 46
            __M_writer(unicode(self.block_branding()))
            __M_writer(u'\n        </div>\n        \n')
            # SOURCE LINE 49
            if user.is_active and user.is_staff:
                # SOURCE LINE 50
                __M_writer(u'\n        <div id="user-tools">')
                # SOURCE LINE 51
                __M_writer(unicode( trans('Welcome,') ))
                __M_writer(u' <strong>\n')
                # SOURCE LINE 52
                if user.first_name:
                    # SOURCE LINE 53
                    __M_writer(unicode( force_escape(user.first_name)))
                    __M_writer(u'\n')
                    # SOURCE LINE 54
                else:
                    # SOURCE LINE 55
                    __M_writer(unicode( force_escape(user.username)))
                    __M_writer(u'\n')
                # SOURCE LINE 57
                __M_writer(u'&nbsp;&nbsp;</strong> ')
                __M_writer(unicode(self.block_userlinks()))
                # SOURCE LINE 58
                __M_writer(u'</div>\n')
            # SOURCE LINE 60
            __M_writer(u'\n        ')
            # SOURCE LINE 61
            __M_writer(unicode(self.block_nav_global()))
            __M_writer(u'\n    </div>\n    <!-- END Header -->\n    ')
            # SOURCE LINE 64
            __M_writer(unicode(self.block_breadcrumbs()))
            # SOURCE LINE 68
            __M_writer(u'\n    \n')
        # SOURCE LINE 71
        __M_writer(u'\n\n        \n')
        # SOURCE LINE 74
        if messages:
            # SOURCE LINE 75
            __M_writer(u'\n        <ul class="messagelist">\n')
            # SOURCE LINE 77
            for message in messages:
                # SOURCE LINE 78
                __M_writer(u'<li>')
                __M_writer(unicode(message))
                __M_writer(u'</li>\n')
            # SOURCE LINE 80
            __M_writer(u'</ul>\n        \n')
        # SOURCE LINE 83
        __M_writer(u'\n\n    <!-- Content -->\n    <div id="content" class="')
        # SOURCE LINE 86
        __M_writer(unicode(self.block_coltype()))
        __M_writer(u'">\n        ')
        # SOURCE LINE 87
        __M_writer(unicode(self.block_pretitle()))
        __M_writer(u'\n        ')
        # SOURCE LINE 88
        __M_writer(unicode(self.block_content_title()))
        # SOURCE LINE 92
        __M_writer(u'\n        ')
        # SOURCE LINE 95
        __M_writer(unicode(self.block_content()))
        __M_writer(u'\n        ')
        # SOURCE LINE 96
        __M_writer(unicode(self.block_sidebar()))
        __M_writer(u'\n        <br class="clear" />\n    </div>\n    <!-- END Content -->\n\n    ')
        # SOURCE LINE 101
        __M_writer(unicode(self.block_footer()))
        __M_writer(u'\n</div>\n<!-- END Container -->\n\n</body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_extrahead(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_breadcrumbs(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        trans = context.get('trans', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 64
        __M_writer(u'<div class="breadcrumbs"><a href="/">')
        __M_writer(unicode(trans('Home')))
        __M_writer(u'</a>\n')
        # SOURCE LINE 65
        if title:
            # SOURCE LINE 66
            __M_writer(u' &rsaquo; ')
            __M_writer(unicode(title))
            __M_writer(u'\n')
        # SOURCE LINE 68
        __M_writer(u'</div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_bodyclass(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_stylesheet(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 14
        __M_writer(unicode(admin_media_prefix()))
        __M_writer(u'css/base.css')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 88
        __M_writer(u'\n')
        # SOURCE LINE 89
        if title:
            # SOURCE LINE 90
            __M_writer(u'<h1>')
            __M_writer(unicode(title))
            __M_writer(u'</h1>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_stylesheet_rtl(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 21
        __M_writer(unicode(admin_media_prefix()))
        __M_writer(u'css/rtl.css')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        def block_object_tools():
            __M_caller = context.caller_stack._push_frame()
            try:
                __M_writer = context.writer()
                return ''
            finally:
                context.caller_stack._pop_frame()
        __M_writer = context.writer()
        # SOURCE LINE 93
        __M_writer(u'\n        ')
        # SOURCE LINE 94
        __M_writer(unicode(block_object_tools()))
        __M_writer(u'\n        ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_coltype(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 86
        __M_writer(u'colM')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'Undefined')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 101
        __M_writer(u'<div id="footer"></div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_branding(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_nav_global(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_blockbots(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 27
        __M_writer(u'<meta name="bang" content="pop"/><meta name="robots" content="NONE,NOARCHIVE" />')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_sidebar(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_pretitle(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_userlinks(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        url = context.get('url', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        django_admindocs_docroot = context.get('django_admindocs_docroot', UNDEFINED)
        root_path = context.get('root_path', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 57
        docsroot = url(django_admindocs_docroot)

        __M_writer(u'\n <a href="')
        # SOURCE LINE 58
        __M_writer(unicode( (root_path+'logout/') if not resolvers.reverse('admin:logout') else resolvers.reverse('admin:logout') ))
        __M_writer(u'">')
        __M_writer(unicode(trans('Log out')))
        __M_writer(u'</a>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_extrastyle(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


