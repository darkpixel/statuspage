# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0002_auto_20141225_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='type',
            field=models.CharField(default=b'Information', max_length=20, choices=[(b'info', b'Information'), (b'warning', b'Warning'), (b'danger', b'Danger')]),
            preserve_default=True,
        ),
    ]
