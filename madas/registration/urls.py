from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'submit', 'madas.registration.views.submit', {'SSL':True}),        
)
