from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^processLogin', views.processLoginView),
    url(r'^processLogout', views.processLogout),
    url(r'^processForgotPassword', views.processForgotPassword),
    url(r'^populateResetPasswordForm', views.populateResetPasswordForm),
    url(r'^processResetPassword', views.processResetPassword),
    url(r'^forgotPassword', views.forgotPasswordRedirect),
]
