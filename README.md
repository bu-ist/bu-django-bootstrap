This is the BU Django base project bootstrap.

It contains an environment and a set of scripts and templates to get
you up and running with Django at BU.

QUICKSTART
==========

Install Vagrant from http://vagrantup.com

    $ cd vagrant
    $ vagrant up
    
    http://localhost:8080

You can always download the latest from GitHub via:

    https://github.com/bu-ist/bu-django-bootstrap/tarball/master

To start a new project, do:

    $ django-admin.py startproject <myproject> --template=./project_template/ repo
    $ cd repo
    $ django-admin.py startapp <myapp> --template=../app_template/

You'll want to use something identifying for ``myproject`` and ``myapp`` -
they should be valid Python module identifiers (so basically a-z and "_").

There are also a few other of setup tasks - see ``/docs/new-project.txt``
for a checklist.

Note that ``repo`` is where you'll put your code (it'll be prepopulated with
the base project scaffolding).  ``repo`` is where you should initialize your
git repository, since we don't want the bootstrap templates mixed in there.

    $ cd repo
    $ git init

As you begin the project, take 5 minutes to review the Django coding style
guide:

    http://docs.djangoproject.com/en/dev/internals/contributing/#coding-style

Now, follow the instructions in ``/docs/new-project.txt`` to get started!
