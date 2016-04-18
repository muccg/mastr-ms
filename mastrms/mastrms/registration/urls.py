from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    (r'submit', 'mastrms.registration.views.submit'),
)
