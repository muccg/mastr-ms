from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User as DjangoUser, Group
from mastrms.users.models import User
from django import forms

class MAUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

    physicalDeliveryOfficeName = forms.CharField(label="Office", required=False)
    telephoneNumber = forms.CharField(label="Office Phone", required=False)
    homePhone = forms.CharField(label="Home Phone", required=False)
    title = forms.CharField(label="Position", required=False)
    destinationIndicator = forms.CharField(label="Department", required=False)
    businessCategory = forms.CharField(label="Institute", required=False)
    postalAddress = forms.CharField(label="Address", required=False)
    registeredAddress = forms.CharField(label="Supervisor", required=False)
    description = forms.CharField(label="Area of Interest", required=False)
    carLicense = forms.CharField(label="Country", required=False)
    passwordResetKey = forms.CharField(label="Password Reset Key", required=False)

class MAUserAdmin(UserAdmin):
    form = MAUserChangeForm
    ma_fieldsets = (
        ("Other info", {'fields': (
                    "physicalDeliveryOfficeName",
                    "telephoneNumber", "homePhone",
                    "title", "destinationIndicator",
                    "businessCategory", "registeredAddress",
                    "postalAddress", "description", "carLicense")}),)

    fieldsets = UserAdmin.fieldsets + ma_fieldsets

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
