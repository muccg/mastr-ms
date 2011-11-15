from blueprint import VirtualConfig
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
baseconfig.add_local('mango',             'Mango-py-1.3.1-ccg-195.tar.gz')      #add dep
baseconfig.add_local('psycopg2',          'psycopg2-2.0.8.tar.gz')        #add dep
baseconfig.add_local('ldap',              'python-ldap-2.3.5.tar.gz')     #add dep
baseconfig.add_local('ccg_python_build',  'ccg-python-build_v1_3.tar.gz')     #add dep
baseconfig.add_local('ccg_django_auth',   'ccg-django-auth-0.3.tar.gz')     #add dep
baseconfig.add_local('ccg_django_extras', 'ccg-django-extras-0.1.1.tar.gz')     #add dep
baseconfig.add_local('ccg_django_makoloader', 'ccg-django-makoloader-0.2.2.tar.gz')     #add dep


devconfig = VirtualConfig('devconfig', base=baseconfig)
devconfig.deps_dir = 'ubuntu_10_4'
devconfig.add_local('werkzeug',              'Werkzeug-0.6.2.tar.gz')    #also be aware of Werkzeug

### Make all three configs available via the 
#Config keys are the names used by the -c flag
CONFIGS = [ baseconfig, devconfig ] 
