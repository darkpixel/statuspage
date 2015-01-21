from django.conf import settings


def analytics(request):
    return {'STATUS_ANALYTICS': settings.STATUS_ANALYTICS}
