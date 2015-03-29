# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0013_auto_20150328_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='status',
            field=models.ForeignKey(blank=True, to='status.Status', null=True),
            preserve_default=True,
        ),
    ]
