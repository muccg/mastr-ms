from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^userload', 'mastrms.users.views.userload', {'SSL':True}),
    (r'^userSave', 'mastrms.users.views.userSave', {'SSL':True}),
    (r'^listAllNodes', 'mastrms.users.views.listAllNodes', {'SSL':True}),
    #(r'listRestrictedGroups', 'mastrms.users.views.listRestrictedGroups', {'SSL':True}),
    
)
