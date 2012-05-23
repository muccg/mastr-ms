# Create your views here.
import md5, time

from django.http import HttpResponse, HttpResponseRedirect
import logging
from django.contrib.auth import authenticate, login, logout
from mastrms.users.user_manager import get_user_manager
from django.shortcuts import render_to_response
from django.utils import simplejson
from ccg.utils import webhelpers
from ccg.utils.webhelpers import siteurl, wsgibase
from mastrms import settings #for LDAP details only, can remove when LDAP is removed
from mastrms.settings import MADAS_SESSION_TIMEOUT
from mastrms.utils.data_utils import jsonResponse, jsonErrorResponse
from mastrms.users.MAUser import *
from mastrms.login.URLState import getCurrentURLState
from mastrms.utils.mail_functions import sendForgotPasswordEmail, sendPasswordChangedEmail

logger = logging.getLogger('madas_log')

def processLoginView(request, *args):
    success = processLogin(request, args)
    return HttpResponseRedirect(siteurl(request)) 


def processLogin(request, *args):
    logger.debug('***processLogin : enter ***' )

    success = False

    if request.method == "POST":
        post = request.POST.copy()
   
        try:
            username = post['username']
            password = post['password']
        except Exception,e:
            username = ''
            password = ''
        print 'username is:', username
        user = None
        try: 
            user = authenticate(username = username, password = password)
            
        except Exception, e:
            logger.warning("Error authenticating user: %s" % ( str(e) ) )

        authenticated = 0
        authorized = 0
        if user is not None:
            if user.is_active:
                try:
                    a = login(request, user)
                except Exception, e:
                    logger.warning("Login error: %s" % ( str(e) ) )
                print 'successful login'
                success = True
                authenticated = True
                authorized = True
                #set the session to expire after
                request.session.set_expiry(MADAS_SESSION_TIMEOUT)
            else:
                #Inactive user
                print 'inactive login'
                success = False
                authenticated = False 
                authorized = False
        else:
            #invalid user
            print 'invalid login'
            success = False
            authenticated = False
            authorized = False

        nextview = 'login:success' #the view that a non admin would see next
        
        should_see_admin = False
        request.user.is_superuser = False

        madasuser = getCurrentUser(request, force_refresh=True) 
       
        if madasuser.IsAdmin:
            should_see_admin = True
            nextview = 'admin:adminrequests'
            request.user.is_superuser = True
        else:
            request.user.is_superuser = False

        #if they are authenticated (i.e. they have an entry in django's user table, and used the right password...)
        if authenticated:
            request.user.save() #save the status of is_admin 
        
        u = request.user
        
        params = []
        mainContentFunction = nextview
        params = params


    logger.debug( '*** processLogin : exit ***')
    return success 

def processLogout(request, *args):
    logger.debug( '*** processLogout : enter***')
    logout(request) #let Django log the user out
    logger.debug('*** processLogout : exit***')
    return HttpResponseRedirect(siteurl(request)) 

def processForgotPassword(request, *args):
    '''
    handles the submission of the 'forgot password' form
    regardless of success it should return success, to obfsucate user existence
    sets a validaton key in the user's ldap entry which is used to validate the user when they click the link in email
    '''
    emailaddress = request.REQUEST['username'].strip()
    user_manager = get_user_manager()
    u = user_manager.get_user_details(emailaddress)
    m = md5.new()
    m.update('madas' + str(time.time()) + 'resetPasswordToken123')
    vk = m.hexdigest()
    u['passwordResetKey'] = vk
    #remove groups info
    try:
        del u['groups']
    except:
        pass

    logger.debug( '\tUpdating user record with verification key')
    user_manager.update_user(emailaddress, None, None, u) 
    logger.debug('\tDone updating user with verification key')

    #Email the user
    sendForgotPasswordEmail(request, emailaddress, vk)

    m = simplejson.JSONEncoder()
    p = {}
    p['message'] = "An email has been sent to %s. Please follow the instructions in that email to continue" % (emailaddress)

    return jsonResponse(params=p, mainContentFunction='message') 

def forgotPasswordRedirect(request, *args):
    u = request.user
    try:
        urlstate = getCurrentURLState(request)
        urlstate.redirectMainContentFunction = 'login:resetpassword'
        urlstate.resetPasswordEmail = request.REQUEST['em']
        urlstate.resetPasswordValidationKey = request.REQUEST['vk']
        return HttpResponseRedirect(siteurl(request))
    except Exception, e:
        logger.warning('Exception in forgot password redirect: %s' % (str(e)))

def populateResetPasswordForm(request, *args):
    u = request.user
    data = {}
    urlstate = getCurrentURLState(request, andClear=True)
    data['email'] = urlstate.resetPasswordEmail
    data['validationKey'] = urlstate.resetPasswordValidationKey
    return jsonResponse(items=[data]) 

def processResetPassword(request, *args):
    
    username = request.REQUEST.get('email', '')
    vk = request.REQUEST.get('validationKey', '')
    passw = request.REQUEST.get('password', '')
    success = True
    if username is not '' and vk is not '' and passw is not '':

        #get existing details
        user_manager = get_user_manager()
        userdetails = user_manager.get_user_details(request.REQUEST['email'])
        if userdetails.has_key('groups'):
            del userdetails['groups'] #remove 'groups' - they don't belong in an update.
        if userdetails.has_key('passwordResetKey') and len(userdetails['passwordResetKey']) == 1 and userdetails['passwordResetKey'][0] == vk:
            #clear out the pager vk
            del userdetails['passwordResetKey']
            #update the password
            user_manager.update_user(username, username, passw, userdetails)
            sendPasswordChangedEmail(request, username)
                
        else:
            logger.warning('\tEither no vk stored in ldap, or key mismatch. uservk was %s, storedvk was %s' % (vk, userdetails.get('pager', None)) )

    else:
        logger.warning('Process reset password: argument error (all blank)')
        success = False
        request.session.flush() #if we don't flush here, we are leaving the redirect function the same.
    if not success:
        raise Exception("Couldn't reset password")
    return jsonResponse(mainContentFunction='login') 

#TODO not sure this function is even needed
def unauthenticated(request, *args):
    return jsonResponse() 

#TODO not sure this function is even needed
def unauthorized(request, *args):
    authorized = False
    mainContentFunction = 'notauthorized'
    #TODO now go to 'pager' with action 'index'
    return jsonResponse(mainContentFunction=mainContentFunction) 

### TODO: not sure this function is even needed
def index(request, *args):
    return jsonResponse() 

def serveIndex(request, *args, **kwargs):
    force = request.GET.get('dev_force', False) #param that can be passed to force access to ccg instance, for debugging purposes
    if not force and siteurl(request).find('ccg.murdoch.edu.au') > -1:
        #display the banner
        return render_to_response('banner.mako',{ 
                'APP_SECURE_URL': siteurl(request), 
                'username': request.user.username,
                'newurl':'https://mastrms.bio21.unimelb.edu.au/mastrms/',
                'wh': webhelpers,
                })
    
    
    currentuser = getCurrentUser(request)
    mcf = 'dashboard'
    params = ''
    if currentuser.IsLoggedIn:
        #only clear if we were logged in.
        urlstate = getCurrentURLState(request, andClear=True)
    else:
        urlstate = getCurrentURLState(request) 
    
    if urlstate.redirectMainContentFunction:
            mcf = urlstate.redirectMainContentFunction
    if urlstate.params:
        params = urlstate.params

    if params:
        sendparams = params[1]
    else:
        sendparams = ''

    jsonparams = simplejson.dumps(sendparams)

    return render_to_response('index.mako', { 
                        'APP_SECURE_URL': siteurl(request),
                        'username': request.user.username,
                        'mainContentFunction': mcf,
                        'wh': webhelpers,
                        'params': jsonparams,
                        })

