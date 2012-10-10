from django.conf.urls.defaults import *
from mastrms import settings

urlpatterns = patterns(
    '',
    (r'^processLogin', 'mastrms.login.views.processLoginView', {'SSL':settings.SSL_ENABLED}),
    (r'^processLogout', 'mastrms.login.views.processLogout', {'SSL':settings.SSL_ENABLED}),
    (r'^processForgotPassword', 'mastrms.login.views.processForgotPassword', {'SSL':settings.SSL_ENABLED}),
    (r'^populateResetPasswordForm', 'mastrms.login.views.populateResetPasswordForm', {'SSL':settings.SSL_ENABLED}),
    (r'^processResetPassword', 'mastrms.login.views.processResetPassword', {'SSL':settings.SSL_ENABLED}),
    (r'^forgotPassword', 'mastrms.login.views.forgotPasswordRedirect', {'SSL':settings.SSL_ENABLED}),

)
