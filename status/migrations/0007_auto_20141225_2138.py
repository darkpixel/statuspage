# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0006_auto_20141225_2137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='modified',
            new_name='updated',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='modified',
            new_name='updated',
        ),
    ]
