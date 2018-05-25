from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from django.views.decorators.cache import cache_page
from tastypie.api import NamespacedApi
from status.api import IncidentResource, StatusResource
from status.models import Incident
from status.views import (
    DashboardView, HomeView, IncidentArchiveMonthView, IncidentArchiveYearView, IncidentDeleteView,
    IncidentDetailView, IncidentUpdateUpdateView, create_incident, IncidentHideView, HiddenDashboardView
)


v1_api = NamespacedApi(api_name='v1', urlconf_namespace='status')
v1_api.register(StatusResource())
v1_api.register(IncidentResource())


urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
    url(r'^$', cache_page(15)(HomeView.as_view()), name='home'),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^dashboard/hidden/$', login_required(HiddenDashboardView.as_view()), name='dashboard_hidden'),
    url(r'^incident/new/$', login_required(create_incident), name='incident_create'),
    url(r'^incident/(?P<pk>\d+)/$', login_required(IncidentDetailView.as_view(model=Incident)), name='incident_detail'),
    url(r'^incident/(?P<pk>\d+)/update/$', login_required(IncidentUpdateUpdateView.as_view()), name='incident_update'),
    url(r'^incident/(?P<pk>\d+)/hide/$', login_required(IncidentHideView.as_view()), name='incident_hide'),
    url(r'^incident/(?P<pk>\d+)/delete/$', login_required(IncidentDeleteView.as_view()), name='incident_delete'),
    url(r'^archive/(?P<year>\d{4})/$', login_required(IncidentArchiveYearView.as_view()), name="archive_year"),
    url(
        r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$',
        login_required(IncidentArchiveMonthView.as_view(month_format='%m')),
        name="archive_month_numeric"
    ),
]
