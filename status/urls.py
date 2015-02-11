from django.conf.urls import patterns, url, include
from django.views.decorators.cache import cache_page
from tastypie.api import NamespacedApi
from status.api import IncidentResource, StatusResource
from status.models import Incident
from status.views import (
    DashboardView, HomeView, IncidentArchiveMonthView, IncidentArchiveYearView, IncidentDeleteView,
    IncidentDetailView, IncidentCreateView, IncidentUpdateView
)


v1_api = NamespacedApi(api_name='v1', urlconf_namespace='status')
v1_api.register(StatusResource())
v1_api.register(IncidentResource())


urlpatterns = patterns(
    '',
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', cache_page(15)(HomeView.as_view()), name='home'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^incident/new/$', IncidentCreateView.as_view(), name='incident_create'),
    url(r'^incident/(?P<pk>\d+)/$', IncidentDetailView.as_view(model=Incident), name='incident_detail'),
    url(r'^incident/(?P<pk>\d+)/edit/$', IncidentUpdateView.as_view(model=Incident), name='incident_edit'),
    url(r'^incident/(?P<pk>\d+)/delete/$', IncidentDeleteView.as_view(), name='incident_delete'),
    url(r'^archive/(?P<year>\d{4})/$', IncidentArchiveYearView.as_view(), name="archive_year"),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$', IncidentArchiveMonthView.as_view(month_format='%m'), name="archive_month_numeric"),
)
