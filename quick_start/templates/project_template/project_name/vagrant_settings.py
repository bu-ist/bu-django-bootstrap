from settings import *

# Put any settings overrides for the local Vagrant environment here
# (Database, Paths, etc.)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/repo/db/email_helper.sqlite',
    }
}

MEDIA_ROOT = '/app/repo/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/app/repo/apps/emailer/static/'
STATIC_URL = '/static/'

CAS_REDIRECT_URL = '/edit'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

ENV = ''

SESSION_COOKIE_PATH = '/'

DEBUG = True
