from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    #admin
    (r'^adminrequests', 'mastrms.admin.views.admin_requests'),
    (r'^usersearch', 'mastrms.admin.views.user_search'),
    (r'^rejectedUsersearch', 'mastrms.admin.views.rejected_user_search'),
    (r'^deletedUsersearch', 'mastrms.admin.views.deleted_user_search'),
    (r'^nodesave', 'mastrms.admin.views.node_save'),
    (r'^nodeDelete', 'mastrms.admin.views.node_delete'),
    (r'^userload', 'mastrms.admin.views.user_load'),
    (r'^userSave', 'mastrms.admin.views.user_save'),
    (r'^orgsave[/]*$', 'mastrms.admin.views.org_save'),
    (r'^orgDelete[/]*$', 'mastrms.admin.views.org_delete'),
    (r'^listOrganisations', 'mastrms.admin.views.list_organisations'),
)
