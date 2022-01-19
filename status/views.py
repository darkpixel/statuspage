from datetime import date, timedelta
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import (
    MonthArchiveView, YearArchiveView, CreateView, DeleteView, DetailView, ListView, TemplateView
)
from status.models import Incident, IncidentUpdate
from status.forms import IncidentCreateForm, IncidentUpdateCreateForm

import logging
logger = logging.getLogger(__name__)


class BaseContextMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'open_incidents': Incident.objects.exclude(hidden=True).order_by('-updated')
        })
        if hasattr(settings, 'STATUS_TICKET_URL'):
            context.update({'STATUS_TICKET_URL': settings.STATUS_TICKET_URL})

        if hasattr(settings, 'STATUS_LOGO_URL'):
            context.update({'STATUS_LOGO_URL': settings.STATUS_LOGO_URL})

        if hasattr(settings, 'STATUS_TITLE'):
            context.update({'STATUS_TITLE': settings.STATUS_TITLE})
        return context


def create_incident(request):
    if request.method == 'POST':
        form = IncidentCreateForm(request.POST)
        form2 = IncidentUpdateCreateForm(request.POST)
        if form.is_valid() and form2.is_valid():
            i = form.save(commit=False)
            i.user = request.user
            i.save()

            f = form2.save(commit=False)
            f.incident = i
            f.user = request.user
            f.save()

            return HttpResponseRedirect('/')
    else:
        form = IncidentCreateForm()
        form2 = IncidentUpdateCreateForm()

    request_context = RequestContext(request)
    request_context.push({'form': form, 'form2': form2})
    t = get_template('status/incident_create_form.html')
    rendered_template = t.render(request_context.flatten(), request)
    return HttpResponse(rendered_template)


class DashboardView(BaseContextMixin, ListView):
    model = Incident

    def get_queryset(self):
        return Incident.objects.filter(hidden=False)


class HiddenDashboardView(BaseContextMixin, ListView):
    model = Incident
    queryset = Incident.objects.filter(hidden=True)


class IncidentHideView(DeleteView):
    model = Incident
    template_name = 'status/incident_hide.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.hidden = True
        self.object.save()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentDeleteView(BaseContextMixin, DeleteView):
    model = Incident

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentUpdateUpdateView(BaseContextMixin, CreateView):
    model = IncidentUpdate
    form_class = IncidentUpdateCreateForm
    template_name = 'status/incident_form.html'

    def get_success_url(self):
        return reverse('status:incident_detail', args=[self.kwargs['pk']])

    def form_valid(self, form):
        iu = form.save(commit=False)
        i = Incident.objects.get(pk=self.kwargs['pk'])
        i.hidden = False
        i.save()
        iu.incident = i
        iu.incident.hidden = False
        iu.incident.save()
        iu.user = self.request.user
        iu.save()
        return HttpResponseRedirect(self.get_success_url())


class IncidentDetailView(BaseContextMixin, DetailView):
    model = Incident

    def dispatch(self, *args, **kwargs):
        return super(IncidentDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IncidentDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': IncidentUpdateCreateForm(),
            'form_url': reverse('status:incident_update', args=[context['object'].pk, ])
        })
        return context


class IncidentArchiveYearView(BaseContextMixin, YearArchiveView):
    make_object_list = True
    queryset = Incident.objects.all()
    date_field = 'updated'

    def dispatch(self, *args, **kwargs):
        return super(IncidentArchiveYearView, self).dispatch(*args, **kwargs)


class IncidentArchiveMonthView(BaseContextMixin, MonthArchiveView):
    make_object_list = True
    queryset = Incident.objects.all()
    date_field = 'updated'
    month_format = '%m'

    def dispatch(self, *args, **kwargs):
        return super(IncidentArchiveMonthView, self).dispatch(*args, **kwargs)


class HomeView(BaseContextMixin, TemplateView):
    http_method_names = ['get', ]
    template_name = 'status/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        status_level = 'success'
        for incident in context['open_incidents']:
            try:
                if incident.get_latest_update().status.type == 'danger':
                    status_level = 'danger'
                    break
                elif incident.get_latest_update().status.type == 'warning':
                    status_level = 'warning'
                elif incident.get_latest_update().status.type == 'info' and not status_level == 'warning':
                    status_level = 'info'
            except AttributeError:
                # Unable to get_latest_update(), 'None' has no .status
                pass

        context.update({
            'status_level': status_level
        })
        return context
