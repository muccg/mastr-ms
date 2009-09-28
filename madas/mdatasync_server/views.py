# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from mdatasync_server.models import *
from mdatasync_server.rules import *

def jsonResponse(data):
    jdata = simplejson.dumps(data)
    return HttpResponse(jdata)

nodeconfig = NodeConfig()
########nodeconfig.AddRule('testnode', 'teststation', '*.swp', ActionType.UPDATE_EXISTING)
#####nodeconfig.AddRule('testnode', 'teststation', '/testsource,/testdest', ActionType.MOVE)
nodeconfig.AddRule('testnode', 'teststation', '*.pdf', ActionType.EXCLUDE)
nodeconfig.AddRule('testnode', 'teststation', 'always/**', ActionType.INCLUDE)

def configureNode(request, *args):
    return jsonResponse(nodeconfig.toDict())

def getNodeClients(request, *args):
    ncs = NodeClient.objects.all()
    result = {}
    for n in ncs:
        if not result.has_key(n.organisation_name):
            result[n.organisation_name] = {}
        o = result[n.organisation_name]
        if not o.has_key(n.site_name):
            o[n.site_name] = []

        o[n.site_name].append(n.station_name)


        
    return jsonResponse(result)
    

def defaultpage(request, *args):
    try:

        pfiles = request.POST.get('files', None)
        pnode = simplejson.loads(request.POST.get('node', ''))
        pstation = simplejson.loads(request.POST.get('station', ''))
        print 'Post var files passed through was: ', pfiles
        print 'Post var node passed through was: ', pnode
        print 'Post var station passed through was: ', pstation

        #try to get a config for this node/station
        n = nodeconfig.toDict()
        print 'Current nodeconfig is : ', n 
        if n.has_key(pnode) and n[pnode].has_key(pstation):
            rules = n[pnode][pstation] 
        else:
            rules = None
        #hardcoded return
        d = {'host':'127.0.0.1',
             'path':'/tmp/madas/filedata/pending/%s' % (pstation),
             'rules' : rules
             #'rules' : None 
            }
        print 'rules DICT: ', d
        return jsonResponse(d)
    except Exception, e:
        return jsonResponse(str(e))

