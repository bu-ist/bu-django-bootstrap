from fabric.api import env, require, cd, local
from fabric.contrib import files
from fabric.colors import red, green, yellow
from fabric.utils import abort
import os

# This is BU's Fabric library.
# It has generic deploy/setup tasks, including some optional handling
# for AFS (both in terms of SCM locations and static media).
# It should ultimately be an independent package, though currently it's
# distributed with the BU Django Bootstrap package.


def start(project=None, app=None):
    """
    Fast start the Django applicatin with the bare bone minimum. USAGE: $ fab start:project=project_name,app=app_name
    """
    #set build the project as it would be normally.
    if(project != None):  start_project(project)
    if(app != None):   start_app(app)
    #if both app and project are provided, continue.
    if(project != None and app != None): 
        pickup(project=project, do_requirements='yes', do_apache='yes', do_sqlite='no', do_wrap_up='yes')


def start_project(project_name):
    env.project_name = project_name
    script = env.venv_bin + "django-admin.py"
    command = "startproject"
    template = "/app/quick_start/templates/project_template"
    destPath = env.app_path
   
    local("python %s %s %s --template=%s %s" %(script, command, env.project_name, template, destPath))
    print green("Created new project '%s' in: %s" % (env.project_name, destPath))

    install_requirements()
    config_project_server()


def start_app(app_name=None):
    apps_module_file = env.apps_path + "__init__.py"
    if not files.exists(apps_module_file):
        os.makedirs(apps_module_file)
        print green("Created apps module: %s" %apps_module_file)

    destPath = env.apps_path + app_name
    os.makedirs(destPath)
    print green("Created folder: %s" %destPath)

    script = env.venv_bin+"django-admin.py"
    command = "startapp"
    template = "/app/quick_start/templates/app_template"

    local("python %s %s %s --template=%s %s" %(script, command, app_name, template, destPath))
    print green("Started new app in: %s" % destPath)

    if(env.project_name != None):
        settings = env.app_path + env.project_name + "/settings.py"
        line = "INSTALLED_APPS +=  ('apps.%s',)" % app_name
        local('echo "%s" >> %s' % (line, settings));
        project_urls = env.app_path + env.project_name + "/urls.py"
        line = "urlpatterns += patterns('',url(r'', include('apps.%s.urls')),)" %app_name;
        local('echo "%s" >> %s' %(line, project_urls))
        print green("Hooked app '%s' into project '%s'" %(app_name, env.project_name))


def pickup(project=None, do_requirements='yes', do_apache='yes', do_sqlite='yes', do_wrap_up='yes'):
    """
    Configure the vagrant vm to use an existing project. USAGE: $ fab pickup:project=project_name
    """
    if project == None:
        print red('You must provide a project name as: $ fab pickup:project="project_name"')
        abort()

    env.project_name = project

    if do_requirements =='yes': install_requirements()
    if do_apache       =='yes': config_project_server()
    if do_sqlite       =='yes': ignore_sqlite_file()
    if do_wrap_up      =='yes': wrap_up()
    

def install_requirements():
    file_name = "requirements.txt"
    file_path = env.app_path + file_name
    check_file_exists(file_path, "do_requirements")
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
    check_file_exists(file_path, "do_sqlite")
    check_file_exists(env.app_path+".git/", "do_sqlite")
    local('cd %s; git update-index --assume-unchanged %s;' %(env.app_path, file_path))


def wrap_up():
    file_name = "sys_requirements.sh"
    file_path = env.app_path + file_name
    check_file_exists(file_path, "do_wrap_up", abort_on_error=False)
    local('sh %s;' % file_path)


def check_file_exists(file_path, skip_arg_name=None, abort_on_error=True):
    if not files.exists(file_path):
        print red('Unable to locate: %s') % (file_path)
        if skip_arg_name is not None:
            print yellow('To skip the installation, add the %s="no" argument.') % (skip_arg_name)
        if abort_on_error:
            abort("Tried to access illegal file path.")

