# Create your views here.
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotFound
from ccg.auth.ldap_helper import LDAPHandler
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib import logging

from madas.utils.data_utils import jsonResponse, jsonErrorResponse, translate_dict
from madas.quote.models import Quoterequest, Formalquote, Organisation, UserOrganisation
from madas.repository.json_util import makeJsonFriendly
from madas.decorators import admins_only, admins_or_nodereps, privileged_only, authentication_required
from madas.users.MAUser import * #All the MAUser functions, plus the groups information 
from madas.utils.mail_functions import sendApprovedRejectedEmail, sendAccountModificationEmail

logger = logging.getLogger('madas_log')


def _filter_users(groups, requestinguser):
    '''This function produces a list of users, according to Madas rules, 
    that is, if the requesting user is an Admin, they see all users in 'groups',
    but if they are only a noderep, they only see members in 'groups' who are 
    also in their node'''

    retval = []
    if not requestinguser.IsPrivileged:
        return retval #early exit. Bad data.
    
    
    searchGroups = []
    if not (requestinguser.IsAdmin or requestinguser.IsMastrAdmin) and requestinguser.IsPrivileged:
        searchGroups += requestinguser.Nodes
    
    searchGroups += groups

    #The default 'method' is and
    userlist = getMadasUsersFromGroups(searchGroups) 
   
    #now do our keyname substitution
    try:
        for entry in userlist:
            d = translate_dict(entry, [\
                           ('uid', 'username'), \
                           ('commonName', 'commonname'), \
                           ('givenName', 'firstname'), \
                           ('sn', 'lastname'), \
                           ('mail', 'email'), \
                           ('telephoneNumber', 'telephoneNumber'), \
                           ('homephone', 'homephone'), \
                           ('physicalDeliveryOfficeName', 'physicalDeliveryOfficeName'), \
                           ('title', 'title'), \
                                ]) 
            retval.append(d)
    except Exception, e:
        logger.warning('_filter_users: Exception: %s' % ( str(e) ) )  
    return retval    


@admins_or_nodereps
def admin_requests(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Active Requests
       Accessible by Administrators, Node Reps
    '''
    currentuser = getCurrentUser(request)
    newlist = _filter_users([MADAS_PENDING_GROUP], currentuser) 
    return jsonResponse(items=newlist)  

@privileged_only
def user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Active User Search
       Accessible by Administrators, Node Reps
    '''
    currentuser = getCurrentUser(request)
    newlist = _filter_users([MADAS_USER_GROUP], currentuser)
    return jsonResponse(items=newlist) 

@admins_or_nodereps
def rejected_user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Rejected User Search
       Accessible by Administrators, Node Reps
    '''
    currentuser = getCurrentUser(request)
    newlist = _filter_users([MADAS_REJECTED_GROUP], currentuser)
    return jsonResponse(items=newlist) 

@admins_or_nodereps
def deleted_user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Deleted User Search
       Accessible by Administrators, Node Reps
    '''
    currentuser = getCurrentUser(request)
    newlist = _filter_users([MADAS_DELETED_GROUP], currentuser)
    return jsonResponse(items=newlist) 

@privileged_only
def user_load(request, *args):
    '''This is called when an admin user opens up an individual user record
       from an admin view e.g. Active User Search
       Accessible by Administrators, Node Reps
    '''
    logger.debug('***admin/user_load : enter ***' )
    d = loadMadasUser(request.REQUEST['username'])
    #find user organisation
    try:
        u = User.objects.get(username=request.REQUEST['username'])
        orgs = UserOrganisation.objects.filter(user=u)
        d['organisation'] = ''
        if len(orgs) > 0:
            d['organisation'] = orgs[0].organisation.id
            logger.debug('user in org %d' % (orgs[0].organisation.id))
    except Exception, e:
        logger.debug('Exception loading organisation %s' % (str(e)) )
        pass

    logger.debug('***admin/user_load : exit ***' )
    return jsonResponse(data=d)

@privileged_only
def user_save(request, *args):
    '''This is called when an admin user hits save on an individual user record
       from an admin view e.g. Active User Search
       Accessible by Administrators, Node Reps
    '''
    logger.debug('***admin/user_save : enter ***') 
    currentuser = getCurrentUser(request)
    parsedform = getDetailsFromRequest(request)
    #look up the user they are editing:
    existingUser = getMadasUser(parsedform['username'])
    existingstatus = existingUser.StatusGroup 
    success = saveMadasUser(currentuser, parsedform['username'], parsedform['details'], parsedform['status'], parsedform['password'])
    existingUser.refresh()
    newstatus = existingUser.StatusGroup

    if newstatus != existingstatus:
        if newstatus == MADAS_USER_GROUP or newstatus == MADAS_REJECTED_GROUP:
            #email to usernames works since usernames are email addresses
            sendApprovedRejectedEmail(request, parsedform['username'], newstatus)
        else:
            sendAccountModificationEmail(request, parsedform['username'])
    #do something based on 'status' (either '' or something new)
    nextview = 'admin:usersearch'
    if newstatus != '':
        if newstatus == MADAS_PENDING_GROUP:
            nextview = 'admin:adminrequests'
        elif newstatus == MADAS_REJECTED_GROUP:
            nextview = 'admin:rejectedUsersearch'
        elif newstatus == MADAS_DELETED_GROUP:
            nextview = 'admin:deletedUsersearch'

    #apply organisational changes
    try:
        targetUser = User.objects.get(username=request.REQUEST['email'])
    except:
        targetUser = User.objects.create_user(request.REQUEST['email'], request.REQUEST['email'], '')
        targetUser.save()
        
    try:
        UserOrganisation.objects.filter(user=targetUser).delete()

        org = Organisation.objects.get(id=request.REQUEST['organisation'])
    
        if org:
            uo = UserOrganisation(user=targetUser, organisation=org)
            uo.save()
            logger.debug('added user to org')
    except Exception, e:
        logger.warning('FATAL error adding or removing user from organisation: %s' % (str(e)))

    logger.debug('***admin/user_save : exit ***' )

    return jsonResponse(mainContentFunction=nextview) 

@admins_or_nodereps
def node_save(request, *args):
    '''This is called when saving node details in the Node Management.
       Madas Dashboard->Admin->Node Management
       Accessible by Administrators, Node Reps
    '''
    logger.debug('*** node_save : enter ***')
    oldname = str(request.REQUEST.get('originalName', ''))
    newname = str(request.REQUEST.get('name', ''))
   
    returnval = False 
    if oldname!=newname and newname !='':
        #Group creation/renaming requires an admin auth to ldap.
        ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
        if oldname == '':
            returnval = ld.ldap_add_group(newname)
            err_msg = "Couldn't add new node: " + newname
        else:
            returnval = ld.ldap_rename_group(oldname, newname)
            err_msg = "Couldn't rename node %s to %s" + (oldname, newname)
    else:
        #make no changes.
        logger.warning("Node save: oldname was newname, or newname was empty. Aborting")
    
    logger.debug('\tnode_save: returnval was %s' % (str(returnval )))     
    #TODO: the javascript doesnt do anything if returnval is false...it just looks like nothing happens.
    logger.debug( '*** node_save : exit ***' )
    if returnval:
        return jsonResponse(mainContentFunction='admin:nodelist')
    else:
        return jsonErrorResponse(err_msg)

@admins_or_nodereps
def node_delete(request, *args):
    '''This is called when saving node details in the Node Management.
       Madas Dashboard->Admin->Node Management
       Accessible by Administrators, Node Reps
    '''
    logger.debug('*** node_delete : enter ***')
    #We must make sure 'Administrator' and 'User' groups cannot be deleted.
    delname = str(request.REQUEST.get('name', ''))
    ldelname = delname.lower()
    if ldelname == 'administrators' or ldelname == 'users':
        #Don't delete these sorts of groups.
        pass
    else:
        #Group creation/renaming requires an admin auth to ldap.
        ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
        ret = ld.ldap_delete_group(delname)

    logger.debug( '*** node_delete : enter ***' )
    return jsonResponse(mainContentFunction='admin:nodelist') 

@admins_or_nodereps
def org_save(request):

    org_id = request.REQUEST.get('id', None)

    if org_id is not None and org_id != '':
        if org_id == '0':
            org = Organisation()
        else:
            org = Organisation.objects.get(id=org_id)
        
    org.name = args['name']
    org.abn = args['abn']
    
    org.save()
        
    return jsonResponse()
    
@admins_or_nodereps
def org_delete(request):

    args = request.REQUEST
    org_id = args['id']

    rows = Organisation.objects.filter(id=org_id)
    rows.delete()

    return jsonResponse()

@authentication_required
def list_organisations(request):

    if request.GET:
        args = request.GET
    else:
        args = request.POST
       

    # basic json that we will fill in
    output = {'metaData': { 'totalProperty': 'results',
                            'successProperty': 'success',
                            'root': 'rows',
                            'id': 'id',
                            'fields': [{'name':'id'}, {'name':'name'}, {'name':'abn'}]
                            },
              'results': 0,
              'authenticated': True,
              'authorized': True,
              'success': True,
              'rows': []
              }

    authenticated = request.user.is_authenticated()
    authorized = True # need to change this
    if not authenticated or not authorized:
        return HttpResponse(json.dumps(output), status=401)


    rows = Organisation.objects.all() 

    # add row count
    output['results'] = len(rows);

    # add rows
    for row in rows:
        d = {}
        d['id'] = row.id
        d['name'] = row.name
        d['abn'] = row.abn

        output['rows'].append(d)


    output = makeJsonFriendly(output)

    return HttpResponse(json.dumps(output))
