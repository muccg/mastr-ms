from django.conf.urls.defaults import *

urlpatterns = patterns('madas.repository.wsviews',
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)[/]*$', 'populate_select'),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)[/]*$', 'populate_select'),
    (r'^populate_select/(?P<model>\w+)/(?P<key>\w+)/(?P<value>\w+)/(?P<field>\w+)/(?P<match>\w+)[/]*$', 'populate_select'),
    (r'^records/(?P<model>\w+)/(?P<field>\w+)/(?P<value>.+)[/]*$', 'records'),
    (r'^create/(?P<model>\w+)[/]*$', 'create_object'),
    (r'^update/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'update_object'),
    (r'^delete/(?P<model>\w+)/(?P<id>\w+)[/]*$', 'delete_object'),
    (r'^associate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'associate_object'),
    (r'^dissociate/(?P<model>\w+)/(?P<association>\w+)/(?P<parent_id>\w+)/(?P<id>\w+)[/]*$', 'dissociate_object'),
    (r'^recreate_sample_classes/(?P<experiment_id>\w+)[/]*$', 'recreate_sample_classes'),
    (r'^sample_class_enable/(?P<id>\w+)[/]*$', 'sample_class_enable'),
)
