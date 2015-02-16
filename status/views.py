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
from status.models import Incident
from status.forms import IncidentCreateForm, IncidentFormset


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        if hasattr(self, 'get_success_message'):
            self.get_success_message(form)
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class IncidentCreateView(FormsetMixin, CreateView):
    template_name = 'status/incident_formset.html'
    model = Incident
    form_class = IncidentCreateForm
    formset_class = IncidentFormset

    def form_valid(self, form, formset):
        form.user = self.request.user
        return super(IncidentCreateView, self).form_valid(form, formset)


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
