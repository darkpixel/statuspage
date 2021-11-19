from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone


STATUS_CHOICES = (
    ('success', 'Success'),
    ('info', 'Information'),
    ('warning', 'Warning'),
    ('danger', 'Danger'),
)


class BaseModel(models.Model):
    """ BaseModel provides information on creation and modification times for all child objects. """
    created = models.DateTimeField(editable=False, blank=True, null=True)
    updated = models.DateTimeField(editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        """ Save an object and note the created or updated time. """
        if not self.pk:
            self.created = timezone.now()
        self.updated = timezone.now()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Status(BaseModel):
    """ Status of an incident or event """
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Information')
    icon = models.CharField(max_length=255, help_text='Font Awesome icon name', default='fa-warning')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Incident(BaseModel):
    """ Creates an incident.  Incidents are displayed at the top of the page until closed. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.name)

    def get_absolute_url(self):
        return reverse('status:incident_detail', args=[self.pk, ])

    def get_first_update(self):
        try:
            first = self.incidentupdate_set.first()
        except IncidentUpdate.DoesNotExist:
            first = None
        return first

    def get_latest_update(self):
        try:
            latest = self.incidentupdate_set.latest()
        except IncidentUpdate.DoesNotExist:
            latest = None
        return latest

    class Meta:
        get_latest_by = 'created'
        verbose_name = 'Incident'
        verbose_name_plural = 'Incidents'
        ordering = ['-created', ]


class IncidentUpdate(BaseModel):
    """ Updates about an incident. """
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    description = models.TextField()

    def __unicode__(self):
        return "%s - %s: %s" % (self.user, self.status, self.description)

    def get_absolute_url(self):
        return reverse('status:incident_detail', args=[self.incident.pk, ])

    class Meta:
        get_latest_by = 'created'
        verbose_name = 'Incident Update'
        verbose_name_plural = 'Incident Updates'
        ordering = ['created', ]

    def save(self, *args, **kwargs):
        """ Update the parent incident update time too. """
        self.incident.updated = timezone.now()
        self.incident.save()
        super(IncidentUpdate, self).save(*args, **kwargs)
