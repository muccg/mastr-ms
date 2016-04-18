from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    (r'^userload', 'mastrms.users.views.user_load_profile'),
    (r'^userSave', 'mastrms.users.views.userSave'),
    (r'^listAllNodes', 'mastrms.users.views.listAllNodes'),
    #(r'listRestrictedGroups', 'mastrms.users.views.listRestrictedGroups'),
)
