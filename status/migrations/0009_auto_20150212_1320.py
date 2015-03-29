# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def split_into_updates(apps, schema_editor):
    Incident = apps.get_model('status', 'Incident')
    IncidentUpdate = apps.get_model('status', 'IncidentUpdate')

    for incident in Incident.objects.all():
        u = IncidentUpdate(
            incident = incident,
            user = incident.user,
            status = incident.status,
            description = incident.description
        )
        u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0008_auto_20150212_1319'),
    ]

    operations = [
        migrations.RunPython(split_into_updates),
        migrations.RemoveField(
            model_name='incident',
            name='description',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='status',
        ),
    ]
