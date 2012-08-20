This is the BU Django base project bootstrap.

It contains an environment and a set of scripts and templates to get
you up and running with Django at BU.

You can always download the latest from GitHub via:

    https://github.com/bu-ist/bu-django-bootstrap/tarball/master

Note that you should DOWNLOAD, not clone, this - unless you actually need
to make changes to the base project.

QUICKSTART
==========

Download and expand the tarball: https://github.com/bu-ist/bu-django-bootstrap/tarball/master

If you prefer ZIP: https://github.com/bu-ist/bu-django-bootstrap/zipball/master

Install Vagrant from http://vagrantup.com

    $ cd vagrant
    $ vagrant up
    $ vagrant ssh

To start a new project, do:

    (venv)$ sudo pip install Django
    (venv)$ mkdir repo
    (venv)$ django-admin.py startproject <myproject> --template=./project_template/ repo
    (venv)$ cd repo
    (venv)$ django-admin.py startapp <myapp> --template=../app_template/

You'll want to use something identifying for ``myproject`` and ``myapp`` -
they should be valid Python module identifiers (so basically a-z and "_").

There are also a few other of setup tasks - see ``/docs/new-project.txt``
for a checklist.

Note that ``repo`` is where you'll put your code (it'll be pre-populated with
the base project scaffolding).  ``repo`` is where you should initialize your
git repository, since we don't want the bootstrap templates mixed in there.

    (venv)$ cd repo
    (venv)$ git init

As you begin the project, take 5 minutes to review the Django coding style
guide:

    http://docs.djangoproject.com/en/dev/internals/contributing/#coding-style

Now, follow the instructions in ``/docs/new-project.txt`` to get started!
