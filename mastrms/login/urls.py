from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^processLogin', 'madas.login.views.processLoginView', {'SSL':True}),
    (r'^processLogout', 'madas.login.views.processLogout', {'SSL':True}),
    (r'^processForgotPassword', 'madas.login.views.processForgotPassword', {'SSL':True}),
    (r'^populateResetPasswordForm', 'madas.login.views.populateResetPasswordForm', {'SSL':True}),
    (r'^processResetPassword', 'madas.login.views.processResetPassword', {'SSL':True}),
    (r'^forgotPassword', 'madas.login.views.forgotPasswordRedirect', {'SSL':True}),

)
