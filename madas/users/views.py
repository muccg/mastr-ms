# Create your views here.
from django.contrib.auth.ldap_helper import LDAPHandler
from madas.utils import setRequestVars, jsonResponse, translate_dict, makeJsonFriendly
from django.conf import settings

from madas.m.views import authorize

def _translate_madas_to_ldap(mdict):
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
                            ])
    return retdict


def _translate_ldap_to_madas(ldict):
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
                            ])
    return retdict


def _userload(username):
    'takes a username, returns a dictionary of results'
    'returns empty dict if the user doesnt exist'
    ld = LDAPHandler()
    r = ld.ldap_get_user_details(username)

    if len(r) == 0:
        return {}

    #Now we do some app specific key renaming
    #for key in r.keys():
    #    print '\t', key, ':', r[key]    

    d = _translate_ldap_to_madas(r) 
    d['originalEmail'] = d['email']

    #groups
    try:
        g = get_madas_user_groups(username, False)
        #substitute 'Active' for 'User' for visual purposes
        l = g['status']
        for index, s in enumerate(l):
            if l[index] == 'User':
                l[index] = 'Active'
        #repackage 'groups' as 'node'
        gr = g['groups']
        nodes = getNodeMemberships(gr)
        #print 'userload: nodes are:', nodes
        if len(nodes) > 0:
            d['node'] = nodes[0]
        else:
            d['node'] = '' #TODO: should this be 'don't know? or something...perhaps 'None'

        #isadmin, isnoderep
        #these are used for the initial values of checkboxes.
        if 'Administrators' in gr:
            d['isAdmin'] = True
        else:
            d['isAdmin'] = False
        if 'Node Reps' in gr:
            d['isNodeRep'] = True
        else:
            d['isNodeRep'] = False
        if len(gr) == 0:
            d['isClient'] = True
        else:
            d['isClient'] = False
        
        d.update(g)
    except Exception, e:
        print '\tEXCEPTION: get madas user group failed: ', str(e)

    

    return d
    


def userload(request, *args):
    '''This is called when loading user details - when the user
       clicks on the User button in the dashboard and selects 'My Account'
       Accessible by any logged in user
    '''
    print '***userload : enter ***' 
    ### Authorisation Check ###
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    u = request.REQUEST.get('username', request.user.username)


    d = _userload(u)

    d = makeJsonFriendly(d)

    setRequestVars(request, success=True, data=d, totalRows=len(d.keys()), authenticated=True, authorized=True)
    print '***userload : exit ***' 
    return jsonResponse(request, [])   




from madas.settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
def get_madas_user_groups(username, include_status_groups = False):
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
	
def _usersave(request, username, admin=False):
    ''' Saves user details, from a form.
    Uses the form details from the request, but and the supplied username.
    If this is an admin save (i.e. the user is not necessarily updating
    their own record), then pass admin = True, so that an admin level LDAP
    connection can be made.'''
    r = request.REQUEST
    u = username
   
    originalEmail = str(u)
    username = str(r.get('email', originalEmail)) #if empty, set to originalEmail
    email = str(r.get('email', originalEmail)) #if empty, set to originalEmail
    password = (str(r.get('password',  ''))).strip() #empty password will be ignored anyway.
    firstname = str(r.get('firstname', ''))
    lastname = str(r.get('lastname', ''))
    telephoneNumber = str(r.get('telephoneNumber', ''))
    homephone = str(r.get('homephone', ''))
    physicalDeliveryOfficeName = str(r.get('physicalDeliveryOfficeName', ''))
    title = str(r.get('title', '' ))
    dept = str(r.get('dept', ''))
    institute = str(r.get('institute', ''))
    address= str(r.get('address', ''))
    supervisor = str(r.get('supervisor', ''))
    areaOfInterest = str(r.get('areaOfInterest', ''))
    country = str(r.get('country', ''))
    
    isAdmin = r.get('isAdmin')
    isNodeRep = r.get('isNodeRep')
    node = str(r.get('node'))
    status = str(r.get('status', None))

    if status == 'Active':
        status = 'User'


    updateDict = {} #A dictionary to hold name value pairs of attrubutes to pass to LDAP to update.
                    #The name fields must match the ldap schema - no translation is done by the 
                    #LDAP module.

    updateDict['mail'] = email
    updateDict['telephoneNumber'] = telephoneNumber 
    updateDict['physicalDeliveryOfficeName'] = physicalDeliveryOfficeName
    updateDict['title'] = title
    updateDict['cn'] = "%s %s" % (firstname, lastname)
    updateDict['givenName'] = firstname
    updateDict['sn'] = lastname
    updateDict['homePhone'] = homephone
    updateDict['postalAddress'] = address
    updateDict['description'] = areaOfInterest
    updateDict['destinationIndicator'] = dept
    updateDict['businessCategory'] = institute
    updateDict['registeredAddress'] = supervisor
    updateDict['carlicense'] = country
   
   
    #Any fields that were passed through as empty should be refilled with their old values, if possible
    #i.e. if the user existed.
    previous_details = _userload(u)
    previous_details = _translate_madas_to_ldap(previous_details)
    
    #print 'Previous: '
    #print previous_details
    for field in updateDict.keys():
        if updateDict[field] == '':
            print 'Empty field. Replacing with previous value: \'',previous_details.get(field, ''), '\'' 
            updateDict[field] = previous_details.get(field, '')

    import utils
    groups = get_madas_user_groups(u, False)
    oldstatus = []
    #sanitise the format of 'groups' - we dont want the statuses.
    if len(groups) > 0:
        #get status info first
        if len(groups['status']) > 0:
            oldstatus = groups['status']
        else:
            oldstatus = []
        #then make groups just the groups part
        groups = groups['groups']
    else:
        groups = []
    oldnodes = getNodeMemberships(groups)
    oldnode = []
    if len(oldnodes) > 0:
        oldnode = [oldnodes[0]] #only allow one 'oldnode'
    else:
        oldnode = []

    print 'Groups is: ', groups
    print 'Nodes is: ', oldnode
    print 'User Groups is: ', get_madas_user_groups(u, False)
    print 'Node is ', node

    #don't let a non-admin change their node
    if request.session.has_key('isAdmin') and request.session['isAdmin'] and admin:
        #TODO do something with the new status
        if node != '': #empty string is 'Don't Know' 
            newnode = [node] #only allow one 'newnode'
            print 'Got new node %s and was admin' % (node)
        else:
            newnode = []
    else:
        #TODO use the old status, don't capture whatever was POSTed.
        newnode = oldnode

    #We dont actually permit the user to modify their email address at the moment for security purposes.
    #Get an admin connection to LDAP
    from madas import settings
    ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
    r = None
    try:
        if previous_details == {}: #the user didnt exist
            #objclasses = ['top', 'inetOrgPerson', 'simpleSecurityObject', 'organizationalPerson', 'person']
            objclasses = 'inetorgperson'
            worked = ld.ldap_add_user(username, updateDict, objectclasses=objclasses, usercontainer='ou=NEMA', userdn='ou=People', basedn='dc=ccg,dc=murdoch,dc=edu,dc=au')
            ld.ldap_add_user_to_group(username, 'Pending')
            if not worked:
                raise Exception, 'Could not add user %s' % (username)
        else:
            r = ld.ldap_update_user(u, username, password, updateDict, pwencoding='md5')
        print '\tUser update successful for %s' % (u) 
    except Exception, e:
        print '\tException when updating user %s: %s' % (u, str(e))
   
    #only trust the isAdmin checkbox if editing user is an admin
    if request.session.has_key('isAdmin') and request.session['isAdmin'] and admin:
        #honour 'isAdmin' checkbox
        if isAdmin is not None:
            if isAdmin:
                print 'isAdmin was True!'
                # add the user to the administrators group - but not if they are already there.
                ld.ldap_add_user_to_group(username, 'Administrators')
            else:
                print 'isAdmin was False!'
                #only remove from admin group if logged in name doesnt match name of user being updated.
                #i.e. don't let an admin user un-admin themselves
                if request.user.username != username:
                    ld.ldap_remove_user_from_group(username, 'Administrators')
        else:
            print 'isAdmin was False!'
            #only remove from admin group if logged in name doesnt match name of user being updated.
            #i.e. don't let an admin user un-admin themselves
            if request.user.username != username:
                ld.ldap_remove_user_from_group(username, 'Administrators')
        
        print '\tperforming node updates for ', username
        print '\tnewnode: ', newnode
        print '\toldnode: ', oldnode
        #update to new nodes
        for nn in newnode:
            if nn not in oldnode:
                print '\tAdding %s to group: %s' % (username, nn)
                ld.ldap_add_user_to_group(username, nn)
        
        for on in oldnodes: #note this is oldnodes, not oldnode. So this is the original list.
            if on not in newnode:
                #remove from any incorrect nodes:
                print '\tRemoving %s from group: %s' % (username, on)
                ld.ldap_remove_user_from_group(username, on)

    else: #user wasnt an admin
        print 'Non admin user. No node updates performed'

    if admin and (request.session['isAdmin'] or request.session['isNodeRep']):
        #honour 'isNodeRep' checkbox
        if isNodeRep is not None:
            if isNodeRep: 
                print 'isNodeRep was True!'
                #add to node reps group
                ld.ldap_add_user_to_group(username, 'Node Reps')
            else:
                print 'isNodeRep was False!'
                #remove from node reps group
                ld.ldap_remove_user_from_group(username, 'Node Reps')
        else:
            print 'isNodeRep was False!'
            #remove from node reps group
            #i.e. don't let a noderep user un-admin themselves
            if request.user.username != username:
                ld.ldap_remove_user_from_group(username, 'Node Reps')

        
        #do status changes
        if status is not None:
            #be careful not to remove the user from all groups - this is a real pain to correct.
            #instead, add them to a group first, and only do the remove if the add succeeds.

            print '\tAdding %s to group %s' % (username, status)
            if ld.ldap_add_user_to_group(username, status):
                for old_st in oldstatus:
                    if old_st != status: #don't remove them from the group we just added them to
                        print '\tRemoving %s from group: %s' % (username, old_st)
                        ld.ldap_remove_user_from_group(username, old_st)
            else:
                print '\tWARNING: Could not add %s to %s, so removal from %s was not done.' % (username, status, oldstatus)
            
    else:
        print 'Non admin/node-rep user. No Status updates performed.'

    #force a new lookup of the users' groups to be cached, in case the modified user is the logged in user.
    import madas.utils
    madas.utils.getGroupsForSession(request, force_reload = True)

    if status is None or not request.session['isAdmin']:
        return oldstatus, oldstatus
    else:
        return oldstatus, status

def userSave(request, *args):
    '''This is called when saving user details - when the user
       clicks on the User button in the dashboard and selects 'My Account',
       changes some details, and hits 'save'
       Accessible by any logged in user
    '''
    print '***users/userSave : enter ***' 
    ### Authorisation Check ###
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
 
    u = request.user.username
    returnval = _usersave(request,u)

    from mail_functions import sendAccountModificationEmail
    sendAccountModificationEmail(request, u)
    setRequestVars(request, success=True, data = None, totalRows = 0, authenticated = True, authorized = True, mainContentFunction='user:myaccount')

    print '***users/userSave : exit ***' 
    return jsonResponse(request, [])

def getNodeMemberships(groups):
    print '\tusers/getNodeMemberships'
    from madas.settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    specialNodes = MADAS_STATUS_GROUPS + MADAS_ADMIN_GROUPS
    #TODO get groups from 'credentials' - cached in MadasUser
    #for now, using groups that are passed in
    print '\tgroups', groups 
    i = [item for item in groups if not item in specialNodes]
    print '\tgetNodeMemberships returning ' , i
    return i
