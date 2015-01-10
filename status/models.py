from django.conf import settings
from django.core.urlresolvers import reverse
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255)
    status = models.ForeignKey(Status)
    description = models.TextField()

    def __unicode__(self):
        return "%s - %s - %s: %s" % (self.user, self.status, self.name, self.description)

    def get_absolute_url(self):
        return reverse('status:incident_detail', args=[self.pk, ])


    class Meta:
        verbose_name = 'Incident'
        verbose_name_plural = 'Incidents'
        ordering = ['-created', ]
