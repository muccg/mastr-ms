# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from webhelpers import siteurl

from madas.utils import setRequestVars, jsonResponse
from django.contrib.auth.ldap_helper import LDAPHandler


def processLogin(request, *args):
    print '***processLogin : enter ***' 

    #firstly, check the session for params.
    params = request.session.get('params', [])
    redirectMainContentFunction = request.session.get('redirectMainContentFunction', None)
    print '\tredirectMainContentFunction is %s' % (redirectMainContentFunction)
    print '\tparams is %s' % (params)

    success = False

    if request.method == "POST":
        post = request.POST.copy()
   
        try:
            username = post['username']
            password = post['password']
        except Exception,e:
            username = ''
            password = ''

        user = None
        from django.contrib.auth import authenticate, login
        try: 
            print 'auth begin'
            user = authenticate(username = username, password = password)
            print 'auth done'
        except Exception, e:
            print str(e)

        authenticated = 0
        authorized = 0
        if user is not None:
            
            print '\tprocessLogin: valid user'
            if user.is_active:
                print '\tprocessLogin: active user'
                print str(user)
                try:
                    a = login(request, user)
                except Exception, e:
                    print str(e)
                print '\tfinished doing auth.login: ', a
                success = True
                authenticated = True
                authorized = True
                #flush the session
                #request.session.flush()
                #set the session to expire after
                from madas import settings
                request.session.set_expiry(settings.SESSION_TIMEOUT)
                request.session['loggedin'] = True
            else:
                print '\tprocessLogin: inactive user'
                success = False
                authenticated = False 
                authorized = False
        else:
            print '\tprocessLogin: invalid user'
            success = False
            authenticated = False
            authorized = False

        nextview = 'login:success' #the view that a non admin would see next
        
        #If they are authenticated, make sure they have their groups cached in the session
        cachedgroups = [] 
        if authenticated:
            import utils
            cachedgroups = utils.getGroupsForSession(request, force_reload = True) #make sure this is reloaded - same session could have 2 logins.

        should_see_admin = False
        request.user.is_staff = False
        for gr in cachedgroups:
            if gr == 'Administrators':
                should_see_admin = True
    
        if should_see_admin is True:
            nextview = 'admin:adminrequests'
            request.user.is_staff = True
            print '\tAdmin! - Setting is_admin to ', request.user.is_staff
        else:
            request.user.is_staff = False
            print '\tNot Admin! - Setting is_admin to ', request.user.is_staff

        
        
        #if they are authenticated (i.e. they have an entry in django's user table, and used the right password...)
        if authenticated:
            request.user.save() #save the status of is_admin 
        
        u = request.user
        if redirectMainContentFunction is not None and redirectMainContentFunction != '': 
            nextview = redirectMainContentFunction
        #    request.session['redirectMainContentFunction'] = None
        #    request.session['params'] = None
               
        mainContentFunction = nextview
        params = params

        print '\tprocessLogin, mainContentFunction: ', mainContentFunction
        setRequestVars(request, success=success, authorized = authorized, authenticated = authenticated, mainContentFunction = mainContentFunction)

    print '*** processLogin : exit ***'
    return success 

def index(request, *args):
    return jsonResponse(request, args) 

def processLogout(request, *args):
    from django.contrib.auth import logout
    print '*** processLogout : enter***'
    print '\tlogging out (django)'
    logout(request) #let Django log the user out
    setRequestVars(request, success=True, mainContentFunction = 'login')
    print '*** processLogout : exit***'
    return HttpResponseRedirect(siteurl(request)) 

def processForgotPassword(request, *args):
    '''
    handles the submission of the 'forgot password' form
    regardless of success it should return success, to obfsucate user existence
    sets a validaton key in the user's ldap entry which is used to validate the user when they click the link in email
    '''
    print '*** processForgotPassword : enter***'
    emailaddress = request.REQUEST['username'].strip()
    from madas import settings
    ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
    u = ld.ldap_get_user_details(emailaddress)
    print 'User details: ', u
    import md5
    m = md5.new()
    import time
    m.update('madas' + str(time.time()) + 'resetPasswordToken123')
    vk = m.hexdigest()

    u['pager'] = [vk]

    #remove groups info
    try:
        del u['groups']
    except:
        pass

    print '\tUpdating user record with verification key'
    ld.ldap_update_user(emailaddress, None, None, u) 
    print '\tDone updating user with verification key'

    #Email the user
    from mail_functions import sendForgotPasswordEmail
    sendForgotPasswordEmail(request, emailaddress, vk)
   
    #$this->getRequest()->setAttribute('params', json_encode(array('message' => 'An email has been sent to '.$email.'. Please follow the instructions in that email to continue')));

    from django.utils import simplejson
    m = simplejson.JSONEncoder()
    p = {}
    p['message'] = "An email has been sent to %s. Please follow the instructions in that email to continue" % (emailaddress)

    setRequestVars(request, success=True, authorized = True, params = p, mainContentFunction='message')
    print '*** processForgotPassword : exit***'
    return jsonResponse(request, args) 

def forgotPasswordRedirect(request, *args):
    print '\tEntered forgot password'
    u = request.user
    try:
        print '\tsetting vars'
        request.session['redirectMainContentFunction'] = 'login:resetpassword'
        request.session['resetPasswordEmail'] = request.REQUEST['em']
        request.session['resetPasswordValidationKey'] = request.REQUEST['vk']
        from django.http import HttpResponseRedirect
        from madas.webhelpers import siteurl
        
        return HttpResponseRedirect(siteurl(request))
        #return jsonResponse(request, args) 
    except Exception, e:
        print str(e)

def populateResetPasswordForm(request, *args):
    u = request.user
    print '***populateResetPasswordForm***: enter'
    data = {}
    data['email'] = request.session['resetPasswordEmail']
    data['validationKey'] = request.session['resetPasswordValidationKey']
    print '\tData: ', data

    setRequestVars(request, success = True, items = [data], authenticated = False, authorized = True, totalRows = 1)
    print '***populateResetPasswordForm***: exit'
    return jsonResponse(request, args) 

def processResetPassword(request, *args):
    print '***populateResetPasswordForm***: enter'
    from madas import settings
    
    username = request.REQUEST.get('email', '')
    vk = request.REQUEST.get('validationKey', '')
    passw = request.REQUEST.get('password', '')
    success = True
    if username is not '' and vk is not '' and passw is not '':

        #get existing details
        ld = LDAPHandler(userdn=settings.LDAPADMINUSERNAME, password=settings.LDAPADMINPASSWORD)
        userdetails = ld.ldap_get_user_details(request.REQUEST['email'])
        if userdetails.has_key('groups'):
            del userdetails['groups'] #remove 'groups' - they don't belong in an update.
        if userdetails.has_key('pager') and len(userdetails['pager']) == 1 and userdetails['pager'][0] == vk:
            #clear out the pager vk
            del userdetails['pager']
            #update the password
            ld.ldap_update_user(username, username, passw, userdetails, pwencoding='md5')
            from mail_functions import sendPasswordChangedEmail
            sendPasswordChangedEmail(request, username)
                
        else:
            print '\tEither no vk stored in ldap, or key mismatch. uservk was %s, storedvk was %s' % (vk, userdetails.get('pager', None))
            success = False

    else:
        print 'Argument error'
        success = False
        request.session.flush() #if we don't flush here, we are leaving the redirect function the same.
    setRequestVars(request, success = success, authenticated = False, authorized = True, totalRows = 0, mainContentFunction = 'login')
    print '***populateResetPasswordForm***: exit'
    return jsonResponse(request, args) 

def unauthenticated(request, *args):
    return jsonResponse(request, args) 

def unauthorized(request, *args):
    print 'executed Login:unauthorized'
    authorized = False
    mainContentFunction = 'notauthorized'
    setRequestVars(request, mainContentFunction = mainContentFunction)
    #TODO now go to 'pager' with action 'index'
    return jsonResponse(request, args) 

