import os
import logging


logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "statuspage.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

try:
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(application)
except:
    logger.warn('Unable to load Sentry.  Disabled.')

try:
    from dj_static import Cling, MediaCling
    application = Cling(MediaCling(application))
except:
    logger.warn('Unable to load Cling to serve static files.')
