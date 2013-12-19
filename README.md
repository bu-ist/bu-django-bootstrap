This is the BU Django base project bootstrap.

It contains an environment and a set of scripts and templates to get
you up and running with Django at BU.

You can always download the latest from GitHub via:

    https://github.com/bu-ist/bu-django-bootstrap/tarball/master

Note that you should DOWNLOAD, not clone, this - unless you actually need to make changes to the Bootstrap itself.

QUICKSTART
==========

Download and expand the tarball: https://github.com/bu-ist/bu-django-bootstrap/tarball/master

If you prefer ZIP: https://github.com/bu-ist/bu-django-bootstrap/zipball/master

If you don't already have it, install Oracle VirtualBox from https://www.virtualbox.org/wiki/Downloads

If you don't already have it, install the latest version (1.2.2) of Vagrant from http://vagrantup.com

START A NEW PROJECT:
=======================

1) Start off with running the following command:

    $ cd /PATH/TO/THIS/BOOTSTRAP/vagrant
    $ vagrant up

This can take a few minutes while vagrant downloads the VM and installs a few core components on the machine.

2) To start a new project, run the following commands in a terminal window, where ``<project_name>`` and ``<app_name>`` should be replaced by whatever makes sense to you. (As a rule of thumb, **use underscores for spaces**, **avoid the words 'project' and 'app'**, and make sure to **use only lower case letters**. This makes the job a lot easier for sys-admins down the road!!!)

    $ vagrant ssh 
    (venv)$ cd quick_start
    (venv)$ fab start:project=<project_name>,app=<app_name>

At this point, If all goes well, you're new application should be reachable at http://localhost:8080. 

3) The Git repository has already been initialized for you. From here on in, ``/app/repo`` is where your code will live. As you may have notice from one of the warnings thrown by the fab start script, all that's left for you to do is add the remote orgin to your local github repository. If you have a github repo. configured, you can do so with the following commands:

    (venv)$ cd /app/repo
    (venv)$ git remote add origin https://<URL_TO_GITHUB_REPO>.git; git remote -v

that final line will let you know if the remote is reachable and if the remote orgin addition was succesful.


CONTINUE AN EXISTING PROJECT:
================================

1) Start off with running the following command:

    $ cd /PATH/TO/THIS/BOOTSTRAP/vagrant
    $ vagrant up

2) Now, you will need to clone the git repository that you will be working on into a folder called repo that matchs the one found in the top level of this Bootstrap. The repo folder already exists in order to satify dependencies within the vagrant VM when you first ran ``vagrant up``. Just make sure to REPLACE the existing repo folder with the new one that will contain the existing project source. 

On OSX, GitHub has a great application that allows you to Clone a repo to a folder with just a few clicks, so if you prefer a GUI interface, that's your best bet. Here's a download link: https://central.github.com/mac/latest


3) Make sure the project dependencies are satified by executing the following commands. Change ``<project_name>`` to read the name of the project that you just cloned from GitHub. This is the same name as the folder containing the settings.py file and will be located in your repo folder.

    $ vagrant ssh
    (venv)$ cd quick_start
    (venv)$ sudo fab continue:project<project_name>

Your Environment is now ready to work on and be reachable via http://localhost:8080 (unless there's some extra vodoo happening on the application end).


NOTES
=====

A database is required to work with a Django application. We recommend using a temporary sqlite database for local development and with Vagrant. If the Oracle database is needed, you may follow the instructions in Oracle setup section.

# SQLite Setup

If you ran the fab start:project=<project_name>,app=<app_name> command, you might have noticed that the git repo is already set up for you. The sqlite file for the project has also been ignored for you and you should be all set in terms of not tracking any further changes done to it.

If by chance something went wrong, and you still need to stop tracking the changes done to a commited database file, you can accomplish this by executing the following command inside your repo folder:
    
    $ git update-index --assume-unchanged sqlite/django.sqlite 

# Oracle Setup

## Getting Oracle set up in your BU Django Bootstrap VM
In the future the bootstrap provisioning should be updated to automatically install Oracle dependencies in the vagrant VM to support projects such as this.  But in the meantime, you can follow these steps to use an Oracle backend for this project:

### 1. Download the Oracle instant client libraries
Download the following client libraries from: http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html

Select the correct architecture (at the time of this writing, the base Vagrant VM is Ubuntu 10.04.4 LTS, i686 arch, so Linux x86).

You'll have a choice of several different components, in either .zip or RPM formats.

Download the latest versions (11.2.0.3.0 at time of writing) of the following RPM's:

* oracle-instantclient-basiclite
* oracle-instantclient-devel
* oracle-instantclient-sqlplus (command line client)


### 2. Install some additional Ubuntu packages
Ubuntu doesn't natively support installation via RPM's, so you'll need to install [Alien](http://manpages.ubuntu.com/manpages/gutsy/man1/alien.1p.html) for translation.

```bash
sudo apt-get install alien
sudo apt-get install libaio1 (needed by sqlplus)
```

Once these are installed, you can install the Oracle tools from the downloaded RPM's using alien:

```bash
alien -i oracle-instantclient-basiclite*.rpm
alien -i oracle-instantclient-sqlplus*.rpm
alien -i oracle-instantclient-devel*.rpm
```
The default install location is `/usr/lib/oracle/<version>/client`.  The rest of these instructures will assume version 11.2.

### 3. Setup Oracle Environment variables
Add the following to `/home/vagrant/.profile`:

```bash
export ORACLE_HOME=/usr/lib/oracle/11.2/client
PATH=$PATH:$ORACLE_HOME/bin
```

### 4. Add dynamic shared library path
The Python library Django utilizes for Oracle DB backends relies on a dynamic shared library that comes with the client libraries you just installed.

Make sure it can find it by running the following:
```bash
echo /usr/lib/oracle/11.2/client/lib | sudo tee /etc/ld.so.conf.d/oracle.conf
sudo ldconfig
```

### 5. Install the cx_oracle Python package
The Oracle DB backend in Django uses the cx_oracle Python package to talk to Oracle databases.

This dependency has been added to the requirements.txt file for this project, but I found that in order to install I had to add the following symlink:
```bash
ln -s /usr/lib/oracle/11.2/client/lib/ibclntsh.so.11.1 /usr/lib/oracle/11.2/client/lib/libclntsh.so
```

At this point, you should be all set to install the cx_oracle Python package, either from requirements.txt or directly using:
```bash
pip install cx_oracle
```

These instructions were modified from:
https://help.ubuntu.com/community/Oracle%20Instant%20Client

For more information on Django and Oracle:
https://docs.djangoproject.com/en/dev/ref/databases/#oracle-notes


LAST BUT NOT LEAST:
===================

As you begin the project, take 5 minutes to review the Django coding style
guide found here:

    http://docs.djangoproject.com/en/dev/internals/contributing/#coding-style

HAPPY CODING!
