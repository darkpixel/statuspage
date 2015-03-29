import logging
import os

from django.core.wsgi import get_wsgi_application

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statuspage.settings")

application = get_wsgi_application()

try:
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(application)
except:
    logger.warn('Unable to load Sentry.  Disabled.')

try:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
except:
    logger.warn('Unable to load whitenoise')
