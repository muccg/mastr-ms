from django.conf.urls import patterns, url, include
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from . import api

urlpatterns = patterns('',
    url(r'^/?$', 'mastrms.login.views.serveIndex', name="home"),

    (r'^userinfo', 'mastrms.users.views.userinfo'),
    (r'^sync/', include('mastrms.mdatasync_server.urls')),

    # hand-written api
    (r'^ws/', include('mastrms.repository.urls')),

    # auto-generated rest api
    url(r'^api/', include(api.v1.urls), name="api"),

    # repoadmin
    (r'^repoadmin/', include(admin.site.urls)),

    # mastrms.admin
    (r'^admin/', include('mastrms.admin.urls')),
    # mastrms.quotes
    (r'^quote/', include('mastrms.quote.urls')),
    # mastrms.registration
    url(r'^(?P<force_mcf>registration)/?$', 'mastrms.login.views.serveIndex',
        name="register"),
    (r'^registration/', include('mastrms.registration.urls')),
    # mastrms.login
    (r'^login/', include('mastrms.login.urls')),
    # mastrms.users
    (r'^user/', include('mastrms.users.urls')),
)

# static
if settings.DEBUG:
    print 'Running with django view for static path.'
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT}),
    )
