import os
import dj_database_url

import logging
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PRODUCTION = os.environ.get('PRODUCTION', False)

STATUS_TICKET_URL = os.environ.get('STATUS_TICKET_URL', None)
STATUS_LOGO_URL = os.environ.get('STATUS_LOGO_URL', None)
STATUS_TITLE = os.environ.get('STATUS_TITLE', None)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ALLOWED_HOSTS = [
    '*',
]

if os.environ.get('PRODUCTION', False) in (True, 'True', 'TRUE', 'true', '1', 1):
    PRODUCTION = True
    DEBUG = False
else:
    PRODUCTION = False
    DEBUG = True

INTERNAL_IPS = (
    '127.0.0.1',
)

ADMINS = (
    ('Aaron C. de Bruyn', 'aaron@heyaaron.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL', "sqlite:///statuspage.db"))
}

TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_REDIRECT_URL = '/'

MEDIA_ROOT = 'media'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3a+pfqp937h9we7hwsoiy4jq3hq46jwusrs7c7xedi6ka4oizeu5drj+j'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STRONGHOLD_DEFAULTS = True
STRONGHOLD_PUBLIC_URLS = (
    r'^/api/',
)

ROOT_URLCONF = 'statuspage.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'statuspage.wsgi.application'

TEMPLATE_DIRS = (
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django_extensions',
    'django_bootstrap5',
    'django_gravatar',
    'gunicorn',
    'status',
)

APPEND_SLASH = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_HOST = os.environ.get('MAIL_SERVER', None)
EMAIL_PORT = os.environ.get('MAIL_PORT', 25)
EMAIL_HOST_USER = os.environ.get('MAIL_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
EMAIL_USE_TLS = os.environ.get('MAIL_TLS', False)
DEFAULT_FROM_EMAIL = os.environ.get('MAIL_FROM', 'statuspage@unconfigured.org')
