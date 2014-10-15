from settings import *

# Put any settings overrides for the local Vagrant environment here
# (Database, Paths, etc.)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../repo/sqlite/django.sqlite',
    }
}

DEBUG = True
SERVE_STATIC = True

# since DEBUG and SERVE_STATIC are True, static content will be served by Django's
# staticfiles view anyway, so don't bother with STATIC_ROOT
STATIC_ROOT = ''
STATIC_URL = '/static/'


# See note about this in settings.py, or read the docs:
# https://docs.djangoproject.com/en/1.4/topics/http/sessions/
SESSION_COOKIE_PATH = '/'

