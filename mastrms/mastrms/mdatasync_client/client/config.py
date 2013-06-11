import sys, os, string, time, cPickle
import os.path
from identifiers import *
SAVEFILE_NAME = os.path.join(DATADIR, 'settings.cfg')
import plogging
outlog = plogging.getLogger('client')


class MSDSConfig(object):
    def __init__(self, **kwargs):
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
                   'updateurl' : ['http://repo.ccgapps.com.au/ma/', 'Program Update URL', 'The web address of the server that should be contacted for program updates'],
                   'logfile'  : [os.path.join(DATADIR, 'rsync_log.txt'), 'Local Log File', 'Sync operations are logged to this file'],
                   'loglevel' : [plogging.get_level('client'), "Log Level", "The log level of the client"],
                   'syncfreq' : [30, 'Sync Frequency (Mins)', 'How often the application should push updates to the server'],
                   'localindexdir' : ['.local_index', 'Local Index Directory', 'Temporary storage area for data transfer'],
                   'syncold' : [False, 'Sync Completed', 'When checked, includes already completed run data for transfer'],
                   'archivesynced' : [False, 'Archive Synced Files', 'When checked, archives a copy of synced files to the specified directory.'],
                   'archivedfilesdir' : ["Choose a directory", 'Archived Files Dir', 'If archiving is enabled, synced files will be archived to this directory.'],
            }
        self.filename = None
        self.update(kwargs)

    def getConfig(self):
        return self.store

    def getNodeName(self):
        return "%s.%s.%s" % (self.getValue('organisation'), self.getValue('sitename'), self.getValue('stationname'))

    def save(self, *args):
        if not self.filename:
            return False

        try:
            with open(self.filename, "wb") as fo:
                cPickle.dump(self.store, fo, protocol = cPickle.HIGHEST_PROTOCOL)
        except EnvironmentError, e:
            return False

        return True

    @classmethod
    def load(cls, filename=SAVEFILE_NAME):
        config = cls()
        config.filename = filename

        try:
            with open(filename, "rb") as fo:
                savedstore = cPickle.load(fo)
            config.store.update(savedstore)
        except EnvironmentError:
            outlog.warning('No saved config existed: %s' % (filename))
        except cPickle.UnpicklingError, e:
            outlog.warning('Exception reading saved configuration: %s' % (str(e)) )

        return config

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

    def __getitem__(self, key):
        return self.getValue(key)

    def __setitem__(self, key, value):
        self.setValue(key, value)

    def update(self, attrs):
        for key, value in attrs.iteritems():
            self[key] = value

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

    def __str__(self):
        return "\n".join("%s=%r" % x for x in self.get_key_values())

    def __repr__(self):
        return repr(dict(self.get_key_values()))

    def get_key_values(self):
        for name, schema in self.store.iteritems():
            yield (name, schema[0])
