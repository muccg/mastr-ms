# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from mastrms.users.MAUser import *
from mastrms.users.MAUser import _translate_ldap_to_madas, _translate_madas_to_ldap
from mastrms.app.utils.data_utils import jsonResponse, makeJsonFriendly
from mastrms.app.utils.mail_functions import sendAccountModificationEmail

##The user info view, which sends the state of the logged in
##user to the frontend.
def userinfo(request):
    m = getCurrentUser(request, force_refresh = True)
    return HttpResponse(m.toJson())


def listAllNodes(request, *args):
    '''
    This view lists all nodes in the system
    These are the groups left over when the
    status and administrative groups are removed

    The format for the return is a list of dicts,
    each entry having a 'name' and a 'submitvalue'

    Note: this is for use in a dropdown which expects
    an additional option "Don't Know" which has the value ''.
    If request.REQUEST has 'ignoreNone', we do not do this.
    ""
    '''
    ldapgroups = getMadasGroups()
    groups = []
    if not request.REQUEST.has_key('ignoreNone'):
        groups.append({'name':'Don\'t Know', 'submitValue':''})

    for groupname in ldapgroups:
        #Cull out the admin groups and the status groups
        if groupname not in MADAS_STATUS_GROUPS and groupname not in MADAS_ADMIN_GROUPS:
            groups.append({'name':groupname, 'submitValue':groupname})
    return jsonResponse(items=groups)



#Use view decorator here
@login_required
def userload(request, *args):
    '''This is called when loading user details - when the user
       clicks on the User button in the dashboard and selects 'My Account'
       Accessible by any logged in user
    '''
    logger.debug('***userload : enter ***')
    u = request.REQUEST.get('username', request.user.username)
    d = [loadMadasUser(u)]
    d = makeJsonFriendly(d)
    logger.debug('***userload : exit ***')
    return jsonResponse(data=d)

def userSave(request, *args):
    '''This is called when saving user details - when the user
       clicks on the User button in the dashboard and selects 'My Account',
       changes some details, and hits 'save'
       Accessible by any logged in user
    '''
    logger.debug('***users/userSave : enter ***' )
    success = False
    currentuser = getCurrentUser(request)
    parsedform = getDetailsFromRequest(request)

    #With a usersave, you are always editing your own user
    parsedform['username'] = currentuser.Username
    success = saveMadasUser(currentuser,parsedform['username'], parsedform['details'], parsedform['status'], parsedform['password'])
    #refresh the user in case their details were just changed
    currentuser = getCurrentUser(request, force_refresh=True)

    if success:
        sendAccountModificationEmail(request, parsedform['username'])
    else:
        logger.error('Error saving user: %s' % (parsedform['username']))
        raise Exception('Error saving user.')

    logger.debug('***users/userSave : exit ***')
    return jsonResponse(mainContentFunction='user:myaccount')





