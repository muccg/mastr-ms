# Create your views here.
import os
import os.path
import posixpath, urllib, mimetypes
import pickle
from datetime import datetime, timedelta
import copy
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import django.utils.webhelpers as webhelpers
from django.http import HttpResponse, Http404
from django.utils import simplejson
from mdatasync_server.models import *
from repository.models import *  
from mdatasync_server.rules import *
from django.conf import settings

from django.contrib import logging
LOGNAME = 'mdatasync_server_log'
logger = logging.getLogger(LOGNAME)
logger.setLevel(logging.WARNING) #default is warning

from settings import KEYS_TO_EMAIL, LOGS_TO_EMAIL, RETURN_EMAIL

from django.core.mail import EmailMessage

class FixedEmailMessage(EmailMessage):
    def __init__(self, subject='', body='', from_email=None, to=None, cc=None,
                 bcc=None, connection=None, attachments=None, headers=None):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).

        All strings used to create the message can be Unicode strings (or UTF-8
        bytestrings). The SafeMIMEText class will handle any necessary encoding
        conversions.
        """
        to_cc_bcc_types = (type(None), list, tuple)
        # test for typical error: people put strings in to, cc and bcc fields
        # see documentation at http://www.djangoproject.com/documentation/email/
        assert isinstance(to, to_cc_bcc_types)
        assert isinstance(cc, to_cc_bcc_types)
        assert isinstance(bcc, to_cc_bcc_types)
        super(FixedEmailMessage, self).__init__(subject, body, from_email, to,
                                           bcc, connection, attachments, headers)
        if cc:
            self.cc = list(cc)
        else:
            self.cc = []

    def recipients(self):
        """
        Returns a list of all recipients of the email (includes direct
        addressees as well as Bcc entries).
        """
        return self.to + self.cc + self.bcc

    def message(self):
        msg = super(FixedEmailMessage, self).message()
        del msg['Bcc'] # if you still use old django versions
        if self.cc:
            msg['Cc'] = ', '.join(self.cc)
        return msg

#This is an object which we will serialise to disk,
#representing a snapshot of client state. It is refreshed
#every time a client syncs
class ClientState(object):
    def __init__(self, org=None, site=None, station = None):
        self.files = {} #the list of files that the client reports it has
        self.lastSyncAttempt = None #the last time the client contacted the service
        self.organisation = org
        self.sitename = site
        self.station = station
        self.lastError = ""


def get_saved_client_state(org, site, station):
    #look for the file, if exists, try deserialising and returning
    clientstatedir = os.path.join(settings.REPO_FILES_ROOT , 'synclogs')
    clientstatefname = os.path.join(clientstatedir, "STATE_%s_%s_%s.dat" % (org, site, station))
    if os.path.exists(clientstatefname):
        try:
            with open(clientstatefname) as f:
                clientstate = pickle.load(f)
            return clientstate
        except Exception, e:
            logger.warning("%s could not be un-pickled: %s" % (clientstatefname, e) )
    else:
        logger.debug("File %s did not exist." % (clientstatefname) )
    #else reuturn a new Clientstate object
    return ClientState(org=org, site=site, station=station)

def save_client_state(clientstate):
    clientstatedir = os.path.join(settings.REPO_FILES_ROOT , 'synclogs')
    clientstatefname = os.path.join(clientstatedir, "STATE_%s_%s_%s.dat" % (clientstate.organisation, clientstate.sitename, clientstate.station))
    try:
        with open(clientstatefname, "wb") as f:
            pickle.dump(clientstate, f)
    except Exception, e:
        logger.warning("Could not save clientstate. %s" % (str(e)))

def get_node_from_request(request, organisation=None, sitename=None, station=None):
    retval = None
    
    if organisation is None:
        organisation = request.REQUEST('organisation', None)
    if sitename is None:
        sitename = request.REQUEST('sitename', None)
    if station is None:
        station = request.REQUEST('station', None)

    logger.debug("Searching for node org=%s, sitename=%s, station=%s" % (organisation, sitename, station))
    try:
        nodeclient = NodeClient.objects.get(organisation_name = organisation, site_name=sitename, station_name = station) 
        if nodeclient is None:
            logger.warning("No nodeclient existed with organisation=%s, sitename=%s, station=%s" % (organisation, sitename, station))
        else:
            retval = nodeclient
    except:
        pass

    return retval

def checkClientVersion(versionstr):
    print "Checking client version: %s" % (versionstr)
    return True


def requestSync(request, organisation=None, sitename=None, station=None):
    '''This is the initial request the client makes of the server.
       The client will have sent (via URL or post fields) its
       organisation, sitename, and station, what verstion it is, and whether
       it wants to re-sync already completed files.

       The server should, after verifying that the node exists and that the 
       version is acceptable, then go through the experiments which the node
       is involved in, and send back a list of files it wants.

       The return format is:
       {
            files: {},
            runsamples: {},
            details{},
            success: T/F (set to False if no node or version check fails)
            message: "" (a message to explain problems if success is false)

       }
    '''
    node = get_node_from_request(request, organisation, sitename, station)
    resp = {"success": False, "message": "", "files": {}, "details":{}, "runsamples":{}}
    syncold = request.GET.get("sync_completed", False)

    if node is not None:
        ncerror, nodeclient_details = get_nodeclient_details(organisation, sitename, station)
        resp["details"] = nodeclient_details
        if not checkClientVersion(request.POST.get('version', None)):
            resp["message"] = "Client version %s is not supported. Please update."
        else:
            resp["success"] = True
            #now get the runs for that nodeclient
            expectedFiles = getExpectedFilesForNode(node, include_completed=syncold)
            expectedincomplete = expectedFiles['incomplete']
            expectedcomplete = expectedFiles['complete']

            for runid in expectedincomplete.keys():
                resp["files"].update(expectedincomplete[runid])

            if syncold:
                for runid in expectedcomplete.keys():
                    resp["files"].update(expectedcomplete[runid])
        
        #not sure why we need this yet
        #fl = FileList(pfiles)
        #clientstate.files = pfiles 
        clientstate = get_saved_client_state(organisation, sitename, station)
        clientstate.lastSyncAttempt = datetime.now()
        ##save the client state
        save_client_state(clientstate)
    else:
        resp["message"] = "Could not find node %s-%s-%s" % (organisation, sitename, station)

    return HttpResponse(simplejson.dumps(resp))
    
'''
class FileList(object):
    def __init__(self, heirarchy):
        self.heirarchy = copy.deepcopy(heirarchy)
        self.currentnode = None
        self.checknodes = [] #a queue of nodes for us to process
        self.runsamplesdict = {}

    def checkFiles(self, filesdict):
        #beginning at the top of the heirarchy, we attempt matches at each level.
        self.checknodes.append(self.heirarchy) #push on the root node
       
        logger.debug( 'The filenames coming out of the database are:' )
        for f in filesdict.keys():
            logger.debug('\t%s' % (f.encode('utf-8') ) )

        while len(self.checknodes):
            self.currentnode = self.checknodes.pop()
            logger.debug('currentnode is %s' % ( self.currentnode ) )
            logger.debug('running checknode')
            self.checknode(filesdict)

        return self.heirarchy

    def markfound(self, node, fname, filesdictentry):
        #Mark a file as 'found' (if it isnt a file it will be None)
        node[fname] = filesdictentry[2] #the relative path
        runid = filesdictentry[0] #the runid
        runsampleid = filesdictentry[1] #the runsampleid
        if runid not in self.runsamplesdict.keys():
            self.runsamplesdict[runid] = []
        self.runsamplesdict[runid].append(runsampleid) 
    
    def checknode(self, filesdict):
        #if there are files at this node. 
        
        #create a list of uppercase keys to do the comparison with.
        #we always do our comparisons with uppercase, so that they are case insensitive,
        #remembering that the filesdict is keyed uppercase.
        
        if (self.currentnode.has_key('.')) and len(self.currentnode['.'].keys()):
            for fname in self.currentnode['.'].keys():
                upperfname = fname.upper() #uppercase the fname, since the filesdict is keyed on uppercase names
                #is the filename in the filesdict keys?
                logger.debug('filename is: %s' % (unicode(fname).encode('utf-8') ) )
                if upperfname in filesdict.keys():
                    self.markfound(self.currentnode['.'], fname, filesdict[upperfname])
                    #rewrite the DB filename to be the supplied one.
                    try:
                        runsampleDBentry = RunSample.objects.get(id=filesdict[upperfname][1])
                        runsampleDBentry.filename = fname
                        runsampleDBentry.save()
                    except Exception, e:
                        logger.debug('Exception renaming runsample filename: %s' % (str(e)) )
                    #remove the entry from the filesdict - no point testing it
                    #again.
                    del filesdict[upperfname]
                    logger.debug('Found file: Setting %s to %s' % (fname.encode('utf-8'), self.currentnode['.'][fname].encode('utf-8')) )
                else:
                    #delete entries that werent found
                    del self.currentnode['.'][fname]
                    logger.debug( 'File %s not associated with a runsample, ignoring' % (fname.encode('utf-8')) )
        #now that you have checked the files at a node, you need to 
        #check the directories at the node.
        #if the dir is found, mark it as such and do nothing else with it.
        #otherwise, push each unfound dir as a new node on the checknodes 
        #queue
        for dirname in self.currentnode.keys():
            upperdirname = dirname.upper()
            if upperdirname not in ['.', '/']: #don't check the filelist or 'path' entry
                logger.debug('checking dir: %s' % (upperdirname.encode('utf-8')) )
                if upperdirname in filesdict.keys():
                    #set the dir to contain the path, not a node.
                    self.markfound(self.currentnode, dirname, filesdict[upperdirname])
                    #rewrite the DB filename to be the supplied one.
                    try:
                        runsampleDBentry =  RunSample.objects.get(id=filesdict[upperdirname][1])
                        runsampleDBentry.filename = dirname
                        runsampleDBentry.save()
                    except Exception, e:
                        logger.debug('Exception renaming runsample filename: %s' % (str(e)) )

                    #remove the found entry from the filesdict
                    del filesdict[upperdirname]
                    logger.debug( 'Found dir: Setting %s to %s' % ( dirname.encode('utf-8'), self.currentnode[dirname].encode('utf-8') ))
                else:
                    #push the dir onto the checknodes.
                    logger.debug('Could not find dir %s, pushing.' % (dirname.encode('utf-8')) )
                    self.checknodes.append(self.currentnode[dirname])
'''


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
    logger.debug( 'trying getNodeClients' )
    ncs = NodeClient.objects.all()
    result = {}
    for n in ncs:
        logger.debug( 'checking a node' )
        if not result.has_key(n.organisation_name):
            result[n.organisation_name] = {}
        o = result[n.organisation_name]
        if not o.has_key(n.site_name):
            o[n.site_name] = []

        o[n.site_name].append(n.station_name)

    return jsonResponse(result)

@login_required
def nodeinfo(request, organisation=None, sitename=None, station=None):
    try:
        nodeclient = get_node_from_request(request, organisation=organisation, sitename=sitename, station=station)
        if nodeclient is None:
            raise Exception("No nodeclient existed with organisation=%s, sitename=%s, station=%s" % (organisation, sitename, station))
        clientstate = get_saved_client_state(organisation, sitename, station)
    #return HttpResponse( simplejson.dumps(nodeclient.__dict__) + simplejson.dumps(clientstate.__dict__) )   
        timediff = datetime.now() - datetime.now() 
        if clientstate.lastSyncAttempt is not None:
            timediff = datetime.now() - clientstate.lastSyncAttempt

        expectedfiles = getExpectedFilesForNode(nodeclient, include_completed=True)
        return render_to_response("node.mako", {'nodeclient':nodeclient, 'expectedfiles': expectedfiles, 'timediff': timediff, 'clientstate': clientstate.__dict__, 'wh':webhelpers} ) 

    except Exception, e:
        return HttpResponse("Could not display node info: %s" % (e))


def getExpectedFilesForNode(nodeclient, include_completed = False):
    '''Based on the experiments that a given nodeclient is involved in,
       return the files which the server expects.
       If include_completed is false, this will be every file which 
       the server cannot see on its filesystem from incomplete experiments/runs.
       If include_complete is true, this will be every file which the 
       server cannot see on its filesystem from incomplete and complete experiments/runs.
    '''

    incomplete = {}
    complete = {}

     #now get the runs for that nodeclient
    runs = Run.objects.filter(machine = nodeclient) 
    for run in runs:
        target_dict = incomplete
        logger.debug('Finding runsamples for run')
        
        if (run.state != RUN_STATES.COMPLETE[0]) or ( (run.state == RUN_STATES.COMPLETE[0]) and include_completed):
            if run.state == RUN_STATES.COMPLETE[0]:
                target_dict = complete
            
            runsamples = RunSample.objects.filter(run = run)
            #Build a filesdict of all the files for these runsamples
            for rs in runsamples:
                logger.debug('Getting files for runsamples');
                if rs.filename is None or rs.filename == "":
                    continue #move to the next record - this one has no filename
                
                if (! checkRunSampleFileExists(rs.id)):
                    abspath, relpath = rs.filepaths()
                    logger.debug( 'Filename: %s belongs in path %s' % ( rs.filename.encode('utf-8'), abspath.encode('utf-8') ) )
                    if target_dict.has_key(rs.filename):
                        logger.debug( 'Duplicate path detected!!!' )
                        error = "%s, %s" % (error, "Duplicate filename detected for %s" % (rs.filename.encode('utf-8')))
                        status = 2
                    #we use the relative path
                    if not(target_dict.has_key(run.id)):
                        target_dict[run.id] = {}

                    logger.debug("Adding %s to target_dict" % (rs.filename) )
                    target_dict[run.id][rs.filename] = [run.id, rs.id, relpath, os.path.exists(os.path.join(abspath, rs.filename))]

    return {'complete': complete, 'incomplete': incomplete}


def get_nodeclient_details(organisation_name, site_name, station_name):
    nodeclient_details = {}
    error = None
    try:
        nodeclient = NodeClient.objects.get(organisation_name = organisation_name, site_name=site_name, station_name = station_name)
        logger.debug( 'Nodeclient found.')
        
        nchost = nodeclient.hostname
        if nchost is not None and len(nchost) > 0:
            nodeclient_details['host'] = str(nchost)
        ncflags = nodeclient.flags
        if ncflags is not None and len(ncflags) > 0:
            nodeclient_details['flags'] = str(ncflags)
        ncuname = nodeclient.username
        if ncuname is not None and len(ncuname) > 0:
            nodeclient_details['username'] = str(ncuname)

        nodeclient_details['rootdir'] = settings.REPO_FILES_ROOT

        logger.debug('Checking for rules')
        try:
            rulesset = NodeRules.objects.filter(parent_node = nodeclient)
            nodeclient_details['rules'] = [x.__unicode__() for x in rulesset]
        except Exception, e:
            #status = 1
            error = '%s, %s' % (error, 'Unable to resolve ruleset: %s' % (str(e)))
    except Exception, e:
        #status = 1
        logger.debug("exception encountered: %s" % (e))
        error = "%s, %s" % (error, 'Unable to resolve end machine to stored NodeClient: %s' % str(e) )

    return error, nodeclient_details


#def retrievePathsForFiles(request, *args):
#    '''This function is called as a webservice by the datasync client.
#       It expects a post var called 'files' which will be a json string
#       which represents a heirarchy of directories and files.
#    '''
#    
#    status = 0 #no error
#    error = '' #no error
#    filesdict = {} 
#    rules = []
#    #default host is this host.
#    host = None 
#    defaultHost = request.__dict__['META']['SERVER_NAME'] 
#    flags = None
#    username = None
#
#    pfiles = request.POST.get('files', None)
#    #pfiles is json for a heirarchy of files and directories
#    if pfiles is not None:
#        pfiles = simplejson.loads(pfiles)
#    else:
#        pfiles = {} 
#    #pfiles is now our heirarchy of file and directory names.
#    porganisation = simplejson.loads(request.POST.get('organisation', "null"))
#    psitename= simplejson.loads(request.POST.get('sitename', "null"))
#    pstation = simplejson.loads(request.POST.get('stationname', "null"))
#    syncold = simplejson.loads(request.POST.get('syncold', 'false')) #defaults to false
#
#    logger.debug( 'Post var files passed through was: %s' % ( pfiles) )
#    logger.debug( 'Post var organisation passed through was: %s' % ( porganisation) )
#    logger.debug( 'Post var station passed through was: %s' % ( pstation ) )
#    logger.debug( 'Post var sitename passed through was: %s' % ( psitename) )
#    logger.debug( 'Post var syncold passed through was: %s' % ( str(syncold) ) )
#
#    #get the saved client state, so we can update it
#    clientstate = get_saved_client_state(porganisation, psitename, pstation)
#
#    filesdict = {}
#
#    #filter by client, node, whatever to 
#    #get a list of filenames in the repository run samples table
#    #to compare against.
#    #for each filename that matches, you use the experiment's ensurepath 
#    
#    ncerror, nodeclient_details = get_nodeclient_details(porganisation, psitename, pstation)
#    if ncerror is not None:
#        status = 1
#        error = ncerror
#    else:
#        #now get the runs for that nodeclient
#        expectedFiles = getExpectedFilesForNode(nodeclient, include_completed=syncold)
#        #merge complete and incomplete
#        for runid in expectedFiles['incomplete'].keys():
#            logger.debug("INCOMPLETE: adding files for run %d" % (runid) )
#            filesdict.update(expectedFiles['incomplete'][runid])
#        for runid in expectedFiles['complete'].keys():
#            logger.debug("COMPLETE: adding files for run %d" % (runid ))
#            filesdict.update(expectedFiles['complete'][runid])
#
#    logger.debug('making filelist obj')
#    #So. Make a FileList object out of pfiles.
#    fl = FileList(pfiles)
#    
#    import json
#    
#    print "pfiles is:"
#    print json.dumps(pfiles, indent=4)
#    
#    print "FileList result from pfiles is:"
#    print json.dumps(fl.runsamplesdict, indent=4)
#
#    logger.debug('checking files')
#    wantedfiles = json.dumps(fl.checkFiles(filesdict), indent=4)
#
#    print "Wantedfiles (from fl.checkfiles) is: "
#    print wantedfiles
#
#    #set the default host
#    if host is None or len(host) == 0:
#        host = defaultHost 
#
#    retval = {'status': status,
#             'error' : error,
#             'filesdict':wantedfiles,
#             'runsamplesdict' : fl.runsamplesdict,
#             'rootdir' : settings.REPO_FILES_ROOT,
#             'rules' : rules,
#             'host' : host,
#             'username': username,
#             'flags': flags,
#             #'rules' : None 
#            }
#
#    clientstate.files = pfiles 
#    clientstate.lastSyncAttempt = datetime.now()
#    #save the client state
#    save_client_state(clientstate)
#
#    logger.debug('RETVAL is %s' % ( retval ) )
#    return jsonResponse(retval)

def checkRunSampleFileExists(runsampleid):
    fileexists = False
    try:
        rs = RunSample.objects.get(id=runsampleid)
        abssamplepath, relsamplepath = rs.filepaths()
        complete_filename = os.path.join(abssamplepath, rs.filename)
        fileexists = os.path.exists(complete_filename)
        logger.debug( 'Checking file %s:%s' % (complete_filename.encode('utf-8'), fileexists) )
    except Exception, e:
        logger.debug('Could not check runsample file for runsampleid: %s: %s' % (str(runsampleid), e))
    
    return fileexists

def checkRunSampleFiles(request):
    ret = {}
    ret['success'] = False;
    ret['description'] = "No Error"
    runsamplefilesjson = request.POST.get('runsamplefiles', None)
    if runsamplefilesjson is not None:
        runsamplefilesdict = simplejson.loads(runsamplefilesjson)
        # so now we have a dict keyed on run, of sample id's whose file should have been received.
        logger.debug('Checking run samples against: %s' % ( runsamplefilesdict) )
        # We iterate through each run, get the samples referred to, and ensure their file exists on disk.
        ret['description'] = ""
        totalruns = 0
        totalsamples = 0
        totalfound = 0
        
        ret['success'] = True 
        ret['description'] = 'Success'
        for runid in runsamplefilesdict.keys():
            totalruns += 1
            logger.debug('Checking files from run %s' % str(runid) )
            runsamples = runsamplefilesdict[runid]
            for runsample in runsamples:
                totalsamples +=1
                runsample = int(runsample)
                try:
                    rs = RunSample.objects.get(id = runsample)
                    rs.complete = checkRunSampleFileExists(runsample) 
                    if rs.complete:
                        totalfound += 1
                    rs.save()
                except Exception, e:
                    logger.debug('Error: %s' % (e) )
                    ret['success'] = False
                    ret['description'] = "%s, %s" % (ret['description'], str(e)) 
        ret['description'] = "%s - %d/%d samples marked complete, from %d run(s)" % (ret['description'], totalfound, totalsamples, totalruns)         
    else:
        ret['description'] = "No files given"

    logger.debug("POST: %s" % (str(request.POST)) )
    org = request.POST.get('organisation', None)
    site = request.POST.get('sitename', None)
    station = request.POST.get('stationname', None)
    if (org is not None) and (site is not None) and (station is not None):
        clientstate = get_saved_client_state(org, site, station)
        clientstate.lastError = request.POST.get('lastError', "Successfully syned %d files from runs: %s." % (totalfound, totalruns))
        clientstate.lastSyncAttempt = datetime.now()
        #update client state if the client posted a file list through
        clientfiles = request.POST.get('clientfiles', None)
        if clientfiles is not None:
            try:
                clientfiledict = simplejson.loads(clientfiles)
                clientstate.files = clientfiledict
            except Exception, e:
                clientstate.lastError = "Could not parse passed filestate: %s" % (str(e))

        save_client_state(clientstate)
        logger.debug("Saved lastError in client state")
    else:
        logger.debug("Could not get clientstate details: %s, %s, %s" % (org, site, station))

    return jsonResponse(ret)

def logUpload(request, *args):
    logger.debug('LOGUPLOAD')
    fname_prefix = 'UNKNOWN_'
    if request.POST.has_key('nodename'):
        fname_prefix = request.POST['nodename'] + '_'
    
    if request.FILES.has_key('uploaded'):
        f = request.FILES['uploaded']
        logger.debug( 'Uploaded file name: %s' % ( f._get_name() ) )
        written_logfile_name = str(os.path.join('synclogs', "%s%s" % (fname_prefix,f._get_name()) ) ) 
        write_success = _handle_uploaded_file(f, written_logfile_name )#dont allow them to replace arbitrary files

        try:
            if write_success:
                body ="An MS Datasync logfile has been uploaded: %s\r\n" % (written_logfile_name)
            else:
                body = "MS Datasync logfile upload failed: %s\r\n" % (written_logfile_name)
            e = FixedEmailMessage(subject="MS Datasync Log Upload (%s)" % (fname_prefix.strip('_')), body=body, from_email = RETURN_EMAIL, to = [LOGS_TO_EMAIL])
            e.send()
        except Exception, e:
            logger.debug( 'Unable to send "Log Sent" email: %s' % (str(e)) )

    else:
        logger.debug( 'logupload: No file in the post' )

    return jsonResponse('ok')

def keyUpload(request, *args):
    fname_prefix = 'UNKNOWN_'
    if request.POST.has_key('nodename'):
        fname_prefix = request.POST['nodename'] + '_'
    
    if request.FILES.has_key('uploaded'):
        f = request.FILES['uploaded']
        logger.debug( 'Uploaded file name: %s' % ( f._get_name() ) )
        written_logfile_name = str(os.path.join('publickeys', "%s%s" % (fname_prefix,'id_rsa.pub')) )
        _handle_uploaded_file(f, written_logfile_name)#dont allow them to replace arbitrary files
        write_success = _handle_uploaded_file(f, written_logfile_name )#dont allow them to replace arbitrary files

        try:
            if write_success:
                body ="An MS Datasync keyfile has been uploaded: %s\r\n" % (written_logfile_name)
            else:
                body = "MS Datasync keyfile upload failed: %s\r\n" % (written_logfile_name)
            e = FixedEmailMessage(subject="MS Datasync Public Key upload (%s)" % (fname_prefix), body=body, from_email = RETURN_EMAIL, to = [KEYS_TO_EMAIL])
            e.send()
        except Exception, e:
            logger.debug( 'Unable to send "Key Sent" email: %s' % (str(e)) )
         
    else:
        logger.debug('Keyupload: No file in the post')

    return jsonResponse('ok')



def _handle_uploaded_file(f, name):
    '''Handles a file upload to the projects REPO_FILES_ROOT
       Expects a django InMemoryUpload object, and a filename'''
    logger.debug( '*** _handle_uploaded_file: enter ***')
    retval = False
    try:
        import os
        dest_fname = str(os.path.join(settings.REPO_FILES_ROOT, name))
        if not os.path.exists(os.path.dirname(dest_fname)):
            logger.debug('creating directory: %s' % ( os.path.dirname(dest_fname) ) )
            os.makedirs(os.path.dirname(dest_fname))

        destination = open(dest_fname, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        retval = True
    except Exception, e:
        retval = False
        logger.debug( '\tException in file upload: %s' % ( str(e) ) )
    logger.debug( '*** _handle_uploaded_file: exit ***')
    return retval

@login_required
def utils(request):
    success = True
    message = ''
    #First, if they posted, they want to change the log level.
    if request.method == 'POST': 
        #set the log level:
        ll = request.POST.get('loglevel', None)
        success = True
        if ll:
            success, message = set_log_level(int(ll))
        else:
            success = False
            message = 'No valid log level posted.'

    #now we proceed as normal.

    nodeclients = NodeClient.objects.all()
    #Screenshots and logs are in the same dir.
    clientlogdir = os.path.join(settings.REPO_FILES_ROOT , 'synclogs')
    fileslist = []
    if os.path.exists(clientlogdir):
        fileslist = os.listdir(clientlogdir )
    clientlogslist = []
    shotslist = []
    for fname in fileslist:
        if fname.endswith('.png'):
            shotslist.append(fname)
        else:    
            clientlogslist.append(fname)

    serverloglist = os.listdir(settings.LOG_DIRECTORY)
    serverloglist.sort()
    clientlogslist.sort()
    shotslist.sort()
    currentLogLevel = logger.getEffectiveLevel()
    levelnames = ['Debug', 'Info', 'Warning', 'Critical', 'Fatal']
    levelvalues = [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL, logging.FATAL]
    return render_to_response("utils.mako", {'wh':webhelpers, 'serverloglist':serverloglist, 'clientlogslist':clientlogslist, 'shotslist':shotslist, 'currentLogLevel':currentLogLevel, 'levelnames':levelnames, 'levelvalues':levelvalues , 'success':success, 'message':message, 'nodeclients': nodeclients})

@login_required
def tail_log(request, filename=None, linesback=10, since=0):
    since = int(since)
    linesback = int(linesback)
    avgcharsperline=75
    pos = 0
    if filename is None:
        filename = 'mdatasync_server_log.log'

    logfilename = os.path.join(settings.LOG_DIRECTORY, filename)
    file = open(logfilename,'r')

    while 1:
        if (since):
            try: file.seek(since,os.SEEK_SET) #seek from start of file.
            except IOError: file.seek(0)
    
        else: #else seek from the end
            try: file.seek(-1 * avgcharsperline * linesback,2)
            except IOError: file.seek(0)
        
        if file.tell() == 0: atstart=1
        else: atstart=0

        lines=file.read().split("\n")
        pos = file.tell()
        
        #break if we were in 'since' mode, or we had enough lines, or we can't go back further
        if since or (len(lines) > (linesback+1)) or atstart: break
        
        #Otherwise, we are wanting to get more lines.
        #The lines are bigger than we thought
        avgcharsperline=int(avgcharsperline * 1.3) #Inc avg for retry
    file.close()

    out=""
    if not since:
        if len(lines) > linesback: 
            start=len(lines)-linesback -1
        else: 
            start=0

        for l in lines[start:len(lines)-1]: 
            out=out + l + "\n"
    else:
        for l in lines:
            out += l + "\n"

    return HttpResponse(simplejson.dumps({'data' : out, 'position':pos}) )

@login_required
def serve_file(request, path):
    root = settings.PERSISTENT_FILESTORE
    path = posixpath.normpath(urllib.unquote(path))
    path = path.lstrip('/') 
    fullpath = os.path.join(root, path)
    if not os.path.isfile(fullpath):
        raise Http404, '"%s" does not exist' % fullpath
    contents = open(fullpath, 'rb').read()
    mimetype = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
    response = HttpResponse(contents, mimetype=mimetype)
    response["Content-Length"] = len(contents)
    return response

def set_log_level(newlevel):
    success = True 
    if newlevel in [logging.INFO, logging.DEBUG, logging.WARNING, logging.FATAL, logging.CRITICAL]:
        logger.setLevel(newlevel)
        msg = 'Logging level set to %s' % (str(newlevel)) 
    else:
        success = False
        msg = 'Unable to set logging level to %s, no such level exists' % (str(newlevel)) 
    #logger.debug('test')
    #logger.info('test')
    #logger.warning('test')
    #logger.critical('test')
    #logger.fatal('test')
    return (success, msg)    
