from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns(
    '',
    (r'^processLogin', 'mastrms.login.views.processLoginView'),
    (r'^processLogout', 'mastrms.login.views.processLogout'),
    (r'^processForgotPassword', 'mastrms.login.views.processForgotPassword'),
    (r'^populateResetPasswordForm', 'mastrms.login.views.populateResetPasswordForm'),
    (r'^processResetPassword', 'mastrms.login.views.processResetPassword'),
    (r'^forgotPassword', 'mastrms.login.views.forgotPasswordRedirect'),

)
