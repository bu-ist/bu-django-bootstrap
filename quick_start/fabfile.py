from fabric.api import env

# BU's Fabric library
from fablib_quickstart import *

# Configuration: set up your project and environment locations
# below. We've prefilled them with defaults based on your project
# name({{ project_name }}), but you should review for accuracy.
# The servers are assumed to be BU's standard Django servers,
# but can be changed below. This process assumes git, but can
# be modified to use SVN.

# common settings - can be overridden per-environment
#env.gitsource = '/afs/.bu.edu/cwis/content/git/{{ project_name }}.git'

env.hosts = ['localhost']
env.user = "vagrant"
env.password = "vagrant"
env.path = "/var/apps/djangoapp/"
env.venv_bin = env.path + "venv/bin/"
env.pkg_path = env.path + "venv/lib/python2.6/site-packages/"
env.app_path = env.path + "releases/current/"  # symlink to "/app/repo/"
env.apps_path = env.app_path + "apps/"
env.project_name = None