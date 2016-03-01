# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0011_auto_20150217_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='hidden',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
