from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from mastrms.repository import admin as repoadmin
from mastrms.quote import admin as mastrmsadmin
from mastrms.mdatasync_server import admin as mdatasync_admin

urlpatterns = patterns('',

    (r'^userinfo', 'mastrms.users.views.userinfo'),
    #(r'^status/', status_view),
    (r'^sync/', include('mastrms.mdatasync_server.urls')),

    # mastrms.epo
    (r'^ws/', include('mastrms.repository.wsurls')),

    # repoadmin
    (r'^repoadmin/', include(admin.site.urls)),

    # mastrms.admin
    (r'^admin/', include('mastrms.admin.urls')),
    # mastrms.quotes
    (r'^quote/', include('mastrms.quote.urls')),
    # mastrms.registration
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
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_ROOT, 'SSL' : settings.SSL_ENABLED} ),
    )
    #default view
urlpatterns += patterns('',
    (r'^', 'mastrms.login.views.serveIndex', {'SSL': settings.SSL_ENABLED}),
    )
