# Create your views here.

from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.core import serializers
#from django.utils import simplejson
from madas.utils.data_utils import jsonResponse, param_remap
from django.shortcuts import render_to_response, render_mako
from django.utils.webhelpers import siteurl, wsgibase
import django.utils.webhelpers as webhelpers
from madas.login.views import processLogin
from django.contrib.auth.models import User

def login(request, *args):
    success = processLogin(request, args)
    return HttpResponseRedirect(siteurl(request) + 'repo/') 

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
        print "Params: " + str(request.session['params'])

    site = siteurl(request)
    if '/repo' in request.META['PATH_INFO']:
        site += 'repo/'

    print 'redirectMain is redirecting to ', site
    return HttpResponseRedirect(site)

    
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
            qsargs = qsargs.strip('?') 
            vars = qsargs.split('&')
            for var in vars:
                if len(var.split('=')) > 1:
                    (key,val) = var.split('=')
                    if key is not None and val is not None:
                        argsdict[key] = val


            argsdict = param_remap(argsdict)

            print 'module: %s, funcname %s, argsdict %s' % (modname, funcname, argsdict)
        #else:
        #    print 'No match'

            params = [argsdict]
            print 'redirecting'
            return redirectMain(request, module = modname, submodule = funcname, params = params)
        else:
            params = request.session.get('params', [])

    #get or create the user
    user, created = User.objects.get_or_create(username=request.user.username)
    if created is True:
        user.save()

    #print 'serve index...' 
    #print settings.APP_SECURE_URL
    #print request.username
    #print request.session.get('mainContentFunction', '')
    request.params = params
    from django.utils import simplejson
    m = simplejson.JSONEncoder()
    paramstr = m.encode(params)
    return render_mako('repo_index.mako', 
                        APP_SECURE_URL = siteurl(request),#settings.APP_SECURE_URL,
                        username = request.user.username,
                        mainContentFunction = request.session.get('mainContentFunction', 'dashboard'),
                        wh = webhelpers,
                        params = '' # params[1] #None #['quote:viewformal', {'qid': 83}]
                      )
def processLogout(request, *args):
    from django.contrib.auth import logout
    print '*** processLogout : enter***'
    print '\tlogging out (django)'
    logout(request) #let Django log the user out
    setRequestVars(request, success=True, mainContentFunction = 'login')
    print '*** processLogout : exit***'
    return jsonResponse()
