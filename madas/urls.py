from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^madas/', include('madas.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
#    (r'^(.*)/authorize', 'madas.madas.views.authorize'),
#    (r'^(.*)/index', 'madas.madas.views.serveIndex'),

    # madasrepo
    (r'^repo/', include('madas.repository.urls')),
    (r'^ws/', include('madas.repository.wsurls')),

    # madas
    (r'^repoadmin[/]*(.*)', admin.site.root),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True}),
    (r'^javascript/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True}),
    (r'^', include('madas.m.urls')),
)
