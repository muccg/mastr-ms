from fabric.api import env
from ccgfab.base import *

env.app_root = '/usr/local/python/ccgapps/'
env.app_name = 'mastrms'
env.app_install_names = ['mastrms'] # use app_name or list of names for each install
env.vc = 'mercurial'

env.writeable_dirs.extend([]) # add directories you wish to have created and made writeable
env.content_excludes.extend([]) # add quoted patterns here for extra rsync excludes
env.content_includes.extend([]) # add quoted patterns here for extra rsync includes
env.auto_confirm_purge = False #controls whether the confirmation prompt for purge is used

def deploy(auto_confirm_purge = False, migration=True):
    """
    Make a user deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_deploy_user(migration=migration)

def snapshot(auto_confirm_purge=False, migration=True):
    """
    Make a snapshot deployment
    """
    env.auto_confirm_purge=auto_confirm_purge
    _ccg_deploy_snapshot(migration=migration)

def release(*args, **kwargs):
    """
    Make a release deployment
    """
    migration = kwargs.get("migration", True)
    requirements = kwargs.get("requirements", "requirements.txt")
    tag = kwargs.get("tag", None)
    env.ccg_requirements = requirements
    env.auto_confirm=False
    _ccg_deploy_release(tag=tag,migration=migration)

def testrelease(auto_confirm_purge=False, migration=True):
    """
    Make a release deployment using the dev settings file
    """
    env.auto_confirm=auto_confirm_purge
    _ccg_deploy_release(devrelease=True, migration=migration)

def purge(auto_confirm_purge=False):
    """
    Remove the user deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_purge_user()

def purge_snapshot(auto_confirm_purge = False):
    """
    Remove the snapshot deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_purge_snapshot()
