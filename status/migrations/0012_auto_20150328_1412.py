# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0011_auto_20150217_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('order',), 'verbose_name': 'Status', 'verbose_name_plural': 'Statuses'},
        ),
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]
