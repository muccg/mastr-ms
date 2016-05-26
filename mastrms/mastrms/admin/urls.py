from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^adminrequests', views.admin_requests),
    url(r'^usersearch', views.user_search),
    url(r'^rejectedUsersearch', views.rejected_user_search),
    url(r'^deletedUsersearch', views.deleted_user_search),
    url(r'^nodesave', views.node_save),
    url(r'^nodeDelete', views.node_delete),
    url(r'^userload', views.user_load),
    url(r'^userSave', views.user_save),
    url(r'^orgsave[/]*$', views.org_save),
    url(r'^orgDelete[/]*$', views.org_delete),
    url(r'^listOrganisations', views.list_organisations),
]
