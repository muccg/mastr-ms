from fabric.api import env
from ccgfab.base import *

env.app_root = '/usr/local/python/ccgapps/'
env.app_name = 'madas'
env.app_install_names = ['madas'] # use app_name or list of names for each install
env.vc = 'svn'
env.git_trunk_url = ""
env.svn_trunk_url = "svn+ssh://store.localdomain/store/techsvn/ccg/madas/trunk/"
env.svn_tags_url = "svn+ssh://store.localdomain/store/techsvn/ccg/madas/tags/"

env.writeable_dirs.extend([]) # add directories you wish to have created and made writeable
env.content_excludes.extend([]) # add quoted patterns here for extra rsync excludes
env.content_includes.extend([]) # add quoted patterns here for extra rsync includes
env.auto_confirm_purge = False #controls whether the confirmation prompt for purge is used

def deploy(auto_confirm_purge = False):
    """
    Make a user deployment
    """
    env.auto_confirm_purge = auto_confirm_purge
    _ccg_deploy_user()

def snapshot(auto_confirm_purge=False):
    """
    Make a snapshot deployment
    """
    env.auto_confirm_purge=auto_confirm_purge
    _ccg_deploy_snapshot()

def release(auto_confirm_purge=False):
    """
    Make a release deployment
    """
    env.auto_confirm=auto_confirm_purge
    _ccg_deploy_release()

def testrelease(auto_confirm_purge=False):
    """
    Make a release deployment using the dev settings file
    """
    env.auto_confirm=auto_confirm_purge
    _ccg_deploy_release(devrelease=True)

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
