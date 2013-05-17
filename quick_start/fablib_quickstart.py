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
    local("pip install -r %s" % (req_path))


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
    requirementsPath = env.repo_path+"requirements.txt"
    settingPath = env.repo_path + project_name + "/settings_vagrant.py"
    for count, value in enumerate(args):
        if count == 0:
            requirementsPath = value
    if not os.path.exists(settingPath):
        print red('Unable to located file: %s', bold=True) % settingPath
        return False
    install_requirements(requirementsPath)
    config_server(project_name)


def start_app_project(project_name, app_name):
    """"
        Because django doesn't support templating projects with a predefined
        context (yet) we can hack this by rendering the project template with the
        app_name context first then again with the project_name in the context.
    """
    repo_template = "/app/quick_start/templates/repo_template/"
    start_app(app_name, **{'template': repo_template, 'destination': env.temp_dir})
    start_project(project_name, **{'template': env.temp_dir})


def start_project(project_name, **kwargs):
    """start up virtualenv and requirements for Vagrant dev environment """

    env.project_name = project_name
    template = "/app/quick_start/templates/project_template"
    if 'template' in kwargs:
        template = kwargs['template']
    destPath = env.repo_path
    if 'destination' in kwargs:
        destPath = kwargs['destination']

    if not os.path.exists(destPath):
        print(cyan("Created directory:"+destPath))
        os.makedirs(destPath)
    local("%s/django-admin.py startproject %s --template=%s %s" %
         (env.venv_bin, project_name, template, destPath))
    install_requirements("/app/repo/requirements.txt")
    config_server(project_name)


def start_app(app_name, **kwargs):
    template = "/app/quick_start/templates/app_template"
    if 'template' in kwargs:
        template = kwargs['template']
    destPath = env.repo_path+"apps/"+app_name
    if 'destination' in kwargs:
        destPath = kwargs['destination']
    if not os.path.exists(destPath):
        print(cyan("Created directory:"+destPath))
        os.makedirs(destPath)
        file(env.repo_path+"apps/__init__.py", "w+")
    local("%s/django-admin.py startapp %s --template=%s %s" %
          (env.venv_bin, app_name, template, destPath))


def setup_vagrant():
    "Set up virtualenv and requirements for Vagrant dev environment"
    require('path')
    with cd(env.path):
        local('if ! [ -e %(path)s/venv ]; then mkdir venv; fi;' % env)
        local('if ! [ -e %(path)s/venv/bin/python ]; ' +
              'then /usr/local/bin/virtualenv %(path)s/venv; fi;' % env)
    env.release = 'current'
    # note that this points to the project template, NOT the current release
    local('%(path)s/venv/bin/python %(path)s/venv/bin/pip install ' +
          '--use-mirrors --log=%(path)s/log/pip.log ' +
          '-r /app/templates/project_template/requirements.txt' % env
          )
    local('sudo apache2ctl restart')
