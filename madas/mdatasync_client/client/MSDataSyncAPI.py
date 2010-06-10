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

def nullFn(*args, **kwargs):
    print 'null fn'
    pass

MSDSCheckFn = nullFn 

from config import MSDSConfig
class MSDataSyncAPI(object):
    def __init__(self, log=None):
        import Queue
        self._tasks = Queue.Queue() 
        if log is None:
            self.log = self.defaultLogSink
        else:
            self.log = log
        
        self._impl = MSDSImpl(self.log, self) 
        self.config = MSDSConfig()
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
        self._appendTask( None, None )  # dummy task to force thread to run
        self._thread.join()             # wait until thread is done
        self._thread = None
        self.useThreading = False

    def _appendTask( self, callback, command, *args, **kwargs ):
        '''Either uses a thread (if available) or not.
           Obviously one doesn't block, and one does.
           Either way, the callback is called once done.'''
        if hasattr( self, "_thread" ) and self._thread != None:
            print 'Using thread'
            self._tasks.put_nowait( ( callback, command, args, kwargs ) )
        else:
            result = None
            try:
                result = command( *args, **kwargs )
            except Exception, e:
                print 'Error running command: ', e
                result = None
            if callback != None:
                callback( result )

    #Actual API methods that DO something
    def checkRsync(self, callingWindow, statuschange, notused, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        c = self.config.getConfig()

        #get the local file list
        #TODO: Call this in the correct manner, using 'Tasks'
        organisation = self.config.getValue('organisation')
        station = self.config.getValue('stationname')
        sitename = self.config.getValue('sitename')

        import urllib
        import simplejson
       
        #grab all files in our local dir:

        localdir = self.config.getValue('localdir')
        filesdict = self.getFiles(localdir)
        localindexdir = self.config.getLocalIndexPath() 
        
        postvars = {'files' : simplejson.dumps(filesdict.keys()), 'organisation' : simplejson.dumps(organisation), 'sitename' : simplejson.dumps(sitename), 'stationname': simplejson.dumps(station)}
        try:
            f = urllib.urlopen(self.config.getValue('synchub'), urllib.urlencode(postvars))
            jsonret = f.read()
        except Exception, e:
            returnFn(retcode = False, retstring = "Could not connect %s" % (str(e)) )
            return

        #self.log('Synchub config: %s' % jsonret)
        j = simplejson.loads(jsonret)
        self.log('Synchub config loaded object is: %s' % j)
        d = simplejson.loads(jsonret)
        print 'Returned Json Obj: ', d
        
        user = self.config.getValue('user')
        #remotehost = self.config.getValue('remotehost')
        #remotedir = self.config.getValue('remotedir')
        remotehost = d['host']
        remotefilesdict = d['filesdict']

        callingWindow.setState(statuschange)
        import os.path
        for filename in remotefilesdict.keys():
            fulllocalpath = os.path.join(filesdict[filename], filename)
            fullremotepath = os.path.join(remotefilesdict[filename], filename)
            self.log( 'Copying %s to %s' % (fulllocalpath, "%s%s" %(localindexdir, fullremotepath) ) )
            self._appendTask(returnFn, self._impl.copyfile, fulllocalpath, "%s%s" % (localindexdir, fullremotepath)) #this could potentially result in not the right path
            
        #now rsync the whole thing over
        self._appendTask(returnFn, self._impl.checkRsync, "%s/" % (localindexdir) , user, j['host'], '/', rules=[j['rules']])

    def defaultReturn(self, *args, **kwargs):
        #print 'rsync returned: ', retval
        self.log('Default return callback:%s' % (str(args)), Debug=True)


    def getFiles(self, dir):
        import os
        retfiles = {}
        for root, dirs, files in os.walk(dir):
            #print files
            for file in files:
                if retfiles.has_key(file):
                    print 'DUPLICATE FILE DETECTED!!: %s' % (file)
                retfiles[file] = root
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
                    print 'worker thread executing %s with args %s' % (str(command), str(args))
                    result = command( *args )
                except Exception, e:
                    print 'Error running command: ', e
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
    def checkRsync(self, sourcedir, remoteuser, remotehost, remotedir, rules = []):
        #self.log('checkRsync implementation entered!', Debug=True)
        
        from subprocess import Popen, PIPE, STDOUT
        logfile = 'rsync_log.txt'
        #Popen('rsync -t %s %s:%s' % (sourcedir, remotehost, remotedir) )
        
        cmdhead = ['rsync', '-tavz'] #t, i=itemize-changes,a=archive,v=verbose,z=zip
        cmdtail = ['--log-file=%s' % (logfile), sourcedir, '%s@%s:%s' % (remoteuser, remotehost, remotedir)]

        cmd = []
        cmd.extend(cmdhead)
    
        #self.log('Rules is %s' %(str(rules)) )
        
        if rules is not None and len(rules) > 0:
            for r in rules:
                if r is not None:
                    cmd.extend(r)
            
        cmd.extend(cmdtail)

        print 'cmd is %s ' % str(cmd)
        #self.log('cmd is %s ' % str(cmd), thread=self.controller.useThreading)

        p = Popen( cmd, shell=False, stdout=PIPE, stderr=PIPE)
        
        #for line in p.stdout:
        #    self.log(line, thread=self.controller.useThreading)
        
        ##p = Popen( cmd,
        ##           stdout=self.log, stderr=self.log, stdin=PIPE)
        
        ##p = Popen( cmd,
        ##           stdout=self.log, stderr=self.log, stdin=PIPE)


        retcode = p.communicate()[0]
        #self.log('the retcode was: %s' % (str(retcode),), Debug=True)
        return retcode

    def copyfile(self, src, dst):
        from shutil import copy2
        import os.path
        print src
        print dst
        
        thepath = os.path.dirname(dst)
        print 'copyfile: %s to %s, path is %s' % (src, dst, thepath)
        try:
            if not os.path.exists(thepath):
                print 'path %s did not exist - creating' % (thepath,)
                os.makedirs(thepath)

            copy2(src, dst)
        except Exception, e:
            print 'Error copying %s to %s : %s' % (src, dst, e)

    def getFileTree(self, dir):
        print 'Entered getFileTree: checking %s' % dir
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
                self.log('File: %s' % (f), thread = self.controller.useThreading )
        except Exception, e:
            print 'Exception: %s' % (str(e))
        print 'Done with getFileTree'
        return allfiles
