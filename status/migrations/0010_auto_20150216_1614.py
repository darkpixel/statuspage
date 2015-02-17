# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0009_auto_20150212_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incident',
            options={'ordering': ['-created'], 'get_latest_by': 'created', 'verbose_name': 'Incident', 'verbose_name_plural': 'Incidents'},
        ),
        migrations.AlterModelOptions(
            name='incidentupdate',
            options={'ordering': ['-created'], 'get_latest_by': 'created', 'verbose_name': 'Incident Update', 'verbose_name_plural': 'Incident Updates'},
        ),
    ]
