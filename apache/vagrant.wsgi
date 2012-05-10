# Replace 'myproject' below with your project shortname

import os
import sys
import site
# use the virtualenv's packages
site.addsitedir( os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../venv/lib/python2.6/site-packages")))

# put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../repo")))

# work around WSGI's output restriction - see: http://code.google.com/p/modwsgi/wiki/ApplicationIssues#Writing_To_Standard_Output
sys.stdout = sys.stderr

# tell WSGI/Django which settings module to use
os.environ["DJANGO_SETTINGS_MODULE"] = "myproject.settings_vagrant"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# watch for changes and reload code as needed (development only!)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import monitor
monitor.start(interval=1.0)
