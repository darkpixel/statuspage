from datetime import date, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from braces.views import UserFormKwargsMixin
from stronghold.decorators import public
from status.models import Incident
from status.forms import IncidentCreateForm


class DashboardView(ListView):
    model = Incident


class IncidentDeleteView(DeleteView):
    model = Incident

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentCreateView(UserFormKwargsMixin, CreateView):
    model = Incident
    form_class = IncidentCreateForm


class IncidentUpdateView(UserFormKwargsMixin, UpdateView):
    model = Incident
    form_class = IncidentCreateForm


class HomeView(TemplateView):
    http_method_names = ['get', ]
    template_name = 'status/home.html'

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update(super(HomeView, self).get_context_data(**kwargs))
        kwargs.update({'incident_list': Incident.objects.filter(created__gt=date.today() - timedelta(days=7))})

        if hasattr(settings, 'STATUS_TICKET_URL'):
            kwargs.update({'STATUS_TICKET_URL': settings.STATUS_TICKET_URL})

        if hasattr(settings, 'STATUS_LOGO_URL'):
            kwargs.update({'STATUS_LOGO_URL': settings.STATUS_LOGO_URL})

        if hasattr(settings, 'STATUS_TITLE'):
            kwargs.update({'STATUS_TITLE': settings.STATUS_TITLE})

        return kwargs
