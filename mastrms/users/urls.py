from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^userload', 'madas.users.views.userload', {'SSL':True}),
    (r'^userSave', 'madas.users.views.userSave', {'SSL':True}),
    (r'^listAllNodes', 'madas.users.views.listAllNodes', {'SSL':True}),
    #(r'listRestrictedGroups', 'madas.users.views.listRestrictedGroups', {'SSL':True}),
    
)
