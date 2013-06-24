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

2) To start a new project, run the following commands in a terminal window, where ``<myproject>`` and ``<myapp>`` should be replaced by whatever makes sense to you. (As a rule of thumb, **use underscores for spaces**, **avoid the words 'project' and 'app'**, and make sure to **use only lower case letters**. This makes the job a lot easier for sys-admins down the road!!!)

    $ vagrant ssh 
    (venv)$ cd quick_start
    (venv)$ fab vagrant start_project:<myproject>
    (venv)$ fab vagrant start_app:<myapp>

From here on in, ``/app/repo`` is where your code will live and where you should init[ialize] your git repository.

If all goes well, you're new application should be reachable at http://localhost:8080. For a full rundown of set tasks, see ``/docs/new-project.txt``.

CONTINUE AN EXISTING PROJECT:
================================

1) Start off with running the following command:

    $ cd /PATH/TO/THIS/BOOTSTRAP/vagrant
    $ vagrant up

2) Now, you will need to clone the git repository that you will be working on into a folder called repo that matchs the one found in the top level of this Bootstrap. The repo folder already exists in order to satify dependencies within the vagrant VM when you first ran ``vigrant up``. Just make sure to REPLACE the existing repo folder with the new one that will contain the existing project source. 

On OSX, GitHub has a great application that allows you to Clone a repo to a folder with just a few clicks, so if you prefer a GUI interface, that's your best bet. Here's a download link: https://central.github.com/mac/latest


3) Make sure the project dependencies are satified by executing the following commands. Change ``<myproject>`` to read the name of the project that you just cloned from GitHub. This is the same name as the folder containing the settings.py file and will be located in your repo folder.

    $ vagrant ssh
    (venv)$ cd quick_start
    (venv)$ sudo fab vagrant continue_project:<myproject>

Your Environment is now ready to work on and be reachable via http://localhost:8080 (unless there's some extra vodoo happening on the application end).

LAST BUT NOT LEAST:
===================

As you begin the project, take 5 minutes to review the Django coding style
guide found here:

    http://docs.djangoproject.com/en/dev/internals/contributing/#coding-sty1le

HAPPY CODING!
