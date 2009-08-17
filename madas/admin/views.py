# Create your views here.
from django.db import models
from ccgauth import LDAPHandler

from madas.utils import setRequestVars, jsonResponse, json_encode, translate_dict
from madas.m.models import Quoterequest, Formalquote
from django.db.models import Q

from django.conf import settings

def admin_requests(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Active Requests
       Accessible by Administrators, Node Reps
    '''
    print '***admin requests : enter***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###

    print 'admin_requests'
    #provide livegrid pager data for admin requests
    searchgroup = []

    import utils
    g = utils.getGroupsForSession(request)
    
    if 'Administrators' not in g and 'Node Reps' in g:
        from madas.users import views
        searchgroup = views.getNodeMemberships(g)
    searchgroup.append('Pending')
    
    print 'Searchgroup was: ', searchgroup    
    
    ld = LDAPHandler() 
    ul = ld.ldap_list_users(searchgroup)
   
    #now do our keyname substitution
    newlist = []
    try:
        for entry in ul:
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
            newlist.append(d)
    except Exception, e:
        print 'admin_requests: Exception: ', str(e)   

    print '***admin requests : exit***'
    setRequestVars(request, success=True, items=newlist, totalRows=len(newlist), authenticated=True, authorized=True)

    return jsonResponse(request, [])  

def setup_groups(request, *args):
    return jsonResponse(request, []) 

def user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Active User Search
       Accessible by Administrators, Node Reps
    '''
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    
    import utils
    g = utils.getGroupsForSession(request)
    searchGroup = []
    
    if 'Administrators' not in g and 'Node Reps' in g:
        from madas.users import views
        searchGroup = views.getNodeMemberships(g)
    
    #no matter what, include Active users in the group. 
    searchGroup.append('User')

    ld = LDAPHandler()
    
    ul = ld.ldap_list_users(searchGroup)
    
    #print 'UL', ul

    #now do our keyname substitution
    newlist = []
    try:
        for entry in ul:
            from madas.users.views import _userload
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
            f = _userload(entry['uid'][0])
            if len(f) > 0:
                d['isClient'] = f['isClient']
            else:
                d['isClient'] = False

            newlist.append(d)
    except Exception, e:
        print json_encode(f)   



    setRequestVars(request, success=True, items=newlist, totalRows=len(newlist), authenticated=True, authorized=True)
    return jsonResponse(request, []) 

def rejected_user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Rejected User Search
       Accessible by Administrators, Node Reps
    '''
    print '***rejected_user_search : enter ***' 
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###


    ld = LDAPHandler()
    searchgroup = []
   
    import utils 
    g = utils.getGroupsForSession(request)
    
    if 'Administrators' not in g and 'Node Reps' in g:
        from madas.users import views
        searchgroup = views.getNodeMemberships(g)
    searchgroup.append('Rejected') #What about if this is already in there?

    print '\tsearch group was ', searchgroup
    ld = LDAPHandler()
    ul = ld.ldap_list_users(searchgroup)
    
    #print 'UL', ul

    #now do our keyname substitution
    newlist = []
    try:
        for entry in ul:
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
            newlist.append(d)
    except Exception, e:
        print '\tEXCEPTION: ', str(e)
    setRequestVars(request, success=True, items=newlist, totalRows=len(newlist), authenticated=True, authorized=True)
    print '***rejected_user_search : exit ***' 
    return jsonResponse(request, []) 

def deleted_user_search(request, *args):
    '''This corresponds to Madas Dashboard->Admin->Deleted User Search
       Accessible by Administrators, Node Reps
    '''
    print '***deleted_user_search : enter ***' 
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    
    import utils
    g = utils.getGroupsForSession(request) 
    searchgroup = [] 
    if 'Administrators' not in g and 'Node Reps' in g:
        from madas.users import views
        searchgroup = views.getNodeMemberships(g)
    searchgroup.append('Deleted') #What about if this is already in there?

    print '\tsearch group was ', searchgroup
    ld = LDAPHandler()
    ul = ld.ldap_list_users(searchgroup)
   
    #now do our keyname substitution
    newlist = []
    try:
        for entry in ul:
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
            newlist.append(d)
    except Exception, e:
        print str(e)
    print '\tNewList: ', newlist
    setRequestVars(request, success=True, items=newlist, totalRows=len(newlist), authenticated=True, authorized=True)
    print '***deleted_user_search : exit ***' 
    return jsonResponse(request, []) 

def user_load(request, *args):
    '''This is called when an admin user opens up an individual user record
       from an admin view e.g. Active User Search
       Accessible by Administrators, Node Reps
    '''
    print '***admin/user_load : enter ***' 
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
   
    import madas.users 
    from madas.users.views import _userload
    d = _userload(request.REQUEST['username'])

    setRequestVars(request, success=True, data=d, totalRows=len(d.keys()), authenticated=True, authorized=True)
    print '***admin/user_load : exit ***' 
    return jsonResponse(request, [])

def user_save(request, *args):
    '''This is called when an admin user hits save on an individual user record
       from an admin view e.g. Active User Search
       Accessible by Administrators, Node Reps
    '''
    print '***admin/user_save : enter ***' 
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
   
    import madas.users 
    from madas.users.views import _usersave
    oldstatus, status =  _usersave(request, request.REQUEST['email'], admin=True)

    #oldstatus is a list. Even though people should only have one status, if there
    #is ever an error state where they do somehow end up in two states (or 0) it is easier
    #to leave oldstatus as a list and use a foreach than it is to test lengths and do a bunch
    #of dereferencing. By rights, oldstatus should only contain one element though.
    if status not in oldstatus:
        print '\toldstatus (%s) was not equal to status (%s)' % (oldstatus, status)
        from mail_functions import sendApprovedRejectedEmail, sendAccountModificationEmail
        if status == 'User':
            status = 'Approved' #transform status name
        if status == 'Approved' or status == 'Rejected':
            sendApprovedRejectedEmail(request, request.REQUEST['email'], status)
        else:
            sendAccountModificationEmail(request, request.REQUEST['email'])
        

    #do something based on 'status' (either '' or something new)
    nextview = 'admin:usersearch'
    if status != '':
        if status == 'Pending':
            nextview = 'admin:adminrequests'
        elif status == 'Rejected':
            nextview = 'admin:rejectedUsersearch'
        elif status == 'Deleted':
            nextview = 'admin:deletedUsersearch'



    setRequestVars(request, success=True, authenticated=True, authorized=True, mainContentFunction = nextview)
    print '***admin/user_save : exit ***' 

    return jsonResponse(request, []) 

def list_groups(request, *args):
    pass
    #return jsonResponse(request, []) 

def node_save(request, *args):
    '''This is called when saving node details in the Node Management.
       Madas Dashboard->Admin->Node Management
       Accessible by Administrators, Node Reps
    '''
    print '*** node_save : enter ***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    oldname = str(request.REQUEST.get('originalName', ''))
    newname = str(request.REQUEST.get('name', ''))
    print '\toriginal name was: ', oldname 
    print '\tnew name is: ', newname
   
    returnval = False 
    if oldname!=newname and newname !='':
        if oldname == '':
            #new group
            #Group creation/renaming requires an admin auth to ldap.
            ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
            returnval = ld.ldap_add_group(newname)
        else:
            #rename
            #Group creation/renaming requires an admin auth to ldap.
            ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
            returnval = ld.ldap_rename_group(oldname, newname)
    print '\tnode_save: returnval was ', returnval      
    #TODO: the javascript doesnt do anything if returnval is false...it just looks like nothing happens.
    setRequestVars(request, success=returnval, authenticated=True, authorized=True, mainContentFunction='admin:nodelist')
    print '*** node_save : exit ***'
    return jsonResponse(request, []) 

def node_delete(request, *args):
    '''This is called when saving node details in the Node Management.
       Madas Dashboard->Admin->Node Management
       Accessible by Administrators, Node Reps
    '''
    print '*** node_delete : enter ***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'admin', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###

 
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

    setRequestVars(request, success=True, authenticated=True, authorized=True, mainContentFunction='admin:nodelist')
    print '*** node_delete : enter ***'
    return jsonResponse(request, []) 

