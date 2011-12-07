from django.contrib.auth.models import User
from madas.users import models

# This class has been created when dependency on LDAP has been removed from application
# The idea is to support the methods LDAPHandler was supporting and return data in the exact same format
# as it was from LDAP (but now from the DB) to minimize the rewriting that has to be done

class DBUserManager(object):
    def get_user_details(self, username):
        django_user = User.objects.get(username=username)
        if not (django_user or django_user.username):
            return {}
        details = models.UserDetail.objects.get(user=django_user)

        details_dict = details.to_dict()
        details_dict['groups'] = [g.name for g in models.Group.objects.filter(user=django_user)]

        return details_dict
