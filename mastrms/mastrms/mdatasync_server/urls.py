from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^utils', views.utils),
    url(r'^nodes', views.get_node_clients),
    url(r'^requestsync/(?P<organisation>.*)/(?P<sitename>.*)/(?P<station>.*)/', views.request_sync),
    url(r'^logupload/', views.log_upload),
    url(r'^keyupload/', views.key_upload),
    url(r'^checksamplefiles/', views.check_run_sample_files),
    url(r'files/(?P<path>.*)$', views.serve_file),
    url(r'^taillog/(?P<filename>.*)/(?P<linesback>\d*)/(?P<since>\d*)/$', views.tail_log),
    url(r'^(.*)', views.get_node_clients),
]
