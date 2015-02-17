from braces.views import UserFormKwargsMixin
from datetime import date, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import (
    MonthArchiveView, YearArchiveView, CreateView, DeleteView, DetailView, ListView, TemplateView,
    UpdateView
)
from stronghold.decorators import public
from status.models import Incident, IncidentUpdate
from status.forms import IncidentCreateForm, IncidentUpdateCreateForm


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

    return render_to_response('status/incident_create_form.html', {
        'form': form,
        'form2': form2,
    }, context_instance=RequestContext(request))


class DashboardView(ListView):
    model = Incident


class IncidentDeleteView(DeleteView):
    model = Incident

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentUpdateUpdateView(CreateView):
    model = IncidentUpdate
    form_class = IncidentUpdateCreateForm

    def get_success_url(self):
        return reverse('status:incident_detail', args=[self.kwargs['pk']])

    def form_valid(self, form):
        i = form.save(commit=False)
        i.incident = Incident.objects.get(pk=self.kwargs['pk'])
        i.user = self.request.user
        i.save()
        return HttpResponseRedirect(self.get_success_url())


class IncidentDetailView(DetailView):
    model = Incident

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(IncidentDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IncidentDetailView, self).get_context_data(**kwargs)
        context.update({
            'form': IncidentUpdateCreateForm(),
        })
        return context


class IncidentArchiveYearView(YearArchiveView):
    make_object_list = True
    queryset = Incident.objects.all()
    date_field = 'updated'

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(IncidentArchiveYearView, self).dispatch(*args, **kwargs)


class IncidentArchiveMonthView(MonthArchiveView):
    make_object_list = True
    queryset = Incident.objects.all()
    date_field = 'updated'
    month_format = '%m'

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(IncidentArchiveMonthView, self).dispatch(*args, **kwargs)


class HomeView(TemplateView):
    http_method_names = ['get', ]
    template_name = 'status/home.html'

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update(super(HomeView, self).get_context_data(**kwargs))
        kwargs.update({'incident_list': Incident.objects.filter(updated__gt=date.today() - timedelta(days=7))})

        if hasattr(settings, 'STATUS_TICKET_URL'):
            kwargs.update({'STATUS_TICKET_URL': settings.STATUS_TICKET_URL})

        if hasattr(settings, 'STATUS_LOGO_URL'):
            kwargs.update({'STATUS_LOGO_URL': settings.STATUS_LOGO_URL})

        if hasattr(settings, 'STATUS_TITLE'):
            kwargs.update({'STATUS_TITLE': settings.STATUS_TITLE})

        return kwargs
