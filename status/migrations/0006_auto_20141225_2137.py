# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0005_status_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='modified',
            field=models.DateTimeField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='status',
            name='created',
            field=models.DateTimeField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='status',
            name='modified',
            field=models.DateTimeField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='incident',
            name='created',
            field=models.DateTimeField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
