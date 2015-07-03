import os
import os.path
import stat
import grp
from django.conf import settings
import logging
LOGNAME = 'mastrms.general'
logger = logging.getLogger(LOGNAME)


def ensure_repo_filestore_dir_with_owner(
        relpath,
        ownerid=os.getuid(),
        groupname=settings.CHMOD_GROUP):
    '''helper function to create directories within the mastrms permanent filestore, with the correct perms'''
    logger.debug('ensuring repo path %s' % (relpath))
    # the input should be a relative path.
    # if it does start with a /, check to see if it is the REPO_FILES_ROOT and chop that out.
    # otherwise chop off the leading /
    if relpath.startswith(os.sep):
        if relpath.startswith(settings.REPO_FILES_ROOT):
            relpath = os.path.relpath(relpath, settings.REPO_FILES_ROOT)
        else:
            relpath = os.path.normpath(relpath).split(os.sep, 1)[1]  # chop off leading /

    abspath = os.path.join(settings.REPO_FILES_ROOT, relpath)
    try:
        if not os.path.exists(abspath):
            logger.debug('creating directory: %s' % (abspath))
            os.makedirs(abspath)

        set_repo_file_ownerships(abspath, ownerid=ownerid, groupname=groupname)
    except Exception as e:
        logger.critical('Exception in ensure_repo_filestore_dir_with_owner: %s' % (e))
        raise

    clean_temp_files(abspath)


def set_repo_file_ownerships(filepath, ownerid=os.getuid(), groupname=settings.CHMOD_GROUP):
    try:
        groupinfo = grp.getgrnam(groupname)
    except KeyError:
        logger.critical("Group \"%s\" not found. Check settings.py." % groupname)
        return False

    gid = groupinfo.gr_gid

    try:
        os.chmod(filepath, stat.S_IRWXU | stat.S_IRWXG)
    except OSError as e:
        logger.critical("Unable to set permissions: %s" % str(e))
        return False

    try:
        os.chown(filepath, ownerid, gid)
    except OSError as e:
        logger.critical("Unable to set ownership to uid %s and "
                        "gid %s: %s" % (ownerid, gid, str(e)))
        return False

    return True


def clean_temp_files(repodir):
    """
    Just in case the client happens to upload temp files, get rid of
    them here.
    """
    targets = set(["TEMPBASE", "TEMPDAT", "TEMPDIR"])
    istemp = lambda f: f in targets

    for root, dirs, files in os.walk(repodir):
        for name in filter(istemp, files):
            path = os.path.join(root, name)
            logger.info("Deleting temp file %s" % path)
            try:
                os.remove(path)
            except EnvironmentError as e:
                logger.error(e)
