from django.conf.urls import *
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
    (r'^utils', 'mastrms.mdatasync_server.views.utils'),
    (r'^nodes', 'mastrms.mdatasync_server.views.get_node_clients'),
    (r'^requestsync/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', 'mastrms.mdatasync_server.views.request_sync'),
    (r'^logupload/', 'mastrms.mdatasync_server.views.log_upload'),
    (r'^keyupload/', 'mastrms.mdatasync_server.views.key_upload'),
    (r'^checksamplefiles/', 'mastrms.mdatasync_server.views.check_run_sample_files'),
    (r'files/(?P<path>.*)$', 'mastrms.mdatasync_server.views.serve_file'),
    (r'^taillog/(?P<filename>.*)/(?P<linesback>\d*)/(?P<since>\d*)/$', 'mastrms.mdatasync_server.views.tail_log'),
    (r'^(.*)', 'mastrms.mdatasync_server.views.get_node_clients'),
)
