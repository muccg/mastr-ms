from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^userload', views.user_load_profile),
    url(r'^userSave', views.userSave),
    url(r'^listAllNodes', views.listAllNodes),
    #url(r'listRestrictedGroups', views.listRestrictedGroups),
]
