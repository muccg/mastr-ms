# Create your views here.
from django.http import HttpResponse
from django.utils import simplejson
from mdatasync_server.models import *
from repository.models import *  
from mdatasync_server.rules import *
from django.conf import settings
import os
import os.path
import posixpath, urllib, mimetypes
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import django.utils.webhelpers as webhelpers


from django.contrib import logging
logger = logging.getLogger('mdatasync_server_log')
logger.setLevel(logging.WARNING) #the default

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



class FileList(object):
    def __init__(self, heirarchy):
        self.heirarchy = heirarchy
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
        #print '\nIn checknode, type of currentnode is: ', type(self.currentnode)
        #print '\nIn checknode, currentnode is', self.currentnode 
        
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
        for dir in self.currentnode.keys():
            upperdirname = dir.upper()
            if upperdirname not in ['.', '/']: #don't check the filelist or 'path' entry
                logger.debug('checking dir: %s' % (upperdirname.encode('utf-8')) )
                if upperdirname in filesdict.keys():
                    #set the dir to contain the path, not a node.
                    self.markfound(self.currentnode, dir, filesdict[upperdirname])
                    #rewrite the DB filename to be the supplied one.
                    try:
                        runsampleDBentry =  RunSample.objects.get(id=filesdict[upperdirname][1])
                        runsampleDBentry.filename = dir
                        runsampleDBentry.save()
                    except Exception, e:
                        logger.debug('Exception renaming runsample filename: %s' % (str(e)) )

                    #remove the found entry from the filesdict
                    del filesdict[upperdirname]
                    logger.debug( 'Found dir: Setting %s to %s' % ( dir.encode('utf-8'), self.currentnode[dir].encode('utf-8') ))
                else:
                    #push the dir onto the checknodes.
                    logger.debug('Could not find dir %s, pushing.' % (dir.encode('utf-8')) )
                    self.checknodes.append(self.currentnode[dir])

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

def retrievePathsForFiles(request, *args):
    '''This function is called as a webservice by the datasync client.
       It expects a post var called 'files' which will be a json string
       which represents a heirarchy of directories and files.
    '''
    
    status = 0 #no error
    error = '' #no error
    filesdict = {} 
    rules = []
    #default host is this host.
    host = None 
    defaultHost = request.__dict__['META']['SERVER_NAME'] 
    flags = None
    username = None

    try:
        pfiles = request.POST.get('files', {})
        #pfiles is json for a heirarchy of files and directories
        pfiles = simplejson.loads(pfiles)
        #pfiles is now our heirarchy of file and directory names.
        porganisation = simplejson.loads(request.POST.get('organisation', ''))
        psitename= simplejson.loads(request.POST.get('sitename', ''))
        pstation = simplejson.loads(request.POST.get('stationname', ''))
        
        logger.debug( 'Post var files passed through was: %s' % ( pfiles) )
        logger.debug( 'Post var organisation passed through was: %s' % ( porganisation) )
        logger.debug( 'Post var station passed through was: %s' % ( pstation ) )
        logger.debug( 'Post var sitename passed through was: %s' % ( psitename) )

        #filter by client, node, whatever to 
        #get a list of filenames in the repository run samples table
        #to compare against.
        #for each filename that matches, you use the experiment's ensurepath 
        try:
            nodeclient = NodeClient.objects.get(organisation_name = porganisation, site_name=psitename, station_name = pstation)
            logger.debug( 'Nodeclient found.')
            
            nchost = nodeclient.hostname
            if nchost is not None and len(nchost) > 0:
                host = str(nchost)
            ncflags = nodeclient.flags
            if ncflags is not None and len(ncflags) > 0:
                flags = str(ncflags)
            ncuname = nodeclient.username
            if ncuname is not None and len(ncuname) > 0:
                username = str(ncuname)

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
                #Build a filesdict of all the files for these runsamples
                for rs in runsamples:
                    fname = rs.filename.upper() #Use uppercase filenames as keys.
                    abspath, relpath = rs.filepaths()
                    logger.debug( 'Filename: %s belongs in path %s' % ( fname.encode('utf-8'), abspath.encode('utf-8') ) )
                    if filesdict.has_key(fname):
                        logger.debug( 'Duplicate path detected!!!' )
                        error = "%s, %s" % (error, "Duplicate filename detected for %s" % (fname.encode('utf-8')))
                        status = 2
                    #we use the relative path    
                    filesdict[fname] = [run.id, rs.id, relpath]

        except Exception, e:
            status = 1
            error = "%s, %s" % (error, 'Unable to resolve end machine to stored NodeClient: %s' % str(e) )
        

    except Exception, e:
        status = 1
        error = str(e)

    logger.debug('making filelist obj')
    #So. Make a FileList object out of pfiles.
    fl = FileList(pfiles)
    logger.debug('checking files')
    fl.checkFiles(filesdict)

    #set the default host
    if host is None or len(host) == 0:
        host = defaultHost 

    retval = {'status': status,
             'error' : error,
             'filesdict':pfiles,
             'runsamplesdict' : fl.runsamplesdict,
             'rootdir' : settings.REPO_FILES_ROOT,
             'rules' : rules,
             'host' : host,
             'username': username,
             'flags': flags,
             #'rules' : None 
            }

    logger.debug('RETVAL is %s' % ( retval ) )
    return jsonResponse(retval)

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
        for runid in runsamplefilesdict.keys():
            logger.debug('Checking files from run %s' % str(runid) )
            runsamples = runsamplefilesdict[runid]
            ret['success'] = True 
            ret['description'] = 'Success'
            for runsample in runsamples:
                runsample = int(runsample)
                try:
                    rs = RunSample.objects.get(id = runsample)
                    abssamplepath, relsamplepath = rs.filepaths()
                    complete_filename = os.path.join(abssamplepath, rs.filename)
                    fileexists = os.path.exists(complete_filename)
                    logger.debug( 'Checking file %s:%s' % (complete_filename.encode('utf-8'), fileexists) )
                    # now change the value in the DB
                    logger.debug( 'Changing value in DB')
                    rs.complete = fileexists
                    rs.save()
                except Exception, e:
                    logger.debug('Error: %s' % (e) )
                    ret['success'] = False
                    ret['description'] = "%s, %s" % (ret['description'], str(e)) 
                
    else:
        ret['description'] = "No files given"

    return jsonResponse(ret)

def logUpload(request, *args):
    logger.info('LOGUPLOAD')
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
            e = FixedEmailMessage(subject="MS Datasync Log Upload (%s)" % (fname_prefix), body=body, from_email = RETURN_EMAIL, to = [LOGS_TO_EMAIL])
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

    #Screenshots and logs are in the same dir.
    import os
    fileslist = os.listdir(os.path.join(settings.REPO_FILES_ROOT , 'synclogs') )
    logslist = []
    shotslist = []
    for fname in fileslist:
        print fname
        if fname.endswith('.png'):
            shotslist.append(fname)
        else:    
            logslist.append(fname)

        logslist.sort()
        shotslist.sort()
        currentLogLevel = logger.getEffectiveLevel()
        levelnames = ['Debug', 'Info', 'Warning', 'Critical', 'Fatal']
        levelvalues = [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL, logging.FATAL]
    return render_to_response("utils.mako", {'wh':webhelpers, 'logslist':logslist, 'shotslist':shotslist, 'currentLogLevel':currentLogLevel, 'levelnames':levelnames, 'levelvalues':levelvalues , 'success':success, 'message':message})


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
