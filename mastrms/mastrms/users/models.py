import logging
import json
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, Group
from mastrms.users.user_manager import GroupManager

MADAS_USER_GROUP = 'User'
MADAS_PENDING_GROUP = 'Pending'
MADAS_DELETED_GROUP = 'Deleted'
MADAS_REJECTED_GROUP = 'Rejected'
MADAS_STATUS_GROUPS = [MADAS_USER_GROUP, MADAS_PENDING_GROUP, MADAS_DELETED_GROUP, MADAS_REJECTED_GROUP]
MADAS_ADMIN_GROUP = 'Administrators'
MADAS_NODEREP_GROUP = 'Node Reps'
MASTR_ADMIN_GROUP = 'Mastr Administrators'
PROJECTLEADER_GROUP = 'Project Leaders'
MASTR_STAFF_GROUP = 'Mastr Staff'
MADAS_ADMIN_GROUPS = [MADAS_ADMIN_GROUP, MADAS_NODEREP_GROUP, MASTR_ADMIN_GROUP, PROJECTLEADER_GROUP, MASTR_STAFF_GROUP]

logger = logging.getLogger('mastrms.users')


class User(AbstractUser):
    """
    Extended user model.
    Some attributes still need to be renamed.
    """
    telephoneNumber = models.CharField(max_length=255, blank=True)
    homePhone = models.CharField(max_length=255, blank=True) # homephone
    physicalDeliveryOfficeName = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    destinationIndicator = models.CharField(max_length=255, blank=True) # dept
    description = models.CharField(max_length=255, blank=True) # areaOfInterest
    postalAddress = models.CharField(max_length=255, blank=True) # address
    businessCategory = models.CharField(max_length=255, blank=True) # institute
    registeredAddress = models.CharField(max_length=255, blank=True) # supervisor
    carLicense = models.CharField(max_length=255, blank=True) # country
    passwordResetKey = models.CharField(max_length=255, blank=True)

    def to_dict(self, ldap_style=True):
        d = {
            'uid' if ldap_style else 'username': self.username,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'email': self.email,
            'telephoneNumber': self.telephoneNumber,
            'homephone': self.homePhone,
            'physicalDeliveryOfficeName': self.physicalDeliveryOfficeName,
            'title': self.title,
            'dept': self.destinationIndicator,
            'areaOfInterest': self.description,
            'address': self.postalAddress,
            'institute': self.businessCategory,
            'supervisor': self.registeredAddress,
            'country': self.carLicense,
            'passwordResetKey': self.passwordResetKey,
        }

        if ldap_style:
            # wrap each value in a list like ldap attrs
            d = dict((k, [v]) for (k, v) in d.iteritems())

        d['groups'] = list(self.groups.values_list("name", flat=True))
        return d

    @property
    def IsAdmin(self):
        return self.groups.filter(name=MADAS_ADMIN_GROUP).exists()
    @IsAdmin.setter
    def IsAdmin(self, value):
        self.update_groups(Group.objects.filter(name=MADAS_ADMIN_GROUP), value)
        self.is_superuser = bool(value)
        self.save()

    @property
    def IsNodeRep(self):
        return self.groups.filter(name=MADAS_NODEREP_GROUP).exists()
    @IsNodeRep.setter
    def IsNodeRep(self, value):
        self.update_groups(Group.objects.filter(name=MADAS_NODEREP_GROUP), value)

    @property
    def IsClient(self):
        "Client users are unprivileged and aren't members of any node group."
        # fixme: this does too many database queries
        return not (self.IsPrivileged or self.IsStaff or self.IsMastrStaff)

    @property
    def IsStaff(self):
        "Staff are not privileged but are members of a node group"
        # fixme: this does too many database queries
        return not self.IsPrivileged and bool(self.Nodes)

    @property
    def IsMastrAdmin(self):
        return self.groups.filter(name=MASTR_ADMIN_GROUP).exists()
    @IsMastrAdmin.setter
    def IsMastrAdmin(self, value):
        self.update_groups(Group.objects.filter(name=MASTR_ADMIN_GROUP), value)

    @property
    def IsProjectLeader(self):
        return self.groups.filter(name=PROJECTLEADER_GROUP).exists()
    @IsProjectLeader.setter
    def IsProjectLeader(self, value):
        self.update_groups(Group.objects.filter(name=PROJECTLEADER_GROUP), value)

    @property
    def IsMastrStaff(self):
        return self.groups.filter(name=MASTR_STAFF_GROUP).exists()
    @IsMastrStaff.setter
    def IsMastrStaff(self, value):
        self.update_groups(Group.objects.filter(name=MASTR_STAFF_GROUP), value)

    @property
    def IsLoggedIn(self):
        return self.is_authenticated()

    @property
    def Username(self):
        return self.username
    @Username.setter
    def Username(self, value):
        self.username = value

    @property
    def IsPrivileged(self):
        return (self.IsAdmin or self.IsMastrAdmin or self.IsNodeRep or self.IsProjectLeader)

    @property
    def StatusGroup(self):
        status = self.groups.filter(name__in=MADAS_STATUS_GROUPS)
        status = status.values_list("name", flat=True)
        if len(status) == 0:
            logger.warning("User %s has no status group, assuming deleted." % self.username)
            return MADAS_DELETED_GROUP
        if len(status) > 1:
            logger.warning("User %s somehow got multiple groups: %s. Using the"
                           " first one." % (self.username, ", ".join(status)))
        return status[0]

    @StatusGroup.setter
    def StatusGroup(self, new_group):
        if new_group not in MADAS_STATUS_GROUPS:
            raise ValueError, "bug: bad user status group \"%s\"" % new_group
        other_groups = [g for g in MADAS_STATUS_GROUPS if g != new_group]
        self.update_groups(self.groups.filter(name__in=other_groups), False)
        self.update_groups(Group.objects.filter(name=new_group), True)
        self.is_active = new_group == MADAS_USER_GROUP
        self.save()

        # strip deleted/rejected users of any admin groups they may
        # have somehow gotten
        if not self.is_active:
            self.update_groups(self.groups.filter(name__in=MADAS_ADMIN_GROUPS), False)

    def disable(self):
        "Deletes the user"
        self.StatusGroup = MADAS_DELETED_GROUP

    def reject(self):
        self.StatusGroup = MADAS_REJECTED_GROUP

    @property
    def Nodes(self):
        groups = self.groups.exclude(name__in=MADAS_STATUS_GROUPS)
        groups = groups.exclude(name__in=MADAS_ADMIN_GROUPS)
        # fixme: remove list conversion, fix json serializer
        return list(groups.values_list("name", flat=True))
    @Nodes.setter
    def Nodes(self, nodes):
        # remove user from all non-special groups which don't include nodes
        other_groups = self.groups.exclude(name__in=MADAS_STATUS_GROUPS)
        other_groups = other_groups.exclude(name__in=MADAS_ADMIN_GROUPS)
        other_groups = other_groups.exclude(name__in=nodes)
        self.update_groups(other_groups, False)

        # add user to node groups
        self.update_groups(Group.objects.filter(name__in=nodes), True)

    def update_groups(self, groups, is_member):
        """
        Adds or removes user from each group in groups, depending on
        the truth of is_member. This method also logs what is done.
        """
        for group in groups:
            in_group = self.groups.filter(id=group.id).exists()
            if is_member and not in_group:
                logger.info("Adding user %s to group \"%s\"" % (self.username, group.name))
                self.groups.add(group)
            elif not is_member and in_group:
                logger.info("Removing user %s from group \"%s\"" % (self.username, group.name))
                self.groups.remove(group)

    @property
    def PrimaryNode(self):
        if len(self.Nodes) >=1:
            return self.Nodes[0]
        else:
            return 'Unknown'

    @property
    def Name(self):
        return self.get_full_name()

    #Just a class to encapsulate data to send to the frontend (as json)
    def getData(self):
        attrs = [ "Username", "IsLoggedIn", "IsAdmin", "IsClient", "IsNodeRep",
                  "IsStaff", "IsMastrAdmin", "IsProjectLeader", "IsMastrStaff",
                  "Nodes" ]

        return dict((attr, getattr(self, attr)) for attr in attrs)

    def toJson(self):
        return json.dumps(self.getData())

    def get_client_dict(self):
        'takes a username, returns a dictionary of results'
        'returns empty dict if the user doesnt exist'

        details = self.to_dict(ldap_style=False)

        #copy one field to a new name
        details['originalEmail'] = details['email']

        #groups
        details['node'] = self.PrimaryNode or []
        details['isAdmin'] = self.IsAdmin
        details['isNodeRep'] = self.IsNodeRep
        details['isMastrAdmin'] = self.IsMastrAdmin
        details['isProjectLeader'] = self.IsProjectLeader
        details['isMastrStaff'] = self.IsMastrStaff
        details['isClient'] = self.IsClient
        status = self.StatusGroup
        #This is done because the javascript wants
        #'Self' to be seen as 'Active'
        if status == MADAS_USER_GROUP:
            status = 'Active'
        details['status'] = status
        #groups - for some reason the frontend code wants this limited to one?
        #         so I choose the most important.
        if self.IsAdmin:
            details['groups'] = MADAS_ADMIN_GROUP
        elif self.IsNodeRep:
            details['groups'] = MADAS_NODEREP_GROUP
        else:
            details['groups'] = details['node']

        details['name'] = self.Name

        return details

    def update_user(self, newusername, newpassword, detailsDict):
        if newusername is None:
            newusername = self.username
        elif newusername != self.username:
            if type(self).objects.filter(username=newusername).exists():
                logger.warning('New Username %s already existed.' % newusername)
            else:
                self.username = newusername

        if newpassword:
            self.set_password(newpassword)
            self.passwordResetKey = ""

        for field, value in detailsDict.iteritems():
            setattr(self, field, value)
        self.save()

        return True


# Gets MAUser for currently logged in user, or a dummy MAUser object
def getCurrentUser(request, force_refresh = False):
    anon_json = json.dumps({
        "Username": "nulluser",
        "IsLoggedIn": False, "IsAdmin": False, "IsClient": False,
        "IsNodeRep": False, "IsStaff": False, "IsMastrAdmin": False,
        "IsProjectLeader": False, "IsMastrStaff": False,
        "Nodes": [],
        })

    user = request.user
    if user.is_anonymous():
        user.toJson = lambda: anon_json
    return user

def getMadasUser(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None

def getMadasUsersFromGroups(grouplist, method='and', ldap_style=False) :
    '''Returns users who are a member of the groups given in grouplist
    The default 'method' is 'and', which will return only users who are a member
    of all groups. Passing 'or' will return users who are a member of any of the groups'''
    def list_users(searchGroup, method):
        users_qs = User.objects.all()
        if searchGroup:
            users_qs = User.objects
            filter_cond = None
            for g in searchGroup:
                if method == 'and':
                    users_qs = users_qs.filter(groups__name=g)
                else:
                    if filter_cond is None:
                        filter_cond = Q(groups__name=g)
                    else:
                        filter_cond = filter_cond | Q(groups__name=g)
            if method != 'and':
                users_qs = User.objects.filter(filter_cond)

        return users_qs

    users = list_users(grouplist, method)
    return [u.to_dict(ldap_style) for u in users]

def addMadasUser(username, detailsdict, password):
    logger.info("Adding new user %s" % username)
    if User.objects.filter(username=username).exists():
        logger.warning('A user called %s already existed. Refusing to add.' % username)
        user = None
    else:
        detailsdict["username"] = username
        user = User.objects.create(**detailsdict)
        user.StatusGroup = MADAS_PENDING_GROUP
        user.set_password(password)
        user.save()

    return user

def updateMadasUserDetails(currentUser, existingUser, username, password, detailsdict):
    #The only people who can edit a record is an admin, or the actual user
    if currentUser.IsAdmin or currentUser.IsMastrAdmin or currentUser == existingUser:
        existingUser.update_user(username, password, detailsdict)
        return True
    return False

def saveMadasUser(currentUser, username, changeddetails, changedstatus, password):
    '''
        the current user is the currently logged in madas user
        the username is the username of the person being edited
        changeddetails is a dict containing only the changed details
        changedstatus is a dict containing {admin:bool, noderep:bool, node:str, status:str}
    '''
    #load the existing user
    existingUser = getMadasUser(username)

    #If the user doesn't exist yet, add them first.
    if existingUser is None:
        existingUser = addMadasUser(username.strip(), changeddetails, password)

    if not currentUser.is_authenticated():
        # if not logged in, the rest of the changes are only doable by
        # adminish users or the user himself, so quit here, job done.
        return True

    if not updateMadasUserDetails(currentUser, existingUser, username, password, changeddetails):
        return False

    if currentUser.IsAdmin:
        # if they are an admin, dont let them unadmin themselves
        if existingUser != currentUser:
            existingUser.IsAdmin = changedstatus['admin']

        # Update Node
        existingUser.Nodes = [changedstatus.get('node')]

    if currentUser.IsAdmin or currentUser.IsMastrAdmin:
        existingUser.IsMastrAdmin = bool(changedstatus['mastradmin'])

    if (currentUser.IsAdmin or currentUser.IsMastrAdmin or
            (currentUser.IsProjectLeader and currentUser.Nodes == existingUser.Nodes)):
        existingUser.IsProjectLeader = bool(changedstatus['projectleader'])

    if (currentUser.IsAdmin or currentUser.IsMastrAdmin or
            (currentUser.IsProjectLeader and currentUser.Nodes == existingUser.Nodes)):
        existingUser.IsMastrStaff = bool(changedstatus['mastrstaff'])

    if (currentUser.IsAdmin or (currentUser.IsNodeRep and currentUser.Nodes == existingUser.Nodes)):
        existingUser.IsNodeRep = bool(changedstatus['noderep'])

        # Status: Pending, Active etc.
        existingUser.StatusGroup = changedstatus.get('status')

    # update django is_staff and is_superuser from madas groups
    existingUser.is_superuser = existingUser.IsAdmin
    existingUser.is_staff = existingUser.is_superuser or existingUser.IsStaff
    existingUser.save()

    return True
