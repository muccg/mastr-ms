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

def deploy():
    ccg_deploy_user()

def snapshot():
    ccg_deploy_snapshot()

def release():
    ccg_deploy_release()

def testrelease():
    ccg_deploy_release(devrelease=True)

def purge():
    ccg_purge_user()

def purge_snapshot():
    ccg_purge_snapshot()
