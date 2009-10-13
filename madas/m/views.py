# Create your views here.

from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.core import serializers
#from django.utils import simplejson
from madas.utils import setRequestVars, jsonResponse
from django.shortcuts import render_to_response, render_mako
from webhelpers import siteurl
from madas.login.views import processLogin

def login(request, *args):
    success = processLogin(request, args)
    return HttpResponseRedirect(siteurl(request)) 

def authorize(request, module='/', perms = [], internal = False):
    print '*** authorize : enter ***'

    print 'Subaction: ', request.REQUEST.get('subaction', '')


    #A variable used to determine if we bother using any of the params (session or request)
    #that we see here. Default should be no, unless under specific circumstances
    #namely doing a password reset or viewing a quote from an external link.
    usecachedparams = False 
    cachedparams = ''

        #from django.core import serializers
        #json_serializer = serializers.get_serializer("json")()
        #
        #try:
        #    #TODO: This is never going to work. Its not a deserializer.
        #    params = json_serializer.deserialize(params) 
        #except Exception, e:
        #    print '\tException: Could not deserialise params (%s): %s' % (params, str(e))
        #    params = None
    redirectMainContentFunction = request.session.get('redirectMainContentFunction', None)
    if redirectMainContentFunction is not None:
        print '\tUsing session params ', redirectMainContentFunction
        cachedparams = request.session.get('params', None)
    #else:
        #passing through params of None means the request params are used anyway

    if module == 'quote':
        cachedparams = request.session.get('params', None)

    print '\tcachedparams: ', cachedparams


    #check if the session is still valid. If not, log the user out.
    loggedin = request.session.get('loggedin', False)
    if not loggedin:
        if not request.user.is_anonymous():
            #if request.user:
            #    request.user.logout() #session gets flushed here
            request.session.flush()
        else:
            #print request.session.__dict__
            if redirectMainContentFunction is not None and\
               redirectMainContentFunction != 'login:resetpassword':
                request.session.flush()

    request.session['params'] = cachedparams
    request.session['redirectMainContentFunction'] = redirectMainContentFunction

    from webhelpers import wsgibase
    print '\tmodule: %s, perms: %s, internal: %s, basepath: %s' % (str(module), str(perms), str(internal), str(wsgibase()))
    #Check the current user status
    authenticated = request.user.is_authenticated()   
    print '\tuser.is_authenticated was: ', authenticated
  
    #If they are authenticated, make sure they have their groups cached in the session
    if authenticated:
        import utils
        cachedgroups = utils.getGroupsForSession(request)
 
    #here we check the module and the permissions
    authorized = True
    if len(perms) > 0:
        authorized = False
        cachedgroups = request.session.get('cachedgroups', [])
        for perm in perms:
            if perm in cachedgroups:
                authorized = True
 
        if not authorized:        
            print '\tAuthorization failure: %s does not in any of %s' % (request.user.username, perms)
        

    print '\tuser authorized? : ', authorized

    if not authorized:
        destination = 'notauthorized'
    else:
        destination = module 
        print '\tauthorize: destination was ', destination
        
        s = request.REQUEST.get('subaction', '')
        print '\tsubaction was "%s"' % (s)        
        #we want to take them to the login page, UNLESS the destination:subaction was 
        #quote:request or login:forgotpassword or login:<nothing>
        if not authenticated:
            #if not internal and
            if ( destination != 'quote' and s != 'request' and\
                 destination != 'login' and s != 'resetpassword' and\
                 destination != 'login' and s != 'forgotpassword'):
                print '\tDestination is now login'
                destination = 'login'
            else:
                usecachedparams = True
                if s is not None and s != '':
                    destination +=  ':' + s
        else:
            if s is not None and str(s) != '':
                #Append the subaction
                destination += ':' + str(s)
  
        #despite all that, respect the redirectMainContentFunction if is is not None
        #TODO: This is a bit of a hack - we do this here so that we don't wreck
        #the /viewquote?id=1234 functionality. Really, it would be better to have a
        #cleaner way of doing it without having to explicitly check for the
        #redirectMainControlFunction here in authorise, but for the moment this works.
        if redirectMainContentFunction is not None:
            if redirectMainContentFunction == 'login:resetpassword':
                print '\tUsing redirectMainContentFunction because it was something useful'
                destination = redirectMainContentFunction
                request.session['redirectMainContentFunction'] = None

        print '\tDestination is now "%s"' % (destination)


    if usecachedparams:
        params = cachedparams 
    else:
        params = request.REQUEST.get('params', '')
        print params

    if authenticated or destination.startswith('login') or destination.startswith('quote'):
        if destination == 'login':
            print 'destination was login, so we are setting our request vars'
        setRequestVars(request, success=True, authenticated=authenticated, authorized=authorized, mainContentFunction=destination, params=params) 
    
    if destination == 'quote:viewformal':
        print 'rejigging for viewformal'
        setRequestVars(request, success=True, authenticated=authenticated, authorized=authorized, mainContentFunction=destination, params=cachedparams[1])
    
    if destination == 'dashboard':
        request.session['redirectMainContentFunction'] = None
        request.session['params'] = None
    
    #We only need to be 'authorized' to be allowed to render the page.
    #if authenticated and authorized:
    if authorized:
        aa = True
    else:
        aa = False

    print '*** authorize : exit ***'
    if not internal:
        return jsonResponse(request, []) 
    else:
        return (aa, jsonResponse(request, []) )  

from django.template import Context, loader

def redirectMain(request, *args, **kwargs):
    #If we have 'params' in the kwargs, we want to store them in the session.
    #We will want to retrieve them on the other side of the redirect, which
    #will probably be the login function.
   
    if kwargs.has_key('module'):
        red_str = kwargs['module']
        if kwargs.has_key('submodule'):
            red_str += ':%s' % (kwargs['submodule'])

        print 'Setting session[redirectMainContentFunction] to %s' % (red_str)
        request.session['redirectMainContentFunction'] = red_str 
    
    if kwargs.has_key('params'):
        request.session['params'] = kwargs['params']    
        request.session['params'].insert(0, red_str)

    print 'redirectMain is redirecting to ', siteurl(request)
    return HttpResponseRedirect(siteurl(request))

    
from django.conf import settings
from webhelpers import siteurl
from string import *
import webhelpers
def serveIndex(request, *args, **kwargs):
    for k in kwargs:
        print '%s : %s' % (k, kwargs[k])
    #so the 'cruft' key will contain a string.
    #we can split this string into 'module/submodule', and have a querystring for good measure
    #we put it in the 'params', and let the login page interpret it.
    if kwargs.has_key('cruft'):
        import re
        #m = re.match(r'(\w+)\/(\w+)?\?(.*)?', kwargs['cruft'])
        m = re.match(r'(\w+)\/(\w+)?', kwargs['cruft'])
        if m is not None:
            fullstring = m.group(0)
            modname = m.group(1)
            funcname = m.group(2)
            qsargs = request.META['QUERY_STRING']
            #for k in request.__dict__['META'].keys():
            #    print '%s : %s ' % (k, request.__dict__['META'][k])

            #parse the qs args
            argsdict = {}
            qsargs = strip(qsargs, '?') #strip off ?
            vars = split(qsargs, '&')
            for var in vars:
                if len(split(var, '=')) > 1:
                    (key,val) = split(var, '=')
                    if key is not None and val is not None:
                        argsdict[key] = val


            from utils import param_remap
            argsdict = param_remap(argsdict)

            print 'module: %s, funcname %s, argsdict %s' % (modname, funcname, argsdict)
        #else:
        #    print 'No match'

            params = [argsdict]
            print 'redirecting'
            return redirectMain(request, module = modname, submodule = funcname, params = params)
        else:
            params = request.session.get('params', '')

    #print 'serve index...' 
    #print settings.APP_SECURE_URL
    #print request.username
    #print request.session.get('mainContentFunction', '')
    request.params = params
    from django.utils import simplejson
    m = simplejson.JSONEncoder()
    paramstr = m.encode(params)
    
    if params:
        sendparams = params[1]
    else:
        sendparams = ''
    
    mcf = request.session.get('redirectMainContentFunction', 'dashboard')
    
    request.session['redirectMainContentFunction'] = None
    
    return render_mako('index.mako', 
                        APP_SECURE_URL = siteurl(request),#settings.APP_SECURE_URL,
                        username = request.user.username,
                        mainContentFunction = mcf,
                        wh = webhelpers,
                        params = sendparams # params[1] #None #['quote:viewformal', {'qid': 83}]
                      )

def serverinfo(request):
    return render_mako('serverinfo.mako', s=settings, request=request, g=globals() )

