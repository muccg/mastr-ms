import sys, os, string, time, cPickle
import os.path
from identifiers import *
SAVEFILE_NAME = os.path.join(DATADIR, 'settings.cfg')
import plogging
outlog = plogging.getLogger('client')


#Dont instantiate this directly - use the module singleton defined at the end of this file

class MSDSConfig(object):
    def __init__(self):
        self.store = {}
        '''hardcoded config for the initial object creation'''
        #format is:
        #key: [value, formalKeyName, helpText]
        #e.g.:
        #'user' : ['jsmith', 'Username', 'The username with which to logon to the remote server']
        self.store = { 'user' : ['default_user', 'Username', 'The username with which to logon to the remote server.'],
                 #'remotehost' : ['127.0.0.1', 'Remote Host', 'The address of the remote rsync machine.'],
                 # 'remotedir' : ['syncdir_dest', 'Dest Dir'],
                  'sitename'  : ['defaultsite', 'Site Name', 'A name to identify this installation, e.g. Lab #1.', False],
                  'stationname'  : ['defaultstation', 'Stationname', 'A name to identify this installation, e.g. Lab #1.', False],
              'organisation'  : ['defaultorg',  'Organisation', 'Identifies which organisation your site belongs to. It is important that this is correct.', False],
                   'localdir' : ['syncdir','Data root directory', 'The local root directory for the data.'],
                   'synchub'  : ['https://ccg.murdoch.edu.au/mastrms/sync/', 'SyncHub Address', 'The web address of the synchub server'],
                   'updateurl' : ['http://ccg.murdoch.edu.au/ma/', 'Program Update URL', 'The web address of the server that should be contacted for program updates'],
                   'logfile'  : [os.path.join(DATADIR, 'rsync_log.txt'), 'Local Log File', 'Sync operations are logged to this file'],
                   'loglevel' : [plogging.get_level('client'), "Log Level", "The log level of the client"],
                   'syncfreq' : [30, 'Sync Frequency (Mins)', 'How often the application should push updates to the server'],
                   'localindexdir' : ['.local_index', 'Local Index Directory', 'Temporary storage area for data transfer'],
                   'syncold' : [False, 'Sync Completed', 'When checked, includes already completed run data for transfer'],
                   'archivesynced' : [False, 'Archive Synced Files', 'When checked, archives a copy of synced files to the specified directory.'],
                   'archivedfilesdir' : ["Choose a directory", 'Archived Files Dir', 'If archiving is enabled, synced files will be archived to this directory.'],
            }
        self.load()


    def getConfig(self):
        return self.store

    def getNodeName(self):
        return "%s.%s.%s" % (self.getValue('organisation'), self.getValue('sitename'), self.getValue('stationname'))

    def save(self, *args):
        try:
            fo = open(SAVEFILE_NAME, "wb")
            cPickle.dump(self.store, fo, protocol = cPickle.HIGHEST_PROTOCOL)
            fo.close()
            return True
        except:
            return False

    def load(self):
        retval = False
        fo = None
        try:
            fo = open(SAVEFILE_NAME, "rb")
        except IOError:
            outlog.warning('No saved config existed: %s' % (SAVEFILE_NAME))
        try:
            savedstore = cPickle.load(fo)
            retval = True
        except Exception, e:
            outlog.warning('Exception reading saved configuration: %s' % (str(e)) )


        if retval:
            self.store.update(savedstore)

        if fo is not None:
            fo.close()
        return retval

    def getLocalIndexPath(self):
        return os.path.join(self.getValue('localdir'), self.getValue('localindexdir'))

    def getValue(self, key):
        try:
            return self.store[key][0]
        except Exception, e:
            return str(None)

    def setValue(self, key, value):
        try:
            self.store[key][0] = value
        except:
            pass

    def getFormalName(self, key):
        try:
            return self.store[key][1]
        except Exception, e:
            return str(key)

    def getHelpText(self, key):
        try:
            return self.store[key][2]
        except:
            return self.getFormalName(key)

    def getShowVar(self, key):
        try:
            return self.store[key][3]
        except:
            return True



CONFIG = MSDSConfig()
