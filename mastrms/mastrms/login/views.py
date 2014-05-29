from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.conf import settings
from ccg_django_utils import webhelpers
from ccg_django_utils.webhelpers import siteurl, wsgibase
from mastrms.app.utils.data_utils import jsonResponse, jsonErrorResponse
from mastrms.users.models import *
from mastrms.login.URLState import getCurrentURLState
from mastrms.app.utils.mail_functions import sendForgotPasswordEmail, sendPasswordChangedEmail
import md5, time
import logging

logger = logging.getLogger('mastrms.login')

def processLoginView(request, *args):
    success = processLogin(request, args)
    return HttpResponseRedirect(siteurl(request))


def processLogin(request, *args):
    logger.debug('***processLogin : enter ***' )

    success = False

    if request.method == "POST":
        post = request.POST.copy()

        username = post.get('username', '')
        password = post.get('password', '')
        logger.debug('username is: %s', username)

        try:
            user = authenticate(username=username, password=password)
        except:
            # fixme: don't think normal django auth will ever raise an
            # exception.
            user = None
            logger.exception("Error authenticating user: %s" % username)

        if user is not None:
            if user.is_active:
                try:
                    login(request, user)
                except Exception, e:
                    # fixme: same as above, don't think django raises exceptions
                    logger.exception("Login error for %s" % user)
                else:
                    logger.debug('successful login')
                    success = True
                    #set the session to expire after
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                logger.debug('inactive login')
        else:
            logger.debug('invalid login')

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
    user = User.objects.get(username=emailaddress)
    u = user.to_dict()
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
    user.update_user(None, None, u)
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
        user = User.objects.get(username=request.REQUEST['email'])
        userdetails = user_manager.to_dict()
        if userdetails.has_key('groups'):
            del userdetails['groups'] #remove 'groups' - they don't belong in an update.
        if userdetails.has_key('passwordResetKey') and len(userdetails['passwordResetKey']) == 1 and userdetails['passwordResetKey'][0] == vk:
            #clear out the pager vk
            del userdetails['passwordResetKey']
            #update the password
            user.update_user(username, passw, userdetails)
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
    currentuser = getCurrentUser(request)
    mcf = 'dashboard'
    params = ''
    if currentuser.is_authenticated():
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

    return render_to_response('index.html', {
                        'APP_SECURE_URL': siteurl(request),
                        'user': request.user,
                        'mainContentFunction': mcf,
                        'wh': webhelpers,
                        'params': jsonparams,
                        }, context_instance=RequestContext(request))
