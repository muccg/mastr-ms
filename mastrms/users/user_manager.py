from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from mastrms.users import models
import logging

# This class has been created when dependency on LDAP has been removed from application
# The idea is to support the methods LDAPHandler was supporting and return data in the exact same format
# as it was from LDAP (but now from the DB) to minimize the rewriting that has to be done

logger = logging.getLogger('madas_log')

def get_user_manager():
    return DBUserManager()

from users.MAUser import getMadasUser
class DBUserManager(object):
    def get_user_details(self, username):
        django_user = None
        django_users = User.objects.filter(username=username)
        if django_users:
            django_user = django_users[0]
        if django_user is None or not django_user.username:
            logger.debug('No user named %s in django\'s users table' % django_user) 
            return {}

        try:
            details = models.UserDetail.objects.get(user=django_user)
        except models.UserDetail.DoesNotExist, e:
            details_dict = {}
        else:
            details_dict = details.to_dict()

        details_dict['groups'] = [g.name for g in models.Group.objects.filter(user=django_user)]

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

    def list_users(self, searchGroup, method= 'and'):
        if not searchGroup:
            users_qs = models.UserDetail.objects.all()
        else:
            users_qs = models.UserDetail.objects
            filter_cond = None
            for g in searchGroup:
                if method == 'and':
                    users_qs = users_qs.filter(user__group__name=g)
                else:
                    if filter_cond is None:
                        filter_cond = Q(user__group__name=g)
                    else:
                        filter_cond = filter_cond | Q(user__group__name=g)
            if method != 'and':
                users_qs = models.UserDetail.objects.filter(filter_cond)  
       
        return [u.to_dict() for u in users_qs]
 

    def update_staff_status(self, user):
        #if the user belongs to more than one users.models.Group, they should be django staff. 
        #Else, they shouldnt.
        mauser = getMadasUser(user.username)
        if not mauser.IsClient:
            user.is_staff=True
            user.save()
        else:
            user.is_staff=False
            user.save()


    def add_user_to_group(self, username, groupname):
        try: 
            user = User.objects.get(username=username)
        except User.DoesNotExist, e:
            logger.warning('User with username % does not exist' % username)
            return False
        try:
            group = models.Group.objects.get(name=groupname)
        except models.Group.DoesNotExist, e:
            logger.warning('Group with name %s does not exist' % groupname)
            return False
        if group.user.filter(username=username):
            logger.warning('User %s already in group %s' % (username, groupname))
            return False
        group.user.add(user)
        
        self.update_staff_status(user)

        return True

    def remove_user_from_group(self, username, groupname):
        try: 
            user = User.objects.get(username=username)
        except User.DoesNotExist, e:
            logger.warning('User with username % does not exist' % username)
            return False
        try:
            group = models.Group.objects.get(name=groupname)
        except models.Group.DoesNotExist, e:
            logger.warning('Group with name %s does not exist' % groupname)
            return False
        if not group.user.filter(username=username):
            logger.warning('User %s not in group %s' % (username, groupname))
            return False
        group.user.remove(user)

        self.update_staff_status(user)
        
        return True

    def add_user(self, username, detailsDict):
        username = username.strip()
        if User.objects.filter(username=username).exists():
            logger.warning('A user called %s already existed. Refusing to add.' % username)
            return False
        django_user = User.objects.create(username=username)
        user_detail = models.UserDetail.objects.create(user=django_user)
        user_detail.set_from_dict(detailsDict)
        user_detail.save()
        return True
            
    def update_user(self, username, newusername, newpassword, detailsDict):
        if newusername is None:
            newusername = username
        
        if newusername != username:
            if User.objects.filter(username=newusername).exists():
                logger.warning('New Useraname %s already existed.' % newusername)

        try:
            django_user = User.objects.get(username=username)
        except User.DoesNotExist, e:
            logger.warning('User with username %s does not exist' % username)
            return False

        user_detail = models.UserDetail.objects.get(user=django_user)

        if username != newusername:
            django_user.username = newusername
            django_user.save()

        if newpassword is not None and newpassword != '':
            django_user.set_password(newpassword) 
            user_detail.passwordResetKey = None
            django_user.save()
            user_detail.save()

        user_detail.set_from_dict(detailsDict)
        user_detail.save()

        return True 

