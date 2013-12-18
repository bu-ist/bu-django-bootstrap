from fabric.api import env, require, cd, local
from fabric.contrib import files
from fabric.colors import red, cyan, blue
from fabric.utils import abort
import os

# This is BU's Fabric library.
# It has generic deploy/setup tasks, including some optional handling
# for AFS (both in terms of SCM locations and static media).
# It should ultimately be an independent package, though currently it's
# distributed with the BU Django Bootstrap package.

def start(project=None, app=None):
    #set build the project as it would be normally.
    if(project != None):  start_project(project)
    if(app != None):   start_app(app)
    #if both app and project are provided, continue.
    if(project != None && app != None): pickup(project=project, do_requirements='yes', do_apache='yes', do_sqlite='yes', do_wrap_up='yes')


def start_project(project_name):
    """start up virtualenv and requirements for Vagrant dev environment """
    env.project_name = project_name
    script = env.venv_bin+"django-admin.py"
    command = "startproject"
    template = "/app/quick_start/templates/project_template"
    destPath = env.app_path
    local("python %s %s %s --template=%s %s" %
         (script, command, env.project_name, template, destPath))

    install_requirements()
    config_project_server()
    ignore_sqlite_file()


def start_app(app_name=None):
    apps_dir = env.app_path + "apps/"
    if not os.path.exists(apps_dir):
        print(cyan("Created directory:"+env.app_path+"apps/"))
        os.makedirs(apps_dir)
        file(apps_dir+"__init__.py", "w+")

    destPath = apps_dir + app_name
    os.makedirs(destPath)

    script = env.venv_bin+"django-admin.py"
    command = "startapp"
    template = "/app/quick_start/templates/app_template"

    local("python %s %s %s --template=%s %s" %
          (script, command, app_name, template, destPath))

    if(env.project_name != None):
        setting_vagrant = env.app_path + env.project_name + "/settings_vagrant.py"
        local('"INSTALLED_APPS +=  (\'%s\',) >> %s"  ' % (app_name, setting_vagrant));


def pickup(project=None, do_requirements='yes', do_apache='yes', do_sqlite='yes', do_wrap_up='yes'):
    if project == None:
        print red('You must provide a project name as: $ fab pickup:project="project_name"')
        return False

    env.project_name = project
    setting_vagrant = env.app_path + env.project_name + "/settings_vagrant.py"
    if not os.path.exists(setting_vagrant):
        print red('Unable to locate settings_vagrant file at: %s') % setting_vagrant
        return False

    if do_requirements =='yes': install_requirements()
    if do_apache       =='yes': config_project_server()
    if do_sqlite       =='yes': ignore_sqlite_file()
    if do_wrap_up      =='yes': wrap_up()
    

def install_requirements():
    file_name = "requirements.txt"
    file_path = env.app_path + file_name
    check_file_path(file_path, file_name, "do_requirements"):
    local("sudo pip install -r %s" % (file_path))


def config_project_server():
    orgPath = "/app/quick_start/templates/apache/"
    dstPath = "/app/apache/"
    context = {'project_name': env.project_name}
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


def ignore_sqlite_file():
    file_name = "django.sqlite"
    file_path = env.app_path + "sqlite/" + file_name
    check_file_path(file_path, file_name, "do_sqlite"):
    local('cd %s; git update-index --assume-unchanged %s;' %(env.app_path, file_path))


def wrap_up():
    file_name = "continue_project.sh"
    file_path = env.app_path + file_name
    check_file_path(file_path, file_name, "do_wrap_up"):
    local('sh %s;' % file_path)


def check_file_path(req_path, file_name, arg_name=None):
    if not os.path.exists(req_path):
        print red('Unable to locate %s file at: %s') % (file_name, req_path)
        if arg_name is not None:
            print blue('To skip the installation of the %s file, add the %s="no" argument.') % (file_name, arg_name)
        abort("encountered illegal file path.")
