from fabric.api import env
import os
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

THIS_PATH = os.path.dirname(os.path.abspath(__file__))

def local():
	env.type = 'local'
	env.hosts = ['localhost']
	env.path = THIS_PATH.rstrip(["/"])+"/../"
	env.venv_bin = env.path + "venv/bin/"
	env.pkg_path = env.path + "venv/lib/python2.6/site-packages/"
	env.repo_path = env.path + "repo/"
	env.apps_path = env.repo_path + "apps/"
	env.git_path = env.repo_path+".git/"
	env.project_name = None

def vagrant():
	env.type = 'vagrant'
	env.hosts = ['localhost']
	env.user = "vagrant"
	env.password = "vagrant"
	env.path = "/var/apps/djangoapp/"
	env.venv_bin = env.path + "venv/bin/"
	env.pkg_path = env.path + "venv/lib/python2.6/site-packages/"
	env.repo_path = env.path + "releases/current/"  # symlink to "/app/repo/"
	env.apps_path = env.repo_path + "apps/"
	env.git_path = env.repo_path+".git/"
	env.project_name = None