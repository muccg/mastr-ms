from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    #admin
    (r'^adminrequests', 'mastrms.admin.views.admin_requests', {'SSL':True}),
    (r'^usersearch', 'mastrms.admin.views.user_search', {'SSL':True}),
    (r'^rejectedUsersearch', 'mastrms.admin.views.rejected_user_search', {'SSL':True}),
    (r'^deletedUsersearch', 'mastrms.admin.views.deleted_user_search', {'SSL':True}),
    (r'^nodesave', 'mastrms.admin.views.node_save', {'SSL':True}),
    (r'^nodeDelete', 'mastrms.admin.views.node_delete', {'SSL':True}),
    (r'^userload', 'mastrms.admin.views.user_load', {'SSL':True}), 
    (r'^userSave', 'mastrms.admin.views.user_save', {'SSL':True}), 
    (r'^orgsave[/]*$', 'mastrms.admin.views.org_save', {'SSL':True}), 
    (r'^orgDelete[/]*$', 'mastrms.admin.views.org_delete', {'SSL':True}), 
    (r'^listOrganisations', 'mastrms.admin.views.list_organisations', {'SSL':True}),
)
