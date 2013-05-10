from settings import *

# Put any settings overrides for the local Vagrant environment here
# (Database, Paths, etc.)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/repo/sqlite/db.sqlite',
    }
}

MEDIA_ROOT = '/app/repo/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/app/repo/apps/{{app_name}}/static/'
STATIC_URL = '/static/'

ENV = ''

SESSION_COOKIE_PATH = '/'
