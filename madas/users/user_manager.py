from django.contrib.auth.models import User
from django.db import transaction
from madas.users import models
import logging

# This class has been created when dependency on LDAP has been removed from application
# The idea is to support the methods LDAPHandler was supporting and return data in the exact same format
# as it was from LDAP (but now from the DB) to minimize the rewriting that has to be done

logger = logging.getLogger('madas_log')

def get_user_manager():
    return DBUserManager()

class DBUserManager(object):
    def get_user_details(self, username):
        django_user = None
        django_users = User.objects.filter(username=username)
        if django_users:
            django_user = django_users[0]
        if not (django_user or django_user.username):
            logger.debug('No user named %s in django\'s users table' % django_user) 
            return {}

        try:
            details = models.UserDetail.objects.get(user=django_user)
        except models.UserDetail.DoesNotExist, e:
            details_dict = {}
        else:
            details_dict = details.to_dict()

        details_dict['groups'] = [g.name for g in models.Group.objects.filter(user=django_user)]

        logger.debug(details_dict)
        return details_dict

    def list_groups(self):
        return [g.name for g in models.Group.objects.all()]

    def add_group(self, groupname):
        try:
            groupname = groupname.strip()
            models.Group.objects.create(name=groupname)
        except Exception, e:
            logger.exception("Couldn't create group %s." % groupname)
            return False
        return True

    def rename_group(self, oldname, newname):
        try:
            oldname = oldname.strip()
            newname = newname.strip()
            group = models.Group.objects.get(name=oldname)
            group.name = newname
            group.save()
        except Exception, e:
            logger.exception("Couldn't rename group %s to group %s." % (oldname, newname))
            return False
        return True

    def delete_group(self, groupname):
        try:
            group = models.Group.objects.get(name=groupname)
            group.delete()
        except Exception, e:
            logger.exception("Couldn't delete group %s." % groupname)
            return False
        return True

    def get_user_groups(self, username):
        return [g.name for g in models.Group.objects.filter(user__username=username)]
        
