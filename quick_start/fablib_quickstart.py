from fabric.api import env, require, cd, local
from fabric.contrib import files
from fabric.colors import red, green, yellow
from sys import exit
import os

def start(project=None, app=None):
    """
    Fast start the Django applicatin with the bare bone minimum. USAGE: $ fab start:project=project_name,app=app_name
    """
    # set build the project as it would be normally.
    if(project != None):
        start_project(project)
    if(app != None):
        start_app(app)

    if files.exists(env.git_path):
        local('cd %s; git add -A; git commit -m "Initial Commit"' %
              (env.repo_path))
        print green("Added and commited your project files to git.")
        print yellow("If you haven't so already, make sure to add a remote orgin with: $ git remote add origin https://PATH_TO_GITHUB_REPO.git; git remote -v", )

    # if both app and project are provided, continue.
    if(project != None and app != None):
        pickup(project=project)


def start_project(project_name):
    env.project_name = project_name
    script = env.venv_bin + "django-admin.py"
    command = "startproject"
    template = "/app/quick_start/templates/project_template"
    destPath = env.repo_path

    local("python %s %s %s --template=%s %s" %
          (script, command, env.project_name, template, destPath))
    print green("Created new project '%s' in: %s" % (env.project_name, destPath))

    local("cd %s; git init" % env.repo_path)
    print green("Initialized a new git repository in '%s'" % (destPath))

    install_requirements()
    config_project_server()


def start_app(app_name=None):
    apps_module_file = env.apps_path + "__init__.py"
    if not files.exists(apps_module_file):
        os.makedirs(apps_module_file)
        print green("Created apps module: %s" % apps_module_file)

    destPath = env.apps_path + app_name
    os.makedirs(destPath)
    print green("Created folder: %s" % destPath)

    script = env.venv_bin + "django-admin.py"
    command = "startapp"
    template = env.path+"/quick_start/templates/app_template"

    local("python %s %s %s --template=%s %s" %
          (script, command, app_name, template, destPath))
    print green("Started new app in: %s" % destPath)

    if(env.project_name != None):
        settings = env.repo_path + env.project_name + "/settings.py"
        line = "INSTALLED_APPS +=  ('apps.%s',)" % app_name
        local('echo "%s" >> %s' % (line, settings))
        project_urls = env.repo_path + env.project_name + "/urls.py"
        line = "urlpatterns += patterns('',url(r'', include('apps.%s.urls')),)" % app_name
        local('echo "%s" >> %s' % (line, project_urls))
        print green("Hooked app '%s' into project '%s'" % (app_name, env.project_name))


def pickup(project=None, do_requirements='yes', do_apache='yes'):
    """
    Configure the vagrant vm to use an existing project. USAGE: $ fab pickup:project=project_name
    """
    if project == None:
        print red('You must provide a project name as: $ fab pickup:project="project_name"')
        exit(0)
    env.project_name = project
    do_sqlite = 'yes' if files.exists(
        env.repo_path + "sqlite/django.sqlite") and files.exists(env.git_path) else 'no'
    do_wrap_up = 'yes' if files.exists(
        env.repo_path + "sys_requirements.sh") else 'no'

    if do_requirements == 'yes':
        install_requirements()
    if do_apache == 'yes':
        config_project_server()
    if do_sqlite == 'yes':
        local(
            'cd %s; git update-index --assume-unchanged sqlite/django.sqlite;' %
            (env.repo_path))
        print green("Ignoring local sqlite file.")
        print yellow("Make sure the host's sqlite folder and contents have permission set to 777.")
    if do_wrap_up == 'yes':
        local('sh %s;' % env.repo_path + "sys_requirements.sh")
        print green("Installed additional sys_requirements.sh")
    print green("setup complete! visit http://localhost:8080 to see the site.")


def install_requirements():
    file_path = env.repo_path + "requirements.txt"
    if not files.exists(file_path):
        print red('Unable to locate: %s') % (file_path)
        print yellow('To skip the installation, add the do_requirements="no" argument.')
        exit(0)
    local("sudo pip install -r %s" % (file_path))
    print green("Sucessfully installed python packages.")


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
        orgPath + "vagrant.wsgi.template",
        dstPath + "vagrant.wsgi",
        context,
        use_jinja,
        template_dir,
        use_sudo,
        backup,
        mirror_local_mode,
        mode
    )
    print green('Vagrant Apache successfully configured')
