from django.conf.urls.defaults import * 
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from madas.repository import admin as repoadmin

#we don't need this line?
#from madas.quote import admin as madasadmin

urlpatterns = patterns('',

#    (r'^(.*)/authorize', 'madas.madas.views.authorize'),
#    (r'^(.*)/index', 'madas.madas.views.serveIndex'),
    (r'^status/', status_view),
    (r'^sync/', include('madas.mdatasync_server.urls')),

    # madasrepo
    (r'^repo/', include('madas.repository.urls')),
    (r'^ws/', include('madas.repository.wsurls')),

    # admin
    (r'^repoadmin/', include(admin.site.urls)),

    # static
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True}),
    (r'^javascript/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True}),

    # madas
    #huh? this doesnt even exist..
    #(r'^', include('madas.quote.urls')),
)
