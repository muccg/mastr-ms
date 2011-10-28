from django.conf.urls.defaults import * 
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from madas.repository import admin as repoadmin
from madas.quote import admin as madasadmin

urlpatterns = patterns('',

    (r'^userinfo', 'madas.users.views.userinfo'),
    (r'^status/', status_view),
    (r'^sync/', include('madas.mdatasync_server.urls')),

    # madasrepo
    (r'^ws/', include('madas.repository.wsurls')),

    # repoadmin
    (r'^repoadmin/', include(admin.site.urls)),

    # madas admin
    (r'^admin/', include('madas.admin.urls')),
    # madas quotes
    (r'^quote/', include('madas.quote.urls')),
    # madas registration
    (r'^registration/', include('madas.registration.urls')),
    # madas login
    (r'^login/', include('madas.login.urls')),
    # madas users 
    (r'^user/', include('madas.users.urls')),
)

# static
if settings.DEBUG:
    print 'Running with django view for static path.'
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT, 'SSL' : True} ),
    )
    #default view
urlpatterns += patterns('', 
    (r'^', 'madas.login.views.serveIndex', {'SSL':True}),
    )
