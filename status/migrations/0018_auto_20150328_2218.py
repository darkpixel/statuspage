# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0017_auto_20150328_2029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['name'], 'verbose_name': 'Component', 'verbose_name_plural': 'Components'},
        ),
        migrations.AddField(
            model_name='component',
            name='last_status',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
