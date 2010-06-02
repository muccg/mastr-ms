# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from mdatasync_server.models import *
from repository.models import *  
from mdatasync_server.rules import *
from django.conf import settings
import os
import os.path

def jsonResponse(data):
    jdata = simplejson.dumps(data)
    return HttpResponse(jdata)

#nodeconfig = NodeConfig()
########nodeconfig.AddRule('testnode', 'teststation', '*.swp', ActionType.UPDATE_EXISTING)
#####nodeconfig.AddRule('testnode', 'teststation', '/testsource,/testdest', ActionType.MOVE)
#nodeconfig.AddRule('testnode', 'teststation', '*.pdf', ActionType.EXCLUDE)
#nodeconfig.AddRule('testnode', 'teststation', 'always/**', ActionType.INCLUDE)

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

def retrievePathsForFiles(request, *args):
    status = 0 #no error
    error = '' #no error
    filesdict = {} 
    rules = []
    import webhelpers
    host = request.__dict__['META']['SERVER_NAME'] #might not be right name

    try:
        pfiles = request.POST.get('files', {})
        #pfiles is json for a list of filenames
        pfiles = simplejson.loads(pfiles)
        #pfiles is now our list of fnames.
        porganisation = simplejson.loads(request.POST.get('organisation', ''))
        psitename= simplejson.loads(request.POST.get('sitename', ''))
        pstation = simplejson.loads(request.POST.get('stationname', ''))
        print 'Post var files passed through was: ', pfiles
        print 'Post var organisation passed through was: ', porganisation
        print 'Post var station passed through was: ', pstation
        print 'Post var sitename passed through was: ', psitename

        #filter by client, node, whatever to 
        #get a list of filenames in the repository run samples table
        #to compare against.
        #for each filename that matches, you use the experiment's ensurepath 
        try:
            nodeclient = NodeClient.objects.get(organisation_name = porganisation, site_name=psitename, station_name = pstation)
            print 'Nodeclient found.'
            try:
                rulesset = NodeRules.objects.filter(parent_node = nodeclient)
                rules = [x.__unicode__() for x in rulesset]
            except Exception, e:
                status = 1
                error = '%s, %s' % (error, 'Unable to resolve ruleset: %s' % (str(e)))
            #now get the runs for that nodeclient
            runs = Run.objects.filter(machine = nodeclient) 
            for run in runs:
                runsamples = RunSample.objects.filter(run = run)
                for rs in runsamples:
                    fname = rs.filename;
                    path = rs.sample.experiment.ensure_dir()
                    print 'Filename: %s belongs in path %s' % ( fname, path )
                    if filesdict.has_key(fname):
                        print 'Duplicate path detected!!!'
                        error = "%s, %s" % (error, "Duplicate filename detected for %s" % (fname))
                        status = 2
                    filesdict[fname] = path 

        except Exception, e:
            status = 1
            error = "%s, %s" % (error, 'Unable to resolve end machine to stored NodeClient: %s' % str(e) )
        

    except Exception, e:
        status = 1
        error = str(e)

    retfilesdict = {}

    #so by this stage, we can go through and test each sent file against the filesdict.
    for fname in pfiles:
        fname = str(fname)
        if fname in filesdict.keys(): #filesdict is keyed on filename
            retfilesdict[fname] = filesdict[fname]
            print 'Setting %s to %s' % (fname, retfilesdict[fname])
        else:
            print '%s not associated with a runsample. Ignored' % (fname)

    retval = {'status': status,
             'error' : error,
             'filesdict':retfilesdict,
             'rules' : rules,
             'host' : host,
             #'rules' : None 
            }

    print 'RETVAL is', retval
    return jsonResponse(retval)

def defaultpage(request, *args):
    try:

        pfiles = request.POST.get('files', None)
        porganisation = simplejson.loads(request.POST.get('organisation', ''))
        psitename= simplejson.loads(request.POST.get('sitename', ''))
        pstation = simplejson.loads(request.POST.get('stationname', ''))
        print 'Post var files passed through was: ', pfiles
        print 'Post var organisation passed through was: ', porganisation
        print 'Post var station passed through was: ', pstation
        print 'Post var sitename passed through was: ', psitename

        #try to get a config for this node/station
        try:
            ncs = NodeClient.objects.filter(organisation_name = porganisation, site_name = psitename, station_name = pstation)
            rulesset = NodeRules.objects.filter(parent_node = ncs)
        except:
            print 'Could not get a matching nodeclient'
        n = ncs[0]
        print 'Current nodeconfig is : ', n 
        rules = [x.__unicode__() for x in rulesset]
        path = '%s/pending/%s/%s/%s' % (settings.PERSISTENT_FILESTORE, porganisation, psitename, pstation)
        
        #make sure the path exists
        if not os.path.exists(path):
            print 'Creating %s' % (path)
            try:
                os.makedirs(path)
            except:
                print 'Could not make the path!'

        import webhelpers
        host = request.__dict__['META']['SERVER_NAME'] #might not be right name
        #host = request.__dict__['META']['REMOTE_ADDR'] #might be client address?
        #host = request.__dict__['META']['HTTP_HOST'] #would include port

        #hardcoded return
        d = {'host':host,
             'path':path,
             'rules' : rules
             #'rules' : None 
            }
        print 'rules DICT: ', d
        return jsonResponse(d)
    except Exception, e:
        return jsonResponse(str(e))


'''
def defaultpage(request, *args):
    try:

        pfiles = request.POST.get('files', None)
        porganisation = simplejson.loads(request.POST.get('organisation', ''))
        psitename= simplejson.loads(request.POST.get('sitename', ''))
        pstation = simplejson.loads(request.POST.get('station', ''))
        print 'Post var files passed through was: ', pfiles
        print 'Post var organisation passed through was: ', porganisation
        print 'Post var station passed through was: ', pstation
        print 'Post var sitename passed through was: ', psitename

        #try to get a config for this node/station
        n = nodeconfig.toDict()
        print 'Current nodeconfig is : ', n 
        if n.has_key(porganisation) and n[porganisation].has_key(psitename):
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
'''



