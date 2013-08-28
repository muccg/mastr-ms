from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    (r'^userload', 'mastrms.users.views.user_load_profile', {'SSL':settings.SSL_ENABLED}),
    (r'^userSave', 'mastrms.users.views.userSave', {'SSL':settings.SSL_ENABLED}),
    (r'^listAllNodes', 'mastrms.users.views.listAllNodes', {'SSL':settings.SSL_ENABLED}),
    #(r'listRestrictedGroups', 'mastrms.users.views.listRestrictedGroups', {'SSL':settings.SSL_ENABLED}),

)
