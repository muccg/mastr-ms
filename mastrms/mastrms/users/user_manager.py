import logging
from django.contrib.auth.models import Group

logger = logging.getLogger('mastrms.general')

class GroupManager(object):
    @staticmethod
    def list_groups():
        return list(Group.objects.values_list("name", flat=True))

    @staticmethod
    def add_group(groupname):
        try:
            groupname = groupname.strip()
            Group.objects.create(name=groupname)
        except Exception, e:
            logger.exception("Couldn't create group %s." % groupname)
            return False
        return True

    @staticmethod
    def rename_group(oldname, newname):
        try:
            oldname = oldname.strip()
            newname = newname.strip()
            group = Group.objects.get(name=oldname)
            group.name = newname
            group.save()
        except Exception, e:
            logger.exception("Couldn't rename group %s to group %s." % (oldname, newname))
            return False
        return True

    @staticmethod
    def delete_group(groupname):
        try:
            group = Group.objects.get(name=groupname)
            group.delete()
        except Exception, e:
            logger.exception("Couldn't delete group %s." % groupname)
            return False
        return True

    @staticmethod
    def get_user_groups(email):
        return [g.name for g in Group.objects.filter(user__email=email)]
