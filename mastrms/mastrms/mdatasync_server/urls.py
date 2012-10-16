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
    (r'^utils', 'mastrms.mdatasync_server.views.utils'),
    (r'^nodes', 'mastrms.mdatasync_server.views.get_node_clients'),
    (r'^node/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', 'mastrms.mdatasync_server.views.nodeinfo'),
    (r'^requestsync/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', 'mastrms.mdatasync_server.views.request_sync'),
    #(r'^syncadmin/(.*)', include(admin.site.urls)),
    (r'^logupload/', 'mastrms.mdatasync_server.views.log_upload'),
    (r'^keyupload/', 'mastrms.mdatasync_server.views.key_upload'),
    (r'^checksamplefiles/', 'mastrms.mdatasync_server.views.check_run_sample_files'),
    (r'files/(?P<path>.*)$', 'mastrms.mdatasync_server.views.serve_file'),
    (r'^taillog/(?P<filename>.*)/(?P<linesback>\d*)/(?P<since>\d*)/$', 'mastrms.mdatasync_server.views.tail_log'),
    (r'^(.*)', 'mastrms.mdatasync_server.views.get_node_clients'),
    #(r'^(.*)', 'mastrms.mdatasync_server.views.defaultpage'),
    # madas
)
