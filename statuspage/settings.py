import os
import dj_database_url

import logging
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PRODUCTION = os.environ.get('PRODUCTION', False)

STATUS_TICKET_URL = os.environ.get('STATUS_TICKET_URL', None)
STATUS_LOGO_URL = os.environ.get('STATUS_LOGO_URL', None)
STATUS_TITLE = os.environ.get('STATUS_TITLE', None)
STATUS_ANALYTICS = os.environ.get('STATUS_ANALYTICS', None)

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
    'default': dj_database_url.config(default="sqlite:///statuspage.db"),
}

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'

MEDIA_ROOT = 'media'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_PATH, '../')

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3a+pfqp937h9we7hwsoiy4jq3hq46jwusrs7c7xedi6ka4oizeu5drj+j'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'status.context_processors.analytics',
)

MIDDLEWARE_CLASSES = (
    'stronghold.middleware.LoginRequiredMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STRONGHOLD_DEFAULTS = True

ROOT_URLCONF = 'statuspage.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'statuspage.wsgi.application'

TEMPLATE_DIRS = (
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'debug_toolbar',
    'django_extensions',
    'bootstrap3',
    'tastypie',
    'avatar',
    'gunicorn',
    'djcelery',
    'djcelery_email',
    'kombu.transport.django',
    'stronghold',
    'status',
)

if os.environ.get('REDIS_URL', None):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "%s/1" % (os.environ.get('REDIS_URL', None)),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

BROKER_URL = os.environ.get("REDIS_URL", None)
CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_TIMEZONE = 'America/Los_Angeles'
CELERY_CREATE_MISSING_QUEUES = True
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", None)
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_CONCURRENCY = 16
CELERY_TRACK_STARTED = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERYD_POOL_RESTARTS = True

APPEND_SLASH = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = os.environ.get('MAIL_SERVER', None)
EMAIL_PORT = os.environ.get('MAIL_PORT', 25)
EMAIL_HOST_USER = os.environ.get('MAIL_USER', None)
EMAIL_HOST_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
EMAIL_USE_TLS = os.environ.get('MAIL_TLS', False)
DEFAULT_FROM_EMAIL = os.environ.get('MAIL_FROM', 'statuspage@unconfigured.org')

if not PRODUCTION:
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False

DISABLE_EXISTING_LOGGERS = False
LOGGING_CONFIG = None

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'status': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'status.api': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'tastypie': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
    },
}

import logging.config
logging.config.dictConfig(LOGGING)

