from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns(
    '',

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    
    (r'^login/processLogin', 'madas.repository.views.login', {'SSL':True}),
    (r'^login/processLogout', 'madas.repository.views.processLogout', {'SSL':True}),

    #(r'serverinfo', 'madas.m.views.serverinfo'),
    #default
    #(r'^(?P<modname>.*)/(?P<submodname.*>)?(P<args>.*)$', 'madas.m.views.serveIndex', {module=modname, submodule=submodname, args=args}),
    (r'^(?P<cruft>.*)$', 'madas.repository.views.serveIndex', {'SSL':True}),
    
) 
