# Create your views here.

from django.db import models
from django.contrib.auth.ldap_helper import LDAPHandler

from madas.utils import setRequestVars, jsonResponse, json_encode
from madas.m.models import Quoterequest, Formalquote, Quotehistory, Emailmap
from django.db.models import Q

from madas import settings

QUOTE_STATE_DOWNLOADED = 'downloaded'
QUOTE_STATE_NEW = 'new' #is the default on the DB column
QUOTE_STATE_ACCEPTED = 'accepted'
QUOTE_STATE_REJECTED = 'rejected'

def listGroups(request, *args):
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True, perms=MADAS_ADMIN_GROUPS)
    #We ignore the auth result here, because we want pages to be able to use listGroups when not authed (i.e. Make an Inquiry)
    #if auth_result is not True:
    #    return auth_response
    ### End Authorisation Check ###
  
    #debug function    
    ld = LDAPHandler()
    r = ld.ldap_list_groups()
    print 'listGroups: the groups were: ', r
    groups = []
    if not request.REQUEST.has_key('ignoreNone'):    
        d = {'name':'Don\'t Know', 'submitValue':''}
        groups.append(d)

    for groupname in r:

        #Cull out the admin groups and the status groups
        if groupname not in MADAS_STATUS_GROUPS and groupname not in MADAS_ADMIN_GROUPS:
            d = {'name':groupname, 'submitValue':groupname}
            groups.append(d)       
    
         
    setRequestVars(request, success=True, items=groups, totalRows=len(groups), authenticated=True, authorized=True)
    return jsonResponse(request, [])
    

def listRestrictedGroups(request, *args):
    print '*** list Restricted Groups : enter ***'
    import utils
    g = utils.getGroupsForSession(request)
    if 'Administrators' in g:
        retval = listGroups(request)
    else:
        from madas.users.views import getNodeMemberships
        n = getNodeMemberships(g)
        print 'NodeMemberships: ', n
        groups = []
        
        from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS

        for groupname in n:

            #Cull out the admin groups and the status groups
            if groupname not in MADAS_STATUS_GROUPS and groupname not in MADAS_ADMIN_GROUPS:
                d = {'name':groupname, 'submitValue':groupname}
                groups.append(d) 
            
            groups.append({'name':'Don\'t Know', 'submitValue':''})
        
        setRequestVars(request, items=groups, success=True, totalRows=len(groups), authenticated=True, authorized=True)
        retval = jsonResponse(request, [])
    print '*** list Restricted Groups : exit ***'
    return retval 


def _handle_uploaded_file(f, name):
    '''Handles a file upload to the projects QUOTE_FILES_ROOT
       Expects a django InMemoryUpload object, and a filename'''
    print '*** _handle_uploaded_file: enter ***'
    retval = False
    try:
        import os
        destination = open(os.path.join(settings.QUOTE_FILES_ROOT, name ), 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        retval = True
    except Exception, e:
        retval = False
        print '\tException in file upload: ', str(e)
    print '*** _handle_uploaded_file: exit ***'
    return retval

def _findAdminOrNodeRepEmailTarget(groupname = 'Administrators'): #TODO use MADAS_ADMIN_GROUP constant
    print '*** _findAdminOrNodeRepEmailTarget : enter ***'
    #find an admin, or a node rep for the group passed in.
    #if no group was passed, we assume 'Administrators'
    grouplist = []
    grouplist.append(groupname)
    if groupname is not 'Administrators':
        grouplist.append('Node Reps')
    
    ld = LDAPHandler()
    users = ld.ldap_list_users(grouplist)
    print '\t Users found: ', users
   
    #NOTE: If this function finds multiple users to email, it only returns the
    #      first one. If we ever need to change this, here is the place to do it!
    retval = users
    print 'returning all records: ', retval
    print '*** _findAdminOrNodeRepEmailTarget : exit ***'
    return retval 



def sendRequest(request, *args):
    print '***quote: sendRequest***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###

    print '\tgetting args'
    email = request.REQUEST.get('email', None)
    firstname = request.REQUEST.get('firstname', None)
    lastname = request.REQUEST.get('lastname', None)
    officePhone = request.REQUEST.get('telephoneNumber', None)
    toNode = request.REQUEST.get('node', None)
    details = request.REQUEST.get('details', None)
    country = request.REQUEST.get('country', None)
    fileName = request.REQUEST.get('fileName', None)
    print '\tfinished getting args' 

    try:
        #add the new quote to the DB
        qr = _addQuoteRequest(email, firstname, lastname, officePhone, toNode, country, details)
    except Exception, e:
        print 'Exception adding quote request: ', str(e) 
  
    #TODO: if there is an exception here, we should really abort.

    try:
        #TODO handle file uploads - check for error values
        if request.FILES.has_key('attachfile'):
            f = request.FILES['attachfile']
            print '\tuploaded file name: ', f._get_name()
            translated_name = 'quote_attachment_' + str(qr.id) + '_' + f._get_name().replace(' ', '_')
            print '\ttranslated name: ', translated_name
            _handle_uploaded_file(f, translated_name)
            qr.attachment = translated_name
        else:
            print '\tNo file attached.'

        qr.save()

    except Exception, e:
        print '\tException: ', str(e)

    try: 
        from django.core.mail import send_mail
        #: to client
        from madas.mail_functions import sendQuoteRequestConfirmationEmail
        sendQuoteRequestConfirmationEmail(request, qr.id, email) 
        
        #email the administrator(s) for the node 
        print 'Argument to _findAdminOrNodeRepEmailTarget is: ', toNode
        if toNode == '': #if the node was 'Dont Know'
            searchgroups = 'Administrators'
        else:
            searchgroups = toNode
        targetUsers = _findAdminOrNodeRepEmailTarget(groupname = searchgroups)
        from madas.mail_functions import sendQuoteRequestToAdminEmail
        for targetUser in targetUsers:
            sendQuoteRequestToAdminEmail(request, qr.id, firstname, lastname, targetUser['uid'][0]) #toemail should be a string, but ldap returns are all lists
    except Exception, e:
        print 'Error sending mail in SendRequest: ', str(e)

    setRequestVars(request, success=True, authenticated=True, authorized=True, mainContentFunction='quote:request')
    print '*** quote:sendRequest: exit ***'
    return jsonResponse(request, [])       


def listQuotes(request, *args):
    '''This corresponds to Madas Dashboard->Quotes->View Quote Requests
       Accessible by Administrators, Node Reps
    '''
    ### Authorisation Check ###
    from madas.m.views import authorize
    from madas.settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS 
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    print '*** quote/listQuotes : enter *** '
    #TODO: Find out which nodes this user represents, or if they are an administrator
    import utils
    g = utils.getGroupsForSession(request)

    print '\tgroups was : ' + str(g)
    from madas.users import views
    print '\tcalling'
    nodelist = views.getNodeMemberships(g)
    print '\tnode was : ' , nodelist

    results = [] 

    try:
        print '\tRetrieving quotes for: ', nodelist[0]
        quoteslist = Quoterequest.objects.filter(tonode=nodelist[0]).values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        for ql in quoteslist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            results.append(ql)
    except Exception, e:
        print 'exception: ', str(e)

    if 'Administrators' in g:
        print '\tchecking administrators'
        print '\tRetrieving quotes for: Administrators' 
        adminlist = Quoterequest.objects.filter(tonode='').values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        print '\tadmini query finished'
        for ql in adminlist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            results.append(ql)
        print '\tkey renaming finished'

    try:
        from madas import utils
        #these may not be unique. need to uniquify them.
        resultsset = utils.uniqueList(results) 
    except Exception, e:
        print '\tEXCEPTION when constructing unique list:', str(e) 
    print '\tfinished generating quoteslist' 

    setRequestVars(request, items=resultsset, totalRows=len(resultsset), success=True, authenticated=True, authorized=True) 
    print '*** quote/listQuotes : exit *** '
    return jsonResponse(request, [])       
    
def listAll(request, *args):
    '''This corresponds to Madas Dashboard->Quotes->Overview List
       Accessible by Administrators, Node Reps
    '''
    ### Authorisation Check ###
    from madas.m.views import authorize
    from madas.settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS 
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    print '*** quote/listAll - enter ***'
    ld = LDAPHandler()
    g =  ld.ldap_get_user_groups(request.user.username)

    print '\tgroups was : ' + str(g)
    from madas.users import views
    print '\tcalling'
    nodelist = views.getNodeMemberships(g)
    print '\tnode was : ' , nodelist

    results = [] 

    try:
        quoteslist = Quoterequest.objects.all().values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        for ql in quoteslist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            
            #find the time when this quote was marked as completed (if it is)
            if ql['completed'] == True:
                qh = Quotehistory.objects.filter(oldcompleted = False, completed = True)
                qh = qh[0]
                ql['changetimestamp'] = qh.changetimestamp
            
            results.append(ql)
    except Exception, e:
        print '\texception getting quotes: ', str(e)

    if 'Administrators' in g:
        print '\tchecking administrators'
        adminlist = Quoterequest.objects.filter(tonode='Administrators').values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        print '\tadmini query finished'
        for ql in adminlist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            
            #find the time when this quote was marked as completed (if it is)
            if ql['completed'] == True:
                qh = Quotehistory.objects.filter(oldcompleted = False, completed = True)
                qh = qh[0]
                ql['changetimestamp'] = qh.changetimestamp
            
            results.append(ql)
        print '\tkey renaming finished'

    try:
        from madas import utils
        resultsset = utils.uniqueList(results) #these may not be unique. need to uniquify them.
    except Exception, e:
        print '\tException making results set unique', str(e) 
    print '\tfinished generating quoteslist' 

    #TODO: The actual query should look like this

#        $sql .= "LEFT JOIN emailmap em ON em.id = qr.emailaddressid WHERE qr.tonode = :tonode";
    #$sql = "select qr.id, qr.completed, qr.unread, qr.tonode, qr.firstname, qr.lastname, qr.officephone, qr.details, to_char(qr.requesttime, 'YYYY/MM/DD HH24:MI:SS') as requesttime, em.emailaddress as email, to_char(qrh.changetimestamp, 'YYYY/MM/DD HH24:MI:SS') as changetimestamp from quoterequest as qr left join (select max(changetimestamp) as changetimestamp, quoteid from quotehistory where completed = true group by quoteid) as qrh on qr.id = qrh.quoteid left join emailmap em on em.id = qr.emailaddressid";

    setRequestVars(request, items=resultsset, success=True, totalRows=len(resultsset), authenticated=True, authorized=True) 
    print '*** quote/listAll - exit ***'
    return jsonResponse(request, []) 


def listFormal(request, *args):
    '''This corresponds to Madas Dashboard->Quotes->My Formal Quotes
       Accessible by Everyone
    '''
    print '*** listFormal : enter ***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    
    uname = request.user.username
    ld = LDAPHandler()
    g =  ld.ldap_get_user_groups(request.user.username)
    from madas.users import views

    nodelist = views.getNodeMemberships(g)

    #if a noderep or admin, and you have a node:
    if ('Administrators' in g or 'Node Reps' in g) and len(nodelist) > 0:
        fquoteslist = Formalquote.objects.filter(Q(fromemail__iexact=uname)|Q(toemail__iexact=uname)|Q(quoterequestid__tonode=nodelist[0])).values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status')        
    #otherwise show all quotes to me, from me, or from this node.
    else:
        fquoteslist = Formalquote.objects.filter(Q(fromemail__iexact=uname)|Q(toemail__iexact=uname)).values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status') 
    


    setRequestVars(request, success=True, items=fquoteslist, totalRows=len(fquoteslist), authenticated=True, authorized=True)
 
    print '*** listFormal : exit ***'
    return jsonResponse(request, []) 

def _loadQuoteRequest(qid):
    print '\tload: qid was ', qid
    if qid is not None and qid.isdigit() and qid is not '':
        qr = Quoterequest.objects.filter(id = qid).values('id', 'emailaddressid__emailaddress', 'tonode', 'details', 'requesttime', 'unread', 'completed', 'firstname', 'lastname', 'officephone', 'country', 'attachment')
        try:
            for ql in qr:
                ql['email'] = ql['emailaddressid__emailaddress']
                del ql['emailaddressid__emailaddress']
        except Exception, e:
            print 'exception: ', str(e)

    else:
        qr = [{}]
 
    qr = qr[0]    
    print '\tqr:', qr
    
    return qr
    

def load(request, *args):
    '''load quote details'''
    print '*** load : enter ***'
    qid = request.REQUEST.get('qid', None)
    if qid is None:
        qid = request.REQUEST.get('quoterequestid', None)

    suc = True
    if qid is not None:
        qr = _loadQuoteRequest(qid)
        
        #mark as read
        quote = Quoterequest.objects.get(id = qid)
        quote.unread = False
        quote.save()
        
        suc = True
    else:
        suc = False
        qr = []

    #TODO: mark quote as 'read' if not already.: updateQuoteRequestStatus($qid, $data['tonode'], ($data['completed'])?1:0, 0);
    setRequestVars(request, data=qr, totalRows=len(qr), success = suc, authenticated = True, authorized = True )
    print '*** load : exit ***'
    return jsonResponse( request, [] )
    
def history(request, *args):
    print '***quote/history : enter***'
    qid = request.REQUEST.get('qid', None)
    print '\tHistory: qid was ', qid
    if qid is not None:
        qh = Quotehistory.objects.filter(quoteid = qid).values()
    else:
        qh = []
 
    qh = list(qh)
    #ensure we have a sorted list by date. Most likely this wont change the list order
    #anyway, because they were probably retrieved in order.
    qh.sort(lambda x,y: cmp(x['changetimestamp'],y['changetimestamp']))
    qh.reverse()
    print '\t', qh 
    setRequestVars(request, data=qh, totalRows=len(qh), success = True, authenticated = True, authorized = True )
    print '***quote/history : exit***'
    return jsonResponse( request, [] )


def _getEmailMapping(email):
    print '*** _getEmailMapping: enter***'
    retval = None
    try:
        emmap = Emailmap.objects.get(emailaddress = email)
        retval = emmap
    except Emailmap.DoesNotExist, e:
        #we need to create a new entry.
        print '\tCreating new email mapping'
        newEmail = Emailmap(emailaddress = email)
        try:
            newEmail.save()
            retval = newEmail
        except Exception, e:
            print '\tEmailMapping exception', e
            retval = None
    print '*** _getEmailMapping: exit ***'
    return retval

def _updateQuoteRequestStatus(qr, tonode, completed=0, unread=0):
    qr.completed = completed
    qr.unread = unread
    qr.tonode = tonode
    qr.save()

def _addQuoteHistory(qr, emailaddress, newnode, oldnode, comment, newcompleted, oldcompleted):
    print '*** _addQuoteHistory: enter ***'
    #get the email mapping for this email address
    emailobj = _getEmailMapping(emailaddress)
    #store the history details
    retval = None
    try:
        q = Quotehistory(quoteid = qr, authoremailid = emailobj, newnode = newnode, oldnode = oldnode, comment=comment, completed = newcompleted, oldcompleted = oldcompleted)
        q.save()
        retval = q
    except Exception, e:
        print '\tThere was an error adding a Quotehistory entry: ', str(e)

    print '*** _addQuoteHistory: exit***'
    return retval

def _addQuoteRequest(emailaddress, firstname, lastname, officephone, tonode, country, details):
    #TODO: input value checking
    retval = None
    emailobj = _getEmailMapping(emailaddress)
    if emailobj is not None:
        qr = Quoterequest(emailaddressid = emailobj, tonode = tonode, details = details, firstname=firstname, lastname=lastname, officephone = officephone, country = country)
        qr.save()
        retval = qr   

    return retval

def save(request, *args):
    print '*** quote: save : enter ***'
    id = request.POST.get('id', '')
    id = int(id)
    comment = request.POST.get('comment', '')
    completed = request.POST.get('completed', '')
    #TODO: this only works because usernames are email addresses in this app.
    email = request.user.username    

    qr = Quoterequest.objects.get(id=id)
    toNode = request.POST.get('tonode', None)
    if toNode is None:
        #no new toNode supplied? Use the old one...
        toNode = qr.tonode
    print '\ttoNode is ', toNode
    #if the node has changed, email the administrator(s) for the new node
    
    try:
        if toNode != qr.tonode:
            targetusers = _findAdminOrNodeRepEmailTarget(groupname = toNode)
            #email the administrators for the node
            for targetuser in targetusers:
                targetemail = targetuser['uid'][0]
                from mail_functions import sendQuoteRequestToAdminEmail
                sendQuoteRequestToAdminEmail(request, id, email, '', targetemail) 
    except Exception, e:
        print 'Exception emailing change to quote request: ', str(e) 

    _updateQuoteRequestStatus(qr, toNode, completed=completed, unread=0);       

    #add the comment to the history
    retval = _addQuoteHistory(qr, email, toNode, qr.tonode, comment, completed, qr.completed)

    setRequestVars(request, success=True, authenticated=True, authorized=True, mainContentFunction = 'quote:list') 
    print '*** quote: save : exit ***'
    return jsonResponse(request, []) 
     



def formalLoad(request, *args, **kwargs):
    '''allow loading either by quote id, or formalquoteid'''
    print '***formalLoad : enter ***'#, args, kwargs
  
    #get qid from quargs, then request, then blank 
    qid = kwargs.get('qid', request.REQUEST.get('qid', '') )
    fqid = request.REQUEST.get('fqid', '')
    retvals = {}

    #retdata
    retdata = { 'quoterequestid' : qid,
                'toemail' : '',
                'fromemail' : '',
                'details' : '',
                'pdf' : '',
                'fromname' : '',
                'officePhone' : '',
                'tonode' : '',
              }

    if qid is not '' or fqid is not '':
        qid = qid.strip() 
        fqid = fqid.strip()
      
        try:
            #This part gets us the linked formal quote data 
            if fqid != '':
                retvals = Formalquote.objects.filter(id=fqid).values( 'id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail' )   
            elif qid != '':
                retvals = Formalquote.objects.filter(quoterequestid=qid).values( 'id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail' )

            if len(retvals) > 0:
                retvals = retvals[0]
                rows = len(retvals)

                #TODO need to load up a bunch of user details here.

                #get the details of the auth user in the toemail
                ld = LDAPHandler()
                d = ld.ldap_get_user_details(retvals['fromemail'])
                if len(d) > 0:
                    #TODO: isnt this dict meant to go through some sort of translation function so that I don't have to access 
                    #       raw LDAP fields here?
                    from madas.users.views import _translate_ldap_to_madas
                    d = _translate_ldap_to_madas(d)
                    print '\tRetrieved user details: ', d
                    retvals['fromname'] = d['firstname'][0] + ' ' + d['lastname'][0]
                    retvals['officePhone'] = d['telephoneNumber']
                    
                    qr = Quoterequest.objects.get(id=retvals['quoterequestid'])
                    
                    retvals['tonode'] = qr.tonode
                retvals['pdf'] = retvals['details']
                
                e = ld.ldap_get_user_details(retvals['toemail'])
                if len(e) > 0:
                    ### Authorisation Check ### we do this here because we need to allow auth if the request is for a formal quote sent to an unregistered user
                    from madas.m.views import authorize
                    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
                    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True)
                    if auth_result is not True:
                        return auth_response
                    ### End Authorisation Check ###  

            else:
                print '\tNo formal quotes.'
                retvals = retdata 
                rows = 0
        except Exception, e:
            print 'Exception (Retvals was %s): %s' % (str(retvals), str(e))
        #so now, we want some user details.
    else:
        print '\tNo qid or fqid passed'
        
    setRequestVars(request, success=True, data=retvals, totalRows=1, params=[], authenticated=True, authorized=True) 
    print '***formalLoad : exit ***'
    return jsonResponse(request, []) 
              
def addFormalQuote(fromemail, toemail, quoterequestid, details):
    '''adds a formal quote to the database'''
    print '*** addFormalQuote : enter ***'
    fromemail = fromemail.strip()
    tomemail = toemail.strip()
    retval = None
    if fromemail == '' or toemail == '':
        print '\tNo from email or to email specified when adding a formal quote. Aborting.'
    else:
        details = details.strip()

        try:
            #delete any formal quotes already attached to this quote
            qr = Quoterequest.objects.filter(id = quoterequestid)[0]
            print 'QR is ', qr
            try: 
                q = Formalquote.objects.get(quoterequestid = qr.id)
            except Exception, e:
                q = None
            
            if q is not None:
                q.delete()
        except Exception, e:
            print '\tError deleting old formalquote entry for quoteid: ', quoterequestid, ': ', str(e)
            qr = None

        if qr is not None:
            try:    
                newrecord = Formalquote(quoterequestid = qr, details = details, fromemail = fromemail, toemail=toemail)
                newrecord.save()
            except Exception, e:
                print '\tException adding new formalquotedata. : ', str(e)

            retval = newrecord.id
        else:
            retval = None
    print '*** addFormalQuote : exit ***'
    return retval

def formalSave(request, *args):
    '''Called when the user clicks the 'Send Formal Quote' button'''
    print '***formalSave : enter ***'
    ### Authorisation Check ###
    from madas.m.views import authorize
    from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
    (auth_result, auth_response) = authorize(request, module = 'quote', internal=True, perms=MADAS_ADMIN_GROUPS)
    if auth_result is not True:
        return auth_response
    ### End Authorisation Check ###
    qid = request.REQUEST.get('quoterequestid', 'wasnt there')
    email = request.user.username
    #print '\tQID: ', qid
    #print '\tREQUEST :', request.REQUEST.__dict__

    attachmentname = ''

    ######## GET INITIAL DETAILS ####################
    print '\tGetting quote details'
    try:
        #qr = Quoterequest.objects.get(id = qid)
        qr_obj = Quoterequest.objects.filter(id=qid)
        qr = qr_obj.values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        qr = qr[0]
        qr_obj = qr_obj[0]
        print 'QR is : ', qr
        for key in qr.keys():
            print '\t\t',key, qr[key]
    except Exception, e:
        print '\tException getting old details: ', str(e)

    ############# FILE UPLOAD ########################
    try:
        #TODO handle file uploads - check for error values
        print request.FILES.keys()
        if request.FILES.has_key('pdf'):
            f = request.FILES['pdf']
            print '\tuploaded file name: ', f._get_name()
            translated_name = 'formalquote_' + str(qr_obj.id) + '_' + f._get_name().replace(' ', '_')
            print '\ttranslated name: ', translated_name
            _handle_uploaded_file(f, translated_name)
            attachmentname = translated_name
        else:
            print '\tNo file attached.'
    except Exception, e:
        print '\tException: ', str(e)
    

    ################# ADD FORMAL QUOTE ################
    print '\tAdding formal quote'
    try:
        newfqid = addFormalQuote(email, qr['emailaddressid__emailaddress'], qid, attachmentname)
        print '\tAdding history'
        _addQuoteHistory(qr_obj, qr['emailaddressid__emailaddress'], qr['tonode'], qr['tonode'], 'Formal quote created/modified', qr['completed'], qr['completed'])
        print '\tFinished adding history'
    except Exception, e:
        print '\tException: ', str(e)
    
    from django.core.mail import send_mail
    toemail = qr['emailaddressid__emailaddress']
    fromemail = email
    from madas.mail_functions import sendFormalQuoteEmail
    #get the list of admins or nodereps which should be notified:
    #note this is completely unsafe if the sequense above caused an exception retrieving the quote details.
    tonode = qr['tonode']
    cc = _findAdminOrNodeRepEmailTarget(groupname = tonode)
    cc = [str(c['uid'][0]) for c in cc]
    if toemail in cc:
        cc.remove(toemail)
    print 'cc list is: %s' % str(cc)
    sendFormalQuoteEmail(request, qid, attachmentname, toemail, cclist = cc, fromemail=fromemail)
    #print '\tSetting request vars: '
    setRequestVars(request, data=None, totalRows=0, authenticated=True, authorized=True, success=True, mainContentFunction = 'quote:list') 
    #print '\tDone setting request vars'
    print '***formalSave : exit ***'
    return jsonResponse(request, []) 


def setFormalQuoteStatus(quoteobject, status):
    '''Sets the status of a formalquote, given the related quote object.
       returns the formalquote object on success, and None on failure.
    '''
    retval = None
    try:
        fq = Formalquote.objects.get(quoterequestid = quoteobject.id)
        #Here we do a quick check.
        #Don't set a quote's state to 'downloaded' unless its previous 
        #state was new.
        if status == QUOTE_STATE_DOWNLOADED and fq.status == QUOTE_STATE_NEW:
            return retval

        fq.status = status
        fq.save()
        retval = fq
    except Exception, e:
        print '\tError updating formalquote status: ', str(e)

    return retval




def formalAccept(request, *args):
    print '*** formalAccept: enter ***'
    #load original details
    qid = request.REQUEST.get('id', None)
    failed = False
    try:
        qr = Quoterequest.objects.filter(id = qid)[0]
        qrvalues = _loadQuoteRequest(qid)
    except Exception, e:
        print '\tException: Error getting initial quote: ', e
        failed = True

    if not failed:
        #try:
        #here we want to store the user details
        #TODO: this section needs some help - can edit arbitrary user details via this form...
        u = request.REQUEST.get('email')
        
        from madas.m.views import authorize
        from settings import MADAS_STATUS_GROUPS, MADAS_ADMIN_GROUPS
        (auth_result, auth_response) = authorize(request, module = 'quote', internal=True, perms=MADAS_ADMIN_GROUPS)
        if auth_result is not True:  #allow node reps to accept quotes but not edit the user details
            from madas.users.views import _usersave
            _usersave(request, u)

        #and then...
        #mark the formal quote as accepted:
        fq = setFormalQuoteStatus(qr, QUOTE_STATE_ACCEPTED)
        

        #leave acceptance in the quote history
        _addQuoteHistory(qr, qrvalues['email'], qr.tonode, qr.tonode, 'Formal quote accepted', qr.completed, qr.completed)

    #email the node rep
        targetusers = _findAdminOrNodeRepEmailTarget(groupname = qr.tonode)
        from django.core.mail import send_mail
        from madas.mail_functions import sendFormalStatusEmail
        for targetuser in targetusers:
            toemail = targetuser['uid'][0]
            sendFormalStatusEmail(request, qid, 'accepted', toemail, fromemail = qrvalues['email'])
        #except Exception, e:
        #    print '\tException: ', str(e)
        #    failed = True


    setRequestVars(request, success=not failed, data = None, totalRows = 0, authenticated = True, authorized = True, mainContentFunction='dashboard')
    print '*** formalAccept: exit ***'
    return jsonResponse(request, [])



def formalReject(request, *args):
    print '*** formalReject : enter ***'
    qid = request.REQUEST.get('qid', None)
    try:
        qrq = Quoterequest.objects.filter(id = qid)
        qr = qrq[0]
        qrvalues = qrq.values('id', 'emailaddressid__emailaddress', 'tonode', 'details', 'requesttime', 'unread', 'completed', 'firstname', 'lastname', 'officephone', 'country', 'attachment' )[0]
    except Exception, e:
        print '\tError getting initial quote: ', e
        qr = None

    if qr is not None:
        try:
            fq = setFormalQuoteStatus(qr, QUOTE_STATE_REJECTED) 
            #leave rejection in the quote history
            _addQuoteHistory(qr, qrvalues['emailaddressid__emailaddress'], qr.tonode, qr.tonode, 'Formal quote rejected', qr.completed, qr.completed)
            #email the node rep
            targetusers = _findAdminOrNodeRepEmailTarget(groupname = qr.tonode)
            from django.core.mail import send_mail
            from madas.mail_functions import sendFormalStatusEmail
            for targetuser in targetusers:
                toemail = targetuser['uid'][0]
                sendFormalStatusEmail(request, qid, 'rejected', toemail, fromemail = qrvalues['emailaddressid__emailaddress'])
        except Exception, e:
            print 'DEBUG Exception: ', str(e)
    #TODO: base success on email success? qr != None?
    setRequestVars(request, success=True, data = None, totalRows = 0, authenticated = True, authorized = True, mainContentFunction='dashboard')
    print '***formalReject : exit ***'
    return jsonResponse(request, []) 



def viewFormal(request, *args):
    '''this would be viewing the quote from an email link. Currently this url /quote/viewformal is passed to loadquote().'''
    pass


def downloadPDF(request, *args):
    print '*** downloadPDF: Enter ***'
    quoterequestid = request.REQUEST.get('quoterequestid', None)
    qrobj = Quoterequest.objects.filter(id = quoterequestid)
    qr = qrobj.values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
    qrobj = qrobj[0]
    qr = qr[0]

    fqrob = Formalquote.objects.filter(quoterequestid = quoterequestid)
    fqr = fqrob.values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status', 'downloaded')
    fqrob = fqrob[0]
    fqr = fqr[0]
    import os
    import madas
    filename = os.path.join(madas.settings.QUOTE_FILES_ROOT, fqr['details'])
    print '\tThe filename is: ', filename
     
   
    try:
        from django.core.servers.basehttp import FileWrapper
        from django.http import HttpResponse
        wrapper = FileWrapper(file(filename))
        content_disposition = 'attachment;  filename=\"%s\"' % (fqr['details'])
        response = HttpResponse(wrapper, content_type='application/pdf')
        response['Content-Disposition'] = content_disposition
        response['Content-Length'] = os.path.getsize(filename)
        
        if fqr['fromemail'] != request.user.username:
            setFormalQuoteStatus(qrobj, QUOTE_STATE_DOWNLOADED)
        
        _addQuoteHistory(qrobj, qr['emailaddressid__emailaddress'], qrobj.tonode, qrobj.tonode, 'Formal quote downloaded', qrobj.completed, qrobj.completed)    

    except Exception, e:
        response = HttpResponse('Error: The Quote file could not be retrieved')
        print '\tException: ', str(e)
    
    print '*** downloadPDF: Exit ***'
    return response 


def downloadAttachment(request, *args):
    quoterequestid = request.REQUEST.get('quoterequestid', None)
    qr = Quoterequest.objects.get(id = quoterequestid)

    print 'downloadAttachment:', str(qr)
    
    import os
    import madas
    filename = os.path.join(madas.settings.QUOTE_FILES_ROOT, qr.attachment)
    from django.core.servers.basehttp import FileWrapper
    from django.http import HttpResponse

    wrapper = FileWrapper(file(filename))
    content_disposition = 'attachment;  filename=\"%s\"' % (str(qr.attachment))
    response = HttpResponse(wrapper, content_type='application/download')
    response['Content-Disposition'] = content_disposition
    response['Content-Length'] = os.path.getsize(filename)
    return response 

