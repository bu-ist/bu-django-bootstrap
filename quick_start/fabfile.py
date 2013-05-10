from fabric.api import env

# BU's Fabric library
from quickstart_fablib import *

# Configuration: set up your project and environment locations
# below. We've prefilled them with defaults based on your project
# name({{ project_name }}), but you should review for accuracy.
# The servers are assumed to be BU's standard Django servers,
# but can be changed below. This process assumes git, but can
# be modified to use SVN.

# common settings - can be overridden per-environment
#env.gitsource = '/afs/.bu.edu/cwis/content/git/{{ project_name }}.git'


def vagrant():
    env.hosts = ['localhost']
    env.user = "vagrant"
    env.password = "vagrant"
    env.virtualenv_bin = "/var/app/djangoapp/venv/bin"
    env.shell = "/bin/bash"
    env.path = "/var/apps/djangoapp/"
    env.app_path = env.path+"releases/current/"
