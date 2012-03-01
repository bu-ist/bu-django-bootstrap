# Django settings for this project.
import os

# BU: you'll want to set this to True for development and False for any
# production deployment; the best place to set it to True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.

# BU: 
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# BU: again, the best place to set this is in the
# deployment-specific settings files (i.e. settings_local, settings_dev)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',                      # Or path to database file if using sqlite3.
#         'USER': '',                      # Not used with sqlite3.
#         'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# BU: a more sensible default
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
# BU: unlikely to be useful here; can always change
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
# BU: unlikely to be useful here; can always change
USE_L10N = False

# The path set on the session cookie. This should either match the URL 
# path of your project or be parent of that path.  Generally you'll want
# it to be relatively restrictive, to avoid leaking the sessionid to other
# applications hosted at BU.  For more on sessions, see:
# https://docs.djangoproject.com/en/1.3/topics/http/sessions/
#
# Note that if you develop locally with runserver, you'll want to override
# this in your settings_local.py (since runserver will usually need a cookie
# path of '/', while an app deployed to a server should have a non-root cookie
# path).
SESSION_COOKIE_PATH = '/myproject/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# used in urls.py to determine whether Django should serve static media
# (in combination with DEBUG, but since DEBUG may sometimes be True even
# on an Apache server, we want this additional flag)
SERVE_STATIC = False

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# BU: make sure to replace this per-app
SECRET_KEY = 'PLEASECHANGEME!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# BU: this defines the IPs for which the debug toolbar will show up -
# generally only the local IP; additionally, django-debug-toolbar will
# check for whether DEBUG is True.
# See http://pypi.python.org/pypi/django-debug-toolbar for further
# configuration options
INTERNAL_IPS = ('127.0.0.1', )

# BU: change this to...
ROOT_URLCONF = 'myproject.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    # BU: enable this if you need it
    # 'django.core.context_processors.request',
)

# BU: first, ask yourself - does this app really need to send mail?
# If the answer is "yes, it really does", populate the SMTP server
# and login info below, as well as the From: header info.
# DEFAULT_FROM_EMAIL = ''
# SERVER_EMAIL = ''
# EMAIL_HOST = ''
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # BU: these are good defaults for every project
    'south',
    'django_extensions',
    'debug_toolbar',

    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# BU: if you want to use Apache-level Weblogin for authentication rather than
# the default backend, follow the instructions here:
# http://docs.djangoproject.com/en/dev/howto/auth-remote-user/


# BU: APPLICATION-SPECIFIC SETTINGS
# Some applications require specific settings (i.e. TinyMCE, etc.)
# Put these settings here - note that depending on the use case,
# you may need to override them in the per-environment settings files


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# BU: if there's a settings_local file, use those setting to override
# deployment settings (paths, for instance, or DB credentials)
try:
    from settings_local import *
except ImportError:
    pass
