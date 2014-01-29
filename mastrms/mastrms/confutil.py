import os
import ConfigParser
import StringIO

__all__ = ["setup_prod_env"]

def setup_prod_env():
    project_name = os.path.basename(os.path.dirname(__file__))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.prodsettings' % project_name)
    os.environ.setdefault('PYTHON_EGG_CACHE', '/tmp/.python-eggs')

    # ccg.utils.webhelpers expects SCRIPT_NAME to be a path such as /mastrms
    os.environ["SCRIPT_NAME"] = "/" + project_name

    os.environ["PROJECT_NAME"] = project_name

    # set up the environment with settings loaded from a config file.
    config_file = "/etc/%s/%s.conf" % (project_name, project_name)

    config = load_config(config_file)

    for key, val in config:
        os.environ["_".join((project_name, key)).lower()] = val

def load_config(filename):
    section = "root"

    try:
        config_text = "[%s]\n%s" % (section, open(filename).read())
    except IOError:
        config_text = ""

    config = ConfigParser.ConfigParser()
    config.readfp(StringIO.StringIO(config_text))

    return config.items(section)
