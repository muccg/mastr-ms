from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    '',
    #admin
    (r'^adminrequests', 'mastrms.admin.views.admin_requests', {'SSL':settings.SSL_ENABLED}),
    (r'^usersearch', 'mastrms.admin.views.user_search', {'SSL':settings.SSL_ENABLED}),
    (r'^rejectedUsersearch', 'mastrms.admin.views.rejected_user_search', {'SSL':settings.SSL_ENABLED}),
    (r'^deletedUsersearch', 'mastrms.admin.views.deleted_user_search', {'SSL':settings.SSL_ENABLED}),
    (r'^nodesave', 'mastrms.admin.views.node_save', {'SSL':settings.SSL_ENABLED}),
    (r'^nodeDelete', 'mastrms.admin.views.node_delete', {'SSL':settings.SSL_ENABLED}),
    (r'^userload', 'mastrms.admin.views.user_load', {'SSL':settings.SSL_ENABLED}),
    (r'^userSave', 'mastrms.admin.views.user_save', {'SSL':settings.SSL_ENABLED}),
    (r'^orgsave[/]*$', 'mastrms.admin.views.org_save', {'SSL':settings.SSL_ENABLED}),
    (r'^orgDelete[/]*$', 'mastrms.admin.views.org_delete', {'SSL':settings.SSL_ENABLED}),
    (r'^listOrganisations', 'mastrms.admin.views.list_organisations', {'SSL':settings.SSL_ENABLED}),
)
