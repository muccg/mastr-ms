from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User as DjangoUser, Group

from mastrms.users.models import User

# register the django auth admins
from django.contrib.auth.admin import UserAdmin, GroupAdmin
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
