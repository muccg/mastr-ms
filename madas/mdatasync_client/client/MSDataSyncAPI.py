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
            self.log = log.WriteText
        self._impl = MSDSImpl(self.log) 
        self.config = MSDSConfig()

    def defaultLogSink(self, *args, **kwargs):
        pass

    def startThread( self ):
        if hasattr( self, "_thread" ) and self._thread != None:
            return
        self._thread = self.Worker( self._tasks )
        self._thread.start()

    def stopThread( self ):
        if not hasattr( self, "_thread" ) or self._thread == None:
            return
        self._tasks.join()              # block until task queue is empty
        self._thread.die()              # tell the thread to die
        self._appendTask( None, None )  # dummy task to force thread to run
        self._thread.join()             # wait until thread is done
        self._thread = None

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
            except:
                result = None
            if callback != None:
                callback( result )

    #Actual API methods that DO something
    def checkRsync(self, sourcedir, remotehost, remotedir, returnFn = None):
        if returnFn is None:
            returnFn = self.defaultReturn
        c = self.config.getConfig()

        #get the local file list
        #TODO: Call this in the correct manner, using 'Tasks'
        files = self.config.getValue('localdir')
        node = self.config.getValue('organisation')
        station = self.config.getValue('sitename')

        import urllib
        import simplejson
        postvars = {'files' : simplejson.dumps(files), 'node' : simplejson.dumps(node), 'station': simplejson.dumps(station)}
        f = urllib.urlopen(self.config.getValue('synchub'), urllib.urlencode(postvars))
        jsonret = f.read()
        self.log('Synchub config: %s' % jsonret)
        j = simplejson.loads(jsonret)
        self.log('Synchub config loaded object is: %s' % j)
        from django.utils import simplejson
        d = simplejson.loads(jsonret)
        print 'Returned Json Obj: ', d
        localdir = self.config.getValue('localdir')
        user = self.config.getValue('user')
        #remotehost = self.config.getValue('remotehost')
        #remotedir = self.config.getValue('remotedir')
        remotehost = d['host']
        remotedir = d['path']
        self._appendTask(returnFn, self._impl.checkRsync, localdir, user, j['host'], j['path'], rules=[j['rules']])

    def defaultReturn(self, *args):
        #print 'rsync returned: ', retval
        self.log('Default return callback:%s' % (str(args)), Debug=True)

class MSDSImpl(object):
    '''the implementation of the MSDataSyncAPI'''
    def __init__(self, log):
       self.log = log #we expect 'log' to be a callable function. 
    
    def checkRsync(self, sourcedir, remoteuser, remotehost, remotedir, rules = []):
        self.log('checkRsync implementation entered!', Debug=True)
        
        
        from subprocess import Popen, PIPE
        logfile = 'rsync_log.txt'
        #Popen('rsync -t %s %s:%s' % (sourcedir, remotehost, remotedir) )
        
        cmdhead = ['rsync', '-tavz']
        cmdtail = ['--log-file=%s' % (logfile), sourcedir, '%s@%s:%s' % (remoteuser, remotehost, remotedir)]

        cmd = []
        cmd.extend(cmdhead)
        cmd.extend(rules)
        cmd.extend(cmdtail)

        print 'cmd is %s' % str(cmd)

        #for rule in rules:
        p = Popen( cmd,
                   stdout=PIPE)


        retcode = p.communicate()[0]
        self.log('the retcode was: %s' % (str(retcode),), Debug=True)
        return retcode

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
                self.log('File: %s' % (f) )
        except Exception, e:
            print 'Exception: %s' % (str(e))
        print 'Done with getFileTree'
        return allfiles
