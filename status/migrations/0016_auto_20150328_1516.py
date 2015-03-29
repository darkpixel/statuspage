# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0015_auto_20150328_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='status',
            field=models.ForeignKey(to='status.Status'),
            preserve_default=True,
        ),
    ]
