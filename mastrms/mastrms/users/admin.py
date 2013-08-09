from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User as DjangoUser, Group
from mastrms.users.models import User
from django import forms

class MAUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # fields = (
        #     "username", "first_name", "last_name",
        #     "email", "password",
        #     "is_staff", "is_active", "is_superuser",
        #     "last_login", "date_joined",
        #     "groups", "user_permissions",
        #     "commonName", "givenName", "sn", "mail",
        #     "telephoneNumber", "homePhone",
        #     "physicalDeliveryOfficeName", "title",
        #     "destinationIndicator", "description", "postalAddress",
        #     "businessCategory", "registeredAddress",
        #     "carLicense", "passwordResetKey")

    commonName = forms.CharField(required=False)
    givenName = forms.CharField(required=False)
    sn = forms.CharField(required=False)
    mail = forms.CharField(required=False)
    telephoneNumber = forms.CharField(required=False)
    homePhone = forms.CharField(required=False)
    physicalDeliveryOfficeName = forms.CharField(required=False)
    title = forms.CharField(required=False)
    destinationIndicator = forms.CharField(required=False)
    description = forms.CharField(required=False)
    postalAddress = forms.CharField(required=False)
    businessCategory = forms.CharField(required=False)
    registeredAddress = forms.CharField(required=False)
    carLicense = forms.CharField(required=False)
    passwordResetKey = forms.CharField(required=False)

class MAUserAdmin(UserAdmin):
    form = MAUserChangeForm
    ma_fieldsets = (
        ("Other info", {'fields': (
                    "commonName", "givenName", "sn", "mail",
                    "telephoneNumber", "homePhone",
                    "physicalDeliveryOfficeName", "title",
                    "destinationIndicator", "description", "postalAddress",
                    "businessCategory", "registeredAddress",
                    "carLicense", "passwordResetKey")}),)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(MAUserAdmin, self).get_fieldsets(request, obj)
        return fieldsets + self.ma_fieldsets

# register the django auth admins
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, MAUserAdmin)
admin.site.register(Group, GroupAdmin)
