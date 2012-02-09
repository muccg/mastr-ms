from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    #admin
    (r'^adminrequests', 'madas.admin.views.admin_requests', {'SSL':True}),
    (r'^usersearch', 'madas.admin.views.user_search', {'SSL':True}),
    (r'^rejectedUsersearch', 'madas.admin.views.rejected_user_search', {'SSL':True}),
    (r'^deletedUsersearch', 'madas.admin.views.deleted_user_search', {'SSL':True}),
    (r'^nodesave', 'madas.admin.views.node_save', {'SSL':True}),
    (r'^nodeDelete', 'madas.admin.views.node_delete', {'SSL':True}),
    (r'^userload', 'madas.admin.views.user_load', {'SSL':True}), 
    (r'^userSave', 'madas.admin.views.user_save', {'SSL':True}), 
    (r'^orgsave[/]*$', 'madas.admin.views.org_save', {'SSL':True}), 
    (r'^orgDelete[/]*$', 'madas.admin.views.org_delete', {'SSL':True}), 
    (r'^listOrganisations', 'madas.admin.views.list_organisations', {'SSL':True}),
)
