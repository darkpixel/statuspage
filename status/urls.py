from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path, register_converter
from django.views.decorators.cache import cache_page
from status.models import Incident
from stronghold.decorators import public
from status.views import (
    DashboardView, HomeView, IncidentArchiveMonthView, IncidentArchiveYearView, IncidentDeleteView,
    IncidentDetailView, IncidentUpdateUpdateView, create_incident, IncidentHideView, HiddenDashboardView
)


app_name = 'status'

urlpatterns = [
    # Public Views
    path('', public(cache_page(15)(HomeView.as_view())), name='home'),
    path('incident/<int:pk>/', public(IncidentDetailView.as_view(model=Incident)), name='incident_detail'),
    path('archive/(<int:year>{4}/', public(IncidentArchiveYearView.as_view()), name="archive_year"),
    path('archive/(<int:year>{4})/<int:month>)/', public(IncidentArchiveMonthView.as_view(month_format='%m')), name="archive_month_numeric"),

    # Authenticated Views
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),
    path('dashboard/hidden/', login_required(HiddenDashboardView.as_view()), name='dashboard_hidden'),
    path('incident/new/', login_required(create_incident), name='incident_create'),
    path('incident/<int:pk>/update/', login_required(IncidentUpdateUpdateView.as_view()), name='incident_update'),
    path('incident/<int:pk>/hide/', login_required(IncidentHideView.as_view()), name='incident_hide'),
    path('incident/<int:pk>/delete/', login_required(IncidentDeleteView.as_view()), name='incident_delete'),
]
