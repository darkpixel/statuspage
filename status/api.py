import logging

from django.contrib.auth.models import \
    User  # BUG: Import the correct user object from settings.py
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import (ALL, ALL_WITH_RELATIONS,
                                NamespacedModelResource, fields)

from .models import Incident, Status

logger = logging.getLogger(__name__)


class ReadOnlyFieldNamespacedModelResource(NamespacedModelResource):
    """ Allows you to add a 'readonly_fields' setting on a ModelResource """
    def __init__(self, **kwargs):
        super(ReadOnlyFieldNamespacedModelResource, self).__init__(**kwargs)
        for fld in getattr(self.Meta, 'readonly_fields', []):
            self.fields[fld].readonly = True


class StatusResource(ReadOnlyFieldNamespacedModelResource):
    class Meta:
        detail_uri_name = 'name'
        queryset = Status.objects.all()
        allowed_methods = ['get']
        resource_name = 'status'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()


class IncidentResource(ReadOnlyFieldNamespacedModelResource):
    status = fields.ForeignKey(StatusResource, 'status', full=True, null=True, blank=True)
    #TODO: We need to include the related user object at some point

    def hydrate(self, bundle):
        u = User.objects.get(username=bundle.request.GET['username'])
        bundle.obj.user = u
        return bundle

    class Meta:
        readonly_fields = ['created', 'updated']
        queryset = Incident.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        resource_name = 'incident'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {
            'created': ALL,
            'updates': ALL,
            'status': ALL_WITH_RELATIONS,
        }
