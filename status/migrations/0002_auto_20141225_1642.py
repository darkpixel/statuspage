# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='data',
            new_name='description',
        ),
        migrations.AddField(
            model_name='incident',
            name='name',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
    ]
