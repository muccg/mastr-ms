from django.conf.urls.defaults import *

urlpatterns = patterns('madas.repository.wsviews',
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)/(?P<field>\w+)/(?P<match>\w+)[/]*$', 'populate_select', {'SSL':True}),
    (r'^records/(?P<model>\w+)/(?P<field>\w+)/(?P<value>.+)[/]*$', 'records', {'SSL':True}),
    (r'^create/(?P<model>\w+)[/]*$', 'create_object', {'SSL':True}),
    (r'^update/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'update_object', {'SSL':True}),
    (r'^delete/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'delete_object', {'SSL':True}),
    (r'^associate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'associate_object', {'SSL':True}),
    (r'^dissociate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'dissociate_object', {'SSL':True}),
    (r'^recreate_sample_classes/(?P<experiment_id>\w+)[/]*$', 'recreate_sample_classes', {'SSL':True}),
    (r'^sample_class_enable/(?P<id>\w+)[/]*$', 'sample_class_enable', {'SSL':True}),
    (r'^files[/]*$', 'experimentFilesList', {'SSL':True}),
    (r'^pendingfiles[/]*$', 'pendingFilesList', {'SSL':True}),
    (r'^moveFile[/]*$', 'moveFile', {'SSL':True}),
    (r'^uploadFile[/]*$', 'uploadFile', {'SSL':True}),
)
