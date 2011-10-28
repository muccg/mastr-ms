from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
# place app url patterns here

urlpatterns = patterns('',
    # Example:
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^conf', 'madas.mdatasync_server.views.configureNode'),
    (r'^utils', 'madas.mdatasync_server.views.utils'),
    (r'^nodes', 'madas.mdatasync_server.views.getNodeClients'),
    (r'^node/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', 'madas.mdatasync_server.views.nodeinfo'),
    (r'^requestsync/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', 'madas.mdatasync_server.views.requestSync'),
    (r'^syncadmin/(.*)', admin.site.root),
    (r'^logupload/', 'madas.mdatasync_server.views.logUpload'),
    (r'^keyupload/', 'madas.mdatasync_server.views.keyUpload'),
    (r'^checksamplefiles/', 'madas.mdatasync_server.views.checkRunSampleFiles'),
    (r'files/(?P<path>.*)$', 'madas.mdatasync_server.views.serve_file'),
    (r'^taillog/(?P<filename>.*)/(?P<linesback>\d*)/(?P<since>\d*)/$', 'madas.mdatasync_server.views.tail_log'),
    (r'^(.*)', 'madas.mdatasync_server.views.retrievePathsForFiles'),
    #(r'^(.*)', 'madas.mdatasync_server.views.defaultpage'),
    # madas
)
