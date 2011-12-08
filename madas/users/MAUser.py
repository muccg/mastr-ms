from django.utils import simplejson
from ccg.auth.ldap_helper import LDAPHandler
from madas.users.user_manager import DBUserManager
import logging
from madas.utils.data_utils import translate_dict, makeJsonFriendly
from madas import settings #for ldap admin username/password
from django.contrib.auth.models import User

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

logger = logging.getLogger('madas_log')

#Just a class to encapsulate data to send to the frontend (as json)
class MAUser(object):
    def __init__(self, username):
        self._dict = {}
        self.Username = username
        self.IsLoggedIn = False

    @property 
    def IsAdmin(self):
        return self._dict.get('IsAdmin', False)
    @IsAdmin.setter
    def IsAdmin(self, value):
        self._dict['IsAdmin'] = value

    @property 
    def IsNodeRep(self):
        return self._dict.get('IsNodeRep', False)
    @IsNodeRep.setter 
    def IsNodeRep(self, value):
        self._dict['IsNodeRep'] = value

    @property 
    def IsClient(self):
        return self._dict.get('IsClient', False)
    @IsClient.setter 
    def IsClient(self, value):
        self._dict['IsClient'] = value

    @property 
    def IsStaff(self):
        return self._dict.get('IsStaff', False)
    @IsStaff.setter 
    def IsStaff(self, value):
        self._dict['IsStaff'] = value 

    @property 
    def IsMastrAdmin(self):
        return self._dict.get('IsMastrAdmin', False)
    @IsMastrAdmin.setter 
    def IsMastrAdmin(self, value):
        self._dict['IsMastrAdmin'] = value 

    @property 
    def IsProjectLeader(self):
        return self._dict.get('IsProjectLeader', False)
    @IsProjectLeader.setter 
    def IsProjectLeader(self, value):
        self._dict['IsProjectLeader'] = value 

    @property 
    def IsMastrStaff(self):
        return self._dict.get('IsMastrStaff', False)
    @IsMastrStaff.setter 
    def IsMastrStaff(self, value):
        self._dict['IsMastrStaff'] = value 

    @property
    def IsLoggedIn(self):
        return self._dict.get('IsLoggedIn', False)
    @IsLoggedIn.setter 
    def IsLoggedIn(self, value):
        self._dict['IsLoggedIn'] = value

    @property 
    def Username(self):
        return self._dict.get('Username', False)
    @Username.setter 
    def Username(self, value):
        self._dict['Username'] = value

    @property
    def CachedGroups(self):
        groups = self._dict.get('CachedGroups', None)
        if groups == None:
            #we do a refresh
            self.refreshCachedGroups()
        return self._dict.get('CachedGroups', [])
    @CachedGroups.setter
    def CachedGroups(self, value):
        self._dict['CachedGroups'] = value

    @property
    def IsPrivileged(self):
        return (self.IsAdmin or self.IsMastrAdmin or self.IsNodeRep or self.IsProjectLeader)
    
    @property
    def StatusGroup(self):
        return self._dict.get('StatusGroup', None)
    @StatusGroup.setter
    def StatusGroup(self, value):
        if isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                value = None
        self._dict['StatusGroup'] = value

    @property
    def Nodes(self):
        return self._dict.get('Nodes', [])
    @Nodes.setter
    def Nodes(self, value):
        self._dict['Nodes'] = value

    @property
    def PrimaryNode(self):
        if len(self.Nodes) >=1:
            return self.Nodes[0]
        else:
            return 'Unknown'
    
    @property 
    def CachedDetails(self):
        details = self._dict.get('CachedDetails', None)
        if details is None:
            #we do a refresh
            self.refreshCachedDetails()
        return self._dict.get('CachedDetails', {})
    @CachedDetails.setter
    def CachedDetails(self, value):
        self._dict['CachedDetails'] = value

    def refreshCachedGroups(self):
        logger.debug('\tNo cached groups for %s. Fetching.' % (self.Username) )
        groupsdict = getMadasUserGroups(self.Username)
        self.CachedGroups = groupsdict['groups'] + groupsdict['status']
        self.StatusGroup = groupsdict['status']
        return self.CachedGroups

    def refreshCachedDetails(self):
        logger.debug('\tRetrieving user details for %s.' % (self.Username) )
        detailsdict = getMadasUserDetails(self.Username)
        self.CachedDetails = dict(detailsdict)
        return self.CachedDetails
    
    def refresh(self):
        #defaults
        #IsLoggedIn is not handled here - it is managed by the getCurrentUser function
        self.IsAdmin = False
        self.IsClient = False
        self.IsNodeRep = False
        self.IsStaff = False
        self.IsMastrAdmin = False
        self.IsProjectLeader = False
        self.IsMastrStaff = False

        #Grab groups, forcing a reload. 
        self.refreshCachedGroups()
        self.refreshCachedDetails()
        self.Nodes = getMadasNodeMemberships(self.CachedGroups)
            
        if MADAS_ADMIN_GROUP in self.CachedGroups:
            self.IsAdmin = True
        if MADAS_NODEREP_GROUP in self.CachedGroups:
            self.IsNodeRep = True
        if MASTR_ADMIN_GROUP in self.CachedGroups:
            self.IsMastrAdmin = True
        if PROJECTLEADER_GROUP in self.CachedGroups:
            self.IsProjectLeader = True
        if MASTR_STAFF_GROUP in self.CachedGroups:
            self.IsMastrStaff = True

        if not self.IsPrivileged and self.Nodes:
            self.IsStaff = True

        if not (self.IsPrivileged or self.IsStaff or self.IsMastrStaff):
            self.IsClient = True

    def getData(self):
        return self._dict

    def toJson(self):
        return simplejson.dumps(self._dict)

#Gets the MAUser object out of the session, or creates a new one
def getCurrentUser(request, force_refresh = False):
    
    currentuser = request.session.get('mauser', False)
    if force_refresh or not currentuser: 
        currentuser = MAUser(request.user.username)
        currentuser.refresh()
        request.session['mauser'] = currentuser 
   
    #if the authentication is different:
    if currentuser.IsLoggedIn != request.user.is_authenticated():
        currentuser.IsLoggedIn = request.user.is_authenticated()
        request.session['mauser'] = currentuser 
    
    return request.session['mauser']

def getMadasUser(username):
    mauser = MAUser(username)
    mauser.refresh()
    return mauser

#Utility methods
def getMadasUserGroups(username, include_status_groups = False):
    ld = LDAPHandler()
    a = ld.ldap_get_user_groups(username)
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
    ld = LDAPHandler()
    users = ld.ldap_list_users(grouplist, method)
    return users

def getMadasGroups():
    user_manager = DBUserManager()
    groups = user_manager.list_groups()
    return groups

def getMadasNodeMemberships(groups):
    if groups is None:
        return []

    specialGroups = MADAS_STATUS_GROUPS + MADAS_ADMIN_GROUPS
    i = [item for item in groups if not item in specialGroups]
    return i

def getMadasUserDetails(username):
    user_manager = DBUserManager()
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
    user.refresh()
    details = user.CachedDetails

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

    return details  

def addMadasUser(username, detailsdict):
    ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD) #need an admin connection

    #create an empty dict with the ldap format
    emptydetails = _translate_madas_to_ldap({}, createEmpty=True)
    #combine in the details dict
    new_details = dict(emptydetails, **detailsdict)

    objectclasses = 'inetorgperson'
    usercontainer = 'ou=NEMA'
    userdn = 'ou=People'
    basedn = 'dc=ccg,dc=murdoch,dc=edu,dc=au'
    success = ld.ldap_add_user(username, detailsdict, objectclasses=objectclasses, usercontainer=usercontainer, userdn=userdn, basedn=basedn)
    if success:
        success = ld.ldap_add_user_to_group(username, MADAS_PENDING_GROUP)
        if not success:
            raise Exception, 'Could not add user %s to group %s' % (username, MADAS_PENDING_GROUP) 
    else:
        raise Exception, 'Could not add user %s' % (username)
        
    return success

def updateMadasUserDetails(currentUser, username, password, detailsdict):
    #The only people who can edit a record is an admin, or the actual user
    if currentUser.IsAdmin or currentUser.IsMastrAdmin or currentUser.Username == username:
        try:
            ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
            #pass username twice, as the old and new username (so we don't allow changing username
            ld.ldap_update_user(username, username, password, detailsdict, pwencoding='md5')
        except Exception, e:
            logger.warning("Could not update user %s: %s" % (username, str(e)) )
            return False
     
    # Only errors will return success False
    return True

def addMadasUserToGroup(user, groupname):
    ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
    #add them to the group as long as they arent already in it
    if groupname not in user.CachedGroups:
        ld.ldap_add_user_to_group(user.Username, groupname)

def removeMadasUserFromGroup(user, groupname):
    ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
    #remove them from the group as long as they are in it.
    if groupname in user.CachedGroups:
        ld.ldap_remove_user_from_group(user.Username, groupname)

def ensureDjangoUserExists(username):
    try:
        django_user = User.objects.get(username=username)
    except User.DoesNotExist:
        django_user = User.objects.create_user(username, username)
        django_user.set_unusable_password()
        django_user.save()

def set_superuser(user, superuser=False):
    django_user = User.objects.get(username=user.Username)
    django_user.is_superuser = superuser
    django_user.save()

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
    if existingUser.CachedDetails == {}:
        logger.debug("Adding new user %s" % (username))
        if not addMadasUser(username, changeddetails):
            return False
    existingUser = getMadasUser(username)

    ensureDjangoUserExists(username)
    
    #translate their details to ldap
    existing_details = _translate_madas_to_ldap(existingUser.CachedDetails)
    #combine the dictionaries, overriding existing_details with changeddetails
    new_details = dict(existing_details, **changeddetails)

    if not updateMadasUserDetails(currentUser, username, password, new_details):
        return False
   
    if currentUser.IsAdmin: 
        if changedstatus['admin']:
            addMadasUserToGroup(existingUser, MADAS_ADMIN_GROUP)
            set_superuser(existingUser, True)
        else:
            #if they are an admin, dont let them unadmin themselves 
            if existingUser.Username != currentUser.Username:
                removeMadasUserFromGroup(existingUser, MADAS_ADMIN_GROUP)
                set_superuser(existingUser, False)

        # Update Node
        oldnodes = existingUser.Nodes
        newnode = changedstatus.get('node')
        if newnode is not None and newnode not in oldnodes: 
            if len(oldnodes) > 0:
                #remove them from the old node:
                removeMadasUserFromGroup(existingUser, oldnodes[0])
            addMadasUserToGroup(existingUser, newnode)
 
    if currentUser.IsAdmin or (currentUser.IsNodeRep and currentUser.Nodes == existingUser.Nodes):
        if changedstatus['noderep']:
            addMadasUserToGroup(existingUser, MADAS_NODEREP_GROUP)
        else:
            removeMadasUserFromGroup(existingUser, MADAS_NODEREP_GROUP)
        
        # Status: Pending, Active etc.
        oldstatus = existingUser.StatusGroup
        newstatus = changedstatus.get('status')
        if newstatus is not None and newstatus != oldstatus:
            if oldstatus is not None:
                removeMadasUserFromGroup(existingUser, oldstatus)
            addMadasUserToGroup(existingUser, newstatus)
        
    if currentUser.IsAdmin or currentUser.IsMastrAdmin:
        if changedstatus['mastradmin']:
            addMadasUserToGroup(existingUser, MASTR_ADMIN_GROUP)
            set_superuser(existingUser, True)
        else:
            removeMadasUserFromGroup(existingUser, MASTR_ADMIN_GROUP)
            set_superuser(existingUser, False)

    if (currentUser.IsAdmin or currentUser.IsMastrAdmin or 
            (currentUser.IsProjectLeader and currentUser.Nodes == existingUser.Nodes)):
        if changedstatus['projectleader']:
            addMadasUserToGroup(existingUser, PROJECTLEADER_GROUP)
        else:
            removeMadasUserFromGroup(existingUser, PROJECTLEADER_GROUP)

    if (currentUser.IsAdmin or currentUser.IsMastrAdmin or 
            (currentUser.IsProjectLeader and currentUser.Nodes == existingUser.Nodes)):
        if changedstatus['mastrstaff']:
            addMadasUserToGroup(existingUser, MASTR_STAFF_GROUP)
        else:
            removeMadasUserFromGroup(existingUser, MASTR_STAFF_GROUP)

    return True                

def getDetailsFromRequest(request):
    '''This is a generic function for parsing the form data passed in
       via one of the user edit forms
       it returns a dictionary with the following format:
       username: <username supplied in form>
       password: <password supplied in form>
       details: <dict of other details as supplied in form>
       status: <dict of status information (node, admin, noderep etc)
    '''
    def getReqVarSTR(key, default=''):
        return str(request.REQUEST.get(key, default))

    updatedusername = getReqVarSTR('email')
    updateDict = {}
    updateDict['mail'] = updatedusername
    updateDict['telephoneNumber'] = getReqVarSTR('telephoneNumber') 
    updateDict['physicalDeliveryOfficeName'] =  getReqVarSTR('physicalDeliveryOfficeName')
    updateDict['title'] = getReqVarSTR('title')
    updateDict['givenName'] = getReqVarSTR('firstname') 
    updateDict['sn'] = getReqVarSTR('lastname')
    updateDict['cn'] = "%s %s" % (updateDict['givenName'], updateDict['sn'])
    updateDict['homePhone'] = getReqVarSTR('homephone')
    updateDict['postalAddress'] = getReqVarSTR('address') 
    updateDict['description'] = getReqVarSTR('areaOfInterest') 
    updateDict['destinationIndicator'] = getReqVarSTR('dept')
    updateDict['businessCategory'] = getReqVarSTR('institute') 
    updateDict['registeredAddress'] = getReqVarSTR('supervisor')
    updateDict['carLicense'] = getReqVarSTR('country')

    #any that are blank, we delete
    for key in updateDict.keys():
        if updateDict[key] == '' or updateDict[key] is None:
            del updateDict[key]

    statusDict = {}
    statusDict['admin'] = request.REQUEST.get('isAdmin')
    statusDict['noderep'] = request.REQUEST.get('isNodeRep')
    statusDict['mastradmin'] = request.REQUEST.get('isMastrAdmin')
    statusDict['projectleader'] = request.REQUEST.get('isProjectLeader')
    statusDict['mastrstaff'] = request.REQUEST.get('isMastrStaff')
    statusDict['node'] = request.REQUEST.get('node')
    status = request.REQUEST.get('status')
    if status == 'Active':
        status = MADAS_USER_GROUP
    statusDict['status'] = status    
    password = getReqVarSTR('password').strip() #empty password is ignored anyway

    retdict = {}
    retdict['username'] =  updatedusername
    retdict['password'] = password 
    retdict['details'] = updateDict 
    retdict['status'] = statusDict
   
    logger.debug('Parsed Form results:')
    logger.debug('Username: %s', updatedusername)
    logger.debug('Password: %s', password)
    logger.debug('Details:')
    for key in updateDict.keys():
        logger.debug('%s : %s' % (key, updateDict[key]))
    logger.debug('Status:')
    for key in statusDict.keys():
        logger.debug('%s : %s' % (key, statusDict[key]))
        

    return retdict       
                
    

