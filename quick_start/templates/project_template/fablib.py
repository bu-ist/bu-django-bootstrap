from fabric.api import env, sudo, require, cd, run
from fabric.colors import cyan
import sys
import time

# This is BU's Fabric library.
# It has generic deploy/setup tasks, including some optional handling
# for AFS (both in terms of SCM locations and static media).
# It should ultimately be an independent package, though currently it's
# distributed with the BU Django Bootstrap package.

# these settings generally don't need to be changed
env.server_group = 'apache'
env.wsgi_script = 'app.wsgi'
env.gettoken_script = 'gettoken'
env.shell = 'ORACLE_HOME=/usr/local/oracle/product/11.2.0 LD_LIBRARY_PATH=/usr/local/oracle/product/11.2.0/lib /bin/bash --noprofile -l -c' # avoid looking for .bash_profile, etc.
env.virtualenv_bin = '/usr/bin/virtualenv-2.6'


# Commands - you shouldn't need to alter these unless you need to change how the app is deployed

def deploy():
    """
    Full deploy: pull code as specified, run migrations, and reload.
    """
    require('use_syncdb')
    require('use_migrations')
    env.release = time.strftime('%Y%m%d%H%M%S')
    
    update_from_git()
    install_site()
    install_requirements()
    copy_settings()
    # this is an optimization that depends on having django-extensions installed - so don't blow up if there's a problem
    try:
        compile_pyc()
    except:
        pass
    symlink_current_release()
    deploy_static()
    if env.use_syncdb:
        sync()
    if env.use_migrations:
        migrate()
    reload_app()


def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, install the requirements.
    """
    require('path')
    require('gitpath')
    require('gitsource')
    require('server_owner')
    require('server_group')
    require('needs_afs_token_for_repo')

    with cd(env.path):
        run_or_sudo('; if ! [ -e %(path)s/releases ]; then mkdir releases; fi;' % env)

    if env.needs_afs_token_for_repo:
        get_afs_token()

    # first checkout of repo
    setup_git_repo()

    # install virtualenv
    setup_virtualenv()

    # create EGG_CACHE, set permissions
    run_or_sudo('; if ! [ -e %(path)s/EGG_CACHE ]; then mkdir %(path)s/EGG_CACHE; fi;' % env)
    run_or_sudo('chmod -R 775 %(path)s/EGG_CACHE' % env)

    # install requirements into virtualenv
    # (can't install requirements until we have a release)
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    update_from_git()
    install_site()
    copy_settings()
    install_requirements()


def setup_git_repo():
    "First checkout of repo - check if it exists first (so that the method is idempotent)"
    require('gitpath')
    require('gitsource')
    require('needs_afs_token_for_repo')
    if env.needs_afs_token_for_repo:
        get_afs_token()
    run_or_sudo('; if ! [ -e %(gitpath)s ]; then mkdir %(gitpath)s; fi;' % env)
    with cd(env.gitpath):
        run_or_sudo('; if ! [ -e %(gitpath)s/.git ]; then git clone %(gitsource)s .; fi;' % env)


def setup_virtualenv():
    with cd(env.path):
        run_or_sudo('if ! [ -e %(path)s/venv ]; then mkdir venv; fi;' % env)
        run_or_sudo('if ! [ -e %(path)s/venv/bin/python ]; then %(virtualenv_bin)s %(path)s/venv; fi;' % env)


def update_from_git():
    require('gitpath')
    require('needs_afs_token_for_repo')
    if env.needs_afs_token_for_repo:
        get_afs_token()
    with cd(env.gitpath):
        run_or_sudo('git pull --rebase' % env)


def git_checkout(branch):
    require('gitpath')
    require('needs_afs_token_for_repo')
    if env.needs_afs_token_for_repo:
        get_afs_token()
    with cd(env.gitpath):
        run_or_sudo('/usr/bin/git pull --rebase')
        run_or_sudo('/usr/bin/git checkout %(branch)s' % {'branch': branch})


def compile_pyc():
    "Pre-compile the .py files for a faster startup"
    require('path')
    require('release')
    require('settings_file')
    require('server_owner')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/%(release)s/manage.py compile_pyc --settings=%(settings_file)s --path=%(path)s/releases/%(release)s' % env)


def install_requirements():
    "Install the required packages from the requirements file using pip"
    require('path')
    require('release')
    require('server_owner')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/venv/bin/pip install --use-mirrors --log=%(path)s/log/pip.log -r %(path)s/releases/%(release)s/requirements.txt' % env)


def install_site():
    require('release')
    require('gitpath')
    require('path')
    require('server_owner')

    run_or_sudo('mkdir %(path)s/releases/%(release)s' % env)

    # TODO: HEAD or tag (argument?)
    with cd(env.gitpath):
        run_or_sudo('git archive --format=tar HEAD | tar -x -C %(path)s/releases/%(release)s' % env)


def manage(cmd=""):
    """Run a management command in the app directory."""
    if not cmd:
        sys.stdout.write(cyan("Command to run: "))
        cmd = raw_input().strip()

    if cmd:
        cmd_args = dict(env)
        cmd_args.update({'cmd': cmd})
        run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py %(cmd)s --settings=%(settings_file)s' % cmd_args)


def loaddata(fixture):
    """Usage: fab [devl|test|prod] loaddata:fixture=[fixture]"""
    require('path')
    require('settings_file')
    require('server_owner')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py loaddata %(fixture)s --settings=%(settings_file)s' % env)


def symlink_current_release():
    "Symlink our current release"
    require('path')
    require('release')
    require('server_owner')
    # all the "if" stuff in case there *is* no current or prev release
    with cd(''.join([env.path, '/releases'])):
        try:
            run_or_sudo('; if [ -e %(path)s/releases/previous ]; then mv -f `readlink %(path)s/releases/previous/` %(path)s/releases/archive/; fi;' % env)
        except:
            # OK if removing previous doesn't work - might be _init, owned by root
            pass
        run_or_sudo('rm -f %(path)s/releases/previous' % env)
        run_or_sudo('; if [ -e %(path)s/releases/current ]; then mv %(path)s/releases/current %(path)s/releases/previous; fi;' % env)
        try:
            run_or_sudo('rm -f %(path)s/releases/current' % env)
        except:
            # OK if removing current doesn't work - might be _init, owned by root
            pass
        run_or_sudo('ln -s %(release)s %(path)s/releases/current' % env)


def migrate():
    "Update the database"
    require('path')
    require('settings_file')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py migrate --settings=%(settings_file)s' % env)


def sync():
    "Sync the database"
    require('path')
    require('settings_file')
    require('server_owner')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py syncdb --settings=%(settings_file)s' % env)


def create_superuser():
    "Calls the django_extensions create_superuser command"
    require('path')
    require('settings_file')
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py createsuperuser --settings=%(settings_file)s' % env)


def get_afs_token():
    require('path')
    require('gettoken_script')
    run_or_sudo('%(path)s/bin/%(gettoken_script)s' % env)


def deploy_static():
    require('path')
    require('settings_file')
    require('needs_afs_token_for_static')
    if env.needs_afs_token_for_static:
        get_afs_token()
    run_or_sudo('%(path)s/venv/bin/python %(path)s/releases/current/manage.py collectstatic --noinput --settings=%(settings_file)s' % env)


def copy_settings():
    """
    Copy the environment-appropriate settings file to the deployment target.
    TODO: this should be incorporated into the standard deployment script,
    possibly in a modified form.
    """
    require('path')
    require('settings_file')
    require('release')
    require('project_name')
    opts = env
    opts.update({ 'env_settings_file': env.settings_file.split('.')[1] + '.py' })
    run_or_sudo('cp %(path)s/settings/%(env_settings_file)s %(path)s/releases/%(release)s/%(project_name)s' % opts)


def reload_app():
    """Reload application code without restarting the web server"""
    require('path')
    require('wsgi_script')
    require('server_owner')
    run_or_sudo('touch %(path)s/apache/%(wsgi_script)s' % env)

def run_or_sudo(cmd):
    """run or sudo the specified command depending on who's running the script"""
    if env.user == env.server_owner:
         run(cmd % env)
    else:
        sudo(cmd, user=env.server_owner)
