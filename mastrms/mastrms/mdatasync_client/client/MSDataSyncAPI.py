#!/usr/bin/env python

#This is the MSDataSync API. This API provides functions to keep a remote set of directories
#synced with a local set.
#It uses rsync to keep the directories in sync, over an SSH tunnel.
#It can be controlled via a GUI or any other means, and can emit log messages back to the control harness.
#
#You can either use a worker thread to get non blocking operation, in which case you
#call startThread and stopThread, or not. Either way will still work, just one will block and the
#other won't.

try: import json as simplejson
except ImportError: import simplejson
import urllib
import os
import time
import os.path
from shutil import rmtree, copytree, copy, move
from shutil import copy2, copytree
import pipes
import tempfile

import Queue
import threading
from subprocess import Popen, PIPE, STDOUT

from identifiers import *
import plogging
outlog = plogging.getLogger('client')
from MainWindow import APPSTATE


def nullFn(*args, **kwargs):
    outlog.debug('null fn')
    pass

from config import CONFIG

class RemoteSyncParams(object):
    def __init__(self, configdict = {}, username="!"):
        self.host = ""
        self.rootdir = ""
        self.flags = []
        self.username = ""
        self.rules = []
        self.fileslist = None

        #pull the configdict into our local class members
        #but only the values we have defined
        try:
            for key in self.__dict__:
                if configdict.has_key(key):
                    setattr(self, key, configdict[key])
        except Exception, e:
            pass

        #Flags are config authoritative
        if self.flags in ['', '!', [] ]: #The config didn't specify anything
            self.flags = ['-rvz']
        else:
            self.flags = self.flags.split(' ') #space separated string from config

        #Username is client authoritative
        if username not in ['', '!']:
            #use passed in value, not json value
            self.username = username

class TransactionVars(object):
    _copiedFiles = {}
    _transferredSamples = {}
    _sampleFileMap = {}
    _samplesverified = False

    def __init__(self):
        self.reset()

    def reset(self):
        self._copiedFiles = {}
        self._transferredSamples = {}
        self._sampleFileMap = {}
        self._samplesverified = False

    @property
    def copied_files(self):
        return self._copiedFiles
    @copied_files.setter
    def copied_files(self, copiedfiles):
        self._copiedFiles = value

    @property
    def transferred_samples(self):
        return self._transferredSamples
    @transferred_samples.setter
    def transferred_samples(self, value):
        self._transferredSamples = value

    @property
    def sample_file_map(self):
        return self._sampleFileMap
    @sample_file_map.setter
    def sample_file_map(self, value):
        self._sampleFileMap = value

    @property
    def samples_verified(self):
        return self._samplesverified

    @samples_verified.setter
    def set_samples_verified(self, value):
        self._samplesverified = value


class MSDataSyncAPI(object):
    def __init__(self, log=None):
        self._tasks = Queue.Queue()
        if log is None:
            self.log = self.defaultLogSink
        else:
            self.log = log

        self._impl = MSDSImpl(self.log, self)
        self.config = CONFIG
        self.useThreading = False #Threading doesn't seem to help at the moment.
                                 #it needs to be enabled and then debugged -
                                 #we are still seeing UI lagging behind worker operations
        self.transactionvars = TransactionVars()

    def defaultLogSink(self, *args, **kwargs):
        pass

    def startThread( self ):
        if hasattr( self, "_thread" ) and self._thread != None:
            return
        self._thread = self.Worker( self._tasks )
        self._thread.start()
        self.useThreading = True
        self.log("Threading is enabled")

    def stopThread( self ):
        if not hasattr( self, "_thread" ) or self._thread == None:
            return
        self._tasks.join()              # block until task queue is empty
        self._thread.die()              # tell the thread to die
        #print 'Flushing with None task'
        self._appendTask(None)          # dummy task to force thread to run
        self._thread.join()             # wait until thread is done
        self._thread = None
        self.useThreading = False
        self.log("Thread is stopped")

    def _appendTask(self, command, command_kwargs={}, callback=None, callback_kwargs={}):
        '''Either uses a thread (if available) or not.
           Obviously one doesn't block, and one does.
           Either way, the callback is called once done.'''
        if hasattr( self, "_thread" ) and self._thread != None:
            self._tasks.put_nowait((command, command_kwargs, callback, callback_kwargs))
        else:
            result = None
            try:
                result = command(**command_kwargs)
            except Exception, e:
                outlog.warning( 'Error running command (nonthreaded): %s' % (str(e)) )
                #print 'command(args, kwargs) was: %s(%s,%s)' % (str(command), str(args), str(kwargs))
                result = None
            if callback != None:
                callback(result, **callback_kwargs)

    def set_progress_state(self, progress, status):
        self.callingWindow.SetProgress(progress)
        self.callingWindow.setState(status)


    def handshakeRsync(self, callingWindow, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        self.callingWindow = callingWindow
        #get the local file list
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')
        self.log("Handshaking with server %s" % (self.config.getValue('synchub')), type=self.log.LOG_NORMAL, thread=self.useThreading)
        postvars = {'files' : simplejson.dumps({}), 'organisation' : simplejson.dumps(organisation), 'sitename' : simplejson.dumps(sitename), 'stationname': simplejson.dumps(station)}
        try:
            f = urllib.urlopen(self.config.getValue('synchub'), urllib.urlencode(postvars))
            jsonret = f.read()
        except Exception, e:
            returnFn(retcode = False, retstring = "Could not connect %s" % (str(e)) )
            return

        outlog.debug( 'Checking response' )
        #now, if something goes wrong interpreting the result, don't panic.
        try:
            d = simplejson.loads(jsonret)
            self.log('Synchub config loaded object is: %s' % simplejson.dumps(d, sort_keys=True, indent=2), type=self.log.LOG_NORMAL, thread=self.useThreading)
        except Exception, e:
            returnFn(retcode=False, retstring="Error: %s\nUnexpected response from server was: %s" % (e, jsonret))
            return


        #I want to do an rsync -n
        rsyncconfig = RemoteSyncParams(username=self.config.getValue('user'))
        #Lets get any of the remote params
        rsyncconfig.host = d['host']
        #rootdir
        rsyncconfig.rootdir = ''
        #flags, server is authoratative
        rsyncconfig.flags = ['-n'] #n = dry run

        outlog.info( 'Handshaking' )
        #now rsync the whole thing over
        self._appendTask(self._impl.perform_rsync,
                         { "sourcedir": self.config.getValue("localdir"),
                           "rsyncconfig": rsyncconfig },
                         self.handshakeReturn)

    def ask_server_for_wanted_files(self, returnFn):
        self.callingWindow.setState(APPSTATE.INITIING_SYNC)
        self.callingWindow.SetProgress(100)
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')
        syncvars = {"version": VERSION , "sync_completed": self.config.getValue("syncold") }
        print syncvars
        details = {}
        files = {}

        #PART 1
        #first, tell the server who we are, and get a response
        try:
            sync_baseurl = self.config.getValue('synchub')
            if not sync_baseurl.endswith('/'):
                sync_baseurl = "%s/" % (sync_baseurl)
            f = urllib.urlopen("%srequestsync/%s/%s/%s/" % (self.config.getValue('synchub'), organisation, sitename, station), urllib.urlencode(syncvars))
            jsonresp = f.read()
            jsonret = simplejson.loads( jsonresp )
            #if there is an error, bail out by calling the return function
            if not jsonret["success"]:
                returnFn(retcode = False, retstring = "Sync Initiation failed: %s" % (jsonret["msg"]))
            else:
                details = jsonret["details"]
                files = jsonret["files"]
        except Exception, e:
            returnFn(retcode = False, retstring = "Could not initiate Sync %s" % (str(e)) )


        #otherwise return the files
        return details, files

    def find_wanted_files(self, wantedfiles, returnFn):
        self.callingWindow.setState(APPSTATE.CHECKING_FILES)
        self.callingWindow.SetProgress(0)
        #if something goes wrong, bail out by calling the return function
        #otherwise return the local file list
        localfilesdict = self.getFiles(self.config.getValue('localdir'), ignoredirs=[self.config.getLocalIndexPath()] )
        localindexdir = self.config.getLocalIndexPath()
        #see if we can resolve all wanted files:
        foundfiles = {}
        runsamplesdict = {}
        samplefilemap = {}
        for wantedfile in wantedfiles.keys():
            result = self.find_local_file_or_directory(localfilesdict, wantedfile, exclude=['TEMP'])
            if result is not None:
                wantedrecord = wantedfiles[wantedfile]
                run_id = wantedrecord[0]
                sample_id = wantedrecord[1]
                relpath = wantedrecord[2]
                foundfiles[result] = os.path.join(localindexdir, relpath, wantedfile)
                print "Foundfiles[%s] = %s" % (result, foundfiles[result])
                if not runsamplesdict.has_key(run_id):
                    runsamplesdict[run_id] = []
                runsamplesdict[run_id].append(sample_id)
                if not samplefilemap.has_key(run_id):
                    samplefilemap[run_id] = {}
                samplefilemap[run_id][sample_id] = result #original file mapped to run:sample
        return foundfiles, runsamplesdict, samplefilemap

    def post_sync_step(self, server_reponse, filename_id_map):
        if self.config.getValue('archivesynced'):
            self._appendTask(self.archive_synced_files,
                             { "synced_samples_dict":
                                   server_reponse['synced_samples'],
                               "filename_id_map": filename_id_map })

        self._appendTask(self.cleanup_localindexdir)

    def archive_synced_files(self, synced_samples_dict, filename_id_map):
        if len(synced_samples_dict) > 0:
            # invert the filename -> id map and make ids strings
            filename_id_map = dict((tuple(map(str, v)), k)
                                   for (k, v) in filename_id_map.items())

            # Build list of (run_id, sample_id) pairs
            id_keys = []
            for run_id, sample_ids in synced_samples_dict.iteritems():
                for sample_id in sample_ids:
                    id_keys.append((str(run_id), str(sample_id)))

            # filenames from sample ids
            filenames = [filename_id_map[id_key] for id_key in id_keys
                         if id_key in filename_id_map]

            # Do the copy
            self.log("Archiving %d/%d synced files" % (len(filenames), len(id_keys)), thread=self.useThreading)
            for filename in filenames:
                self.archive_file(filename)
            self.log("Archive complete.", thread=self.useThreading)
        else:
            self.log("Nothing to archive.", thread=self.useThreading)

    def archive_file(self, filepath):
        "Move a file from config.localindexdir to config.archivedfilesdir."
        localindexdir = self.config.getLocalIndexPath()
        archivedfilesdir = self.config.getValue('archivedfilesdir')

        src = os.path.join(localindexdir, filepath)
        dst = os.path.join(archivedfilesdir, filepath)

        self.log("Move %s -> %s" % (src, dst), thread=self.useThreading)

        try:
            os.makedirs(os.path.dirname(dst))
        except OSError:
            pass # directory probably already exists

        try:
            move(src, dst)
        except IOError, e:
            self.log("Could not archive file: %s" % str(e),
                     thread=self.useThreading)

    def cleanup_localindexdir(self):
        localindexdir = self.config.getLocalIndexPath()
        if os.path.exists(localindexdir):
            self.log("Clearing local index directory: %s" % localindexdir, thread=self.useThreading)
            try:
                rmtree(localindexdir)
            except Exception, e:
                self.log("Could not clear local index dir: %s" % e,
                         type=self.log.LOG_WARNING, thread=self.useThreading)

    #Actual API methods that DO something
    def checkRsync(self, callingWindow, statuschange, notused, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        c = self.config.getConfig()
        #get the local file list
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')

        self.callingWindow = callingWindow

        remote_params, wantedfiles = self.ask_server_for_wanted_files(returnFn)
        self.transactionvars.reset()

        #localfilesdict is our map between local files that were found that the server wants,
        #and the file path that should exist on the remote end (and relative to our localindexdir)
        #runsamplesdict is just the list of found file sampleids, keyed on runid
        localfilesdict, runsamplesdict, samplefilemap = self.find_wanted_files(wantedfiles, returnFn)
        self.transactionvars.sample_file_map = samplefilemap
        rsyncconfig = RemoteSyncParams(configdict = remote_params, username=self.config.getValue('user'))

        def wanted_filename((name, attrlist)):
            "Returns a tuple of (filename, (run_id, sample_id))"
            return (os.path.join(attrlist[2], name), (attrlist[0], attrlist[1]))

        filename_id_map = dict(map(wanted_filename, wantedfiles.items()))
        rsyncconfig.fileslist = sorted(filename_id_map.keys())

        self.log('Server expects sync of %d files' % len(wantedfiles))
        self.log('Client found %d/%d files' % (len(localfilesdict), len(wantedfiles)))

        self.log("Server wants these files:\n%s" % "\n".join(rsyncconfig.fileslist),
                 type=self.log.LOG_DEBUG)

        #copy all the files
        self._appendTask(self._impl.copyfiles,
                         { "copydict": localfilesdict },
                         self.copyFilesReturn)

        if localfilesdict:
            # rsync the whole thing over
            self._appendTask(self._impl.perform_rsync,
                             { "sourcedir": self.config.getLocalIndexPath(),
                               "rsyncconfig": rsyncconfig },
                             self.rsyncReturn,
                             { "rsyncconfig": rsyncconfig,
                               "returnFn": returnFn,
                               "filename_id_map": filename_id_map })
        else:
            self.log("No files to sync.", thread = self.useThreading)
            self.set_progress_state(100, APPSTATE.IDLE)

    def defaultReturn(self, *args, **kwargs):
        #print 'rsync returned: ', retval
        self.log('Default return callback: args=%s, kwargs=%s' % (str(args), str(kwargs)), Debug=True, thread = self.useThreading)

    def copyFilesReturn(self, *args, **kwargs):
        self.log('Local file copy stage complete', thread = self.useThreading)
        #about to do the rsync. Set the progress state
        self.set_progress_state(50, APPSTATE.UPLOADING_DATA)
        outlog.debug("Finished copying")

    def rsyncReturn(self, success, rsyncconfig, returnFn, filename_id_map):
        "After rsync is finished, request the server to update samples."
        self.log('Remote transfer stage complete', thread = self.useThreading)
        self.set_progress_state(90, APPSTATE.CONFIRMING_TRANSFER)

        # It's difficult to know when a complete sample is
        # transferred. So we consider a sample file to be complete
        # when the *second time* it is rsynced across, the file is not
        # updated.
        runsampledict = {}
        for filename, updated in rsyncconfig.file_changes.iteritems():
            if not updated and filename in filename_id_map:
                run_id, sample_id = filename_id_map[filename]
                runsampledict.setdefault(run_id, []).append(sample_id)

        #now tell the server to check the files off
        baseurl =  self.config.getValue('synchub')
        self._appendTask(self._impl.serverCheckRunSampleFiles,
                         { "runsampledict": runsampledict,
                           "filename_id_map": filename_id_map,
                           "baseurl": baseurl },
                         returnFn)

    def handshakeReturn(self, success):
        self.log('Handshake complete', thread = self.useThreading)
        self.set_progress_state(100, APPSTATE.IDLE)

    def getFiles(self, dir, ignoredirs = []):
        '''returns a dictionary like structure representing the
           files. Like this:
           { '.' : [list of filenames],
             '..' : 'path to this dir'
             'dirname' : {dict like this one},
             'dirname2' : {dict like this one},
           }
        '''

        retfiles = {}
        retfiles['/'] = dir
        retfiles['.'] = {}
        for root, dirs, files in os.walk(dir):
            shouldignore = False
            for ignoredir in ignoredirs:
                if root.startswith(ignoredir):
                    shouldignore = True
                    break

            if shouldignore:
                #print 'did an ignore of: ', root, dirs, files
                continue #go to the next iteration of the loop

            #get the current 'node' of the dict for this level
            path = root.split(dir)[1].split(os.sep)
            node = retfiles
            for p in path:
                if len(p):
                    node = node[p]

            #don't create ignored dirs..
            for dirname in dirs:
                if not node.has_key(dirname) and os.path.join(root, dirname) not in ignoredirs:
                    outlog.debug( 'creating dirname: %s' % ( dirname.encode('utf-8') ) )
                    node[dirname] = {}
                    node[dirname]['.'] = {}
                    node[dirname]['/'] = os.path.join(root, dirname)

            for file in files:
                #print 'setting filename %s to None' % (file.encode('utf-8'))
                node['.'][file] = None

        #print 'retfiles is: ', unicode(retfiles).encode('utf-8')
        return retfiles

    def find_local_file_or_directory(self, localfiledict, filename, exclude=[]):
        ''' does a depth first search of the localfiledict.
            will return the local path to the file/directory if found, or None.
            The filename comparison is non case sensitive '''

        def should_exclude(objectname):
            will_exclude = False
            for excludestring in exclude:
                if objectname.upper().startswith(excludestring.upper()):
                    will_exclude = True
            return will_exclude

        def checkfilesatnode(node, filename):
            #print "Node:", node
            #print

            #check against files.
            if node.has_key('.'):
                for fname in node['.']:
                    #print "Checking file ", fname
                    if fname.upper() == filename.upper():
                        if not should_exclude(filename):
                            return os.path.join(node['/'], fname)

            #check against dirs
            for dname in node.keys():
                if dname not in ['.', '/']:
                    #print 'checking dir ', dname
                    if dname.upper() == filename.upper():
                        #for dirs, their correct path will be in their node:
                        found_exclude = False
                        for fname in node[dname]['.']:
                            if should_exclude(fname):
                                found_exclude = True
                        if not found_exclude:
                            return node[dname]['/']
                    else:
                        #descend into the dir
                        found =  checkfilesatnode(node[dname], filename)
                        if found is not None:
                            return found


            #no directories to descend into?
            #and you got this far?
            #then return None.
            return None

        return checkfilesatnode(localfiledict, filename)

    #------- WORKER CLASS-----------------------
    class Worker( threading.Thread ):
        SLEEP_TIME = 0.1

        #-----------------------------------------------------------------------
        def __init__( self, tasks ):
            threading.Thread.__init__( self )
            self._isDying = False
            self._tasks = tasks

        #-----------------------------------------------------------------------
        def run( self ):
            while not self._isDying:
                (command, command_kwargs, callback, callback_kwargs) = self._tasks.get()
                if command is None:
                    continue
                result = None
                try:
                    #print 'worker thread executing %s with args %s' % (str(command), str(command_kwargs))
                    result = command(**command_kwargs)
                except Exception, e:
                    outlog.warning( 'Error running command (threaded): %s' % ( str(e) ) )
                    #print 'command(kwargs) was: %s(%s,%s)' % (str(command), str(command_kwargs))

                    result = None
                if callback != None:
                    callback(result, **callback_kwargs)
                self._tasks.task_done()

        #-----------------------------------------------------------------------
        def die( self ):
            self._isDying = True


class MSDSImpl(object):
    '''the implementation of the MSDataSyncAPI'''
    def __init__(self, log, controller):
       self.log = log #we expect 'log' to be a callable function.
       self.controller = controller
       self.lastError = ""

    def perform_rsync(self, sourcedir, rsyncconfig):
        outlog.debug('checkRsync implementation entered!')

        #fix the sourcedir.
        #On windows, the driveletter and colon make rsync think
        #that it is a host:path pair. So on windows, we need to fix that.
        #What we do is find the drive letter, get rid of the colon, and then prefix
        #the sourcedir name with /cygdrive
        #we also make sure the path is 'normalised', so that they look like posix paths,
        #since both mac, linux, and cygwin all use it.
        if self.controller.isMSWINDOWS:
            #print 'WINDOWS SOURCE DIR HACK IN PROGRESS'
            #os.path.normpath makes sure slashes are native - on windows this is an escaped backslash \\
            #os.sep gives you the dir sepator for this platform (windows = \\)
            #os.path.splitdrive splits the path into drive,path : ('c:', '\something\\somethingelse')
            drive,winpath = os.path.splitdrive(os.path.normpath(sourcedir))
            drive = str(drive)
            outlog.debug('drive is %s' % (drive) )

            outlog.debug('winpath is %s' % (winpath) )
            #so for the winpath, we replace all \\ and then \ with /
            winpath=winpath.replace(os.sep, '/')
            winpath=winpath.replace('\\', '/')
            #then we take the drive letter (drive[0]) and put it after /cygdrive
            cygpath = "/%s/%s%s/" % ('cygdrive', drive[0], winpath)
            outlog.debug('cygpath is: %s' % ( cygpath ) )
            sourcedir = cygpath

        else:
            sourcedir += '/' #make sure it ends in a slash

        logfile = CONFIG.getValue('logfile').replace('\\', '/') #if its a windows path, convert it. cwrsync wants posix paths ALWAYS
        #Popen('rsync -t %s %s:%s' % (sourcedir, remotehost, remotedir) )
        print 'flags:', rsyncconfig.flags
        #cmdhead = ['rsync', '-tavz'] #t, i=itemize-changes,a=archive,v=verbose,z=zip
        cmdhead = ['rsync']
        cmdhead.extend(rsyncconfig.flags)
        cmdtail = ['--log-file=%s' % (logfile), str(sourcedir), '%s@%s:%s' % ((rsyncconfig.username), str(rsyncconfig.host), str(rsyncconfig.rootdir) )]

        cmd = []
        cmd.extend(cmdhead)

        #self.log('Rules is %s' %(str(rules)) )
        rules = rsyncconfig.rules
        if rules is not None and len(rules) > 0:
            for r in rules:
                if r is not None:
                    cmd.append(r)

        cmd.extend(cmdtail)

        files_list = tempfile.NamedTemporaryFile()

        if rsyncconfig.fileslist is not None:
            files_list.write("\0".join(sorted(rsyncconfig.fileslist)))
            files_list.flush()
            cmd.extend(["--include-from", files_list.name, "--from0"])

        cmd.extend(["--itemize-changes"] * 2)

        self.log('Rsync command is: %s' % " ".join(map(pipes.quote, cmd)),
                 thread=self.controller.useThreading, type=self.log.LOG_DEBUG)

        p = Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE,
                  universal_newlines=True)

        (stdoutdata, stderrdata) = p.communicate()
        self.lastError = stderrdata

        self.log("rsync output is:\n%s" % stdoutdata,
                 thread=self.controller.useThreading, type=self.log.LOG_DEBUG)

        rsyncconfig.file_changes = self.parse_rsync_changes(stdoutdata)

        if len(stderrdata) > 0:
            self.log('Error Rsyncing: %s' % (str(stderrdata),), type=self.log.LOG_ERROR, thread = self.controller.useThreading)

        return p.returncode == 0

    def parse_rsync_changes(self, data):
        """
        The rsync --itemize-changes option produces data on which
        files changed during transfer. This function parses the output
        and returns a map of filename -> bool indicating which files
        changed during rsync.
        """
        def parse_line(line):
            # See rsync(1) for information on the %i format
            split = 11
            code = line[:split]
            filename = line[split+1:]
            if len(code) == split:
                ischanged = lambda c: c not in (".", " ")
                changed = code[0] == "<" and (ischanged(code[2]) or ischanged(code[3]))
                return (code[1] == "d", strip_trailing_slash(filename), changed)
            else:
                return None

        def strip_trailing_slash(path):
            return path.rstrip("/")

        def changes_dict(change_list):
            """
            Convert [(isdir, filename, changed)] to a dict mapping
            filename -> changed. If files are changed within a
            directory, then it is also marked as changed.
            """
            changes = {}
            for isdir, filename, changed in change_list:
                if changed:
                    # mark filename as changed and propagate this up
                    # the directory tree
                    parent = filename
                    while parent:
                        changes[parent] = True
                        parent = os.path.split(parent)[0]
                else:
                    changes.setdefault(filename, False)
            return changes

        change_list = filter(bool, map(parse_line, data.split("\n")))
        return changes_dict(change_list)

    def serverCheckRunSampleFiles(self, runsampledict, filename_id_map, baseurl):
        self.log('Informing the server of transfer: %s' % (runsampledict), thread = self.controller.useThreading)

        postvars = {
            'runsamplefiles' : simplejson.dumps(runsampledict),
            'lastError': self.lastError,
            'organisation': self.controller.config.getValue('organisation'),
            'sitename': self.controller.config.getValue('sitename'),
            'stationname': self.controller.config.getValue('stationname'),
            }
        outlog.debug("Postvars: %s " % (str(postvars)) )
        url = "%s%s/" % (baseurl, "checksamplefiles")
        try:
            f = urllib.urlopen(url, urllib.urlencode(postvars))
            jsonret = f.read()
            self.log('Server returned %s' % (str(jsonret)), thread = self.controller.useThreading)
            self.log('Finished informing the server of transfer', thread = self.controller.useThreading)
            self.controller.post_sync_step(simplejson.loads(jsonret), filename_id_map)
        except Exception, e:
            self.log('Could not connect to %s: %s' % (url, str(e)), type=self.log.LOG_ERROR, thread = self.controller.useThreading)


    def copyfiles(self, copydict):
        '''Takes a dict keyed on source filename, and copies each one to the dest filename (value) '''
        outlog.debug("Entered copy procedure")

        copiedfiles = {}

        try:
            for filename in copydict.keys():
                self.log( '\tCopying %s to %s' % (os.path.normpath(filename), os.path.normpath(copydict[filename] ) ), thread=self.controller.useThreading  )
                src = os.path.normpath(filename)
                dst = os.path.normpath(copydict[filename])
                self.copyfile( src, dst)
                copiedfiles[src] = dst
        except Exception, e:
            self.log('Problem copying: %s' % (str(e)), type=self.log.LOG_ERROR,  thread = self.controller.useThreading )

        self.controller.transactionvars.copied_files = copiedfiles

    def copyfile(self, src, dst):
        import os.path
        try:
            if os.path.isdir(src) and not os.path.exists(dst):
                copytree(src, dst)
            else:
                thepath = str(os.path.dirname(dst))
                if not os.path.exists(thepath):
                    self.log('Path %s did not exist - creating' % (thepath,) , thread = self.controller.useThreading )
                    os.makedirs(thepath)
                copy2(src, dst)
        except Exception, e:
            self.log('Error copying %s to %s : %s' % (src, dst, e), type = self.log.LOG_ERROR,  thread = self.controller.useThreading )

    def getFileTree(self, directory):
        allfiles = []
        try:
            for root, dirs, files in os.walk(directory): #topdown=True, onerror=None, followlinks=False
                for f in files:
                    allfiles.append(os.path.join(root, f))
                #self.log('root: %s' % (str(root)) )
                #self.log('dirs: %s' % (str(dirs)) )
                #self.log('files: %s' % (str(files)) )
            for f in allfiles:
                self.log('File: %s' % (str(f)), thread = self.controller.useThreading )
        except Exception, e:
            self.log('getFileTree: Exception: %s' % (str(e)), self.log.LOG_ERROR, thread = self.controller.useThreading)
        return allfiles
