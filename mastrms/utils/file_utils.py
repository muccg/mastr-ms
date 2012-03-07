import os
import os.path
import stat
import grp
from mastrms import settings
import logging
LOGNAME = 'madas_log'
logger = logging.getLogger(LOGNAME)

def ensure_repo_filestore_dir_with_owner(relpath, ownerid=os.getuid(), groupname=settings.CHMOD_GROUP):
    '''helper function to create directories within the mastrms permanent filestore, with the correct perms''' 
    #the input should be a relative path.
    #if it does start with a /, check to see if it is the REPO_FILES_ROOT and chop that out.
    #otherwise chop off the leading /
    if relpath.startswith(os.sep):
        if relpath.startswith(settings.REPO_FILES_ROOT):
            relpath = os.path.relpath(relpath, settings.REPO_FILES_ROOT)
        else:
            relpath = os.path.normpath(relpath).split(os.sep, 1)[1] #chop off leading / 

    abspath = os.path.join(settings.REPO_FILES_ROOT, relpath)
    if not os.path.exists(abspath):
        logger.debug('creating directory: %s' % ( os.path.dirname(abspath) ) )
        os.makedirs(abspath)
        os.chmod(abspath, stat.S_IRWXU|stat.S_IRWXG)
            
    groupinfo = grp.getgrnam(groupname)
    gid = groupinfo.gr_gid
        
    os.chown(abspath, ownerid, gid)

def set_repo_file_ownerships(filepath, ownerid=os.getuid(), groupname=settings.CHMOD_GROUP):
    groupinfo = grp.getgrnam(groupname)
    gid = groupinfo.gr_gid
    os.chown(filepath, ownerid, gid) 


