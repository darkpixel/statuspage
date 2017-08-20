from datetime import date, timedelta
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext, Template
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import (
    MonthArchiveView, YearArchiveView, CreateView, DeleteView, DetailView, ListView, TemplateView
)
from stronghold.decorators import public
from status.models import Incident, IncidentUpdate
from status.forms import IncidentCreateForm, IncidentUpdateCreateForm

import slack
import slack.chat
import logging
logger = logging.getLogger(__name__)


def send_to_slack(message, channel='engineering', username='statusbot', emoji=':statusbot:', override_debug=False):
    slack.api_token = settings.SLACK_TOKEN
    if settings.DEBUG and not override_debug:
        logger.info('Diverting from %s to dev while in debug mode as %s: %s' % (channel, username, message))
        slack.chat.post_message('dev', 'DEBUG: ' + message, username=username, icon_emoji=emoji)
    else:
        logger.info('Sending to channel %s as %s: %s' % (channel, username, message))
        slack.chat.post_message(channel, message, username=username, icon_emoji=emoji)


def create_incident(request):
    if request.method == 'POST':
        form = IncidentCreateForm(request.POST)
        form2 = IncidentUpdateCreateForm(request.POST)
        if form.is_valid() and form2.is_valid():
            i = form.save(commit=False)
            i.user = request.user
            print i
            i.save()

            f = form2.save(commit=False)
            f.incident = i
            f.user = request.user
            f.save()

            if settings.SLACK_CHANNEL and settings.SLACK_TOKEN:
                if len(f.description) > 50:
                    description = f.description[:50] + '...'
                else:
                    description = f.description
                try:
                    message = "<https://%s%s|%s> (%s): %s" % (
                        get_current_site(request),
                        reverse('status:incident_detail', args=[i.pk, ]),
                        i.name,
                        f.status.name,
                        description
                    )
                    send_to_slack(message, username=settings.SLACK_USERNAME, channel=settings.SLACK_CHANNEL)
                except Exception as e:
                    logger.warn('Unable to send to slack: %s' % (e))

            return HttpResponseRedirect('/')
    else:
        form = IncidentCreateForm()
        form2 = IncidentUpdateCreateForm()

    request_context = RequestContext(request)
    request_context.push({'form': form, 'form2': form2})
    t = get_template('status/incident_create_form.html')
    rendered_template = t.render(request_context.flatten(), request)
    return HttpResponse(rendered_template)
    #return get_template('status/incident_create_form.html').render(request_context.flatten(), request)

    #return render(request, template_name='status/incident_create_form.html', context=request_context)


class DashboardView(ListView):
    model = Incident

    def get_queryset(self):
        return Incident.objects.exclude(hidden=True)


class HiddenDashboardView(ListView):
    model = Incident


class IncidentHideView(DeleteView):
    model = Incident
    template_name = 'status/incident_hide.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.hidden = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentDeleteView(DeleteView):
    model = Incident

    def get_success_url(self):
        return reverse('status:dashboard')


class IncidentUpdateUpdateView(CreateView):
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
        context = super(HomeView, self).get_context_data(**kwargs)
        incident_list = Incident.objects.filter(hidden=False).order_by('-updated')
        context.update({
            'incident_list': incident_list
        })

        if hasattr(settings, 'STATUS_TICKET_URL'):
            context.update({'STATUS_TICKET_URL': settings.STATUS_TICKET_URL})

        if hasattr(settings, 'STATUS_LOGO_URL'):
            context.update({'STATUS_LOGO_URL': settings.STATUS_LOGO_URL})

        if hasattr(settings, 'STATUS_TITLE'):
            context.update({'STATUS_TITLE': settings.STATUS_TITLE})

        status_level = 'success'
        for incident in incident_list:
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
