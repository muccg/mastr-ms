# Create your views here.
import os, grp, stat
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ccg.utils.webhelpers import siteurl, wsgibase
from django.core.servers.basehttp import FileWrapper
from django.utils import simplejson
from django.core.mail import send_mail
import logging

from mastrms.decorators import *
from mastrms.app.utils.data_utils import jsonResponse, jsonErrorResponse, json_encode, uniqueList
from mastrms.app.utils.file_utils import ensure_repo_filestore_dir_with_owner, set_repo_file_ownerships
from mastrms.quote.models import Quoterequest, Formalquote, Quotehistory, Emailmap
from mastrms.users.MAUser import *
from mastrms.login.URLState import getCurrentURLState
#from string import *
from mastrms.app.utils.mail_functions import sendQuoteRequestConfirmationEmail, sendQuoteRequestToAdminEmail, sendFormalQuoteEmail, sendFormalStatusEmail

logger = logging.getLogger('madas_log')

QUOTE_STATE_DOWNLOADED = 'downloaded'
QUOTE_STATE_NEW = 'new' #is the default on the DB column
QUOTE_STATE_ACCEPTED = 'accepted'
QUOTE_STATE_REJECTED = 'rejected'

def _handle_uploaded_file(f, name):
    '''Handles a file upload to the projects QUOTE_FILES_ROOT
       Expects a django InMemoryUpload object, and a filename'''
    logger.debug('*** _handle_uploaded_file: enter ***')
    retval = False
    try:
        ensure_repo_filestore_dir_with_owner(settings.QUOTE_FILES_ROOT)
        destfname = os.path.join(settings.QUOTE_FILES_ROOT, name ) 
        destination = open(destfname, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        
        set_repo_file_ownerships(destfname)
        retval = True
    except Exception, e:
        retval = False
        logger.debug('\tException in file upload: %s' % (str(e)) )
    logger.debug('*** _handle_uploaded_file: exit ***')
    return retval

def _findAdminOrNodeRepEmailTarget(groupname = 'Administrators'): #TODO use MADAS_ADMIN_GROUP constant
    logger.debug('*** _findAdminOrNodeRepEmailTarget : enter ***')
    #find an admin, or a node rep for the group passed in.
    #if no group was passed, we assume 'Administrators'
    grouplist = []
    grouplist.append(groupname)
    if groupname is not MADAS_ADMIN_GROUP:
        grouplist.append(MADAS_NODEREP_GROUP)
    
    users = getMadasUsersFromGroups(grouplist) 
    
    logger.debug('\t Users found: %s' % (users))
   
    #NOTE: If this function finds multiple users to email, it only returns the
    #      first one. If we ever need to change this, here is the place to do it!
    retval = users
    logger.debug( '*** _findAdminOrNodeRepEmailTarget : exit ***' )
    return retval 

def sendRequest(request, *args):
    logger.debug('***quote: sendRequest***')
    email = request.REQUEST.get('email', None)
    firstname = request.REQUEST.get('firstname', None)
    lastname = request.REQUEST.get('lastname', None)
    officePhone = request.REQUEST.get('telephoneNumber', None)
    toNode = request.REQUEST.get('node', None)
    details = request.REQUEST.get('details', None)
    country = request.REQUEST.get('country', None)
    fileName = request.REQUEST.get('fileName', None)

    try:
        #add the new quote to the DB
        qr = _addQuoteRequest(email, firstname, lastname, officePhone, toNode, country, details)
    except Exception, e:
        logger.exception('Exception adding quote request.')
        raise Exception('Exception adding quote request.')
  
    try:
        if request.FILES.has_key('attachfile'):
            f = request.FILES['attachfile']
            translated_name = 'quote_attachment_' + str(qr.id) + '_' + f._get_name().replace(' ', '_')
            _handle_uploaded_file(f, translated_name)
            qr.attachment = translated_name
        qr.save()

    except Exception, e:
        logger.exception('Exception saving attached file.')
        raise Exception('Exception saving attached file.')

    try: 
        sendQuoteRequestConfirmationEmail(request, qr.id, email) 
        #email the administrator(s) for the node 
        logger.debug('Argument to _findAdminOrNodeRepEmailTarget is: %s' % (str(toNode)) )
        if toNode == '': #if the node was 'Dont Know'
            searchgroups = MADAS_ADMIN_GROUP
        else:
            searchgroups = toNode
        targetUsers = _findAdminOrNodeRepEmailTarget(groupname = searchgroups)
        for targetUser in targetUsers:
            sendQuoteRequestToAdminEmail(request, qr.id, firstname, lastname, targetUser['uid'][0]) #toemail should be a string, but ldap returns are all lists
    except Exception, e:
        logger.exception('Error sending mail in SendRequest: %s' % ( str(e) ) )

    logger.debug( '*** quote:sendRequest: exit ***' )
    return jsonResponse( mainContentFunction='quote:request')       

@admins_or_nodereps
def listQuotesRequiringAttention(request):
    '''Used by dashboard to list the quotes that aren't Completed and don't have
       a formal quote yet.'''

    qs = Quoterequest.objects.filter(completed=False,formalquote__id=None)
    
    #If they are a noderep (only), we filter the qs by node
    currentuser = getCurrentUser(request)
    if currentuser.IsNodeRep and not currentuser.IsAdmin:
        nodelist = getMadasNodeMemberships(currentuser.CachedGroups)
        node = nodelist[0]
        qs.filter(tonode=node) 

    results = []
    qs.values('id', 'unread', 'firstname', 'lastname', 'requesttime', 'tonode', 'emailaddressid__emailaddress' )
    for ql in quoteslist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            results.append(ql)

    results = []

    return jsonResponse( items=resultsset)


def listQuotes(request, *args):
    '''This corresponds to Madas Dashboard->Quotes->View Quote Requests
       Accessible by Administrators, Node Reps and Clients but it filters down to just Client's quote requests if it is a Client
    '''
    g = getCurrentUser(request).CachedGroups
    nodelist = getMadasNodeMemberships(g)

    results = [] 
    quoteslist = []
    if MADAS_NODEREP_GROUP in g:
        #retrieve quotes for the first node in the list (there shouldnt be more than 1)
        quoteslist = Quoterequest.objects.filter(Q(tonode=nodelist[0]) | Q()).values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'country', 'requesttime', 'emailaddressid__emailaddress' )
    else: #they are just a client. Show only their own quotes
        quoteslist = Quoterequest.objects.filter(emailaddressid__emailaddress=request.user.username).values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'country', 'requesttime', 'emailaddressid__emailaddress' )
    
    quoteslist = list(quoteslist) #convert to normal list

    #If they are an admin, ALSO show quotes which don't yet have a node
    if MADAS_ADMIN_GROUP in g:
        homelessquotes = Quoterequest.objects.filter(tonode='').values('id', 'completed', 'unread', 'tonode', 'firstname', 'country', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        quoteslist += list(homelessquotes)
    
    #transform the email field to be named correctly.
    for ql in quoteslist:
        ql['email'] = ql['emailaddressid__emailaddress']
        del ql['emailaddressid__emailaddress']
        results.append(ql)

    #make the list unique. We can't use a set because the list contains unhashable types
    resultsset = uniqueList(results)
    

    return jsonResponse( items=resultsset)       

@admins_or_nodereps
def listAll(request, *args):
    '''This corresponds to Madas Dashboard->Quotes->Overview List
       Accessible by Administrators, Node Reps
    '''
    logger.debug( '*** quote/listAll - enter ***' )
    g = getCurrentUser(request).CachedGroups

    nodelist = getMadasNodeMemberships(g)
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
        logger.exception('Exception getting quotes.')
        raise Exception('Exception getting quotes.')

    if MADAS_ADMIN_GROUP in g:
        adminlist = Quoterequest.objects.filter(tonode='Administrators').values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        for ql in adminlist:
            ql['email'] = ql['emailaddressid__emailaddress']
            del ql['emailaddressid__emailaddress']
            
            #find the time when this quote was marked as completed (if it is)
            if ql['completed'] == True:
                qh = Quotehistory.objects.filter(oldcompleted = False, completed = True)
                qh = qh[0]
                ql['changetimestamp'] = qh.changetimestamp
            
            results.append(ql)

    try:
        resultsset = uniqueList(results) #these may not be unique. need to uniquify them.
    except Exception, e:
        logger.exception('Exception making results set unique')
        raise Exception('Exception making results set unique')
    logger.debug('\tfinished generating quoteslist')

    logger.debug('*** quote/listAll - exit ***')
    return jsonResponse( items=resultsset) 


def listFormal(request, *args, **kwargs):
    '''This corresponds to Madas Dashboard->Quotes->My Formal Quotes
       Accessible by Everyone
    '''
    logger.debug('*** listFormal : enter ***')
    uname = request.user.username
    currentUser = getCurrentUser(request)
    nodelist = getMadasNodeMemberships(currentUser.CachedGroups)

    #if a noderep or admin, and you have a node:
    if (currentUser.IsAdmin or currentUser.IsNodeRep) and len(nodelist) > 0:
        fquoteslist = Formalquote.objects.filter(Q(fromemail__iexact=uname)|Q(toemail__iexact=uname)|Q(quoterequestid__tonode=nodelist[0])).values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status')        
    #otherwise show all quotes to me, from me, or from this node.
    else:
        fquoteslist = Formalquote.objects.filter(Q(fromemail__iexact=uname)|Q(toemail__iexact=uname)).values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status') 
    
    qid = kwargs.get('qid', request.REQUEST.get('qid', '') )
    if qid != '':
        logger.debug('filtering fquotes where qid is %s' % (qid) )
        fquoteslist = fquoteslist.filter(quoterequestid=qid)

    logger.debug('*** listFormal : exit ***')
    return jsonResponse( items=list(fquoteslist)) 


def _loadQuoteRequest(qid):
    logger.debug('\t_loadQuoteRequest: qid was %s' % (qid) )
    if qid is not None and qid.isdigit() and qid is not '':
        qr = Quoterequest.objects.filter(id = qid).values('id', 'emailaddressid__emailaddress', 'tonode', 'details', 'requesttime', 'unread', 'completed', 'firstname', 'lastname', 'officephone', 'country', 'attachment')
        try:
            for ql in qr:
                ql['email'] = ql['emailaddressid__emailaddress']
                del ql['emailaddressid__emailaddress']
        except Exception, e:
            logger.warning('exception: %s' % (str(e)))

    else:
        qr = [{}]

    #TODO: REFACTOR If there was more than one quote request, something went wrong, and we should error
    qr = qr[0]    
    
    return qr
    
@authentication_required
def load(request, *args):
    '''load quote details'''
    logger.debug('*** load : enter ***')
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

    logger.debug('*** load : exit ***')
    if not suc:
        return jsonErrorResponse("Couldn't load quote " + qid)
    return jsonResponse(data=qr)
    
def history(request, *args):
    logger.debug('***quote/history : enter***')
    qid = request.REQUEST.get('qid', None)
    logger.debug('\tHistory: qid was %s' % (str(qid)))
    if qid is not None:
        qh = Quotehistory.objects.filter(quoteid = qid).values()
    else:
        qh = []
 
    qh = list(qh)
    #ensure we have a sorted list by date. Most likely this wont change the list order
    #anyway, because they were probably retrieved in order.
    qh.sort(lambda x,y: cmp(x['changetimestamp'],y['changetimestamp']))
    qh.reverse()
    logger.debug('***quote/history : exit***')
    return jsonResponse( data = qh )


def _getEmailMapping(email):
    logger.debug( '*** _getEmailMapping: enter***' )
    retval = None
    try:
        emmap = Emailmap.objects.get(emailaddress = email)
        retval = emmap
    except Emailmap.DoesNotExist, e:
        #we need to create a new entry.
        logger.debug( '\tCreating new email mapping' )
        newEmail = Emailmap(emailaddress = email)
        newEmail.save()
        retval = newEmail
    logger.debug('*** _getEmailMapping: exit ***')
    return retval

def _updateQuoteRequestStatus(qr, tonode, completed=0, unread=0):
    qr.completed = completed
    qr.unread = unread
    qr.tonode = tonode
    qr.save()

def _addQuoteHistory(qr, emailaddress, newnode, oldnode, comment, newcompleted, oldcompleted):
    logger.debug('*** _addQuoteHistory: enter ***')
    #get the email mapping for this email address
    emailobj = _getEmailMapping(emailaddress)
    #store the history details
    retval = None
    try:
        q = Quotehistory(quoteid = qr, authoremailid = emailobj, newnode = newnode, oldnode = oldnode, comment=comment, completed = newcompleted, oldcompleted = oldcompleted)
        q.save()
        retval = q
    except Exception, e:
        logger.exception('There was an error adding a Quotehistory entry')
        raise Exception('There was an error adding a Quotehistory entry')

    logger.debug('*** _addQuoteHistory: exit***')
    return retval

def _addQuoteRequest(emailaddress, firstname, lastname, officephone, tonode, country, details):
    retval = None
    emailobj = _getEmailMapping(emailaddress)
    if emailobj is not None:
        qr = Quoterequest(emailaddressid = emailobj, tonode = tonode, details = details, firstname=firstname, lastname=lastname, officephone = officephone, country = country)
        qr.save()
        retval = qr   

    return retval

def save(request, *args):
    logger.debug('*** quote: save : enter ***')
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
    logger.debug('\ttoNode is %s' % (str(toNode)) )
    #if the node has changed, email the administrator(s) for the new node
    try:
        if toNode != qr.tonode:
            targetusers = _findAdminOrNodeRepEmailTarget(groupname = toNode)
            #email the administrators for the node
            for targetuser in targetusers:
                targetemail = targetuser['uid'][0]
                sendQuoteRequestToAdminEmail(request, id, email, '', targetemail) 
    except Exception, e:
        logger.exception('Exception emailing change to quote request') 

    _updateQuoteRequestStatus(qr, toNode, completed=completed, unread=0);       

    #add the comment to the history
    _addQuoteHistory(qr, email, toNode, qr.tonode, comment, completed, qr.completed)

    logger.debug('*** quote: save : exit ***')
    return jsonResponse( mainContentFunction='quote:list') 
     
def formalLoad(request, *args, **kwargs):
    '''allow loading either by quote id, or formalquoteid'''
    logger.debug('***formalLoad : enter ***')
  
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
                'purchase_order_number' : ''
              }

    if qid is not '' or fqid is not '':
        qid = qid.strip() 
        fqid = fqid.strip()
      
        try:
            #This part gets us the linked formal quote data 
            if fqid != '':
                retvals = Formalquote.objects.filter(id=fqid).values( 'id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'purchase_order_number' )   
            elif qid != '':
                retvals = Formalquote.objects.filter(quoterequestid=qid).values( 'id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'purchase_order_number' )

            if len(retvals) > 0:
                retvals = retvals[0]
                rows = len(retvals)

                #get the details of the auth user in the toemail
                d = getMadasUserDetails(retvals['fromemail'])
                if len(d) > 0:
                    d = _translate_ldap_to_madas(d)
                    retvals['fromname'] = d['firstname'][0] + ' ' + d['lastname'][0]
                    retvals['officePhone'] = d['telephoneNumber']
                    
                    qr = Quoterequest.objects.get(id=retvals['quoterequestid'])
                    
                    retvals['tonode'] = qr.tonode
                retvals['pdf'] = retvals['details']
                
            else:
                logger.debug('\tNo formal quotes.')
                retvals = retdata 
                rows = 0
        except Exception, e:
            logger.exception('Exception loading quote') 
            raise Exception('Exception loading quote')
    else:
        logger.warning('\tNo qid or fqid passed')
        
    logger.warning('***formalLoad : exit ***')
    return jsonResponse(data=retvals) 
   
   
def viewFormalRedirect(request, *args):
    urlstate = getCurrentURLState(request)
    urlstate.redirectMainContentFunction = 'quote:viewformal'
    urlstate.params = ['quote:viewformal', {'qid':int(request.REQUEST.get('quoterequestid', 0))}]
    return HttpResponseRedirect(siteurl(request)) 

def addFormalQuote(fromemail, toemail, quoterequestid, details):
    '''adds a formal quote to the database'''
    logger.debug('*** addFormalQuote : enter ***')
    fromemail = fromemail.strip()
    tomemail = toemail.strip()
    retval = None
    if fromemail == '' or toemail == '':
        logger.warning('\tNo from email or to email specified when adding a formal quote. Aborting.')
    else:
        details = details.strip()

        try:
            #delete any formal quotes already attached to this quote
            qr = Quoterequest.objects.filter(id = quoterequestid)[0]
            try: 
                q = Formalquote.objects.get(quoterequestid = qr.id)
            except Exception, e:
                q = None
            
            if q is not None:
                q.delete()
        except Exception, e:
            logger.warning('\tError deleting old formalquote entry for quoteid %s : %s ' % ( str(quoterequestid), str(e)) )
            qr = None

        if qr is not None:
            try:    
                newrecord = Formalquote(quoterequestid = qr, details = details, fromemail = fromemail, toemail=toemail)
                newrecord.save()
            except Exception, e:
                logger.warning('\tException adding new formalquotedata. : %s' % (str(e)))

            retval = newrecord.id
        else:
            retval = None
    logger.debug('*** addFormalQuote : exit ***')
    return retval

def formalSave(request, *args):
    '''Called when the user clicks the 'Send Formal Quote' button'''
    logger.debug('***formalSave : enter ***')
    qid = request.REQUEST.get('quoterequestid', 'wasnt there')
    email = request.user.username
    attachmentname = ''

    # Get initial details
    logger.debug('\tGetting quote details')
    try:
        #qr = Quoterequest.objects.get(id = qid)
        qr_obj = Quoterequest.objects.filter(id=qid)
        qr = qr_obj.values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
        qr = qr[0]
        qr_obj = qr_obj[0]
        for key in qr.keys():
            logger.debug('\t\t',key, qr[key])
    except Exception, e:
        logger.exception('Exception getting old details')
        raise Exception('Exception getting old details')

    # File upload
    try:
        #TODO: REFACTOR : there is other code just like this...'
        if request.FILES.has_key('pdf'):
            f = request.FILES['pdf']
            logger.debug('\tuploaded file name: %s' % (f._get_name()) )
            translated_name = 'formalquote_' + str(qr_obj.id) + '_' + f._get_name().replace(' ', '_')
            logger.debug('\ttranslated name: %s' % (translated_name))
            _handle_uploaded_file(f, translated_name)
            attachmentname = translated_name
        else:
            logger.debug('\tNo file attached.')
    except Exception, e:
       logger.exception('Exception handling uploaded file')
       raise Exception('Exception handling uploaded file')
    

    ################# ADD FORMAL QUOTE ################
    logger.debug('\tAdding formal quote')
    try:
        newfqid = addFormalQuote(email, qr['emailaddressid__emailaddress'], qid, attachmentname)
        logger.debug('\tAdding history')
        _addQuoteHistory(qr_obj, qr['emailaddressid__emailaddress'], qr['tonode'], qr['tonode'], 'Formal quote created/modified', qr['completed'], qr['completed'])
        logger.debug('\tFinished adding history')
    except Exception, e:
        logger.exception('Exception adding formal quote')
        raise Exception('Exception adding formal quote')
    
    toemail = qr['emailaddressid__emailaddress']
    fromemail = email
    #get the list of admins or nodereps which should be notified:
    #note this is completely unsafe if the sequense above caused an exception retrieving the quote details.
    tonode = qr['tonode']
    cc = _findAdminOrNodeRepEmailTarget(groupname = tonode)
    cc = [str(c['uid'][0]) for c in cc]
    if toemail in cc:
        cc.remove(toemail)
    logger.debug('cc list is: %s' % str(cc))
    sendFormalQuoteEmail(request, qid, attachmentname, toemail, cclist = cc, fromemail=fromemail)
    logger.debug('***formalSave : exit ***')
    return jsonResponse( mainContentFunction='quote:list') 


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
        logger.warning('\tError updating formalquote status: %s' % (str(e)) )

    return retval




def formalAccept(request, *args):
    logger.debug( '*** formalAccept: enter ***' )
    #load original details
    qid = request.REQUEST.get('id', None)
    failed = False
    try:
        qr = Quoterequest.objects.filter(id = qid)[0]
        qrvalues = _loadQuoteRequest(qid)
    except Exception, e:
        logger.exception('Error getting initial quote')
        raise Exception('Error getting initial quote ' + qid)

    #try:
    #here we want to store the user details
    #TODO: this section needs some help - can edit arbitrary user details via this form...
    u = request.REQUEST.get('email')
        
    #mark the formal quote as accepted:
    fq = setFormalQuoteStatus(qr, QUOTE_STATE_ACCEPTED)
        
    #add optional purchase_order_number to the qr
    po = request.REQUEST.get('purchase_order_number')
    fq.purchase_order_number = po
    fq.save()

    #leave acceptance in the quote history
    _addQuoteHistory(qr, qrvalues['email'], qr.tonode, qr.tonode, 'Formal quote accepted', qr.completed, qr.completed)

    #email the node rep
    targetusers = _findAdminOrNodeRepEmailTarget(groupname = qr.tonode)
    for targetuser in targetusers:
        toemail = targetuser['uid'][0]
        sendFormalStatusEmail(request, qid, 'accepted', toemail, fromemail = qrvalues['email'])

    logger.debug('*** formalAccept: exit ***')
    return jsonResponse(mainContentFunction='dashboard')

def formalReject(request, *args):
    logger.debug('*** formalReject : enter ***')
    qid = request.REQUEST.get('qid', None)
    try:
        qrq = Quoterequest.objects.filter(id = qid)
        qr = qrq[0]
        qrvalues = qrq.values('id', 'emailaddressid__emailaddress', 'tonode', 'details', 'requesttime', 'unread', 'completed', 'firstname', 'lastname', 'officephone', 'country', 'attachment' )[0]
    except Exception, e:
        logger.exception('Error getting initial quote')
        raise Exception('Error getting initial quote ' + qid)

    try:
        fq = setFormalQuoteStatus(qr, QUOTE_STATE_REJECTED) 
        #leave rejection in the quote history
        _addQuoteHistory(qr, qrvalues['emailaddressid__emailaddress'], qr.tonode, qr.tonode, 'Formal quote rejected', qr.completed, qr.completed)
        #email the node rep
        targetusers = _findAdminOrNodeRepEmailTarget(groupname = qr.tonode)
        for targetuser in targetusers:
            toemail = targetuser['uid'][0]
            sendFormalStatusEmail(request, qid, 'rejected', toemail, fromemail = qrvalues['emailaddressid__emailaddress'])
    except Exception, e:
        logger.exception('Exception in rejecting formal quote')
        raise Exception('Exception in rejecting formal quote')
    logger.debug('***formalReject : exit ***')
    return jsonResponse( mainContentFunction='dashboard') 

def downloadPDF(request, *args):
    logger.debug('*** downloadPDF: Enter ***')
    quoterequestid = request.REQUEST.get('quoterequestid', None)
    qrobj = Quoterequest.objects.filter(id = quoterequestid)
    qr = qrobj.values('id', 'completed', 'unread', 'tonode', 'firstname', 'lastname', 'officephone', 'details', 'requesttime', 'emailaddressid__emailaddress' )
    qrobj = qrobj[0]
    qr = qr[0]

    fqrob = Formalquote.objects.filter(quoterequestid = quoterequestid)
    fqr = fqrob.values('id', 'quoterequestid', 'details', 'created', 'fromemail', 'toemail', 'status', 'downloaded')
    fqrob = fqrob[0]
    fqr = fqr[0]
    filename = os.path.join(settings.QUOTE_FILES_ROOT, fqr['details'])
    logger.debug('\tThe filename is: %s' % ( filename ) )
     
   
    try:
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
        logger.warning('\tException: %s' % (str(e)) )
    
    logger.debug('*** downloadPDF: Exit ***')
    return response 


def downloadAttachment(request, *args):
    quoterequestid = request.REQUEST.get('quoterequestid', None)
    qr = Quoterequest.objects.get(id = quoterequestid)

    logger.debug('downloadAttachment: %s' % (str(qr)) )
    
    filename = os.path.join(settings.QUOTE_FILES_ROOT, qr.attachment)
    wrapper = FileWrapper(file(filename))
    content_disposition = 'attachment;  filename=\"%s\"' % (str(qr.attachment))
    response = HttpResponse(wrapper, content_type='application/download')
    response['Content-Disposition'] = content_disposition
    response['Content-Length'] = os.path.getsize(filename)
    return response 

