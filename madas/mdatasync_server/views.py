# Create your views here.
import os
import os.path
import posixpath, urllib, mimetypes
import pickle
from datetime import datetime, timedelta
import copy
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import ccg.utils.webhelpers as webhelpers
from django.http import HttpResponse, Http404
from django.utils import simplejson
from mdatasync_server.models import *
from repository.models import *  
from mdatasync_server.rules import *
from ClientState import * #All the functions for dealing with clientstates
from django.conf import settings

import logging
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


def checkClientVersion(versionstr):
    print "Checking client version: %s" % (versionstr)
    components = versionstr.split('.')
    if len(components) < 2:
        return False
    
    major = components[0]
    minor = components[1]

    #accept anything better than 1.4
    if major < 1:
        if minor < 4:
            return False
    return True

def jsonResponse(data):
    jdata = simplejson.dumps(data)
    return HttpResponse(jdata)

def request_sync(request, organisation=None, sitename=None, station=None):
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
    resp = {"success": False, 
            "message": "", 
            "files": {}, 
            "details":{}, 
            "runsamples":{}}
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
        
        clientstate = get_saved_client_state(organisation, sitename, station)
        clientstate.lastSyncAttempt = datetime.now()
        ##save the client state
        save_client_state(clientstate)
    else:
        resp["message"] = "Could not find node %s-%s-%s" % (organisation, sitename, station)

    return HttpResponse(simplejson.dumps(resp))
    
def get_node_clients(request, *args):
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
       
       Returns a dictionary with 'complete' and 'incomplete' keys, whose values are
       dicts keyed on runid.
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
                
                if not check_run_sample_file_exists(rs.id):
                    abspath, relpath = rs.filepaths()
                    if target_dict.has_key(rs.filename):
                        logger.warning( 'Duplicate filename detected for %s' % (rs.filename.encode('utf-8')))
                    if not(target_dict.has_key(run.id)):
                        target_dict[run.id] = {}
                    target_dict[run.id][rs.filename] = [run.id, rs.id, relpath, os.path.exists(os.path.join(abspath, rs.filename))]

    return {'complete': complete, 'incomplete': incomplete}


def get_nodeclient_details(organisation_name, site_name, station_name):
    nodeclient_details = {}
    error = None
    try:
        nodeclient = NodeClient.objects.get(organisation_name = organisation_name, site_name=site_name, station_name = station_name)
        
        nchost = nodeclient.hostname
        if nchost is not None and len(nchost) > 0:
            nodeclient_details['host'] = str(nchost)
        ncflags = nodeclient.flags
        if ncflags is not None and len(ncflags) > 0:
            nodeclient_details['flags'] = str(ncflags)
        ncuname = nodeclient.username
        if ncuname is not None and len(ncuname) > 0:
            nodeclient_details['username'] = str(ncuname)

        #The rootdir tells the client where on the host filesystem to dump the files
        nodeclient_details['rootdir'] = settings.REPO_FILES_ROOT

        try:
            rulesset = NodeRules.objects.filter(parent_node = nodeclient)
            nodeclient_details['rules'] = [x.__unicode__() for x in rulesset]
        except Exception, e:
            error = '%s, %s' % (error, 'Unable to resolve ruleset: %s' % (str(e)))
    except Exception, e:
        #status = 1
        logger.debug("exception encountered: %s" % (e))
        error = "%s, %s" % (error, 'Unable to resolve end machine to stored NodeClient: %s' % str(e) )

    return error, nodeclient_details


def check_run_sample_file_exists(runsampleid):
    ''' Checks that the file for a given runsampleid is present in the filesystem'''
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

def check_run_sample_files(request):
    ret = {}
    ret['success'] = False
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
                    rs.complete = check_run_sample_file_exists(runsample) 
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

    #Update the clientstate. The client may have sent a file tree, which we can use
    #to update our clientstate views
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

def log_upload(request, *args):
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
            logger.warning( 'Unable to send "Log Sent" email: %s' % (str(e)) )

    else:
        logger.warning( 'logupload: No file in the post' )

    return jsonResponse('ok')

def key_upload(request, *args):
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
            logger.warning( 'Unable to send "Key Sent" email: %s' % (str(e)) )
         
    else:
        logger.warning('Keyupload: No file in the post')

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
