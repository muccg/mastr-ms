#!/usr/bin/env python

#This is the MSDataSync API. This API provides functions to keep a remote set of directories 
#synced with a local set.
#It uses rsync to keep the directories in sync, over an SSH tunnel.
#It can be controlled via a GUI or any other means, and can emit log messages back to the control harness.
#
#You can either use a worker thread to get non blocking operation, in which case you 
#call startThread and stopThread, or not. Either way will still work, just one will block and the 
#other won't.
#
#This makes use of the rsync script by Vivian De Smedt, relased under the BSD license.

try: import json as simplejson
except ImportError: import simplejson
import urllib
import os
import os.path
from identifiers import *
import plogging
outlog = plogging.getLogger('client')


def nullFn(*args, **kwargs):
    outlog.debug('null fn')
    pass

MSDSCheckFn = nullFn 

from config import CONFIG
class MSDataSyncAPI(object):
    def __init__(self, log=None):
        import Queue
        self._tasks = Queue.Queue() 
        if log is None:
            self.log = self.defaultLogSink
        else:
            self.log = log
        
        self._impl = MSDSImpl(self.log, self) 
        self.config = CONFIG 
        self.useThreading = False

    def defaultLogSink(self, *args, **kwargs):
        pass

    def startThread( self ):
        if hasattr( self, "_thread" ) and self._thread != None:
            return
        self._thread = self.Worker( self._tasks )
        self._thread.start()
        self.useThreading = True

    def stopThread( self ):
        if not hasattr( self, "_thread" ) or self._thread == None:
            return
        self._tasks.join()              # block until task queue is empty
        self._thread.die()              # tell the thread to die
        #print 'Flushing with None task'
        self._appendTask( None, None )  # dummy task to force thread to run
        self._thread.join()             # wait until thread is done
        self._thread = None
        self.useThreading = False

    def _appendTask( self, callback, command, *args, **kwargs ):
        '''Either uses a thread (if available) or not.
           Obviously one doesn't block, and one does.
           Either way, the callback is called once done.'''
        if hasattr( self, "_thread" ) and self._thread != None:
            self._tasks.put_nowait( ( callback, command, args, kwargs ) )
        else:
            result = None
            try:
                result = command( *args, **kwargs )
            except Exception, e:
                outlog.warning( 'Error running command (nonthreaded): %s' % (str(e)) )
                #print 'command(args, kwargs) was: %s(%s,%s)' % (str(command), str(args), str(kwargs))
                result = None
            if callback != None:
                callback( result )


    def handshakeRsync(self, callingWindow, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        self.callingWindow = callingWindow
        #get the local file list
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')
        localindexdir = self.config.getLocalIndexPath() 
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
        rsyncconfig = {}
        #Lets get any of the remote params
        rsyncconfig['host'] = d['host']
        #rootdir
        rsyncconfig['rootdir'] = ''
        #flags, server is authoratative
        rsyncconfig['flags'] = ['-n'] #n = dry run
        #User, client is authoratative
        if self.config.getValue('user') in ['!', '']:
            rsyncconfig['user'] = d['username'] #use the server value
        else:
            rsyncconfig['user'] = self.config.getValue('user')
        
        outlog.info( 'Handshaking' )
        #now rsync the whole thing over
        self._appendTask(self.handshakeReturn, self._impl.perform_rsync, "%s" % (localindexdir) , rsyncconfig)

    #Actual API methods that DO something
    def checkRsync(self, callingWindow, statuschange, notused, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        c = self.config.getConfig()

        #get the local file list
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')
       
        #grab all files in our local dir:
        localdir = self.config.getValue('localdir')
        localindexdir = self.config.getLocalIndexPath() 
        filesdict = self.getFiles(localdir, ignoredirs=[localindexdir])
        syncold = self.config.getValue('syncold') 
        self.log("Syncing with server %s" % (self.config.getValue('synchub')), type=self.log.LOG_NORMAL, thread=self.useThreading)
        postvars = {'files' : simplejson.dumps(filesdict), 'organisation' : simplejson.dumps(organisation), 'sitename' : simplejson.dumps(sitename), 'stationname': simplejson.dumps(station), 'syncold': simplejson.dumps(syncold)}
        outlog.debug("Sync request to server. Postvars: %s" % (str(postvars)) )
        try:
            f = urllib.urlopen(self.config.getValue('synchub'), urllib.urlencode(postvars))
            jsonret = f.read()
        except Exception, e:
            returnFn(retcode = False, retstring = "Could not connect %s" % (str(e)) )
            return

        #now, if something goes wrong interpreting the result, don't panic.
        try:
            #self.log('Synchub config: %s' % jsonret)
            d = simplejson.loads(jsonret)
            self.log('Synchub config loaded object is: %s' % simplejson.dumps(d, sort_keys=True, indent=2), type=self.log.LOG_NORMAL, thread=self.useThreading)


            #print 'Returned Json Obj: ', d
        except Exception, e:
            returnFn(retcode=False, retstring="Error: %s\nUnexpected response from server was: %s" % (e, jsonret))
            return

        rsyncconfig = {}
        #Lets get any of the remote params
        rsyncconfig['host'] = d['host']
        #rootdir
        rsyncconfig['rootdir'] = d['rootdir']
        #flags, server is authoratative
        if d['flags'] not in ['', '!'] :
            rsyncconfig['flags'] = d['flags'].split(' ') #split on space
        else:
            rsyncconfig['flags'] = ['-rvz'] #r=recursive v=verbose,z=zip #a=archive (preserves times)
        #User, client is authoratative
        if self.config.getValue('user') in ['!', '']:
            rsyncconfig['user'] = d['username'] #use the server value
        else:
            rsyncconfig['user'] = self.config.getValue('user')
        #rules
        rsyncconfig['rules'] = [d['rules']]

        #Other variables for local analysis before syncing
        remotefilesdict = d['filesdict']
        remoterunsamplesdict = d['runsamplesdict']

        outlog.debug( "remote files dict: %s" % ( unicode(remotefilesdict).encode('utf-8') ) )
        outlog.debug( "remote runsamples dict: %s" % (unicode(remoterunsamplesdict).encode('utf-8') ) )

        callingWindow.setState(statuschange)
        self.callingWindow = callingWindow

        copydict = {} #this is our list of files to copy

        #now we explore the returned heirarchy recursively, and flatten it into a 
        #dict of source:dest's

        def extract_file_target(node, resultdict):
            '''method to recursively extract valid file targets from a nested dict structure
               relies on external scope to contain 'localindexdir' string
            '''
            for filename in node['.'].keys():
                outlog.debug("Checking for %s" % (filename))
                #any keys in . should be valid targets.
                #their full source path will be ['/'] joined with the 'key'.
                #theif full dest path will be the 'value'
                if node['.'][filename] is not None:
                    outlog.debug("Client: adding file")
                    fulllocalpath = os.path.join(node['/'], filename)
                    fullremotepath = os.path.join(node['.'][filename], filename)
                    resultdict[fulllocalpath] = "%s" %(os.path.join(localindexdir, fullremotepath) )
            
            #now for the directories
            for dirname in node.keys():
                if dirname not in ['.', '/']:
                    #if the value is a dict, then this dir needs to be more thouroughly explored
                    if isinstance(node[dirname], dict):
                        outlog.debug("Checking dir %s" % (dirname))
                        extract_file_target(node[dirname], resultdict)
                    else:
                        outlog.debug("Client: adding dir")
                        fulllocalpath = os.path.join(node['/'], dirname)
                        fullremotepath = os.path.join(node[dirname], dirname)
                        resultdict[fulllocalpath] = "%s" %(os.path.join(localindexdir, fullremotepath) )

        extract_file_target(remotefilesdict, copydict)

        if len(copydict.keys()):
        
            self.log("Clearing local index directory")
            try:
                from shutil import rmtree
                rmtree(localindexdir)
            except Exception, e:
                self.log('Could not clear local index dir: %s' % (str(e)), type=self.log.LOG_WARNING, thread=self.useThreading)

            callingWindow.SetProgress(20)
            self.log("Initiating file copy to local index (%d files)" % (len(copydict.keys())) )
            #copy all the files
            self._appendTask(self.copyFilesReturn, self._impl.copyfiles, copydict)
            
            #now rsync the whole thing over
            self._appendTask(self.rsyncReturn, self._impl.perform_rsync, "%s" % (localindexdir) , rsyncconfig)

            #now tell the server to check the files off
            baseurl =  self.config.getValue('synchub')
            self._appendTask(returnFn, self._impl.serverCheckRunSampleFiles, remoterunsamplesdict, baseurl)
        else:
            self.log("No files to sync.", thread = self.useThreading)
            callingWindow.SetProgress(100)
            from MainWindow import APPSTATE
            callingWindow.setState(APPSTATE.IDLE)

    def defaultReturn(self, *args, **kwargs):
        #print 'rsync returned: ', retval
        self.log('Default return callback: args=%s, kwargs=%s' % (str(args), str(kwargs)), Debug=True, thread = self.useThreading)

    def copyFilesReturn(self, *args, **kwargs):
        self.log('Local file copy stage complete', thread = self.useThreading)
        self.callingWindow.SetProgress(50)

    def rsyncReturn(self, *args, **kwargs):
        self.log('Remote transfer stage complete', thread = self.useThreading)
        self.callingWindow.SetProgress(90) 

    def handshakeReturn(self, *args, **kwargs):
        self.log('Handshake complete', thread = self.useThreading)
        self.callingWindow.SetProgress(100)  

    def getFiles(self, dir, ignoredirs = []):
        '''returns a dictionary like structure representing the 
           files. Like this:
           { '.' : [list of filenames],
             '..' : 'path to this dir'
             'dirname' : {dict like this one},
             'dirname2' : {dict like this one},
           }  
        '''

        import os
        retfiles = {}
        retfiles['/'] = dir
        retfiles['.'] = {}
        for root, dirs, files in os.walk(dir):
            #print files
            shouldignore = False
            for ignoredir in ignoredirs:
                if root.startswith(ignoredir):
                    #print 'ignoring ', root.encode('utf-8')
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
    
    #------- WORKER CLASS-----------------------
    import threading
    class Worker( threading.Thread ):
        SLEEP_TIME = 0.1

        #-----------------------------------------------------------------------
        def __init__( self, tasks ):
            import threading
            threading.Thread.__init__( self )
            self._isDying = False
            self._tasks = tasks

        #-----------------------------------------------------------------------
        def run( self ):
            while not self._isDying:
                ( callback, command, args, kwargs ) = self._tasks.get()
                result = None
                try:
                    #print 'worker thread executing %s with args %s' % (str(command), str(args))
                    result = command( *args, **kwargs )
                except Exception, e:
                    outlog.warning( 'Error running command (threaded): %s' % ( str(e) ) )
                    #print 'command(args, kwargs) was: %s(%s,%s)' % (str(command), str(args), str(kwargs))

                    result = None
                if callback != None:
                    callback( result )
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
        #self.log('checkRsync implementation entered!', Debug=True)
      
        #fix the sourcedir.
        #On windows, the driveletter and colon make rsync think 
        #that it is a host:path pair. So on windows, we need to fix that.
        #What we do is find the drive letter, get rid of the colon, and then prefix
        #the sourcedir name with /cygdrive
        #we also make sure the path is 'normalised', so that they look like posix paths,
        #since both mac, linux, and cygwin all use it.
        if self.controller.isMSWINDOWS:
            import os
            import os.path
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
            #print 'NO NEED FOR WINDOWS SOURCE DIR HACK'
            sourcedir += '/' #make sure it ends in a slash

        from subprocess import Popen, PIPE, STDOUT
        logfile = CONFIG.getValue('logfile').replace('\\', '/') #if its a windows path, convert it. cwrsync wants posix paths ALWAYS
        #Popen('rsync -t %s %s:%s' % (sourcedir, remotehost, remotedir) )
        
        #cmdhead = ['rsync', '-tavz'] #t, i=itemize-changes,a=archive,v=verbose,z=zip
        cmdhead = ['rsync']
        cmdhead.extend(rsyncconfig['flags']) 
        cmdtail = ['--log-file=%s' % (logfile), str(sourcedir), '%s@%s:%s' % (str(rsyncconfig['user']), str(rsyncconfig['host']), str(rsyncconfig['rootdir']) )]

        cmd = []
        cmd.extend(cmdhead)
    
        #self.log('Rules is %s' %(str(rules)) )
        rules = rsyncconfig.get('rules', None) 
        if rules is not None and len(rules) > 0:
            for r in rules:
                if r is not None:
                    cmd.extend(r)
            
        cmd.extend(cmdtail)

        self.log('Rsync command is: %s ' % str(cmd), thread=self.controller.useThreading, type=self.log.LOG_DEBUG)
        #self.log('cmd is %s ' % str(cmd), thread=self.controller.useThreading)

        p = Popen( cmd, shell=False, stdout=PIPE, stderr=PIPE)
        
        #for line in p.stdout:
        #    self.log("RSYNC %s: " % (line,), thread=self.controller.useThreading)
        
        (retcode, pstderr) = p.communicate()
        self.lastError = pstderr

        if len(pstderr) > 0:
            self.log('Error Rsyncing: %s' % (str(pstderr),), type=self.log.LOG_ERROR, thread = self.controller.useThreading)
        return retcode

    
    def serverCheckRunSampleFiles(self, runsampledict, baseurl):
        self.log('Informing the server of transfer: %s' % (runsampledict), thread = self.controller.useThreading)
        postvars = {'runsamplefiles' : simplejson.dumps(runsampledict), 'lastError': self.lastError, 'organisation': self.controller.config.getValue('organisation'), 'sitename': self.controller.config.getValue('sitename'), 'stationname': self.controller.config.getValue('stationname') }
        self.log("Postvars: %s " % (str(postvars)) )
        url = "%s%s/" % (baseurl, "checksamplefiles")
        try:
            f = urllib.urlopen(url, urllib.urlencode(postvars))
            jsonret = f.read()
            self.log('Server returned %s' % (str(jsonret)), thread = self.controller.useThreading)
            self.log('Finished informing the server of transfer', thread = self.controller.useThreading)
        except Exception, e:
            self.log('Could not connect to %s: %s' % (url, str(e)), type=self.log.LOG_ERROR, thread = self.controller.useThreading)
        

    def copyfiles(self, copydict):
        '''Takes a dict keyed on source filename, and copies each one to the dest filename (value) '''
        import os.path
        #print 'Copyfiles dict: ', copydict
        try:
            for filename in copydict.keys():
                self.log( '\tCopying %s to %s' % (os.path.normpath(filename), os.path.normpath(copydict[filename] ) ), thread=self.controller.useThreading  )
                #print 'doing copyfile'
                self.copyfile( os.path.normpath(filename), os.path.normpath(copydict[filename]))
        except Exception, e:
            self.log('Problem copying: %s' % (str(e)), type=self.log.LOG_ERROR,  thread = self.controller.useThreading )

    def copyfile(self, src, dst):
        from shutil import copy2, copytree
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

    def getFileTree(self, dir):
        #print 'Entered getFileTree: checking %s' % dir
        import os
        allfiles = []
        try:
            for root, dirs, files in os.walk(dir): #topdown=True, onerror=None, followlinks=False
                for f in files:
                    allfiles.append(os.path.join(root, f))
                #self.log('root: %s' % (str(root)) )
                #self.log('dirs: %s' % (str(dirs)) )
                #self.log('files: %s' % (str(files)) )
            for f in allfiles:
                self.log('File: %s' % (str(f)), thread = self.controller.useThreading )
        except Exception, e:
            self.log('getFileTree: Exception: %s' % (str(e)), self.log.LOG_ERROR, thread = self.controller.useThreading)
        #print 'Done with getFileTree'
        return allfiles
