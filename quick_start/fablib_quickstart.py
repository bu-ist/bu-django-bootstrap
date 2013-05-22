from fabric.api import env, require, cd, local
from fabric.contrib import files
from fabric.colors import red, cyan
import os

# This is BU's Fabric library.
# It has generic deploy/setup tasks, including some optional handling
# for AFS (both in terms of SCM locations and static media).
# It should ultimately be an independent package, though currently it's
# distributed with the BU Django Bootstrap package.

# these settings generally don't need to be changed
# these settings can be modified in fabfile.py vagrant():
env.server_group = 'apache'
env.wsgi_script = 'app.wsgi'
env.gettoken_script = 'gettoken'
env.shell = 'ORACLE_HOME=/usr/local/oracle/product/11.2.0 LD_LIBRARY_PATH=/usr/local/oracle/product/11.2.0/lib /bin/bash --noprofile -l -c' # avoid looking for .bash_profile, etc.
env.venv_bin = '/usr/bin/virtualenv-2.6'


def install_requirements(req_path):
    local("sudo pip install -r %s" % (req_path))


def config_server(name=None):
    orgPath = "/app/quick_start/templates/apache/"
    dstPath = "/app/apache/"
    context = {'project_name': name}
    use_jinja = False
    template_dir = None
    use_sudo = False
    backup = True
    mirror_local_mode = True
    mode = None
    files.upload_template(
        orgPath+"vagrant.wsgi.template",
        dstPath+"vagrant.wsgi",
        context,
        use_jinja,
        template_dir,
        use_sudo,
        backup,
        mirror_local_mode,
        mode
    )


def continue_project(project_name=None, *args):
    requirementsPath = env.app_path+"requirements.txt"
    settingPath = env.app_path + project_name + "/settings_vagrant.py"
    for count, value in enumerate(args):
        if count == 0:
            requirementsPath = value
    if not os.path.exists(settingPath):
        print red('Unable to located file: %s', bold=True) % settingPath
        return False
    install_requirements(requirementsPath)
    config_server(project_name)


def start_project(project_name=None):
    """start up virtualenv and requirements for Vagrant dev environment """
    env.project_name = project_name
    script = env.path+"venv/bin/django-admin.py"
    command = "startproject"
    template = "/app/quick_start/templates/project_template"
    destPath = env.app_path
    local("python %s %s %s --template=%s %s" %
         (script, command, project_name, template, destPath))

    install_requirements("/app/repo/requirements.txt")
    config_server(project_name)


def start_app(app_name=None, *args):
    script = env.path+"/venv/bin/django-admin.py"
    command = "startapp"
    template = "/app/quick_start/templates/app_template"
    destPath = env.app_path+"/apps/"+app_name
    for count, value in enumerate(args):
        if count == 0:
            destPath = env.app_path+"/apps/"

    if not os.path.exists(destPath):
        print(cyan("Created directory:"+env.app_path+"/apps/"))
        os.makedirs(destPath)
        file(env.repo_path+"apps/__init__.py", "w+")
    local("python %s %s %s --template=%s %s" %
          (script, command, app_name, template, destPath))
