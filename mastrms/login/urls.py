from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    (r'^processLogin', 'mastrms.login.views.processLoginView', {'SSL':True}),
    (r'^processLogout', 'mastrms.login.views.processLogout', {'SSL':True}),
    (r'^processForgotPassword', 'mastrms.login.views.processForgotPassword', {'SSL':True}),
    (r'^populateResetPasswordForm', 'mastrms.login.views.populateResetPasswordForm', {'SSL':True}),
    (r'^processResetPassword', 'mastrms.login.views.processResetPassword', {'SSL':True}),
    (r'^forgotPassword', 'mastrms.login.views.forgotPasswordRedirect', {'SSL':True}),

)
