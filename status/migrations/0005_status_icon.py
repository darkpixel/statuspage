# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0004_auto_20141225_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='icon',
            field=models.CharField(default=b'fa-warning', help_text=b'Font Awesome icon name', max_length=255),
            preserve_default=True,
        ),
    ]
