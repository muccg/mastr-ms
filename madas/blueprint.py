#!/usr/bin/python
import os
import os.path
import sys
import subprocess
import copy

TEMPLATE_TEXT = '''from blueprint import VirtualConfig
###
# This is a template for a config.py to be used with blueprint
# Useful VirtualConfig operations:
# blah = VirtualConfig(configname, base=config_to_derive_from)
# .deps_root = root dir where dependencies are stored
# .deps_dir = dir relative to root to find deps. Default is configname, unless overridden ('' for none)
# .deps_motd_file = file in deps_dir which contains important text to display during install (default DEPENDENCIES)
# .deps_env_file = file in deps dir which contains env to be injected into your virtualenv (default ENVIRONMENT)
# .add_local(common name, file name), 
# .override_local(common name) : adds a local file to the deps to install, keyed by the given 'common name'
# .add_remote(common name, package name) : adds a remote package to fetch via pip, keyed on given 'common name'
# .remove_local(common name), .remove_remote(common_name) : remove a named local/remote dependency
###


### Example base config ###
### Just the specific deps, all located in the eggs dir
baseconfig = VirtualConfig('baseconfig')  #Begin a new config, call it baseconfig
baseconfig.deps_root = 'eggs'             #Set the root deps dir, for self and all derivatives
baseconfig.deps_dir = ''                  #Deps dir relative to root - empty has no effect
baseconfig.add_local('ccg-python-build',  'ccg-python-build_v1_3.tar.gz') #add dep
baseconfig.add_local('mango',             'mango-1.2.3-r207.tar.gz')      #add dep
baseconfig.add_local('psycopg2',          'psycopg2-2.0.8.tar.gz')        #add dep
baseconfig.add_local('ldap',              'python-ldap-2.3.5.tar.gz')     #add dep
baseconfig.add_local('virtualenv',        'virtualenv-1.6.1.tar.gz')      #add dep


### Example 'clean slate' config ###
### You might want the base stuff, plus some remote
### packages like mercurial and fabric
cscfg = VirtualConfig('clean', base=baseconfig)
cscfg.deps_dir=''
cscfg.add_remote('fabric', 'fabric')
cscfg.add_remote('mercurial', 'mercurial')

### Example config for a specific ubuntu
### You want to override the ldap egg with a specific version
### And be able to use Werkzeug for local debugging
ub1010 = VirtualConfig('ubuntu_10_10_amd64_clientdev', base=baseconfig)
#by default this now has a deps dir of eggs/ubuntu_10_10_amd_clientdev
ub1010.override_local('ldap',             'python-ldap-2.4.0.tar.gz') #don't use base ldap, use mine
ub1010.add_local('werkzeug',              'Werkzeug-0.6.2.tar.gz')    #also be aware of Werkzeug

### Make all three configs available via the 
#Config keys are the names used by the -c flag
CONFIGS = [ baseconfig, ub1010, cscfg ] '''


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class VirtualConfig(object):
    def __init__(self, name, base=None):
        #Here lie the full list of attrs for this class
        self.__dict__['_d'] = {
                               'deps_root': 'eggs',
                               'deps_dir' : '',
                               'deps_local' : {},
                               'deps_overrides' : {},
                               'deps_remote' : {},
                               #'deps_pattern' : '*.*',
                               'deps_motd_file' : 'DEPENDENCIES',
                               'deps_env_file' : 'ENVIRONMENT',
                              }
        self.__dict__['name'] = name
        if base is not None:
            self.__dict__['_d'] = copy.deepcopy(base._d)
        self.deps_dir = self.name #starting value for deps dir

    

    #So this is all to stop people accidentally setting variables they shouldnt
    #on a virtualconfig - i.e. misspelling something and not noticing the problem.
    def __getattr__(self, key):
        if key not in self.__dict__['_d'].keys():
            print '%s is not a valid Virtualconfig attribute' % (key)
            raise AttributeError
        else:
            return self._d[key] 

    def __setattr__(self, key, value):
        if key not in self.__dict__['_d'].keys():
            print 'Cannot set %s - not a valid Virtualconfig attribute.' % (key)
            raise AttributeError
        else:
            self._d[key] = value
    
    def add_local(self, name, filename):
        self.deps_local[name] = self.get_local_deps_path(filename)

    def remove_local(self, name):
        if self.deps_local.has_key(name):
            del self.deps_local[name]
     
    def override_local(self, name, filename):
        '''override local just calls add_local, but that would be an unintuitive name'''
        self.add_local(name, filename)
        
    def add_remote(self, name, packagename):
        '''add a remote package to get via easy_install'''
        self.deps_remote[name] = packagename
    def remove_remote(self, name):
        if self.deps_remote.has_key(name):
            del self.deps_remote[name]

    def get_local_deps_path(self, depfile=''):
        '''Return the path to the local deps, or to a specific dep if you
           provide its filename'''
        return os.path.join(self.deps_root, self.deps_dir, depfile)


    def get_local_dep_filenames(self):
        return set(self.deps_local.values()) 

    def get_remote_dep_packages(self):
        return set(self.deps_remote.values())

    def verify(self, src_python):
        '''checks the config. All ok? returns true. Problems? returns false'''
        print bcolors.OKBLUE + 'Verifying Config' + bcolors.ENDC
        retval = True
        results = {}
        #is SRC_PYTHON findable?
        pythonbin = subprocess.Popen(["which", src_python], stdout=subprocess.PIPE).communicate()[0].strip()
        results['Source Python Exists? (%s)' % (pythonbin)] = os.path.exists(pythonbin)
        #is SRC_PYTHON executable?
        results['Source Python Executable?'] = os.access(pythonbin, os.X_OK)
        #are all deps findable?
        results['Deps dir exists (%s)' % (self.get_local_deps_path())] = os.path.exists(self.get_local_deps_path())

        for fname in self.get_local_dep_filenames(): 
            results[fname] = os.path.exists(fname)
    
        print "=========================== CONFIG RESULTS =============================="
        for key in results.keys():
            print bcolors.OKBLUE + key,
            if results[key]:
                print bcolors.OKGREEN + '\t\t\t\t[ OK ]' + bcolors.ENDC
            else:
                print bcolors.FAIL + '\t\t\t\t[ FAILED ]' + bcolors.ENDC
                retval = False
        print "========================================================================="
        if retval:
            print bcolors.OKGREEN + 'Config OK!' + bcolors.ENDC
        else:
            print bcolors.WARNING + 'Problems with Config!!' + bcolors.ENDC
        print "========================================================================="

        return retval


CONFIG_MODULE = 'blueprint_config'
CONFIG_FILE = '%s.py' % CONFIG_MODULE
DEFAULT_PYTHON_SOURCE = 'python'
VIRTUALENV = 'virtualenv-1.6.1'
VIRTUALENV_TARBALL = '%s.tar.gz' % (VIRTUALENV)
VIRTUALENV_URL = 'http://pypi.python.org/packages/source/v/virtualenv/%s' % (VIRTUALENV_TARBALL)

try:
    import argparse
except Exception, e:
    print bcolors.FAIL + "Could not import argparse. You are probably trying to run blueprint from inside a virtualenv. " + bcolors.WARNING + "Don't do that. Deactivate first" + bcolors.ENDC
    exit()
parser = argparse.ArgumentParser(description='Bootstrap a basic environment. Config is read from %s, which is created if you don\'t have it' % (CONFIG_FILE))
parser.add_argument('-p', '--python', type=str, default=DEFAULT_PYTHON_SOURCE, help='The source python to use (default=%s)' % (DEFAULT_PYTHON_SOURCE))
parser.add_argument('-c', '--configname', type=str, default='none', help='The name of the config (from the config file) that you want to use.')
parser.add_argument('-n', '--name', type=str, default=None, help='The name of the virtual environment directory to create.')
#parser.add_argument('--configfile', type=str, default=DEFAULT_CONFIGFILE, help='The name of the config file to import (default=%s)' % (DEFAULT_CONFIGFILE) )
parser.add_argument('-r', '--reinstall', type=str, default='all', choices=['all', 'deps', 'ldeps', 'rdeps' ,'env'], help='Reinstalls components (all, deps only, local deps only, remote deps only, environment only)')
parser.add_argument('-v', '--verify', default=False, action="store_true", help='Verify config, showing what would be installed, then exit')
parser.add_argument('-f', '--force', default=False, action="store_true", help='Force installation to occur, even with config errors')
args = parser.parse_args()


CONFIGNAME = args.configname
VENV_NAME = args.name
if VENV_NAME is None:
    thisdir = subprocess.Popen(["basename ${PWD}"], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()
    VENV_NAME = "virt_%s_%s" % (thisdir, CONFIGNAME)

SRC_PYTHON = args.python
CONFIG = None
REINSTALL = args.reinstall
VERIFY_ONLY = args.verify


def create_virtualpython(venvname, src_python=None, force=False):
    if force is False and os.path.exists(venvname):
        print bcolors.OKBLUE + "Virtual Env named " + bcolors.OKGREEN + venvname + bcolors.OKBLUE + ' already existed.' + bcolors.ENDC
    else:
        if not os.path.exists(venvname):
            print bcolors.WARNING + "Virtual Env does not exist, creating" + bcolors.ENDC
        else:
            print bcolors.WARNING + 'Recreating Virtual Env' + bcolors.ENDC
        if not os.path.exists(VIRTUALENV_TARBALL): 
            subprocess.call('wget %s' % (VIRTUALENV_URL), shell=True)
        installcmds = ['tar zxvf %s' % (VIRTUALENV_TARBALL),
                       'cd %s' % (VIRTUALENV),
                       '%s setup.py build --build-lib blueprint_bld' % (src_python),
                       'cd ..']
        subprocess.call(' && '.join(installcmds), shell=True)
        #create the v env
        subprocess.call('%s %s/blueprint_bld/virtualenv.py --no-site-packages %s' % (src_python, VIRTUALENV, venvname), shell=True )

def alter_venv(venvname, config):
    print 'alter venv'
    subprocess.call('echo "PROJECT_DIRECTORY=`pwd`;" >>  %s/bin/activate' % (venvname) , shell=True)
    subprocess.call('echo "export PROJECT_DIRECTORY " >>  %s/bin/activate' % (venvname) , shell=True)
    subprocess.call('echo "PS1=\\"\\\[\\\\033[44m\\\](\`basename \"%s\"\`)\\\[\\\\033[00m\\\]\$_OLD_VIRTUAL_PS1\\"" >> %s/bin/activate' % (venvname, venvname) , shell=True)
    subprocess.call('echo "export PS1" >> %s/bin/activate' % (venvname) , shell=True)
    env_file = os.path.join(config.deps_dir, config.deps_env_file)
    if os.path.exists(env_file):
        print bcolors.OKBLUE + "Running custom ENV commands in " + bcolors.OKGREEN + env_file + bcolors.ENDC
        subprocess.call('export VPYTHON_DIR=%s && . %s' % (venvname, env_file), shell=True)

def install_local_deps(venvname, config):
    print bcolors.OKBLUE + 'Installing Local Dependencies' + bcolors.ENDC
    deps_motd_file = os.path.join(config.get_local_deps_path(), config.deps_motd_file)
    if os.path.exists(deps_motd_file):
        print bcolors.WARNING + "======== DEPS MESSAGE: Take note! ==========" + bcolors.ENDC
        subprocess.call('cat %s' % (deps_motd_file) , shell=True)
        print bcolors.WARNING + "============================================" + bcolors.ENDC

    for fname in config.get_local_dep_filenames():
        subprocess.call('./%s/bin/easy_install %s' % (venvname, fname), shell=True)
    print bcolors.OKGREEN + '[ DONE ]' + bcolors.ENDC 

def install_remote_deps(venvname, config):
    print bcolors.OKBLUE + 'Installing Remote Dependencies' + bcolors.ENDC
    for name in config.get_remote_dep_packages(): 
        subprocess.call('./%s/bin/pip install %s' % (venvname, name), shell=True)
    print bcolors.OKGREEN + '[ DONE ]' + bcolors.ENDC 

def load_config(configfile, configname):
    print bcolors.OKBLUE + 'Loading Config ' + bcolors.OKGREEN + configname + bcolors.OKBLUE + ' from ' + bcolors.OKGREEN + configfile + '.py' + bcolors.ENDC
    retval = False
    try:
        import blueprint_config #CONFIG_MODULE
        for cfg in blueprint_config.CONFIGS:
            if configname == cfg.name:
                global CONFIG
                CONFIG = cfg 
                retval = True
                break
        else:
            print bcolors.WARNING + "Config name " + bcolors.OKBLUE + configname + bcolors.WARNING + " was not found in " + configfile + '.py' + bcolors.ENDC
            print bcolors.WARNING + "Perhaps you meant one of these: " + bcolors.ENDC
            for cfg in blueprint_config.CONFIGS:
                print bcolors.OKBLUE + '\t' + cfg.name + bcolors.ENDC
        
    except Exception, e:
        msg = "Error loading config (%s) : %s" % (configname, e)
        print bcolors.FAIL + msg + bcolors.ENDC
    return retval

def create_config():
    '''creates a default config file'''
    try:
        f = open(CONFIG_FILE, "w")
        default_config = TEMPLATE_TEXT 
        f.write(default_config)
        f.close()
    except Exception, e:
        print bcolors.FAIL + "ERROR: " + bcolors.ENDC + "Could not create blueprint_config.py: " + e

if __name__ == '__main__':
    print bcolors.OKBLUE + 'Running blueprint' + bcolors.ENDC
    if not os.path.exists(CONFIG_FILE):
        print bcolors.WARNING + 'You do not have a ' + CONFIG_FILE + ' - Creating a default one for you.' + bcolors.ENDC
        create_config()

    if load_config(CONFIG_FILE, CONFIGNAME):
        config_ok = CONFIG.verify(SRC_PYTHON)
        if (config_ok or args.force) and not VERIFY_ONLY:
            if REINSTALL in ['all', 'env']:
                create_virtualpython(VENV_NAME, src_python=SRC_PYTHON, force=REINSTALL in ['all', 'env'])
                alter_venv(VENV_NAME, CONFIG)
            #now for the deps:
            if not os.path.exists(VENV_NAME):
                msg = "Virtual Env %s did not exist. Refusing to install deps." % (venvname)
                print bcolors.FAIL + msg + bcolors.ENDC
            else:
                #remote deps
                if REINSTALL in ['all', 'deps', 'rdeps']:
                    install_remote_deps(VENV_NAME, CONFIG)
                #Local deps
                if REINSTALL in ['all', 'deps', 'ldeps']:
                    install_local_deps(VENV_NAME, CONFIG)
        else:
            if not config_ok:
                print "There was a problem with your config. If you *really* want to run this, use --force"
            else:
                print "Halting after config verification" 
    else:
        print 'Aborted'
