from fabric.api import env, require, cd, local
from fabric.contrib import files
from fabric.colors import red, green, yellow
from fabric.context_managers import prefix
from sys import exit
import os

def start(project=None, app=None, do_requirements='yes', do_apache=None):
    """
    Fast start the Django applicatin with the bare bone minimum. USAGE: $ fab start:project=project_name,app=app_name
    """
    # set build the project as it would be normally.
    if(project != None):
        start_project(project)
    if(app != None):
        start_app(app)

    if os.path.exists(env.git_path):
        local('cd %s; git add -A; git commit -m "Initial Commit"' %
              (env.repo_path))
        print green("Added and commited your project files to git.")
        print yellow("If you haven't so already, make sure to add a remote orgin with: $ git remote add origin https://PATH_TO_GITHUB_REPO.git; git remote -v", )

    # if both app and project are provided, continue.
    if(project != None and app != None):
        do_apache = 'yes' if not do_apache and env.type=="vagrant" else 'no'
        pickup(project=project, do_requirements=do_requirements, do_apache=do_apache)


def start_project(project_name):
    env.project_name = project_name
    script = env.venv_bin + "django-admin.py"
    command = "startproject"
    template =  env.path+"quick_start/templates/project_template"
    destPath = env.repo_path
    
    create_repo_folder()
    
    local("python %s %s %s --template=%s %s" %
          (script, command, env.project_name, template, destPath))
    print green("Created new project '%s' in: %s" % (env.project_name, destPath))

    local("cd %s; git init" % env.repo_path)
    print green("Initialized a new git repository in '%s'" % (destPath))

    #move requirements outside of repo folder
    if not os.path.exists("%s../sqlite/" % env.repo_path):
        local("mv %ssqlite/ ../" % env.repo_path)
    else:
        print yellow("An existing sqlite folder is already in place.")
        local("rm -rf %ssqlite/" % env.repo_path)

    install_requirements()
    if env.type == 'vagrant':
        config_project_server()


def start_app(app_name=None):
    apps_module_file = env.apps_path + "__init__.py"
    if not os.path.exists(apps_module_file):
        os.makedirs(apps_module_file)
        print green("Created apps module: %s" % apps_module_file)

    destPath = env.apps_path + app_name
    os.makedirs(destPath)
    print green("Created folder: %s" % destPath)

    script = env.venv_bin + "django-admin.py"
    command = "startapp"
    template = env.path+"quick_start/templates/app_template"

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


def pickup(project=None, do_requirements='yes', do_apache='no'):
    """
    Configure the vagrant vm to use an existing project. USAGE: $ fab pickup:project=project_name
    """
    if project == None:
        print red('You must provide a project name as: $ fab pickup:project="project_name"')
        exit(0)
    env.project_name = project
    do_sqlite = 'yes' if os.path.exists(
        env.repo_path + "sqlite/django.sqlite") and os.path.exists(env.git_path) else 'no'
    do_wrap_up = 'yes' if os.path.exists(
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
        local('sh %ssys_requirements.sh;' % env.repo_path)
        print green("Installed additional sys_requirements.sh")
    print green("setup complete! visit http://localhost:%s to see the site." % (env.port,))

def create_repo_folder():
    if not os.path.exists(env.repo_path):
        os.makedirs(env.repo_path)
        print green("Created apps module: %s" % env.repo_path)

def install_requirements():
    file_path = env.repo_path + "requirements.txt"
    if not os.path.exists(file_path):
        print red('Unable to locate: %s') % (file_path)
        print yellow('To skip the installation, add the do_requirements="no" argument.')
        exit(0)
    with cd ('%s' % env.venv_bin ):
        with prefix('source activate'):
            local("pip install -r %s" % (file_path))
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
