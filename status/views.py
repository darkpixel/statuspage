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
from extra_views import ModelFormSetView, InlineFormSet, CreateWithInlinesView
from stronghold.decorators import public
from status.models import Incident, IncidentUpdate
from status.forms import IncidentCreateForm, IncidentFormset


#class IncidentCreateView(CreateView):
#    template_name = 'status/incident_formset.html'
#    model = Incident
#    form_class = IncidentCreateForm
#
#    def get_context_data(self, **kwargs):
#        context = super(IncidentCreateView, self).get_context_data(**kwargs)
#        if self.request.POST:
#            context['incidentupdate_form'] = IncidentFormset(self.request.POST, instance=self.object, user=self.request.user)
#        else:
#            context['incidentupdate_form'] = IncidentFormset(instance=self.object)
#        return context
#
#    def form_valid(self, form):
#        context = self.get_context_data()
#        incidentform = context['incidentupdate_form']
#        if form.is_valid() and incidentform.is_valid():
#            self.object = form.save(commit=False)
#            self.object.user = self.request.user
#            self.object.save()
#            incidentform.instance = self.object
#            incidentform.save()
#
#            return HttpResponseRedirect(self.get_success_url())
#        else:
#            return self.render_to_response(self.get_context_data(form=form))


class IncidentUpdateInline(InlineFormSet):
    model = IncidentUpdate


class IncidentCreateView(CreateWithInlinesView):
    model = Incident
    form_class = IncidentCreateForm
    template_name = 'status/incident_formset.html'
    inlines = [IncidentUpdateInline]


def create_incident(request):
    if request.method == 'POST':
        form = IncidentCreateForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident_formset = IncidentFormset(request.POST)
            if incident_formset.is_valid():
                incident.user = request.user
                incident.save()

                incident_formset.save()
                return HttpResponseRedirect('/')
    else:
        form = IncidentCreateForm()
        incident_formset = IncidentFormset(instance=Incident())
    return render_to_response('status/incident_formset.html', {
        'form': form,
        'incident_formset': incident_formset,
    }, context_instance=RequestContext(request))


class DashboardView(ListView):
    model = Incident


class IncidentDeleteView(DeleteView):
    model = Incident

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentUpdateView(UserFormKwargsMixin, UpdateView):
    model = Incident
    form_class = IncidentCreateForm


class IncidentDetailView(DetailView):
    model = Incident

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(IncidentDetailView, self).dispatch(*args, **kwargs)


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
