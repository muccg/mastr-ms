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
    logger.debug('ensuring repo path %s' % (relpath) )
    #the input should be a relative path.
    #if it does start with a /, check to see if it is the REPO_FILES_ROOT and chop that out.
    #otherwise chop off the leading /
    if relpath.startswith(os.sep):
        if relpath.startswith(settings.REPO_FILES_ROOT):
            relpath = os.path.relpath(relpath, settings.REPO_FILES_ROOT)
        else:
            relpath = os.path.normpath(relpath).split(os.sep, 1)[1] #chop off leading /

    abspath = os.path.join(settings.REPO_FILES_ROOT, relpath)
    try:
        if not os.path.exists(abspath):
            logger.debug('creating directory: %s' % ( abspath ) )
            os.makedirs(abspath)

        try:
            set_repo_file_ownerships(abspath, ownerid=ownerid, groupname=groupname)
        except Exception, perm_e:
            logger.critical('Unable to set permissions/ownership for %s: %s' % (abspath, perm_e) )
            #we don't re-raise
    except Exception, e:
        logger.critical('Exception in ensure_repo_filestore_dir_with_owner: %s' % (e))
        raise

def set_repo_file_ownerships(filepath, ownerid=os.getuid(), groupname=settings.CHMOD_GROUP):
    groupinfo = grp.getgrnam(groupname)
    gid = groupinfo.gr_gid
    os.chmod(filepath, stat.S_IRWXU|stat.S_IRWXG)
    os.chown(filepath, ownerid, gid)


