# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0010_auto_20150216_1614'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incidentupdate',
            options={'ordering': ['created'], 'get_latest_by': 'created', 'verbose_name': 'Incident Update', 'verbose_name_plural': 'Incident Updates'},
        ),
    ]
