import logging
import json
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from mastrms.users.user_manager import get_user_manager
from mastrms.app.utils.data_utils import translate_dict, makeJsonFriendly

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
    Some attributes still need to be chopped out or renamed.
    """
    telephoneNumber = models.CharField(max_length=255, blank=True)
    homePhone = models.CharField(max_length=255, blank=True)
    physicalDeliveryOfficeName = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    destinationIndicator = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    postalAddress = models.CharField(max_length=255, blank=True)
    businessCategory = models.CharField(max_length=255, blank=True)
    registeredAddress = models.CharField(max_length=255, blank=True)
    carLicense = models.CharField(max_length=255, blank=True)
    passwordResetKey = models.CharField(max_length=255, blank=True)

    @property
    def uid(self):
        return self.username

    def to_dict(self):
        d = {
            'uid': [self.uid],
            'givenName': [self.first_name],
            'sn': [self.last_name],
            'mail': [self.email],
            'telephoneNumber': [self.telephoneNumber],
            'homePhone': [self.homePhone],
            'physicalDeliveryOfficeName': [self.physicalDeliveryOfficeName],
            'title': [self.title],
            'destinationIndicator': [self.destinationIndicator],
            'description': [self.description],
            'postalAddress': [self.postalAddress],
            'businessCategory': [self.businessCategory],
            'registeredAddress': [self.registeredAddress],
            'carLicense': [self.carLicense],
            'passwordResetKey': [self.passwordResetKey]
        }
        return d

    def set_from_dict(self, d):
        trans = [('givenName', 'first_name'),
                 ('sn', 'last_name'),
                 ('mail', 'email'),
                 ('telephoneNumber', 'telephoneNumber'),
                 ('homePhone', 'homePhone'),
                 ('physicalDeliveryOfficeName', 'physicalDeliveryOfficeName'),
                 ('title', 'title'),
                 ('destinationIndicator', 'destinationIndicator'),
                 ('description', 'description'),
                 ('postalAddress', 'postalAddress'),
                 ('businessCategory', 'businessCategory'),
                 ('registeredAddress', 'registeredAddress'),
                 ('carLicense', 'carLicense'),
                 ('passwordResetKey', 'passwordResetKey')]
        for ldap_attr, model_attr in trans:
            val = d.get(ldap_attr, None)
            if val:
                if isinstance(val, list):
                    val = val[0]
                setattr(self, model_attr, val)

    @property
    def IsAdmin(self):
        return self.groups.filter(name=MADAS_ADMIN_GROUP).exists()
    @IsAdmin.setter
    def IsAdmin(self, value):
        self.update_groups(Group.objects.filter(name=MADAS_ADMIN_GROUP), value)
        self.is_admin = value
        self.save()

    @property
    def IsNodeRep(self):
        return self.groups.filter(name=MADAS_NODEREP_GROUP).exists()
    @IsNodeRep.setter
    def IsNodeRep(self, value):
        self.update_groups(Group.objects.filter(name=MADAS_NODEREP_GROUP), value)

    @property
    def IsClient(self):
        # fixme: this does too many database queries
        return not (self.IsPrivileged or self.IsStaff or self.IsMastrStaff)
    @IsClient.setter
    def IsClient(self, value):
        raise NotImplemented

    @property
    def IsStaff(self):
        # fixme: this does too many database queries
        return not self.IsPrivileged and self.Nodes
    @IsStaff.setter
    def IsStaff(self, value):
        raise NotImplemented

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
    def CachedGroups(self):
        self.refreshCachedGroups()
        return self._cached_groups

    @property
    def IsPrivileged(self):
        return (self.IsAdmin or self.IsMastrAdmin or self.IsNodeRep or self.IsProjectLeader)

    @property
    def StatusGroup(self):
        self.refreshCachedGroups()
        return self._status_group
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
            if is_member:
                logger.info("Adding user %s to group \"%s\"" % (self.username, group.name))
                self.groups.add(group)
            else:
                logger.info("Removing user %s from group \"%s\"" % (self.username, group.name))
                self.groups.remove(group)

    @property
    def PrimaryNode(self):
        if len(self.Nodes) >=1:
            return self.Nodes[0]
        else:
            return 'Unknown'

    @property
    def CachedDetails(self):
        self.refreshCachedDetails()
        return self._cached_details

    @property
    def Name(self):
        return self.get_full_name()

    def refreshCachedGroups(self):
        if getattr(self, "_cached_groups", None) is None:
            #logger.debug('\tRefreshing groups for %s. Fetching.' % (self.Username) )
            groupsdict = getMadasUserGroups(self.Username)
            self._cached_groups = groupsdict['groups'] + groupsdict['status']
            self._status_group = groupsdict['status']

    def refreshCachedDetails(self):
        if not hasattr(self, "_cached_details"):
            #logger.debug('\tRefreshing user details for %s.' % (self.Username) )
            self._cached_details = dict(getMadasUserDetails(self.Username))

    #Just a class to encapsulate data to send to the frontend (as json)
    def getData(self):
        attrs = [ "Username", "IsLoggedIn", "IsAdmin", "IsClient", "IsNodeRep",
                  "IsStaff", "IsMastrAdmin", "IsProjectLeader", "IsMastrStaff",
                  "Nodes", "CachedGroups", "StatusGroup", "CachedDetails" ]

        return dict((attr, getattr(self, attr)) for attr in attrs)


    def toJson(self):
        return json.dumps(self.getData())


# Gets MAUser for currently logged in user, or a dummy MAUser object
def getCurrentUser(request, force_refresh = False):
    anon_json = json.dumps({
        "Username": "nulluser",
        "IsLoggedIn": False, "IsAdmin": False, "IsClient": False,
        "IsNodeRep": False, "IsStaff": False, "IsMastrAdmin": False,
        "IsProjectLeader": False, "IsMastrStaff": False,
        "Nodes": [],  "CachedDetails": [],
        "CachedGroups": [], "StatusGroup": []
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

#Utility methods
def getMadasUserGroups(username, include_status_groups = False):
    user_manager = get_user_manager()
    a = user_manager.get_user_groups(username)
    groups = []
    status = []

    if a:
        for name in a:
            if include_status_groups or name not in MADAS_STATUS_GROUPS:
                groups.append(name)

            #set the status group (even if being shown in 'groups')
            if name in MADAS_STATUS_GROUPS:
                status.append(name)

    return {'groups': groups, 'status': status}

def getMadasUsersFromGroups(grouplist, method='and') :
    '''Returns users who are a member of the groups given in grouplist
    The default 'method' is 'and', which will return only users who are a member
    of all groups. Passing 'or' will return users who are a member of any of the groups'''
    user_manager = get_user_manager()
    users = user_manager.list_users(grouplist, method)
    return users

def getMadasGroups():
    user_manager = get_user_manager()
    groups = user_manager.list_groups()
    return groups

def getMadasUserDetails(username):
    user_manager = get_user_manager()
    d = user_manager.get_user_details(username)
    #this is a function to un-listify values in the dict, since
    #ldap often returns them that way
    def _stripArrays(inputdict):
        for key in inputdict.keys():
            if isinstance(inputdict[key], list) and len(inputdict[key]) > 0:
                inputdict[key] = inputdict[key][0]
        return inputdict
    d = _stripArrays(d)
    return _translate_ldap_to_madas(d)

def _translate_madas_to_ldap(mdict, createEmpty=False):
    retdict = translate_dict(mdict, [('username', 'uid'), \
                           ('commonname', 'commonName'), \
                           ('firstname', 'givenName'), \
                           ('lastname', 'sn'), \
                           ('email', 'mail'), \
                           ('telephoneNumber', 'telephoneNumber'), \
                           ('homephone', 'homePhone'), \
                           ('physicalDeliveryOfficeName', 'physicalDeliveryOfficeName'), \
                           ('title', 'title'), \
                           ('dept', 'destinationIndicator'), \
                           ('areaOfInterest', 'description'), \
                           ('address', 'postalAddress'), \
                           ('institute', 'businessCategory'), \
                           ('supervisor', 'registeredAddress'), \
                           ('country', 'carLicense'), \
                            ], createEmpty=createEmpty)
    return retdict


def _translate_ldap_to_madas(ldict, createEmpty=False):
    retdict = translate_dict(ldict, [('uid', 'username'), \
                           ('commonName', 'commonname'), \
                           ('givenName', 'firstname'), \
                           ('sn', 'lastname'), \
                           ('mail', 'email'), \
                           ('telephoneNumber', 'telephoneNumber'), \
                           ('homePhone', 'homephone'), \
                           ('physicalDeliveryOfficeName', 'physicalDeliveryOfficeName'), \
                           ('title', 'title'), \
                           ('destinationIndicator', 'dept'), \
                           ('description', 'areaOfInterest'), \
                           ('postalAddress', 'address'), \
                           ('businessCategory', 'institute'), \
                           ('registeredAddress', 'supervisor'), \
                           ('carLicense', 'country'), \
                            ], createEmpty=createEmpty)
    return retdict

def loadMadasUser(username):
    'takes a username, returns a dictionary of results'
    'returns empty dict if the user doesnt exist'

    user = getMadasUser(username)
    details = user.CachedDetails if user else {}

    if len(details) == 0:
        return {}

    #copy one field to a new name
    details['originalEmail'] = details['email']

    #groups
    nodes = user.Nodes
    if len(nodes) > 0:
        details['node'] = user.PrimaryNode
    else:
        details['node'] = []
    details['isAdmin'] = user.IsAdmin
    details['isNodeRep'] = user.IsNodeRep
    details['isMastrAdmin'] = user.IsMastrAdmin
    details['isProjectLeader'] = user.IsProjectLeader
    details['isMastrStaff'] = user.IsMastrStaff
    details['isClient'] = user.IsClient
    status = user.StatusGroup
    #This is done because the javascript wants
    #'User' to be seen as 'Active'
    if status == MADAS_USER_GROUP:
        status = 'Active'
    details['status'] = status
    #groups - for some reason the frontend code wants this limited to one?
    #         so I choose the most important.
    if user.IsAdmin:
        details['groups'] = MADAS_ADMIN_GROUP
    elif user.IsNodeRep:
        details['groups'] = MADAS_NODEREP_GROUP
    else:
        details['groups'] = details['node']

    details['name'] = user.Name

    return details

def addMadasUser(username, detailsdict):
    user_manager = get_user_manager()

    #create an empty dict with the ldap format
    emptydetails = _translate_madas_to_ldap({}, createEmpty=True)
    #combine in the details dict
    new_details = dict(emptydetails, **detailsdict)

    user = user_manager.add_user(username, detailsdict)

    if user:
        user.StatusGroup = MASTR_USER_PENDING

    return user is not None

def updateMadasUserDetails(currentUser, existingUser, username, password, detailsdict):
    #The only people who can edit a record is an admin, or the actual user
    if currentUser.IsAdmin or currentUser.IsMastrAdmin or currentUser == existingUser:
        try:
            user_manager = get_user_manager()
            #pass username twice, as the old and new username (so we don't allow changing username
            user_manager.update_user(existingUser, username, password, detailsdict)
        except Exception, e:
            logger.warning("Could not update user %s: %s" % (username, str(e)) )
            return False

    # Only errors will return success False
    return True

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
        logger.debug("Adding new user %s" % (username))
        if not addMadasUser(username, changeddetails):
            return False
    existingUser = getMadasUser(username)

    #translate their details to ldap
    existing_details = _translate_madas_to_ldap(existingUser.CachedDetails)
    #combine the dictionaries, overriding existing_details with changeddetails
    new_details = dict(existing_details, **changeddetails)

    if not updateMadasUserDetails(currentUser, existingUser, username, password, new_details):
        return False

    if not currentUser.is_authenticated():
        # if not logged in, the rest of the changes are only doable by
        # adminish users, so quit here, job done.
        return True

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

    return True
