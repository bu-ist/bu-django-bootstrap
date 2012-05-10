from fabric.api import env

# BU's Fabric library
from fablib import *

# Configuration: set up your project and environment locations below.
# We've prefilled them with defaults based on your project name ({{ project_name }}),
# but you should review for accuracy.
# The servers are assumed to be BU's standard Django servers, but can be changed below.
# This process assumes git, but can be modified to use SVN.

# common settings - can be overridden per-environment
env.project_name = '{{ project_name }}' # name of project module in root of repo
env.gitsource = '/afs/.bu.edu/cwis/content/git/{{ project_name }}.git' # full path (filesystem or git: to .git repo)
env.server_owner = '{{ project_name }}-svc'
env.needs_afs_token_for_repo = True # is the repo in AFS?
env.needs_afs_token_for_static = False # is the static content being deployed to AFS?
env.use_syncdb = True # do you want to run 'syncdb' on deploy?
env.use_migrations = True # do you want to run 'migrate' on deploy?

# Deployment Environments

def vagrant():
    env.virtualenv_bin = '/usr/local/bin/virtualenv'
    env.shell = '/bin/bash'
    # path on disk
    env.path = '/var/apps/djangoapp'
    # settings module to use for this environment - typically projectname.settings_[env]
    env.settings_file = env.project_name + '.settings'


def devl():
    # host or hosts for this environment
    env.hosts = ['vsc64.bu.edu']
    # path on disk
    env.path = '/apps/{{ project_name }}-devl'
    # path to repo - typically env.path + '/repo'
    env.gitpath = env.path + '/repo'
    # settings module to use for this environment - typically projectname.settings_[env]
    env.settings_file = env.project_name + '.settings_devl'


def test():
    # host or hosts for this environment
    env.hosts = ['vsc66.bu.edu', 'vsc67.bu.edu']
    # path on disk
    env.path = '/apps/{{ project_name }}-test'
    # path to repo - typically env.path + '/repo'
    env.gitpath = env.path + '/repo'
    # settings module to use for this environment - typically projectname.settings_[env]
    env.settings_file = env.project_name + '.settings_test'


def prod():
    # host or hosts for this environment
    env.hosts = ['vsc68.bu.edu', 'vsc69.bu.edu']
    # path on disk
    env.path = '/apps/{{ project_name }}-prod'
    # path to repo - typically env.path + '/repo'
    env.gitpath = env.path + '/repo'
    # settings module to use for this environment - typically projectname.settings_[env]
    env.settings_file = env.project_name + '.settings_prod'

