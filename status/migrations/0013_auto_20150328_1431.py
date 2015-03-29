# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_status_order(apps, schema_editor):
    Status = apps.get_model('status', 'Status')
    i = 0
    for s in Status.objects.all():
        s.order = i
        i += 1
        s.save()


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0012_auto_20150328_1412'),
    ]

    operations = [
        migrations.RunPython(migrate_status_order,)
    ]
