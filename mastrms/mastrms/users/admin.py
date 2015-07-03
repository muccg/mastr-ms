from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from mastrms.users.models import User
from django import forms


class MAUserChangeForm(forms.ModelForm):

    "Mostly copied from django.contrib.auth.forms.UserChangeForm"

    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>.")

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

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MAUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MAUserCreationForm(forms.ModelForm):

    "Adapted from django.contrib.auth.forms.UserCreationForm"
    INITIAL_GROUPS = ["User"]

    error_messages = {
        'duplicate_email': "A user with that e-mail already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    email = forms.EmailField(label="E-mail address", max_length=100)
    #username = forms.HiddenInput()
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        # Since User.email is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(MAUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Add the user to a group
            for g in Group.objects.filter(name__in=self.INITIAL_GROUPS):
                user.groups.add(g)
        return user


class MAUserAdmin(UserAdmin):
    form = MAUserChangeForm
    add_form = MAUserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ("Other info", {'fields': (
            "physicalDeliveryOfficeName",
            "telephoneNumber", "homePhone",
            "title", "destinationIndicator",
            "businessCategory", "registeredAddress",
            "postalAddress", "description", "carLicense")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)


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
