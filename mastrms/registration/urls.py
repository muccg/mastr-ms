from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'submit', 'mastrms.registration.views.submit', {'SSL':True}),        
)
