# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_current_status(apps, schema_editor):
    Incident = apps.get_model('status', 'Incident')
    for incident in Incident.objects.all():
        u = incident.incidentupdate_set.latest()
        incident.status = u.status
        incident.save()


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0014_incident_status'),
    ]

    operations = [
        migrations.RunPython(migrate_current_status,),
    ]
