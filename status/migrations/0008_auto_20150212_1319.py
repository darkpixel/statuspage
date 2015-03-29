# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0007_auto_20141225_2138'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('updated', models.DateTimeField(null=True, editable=False, blank=True)),
                ('description', models.TextField()),
                ('incident', models.ForeignKey(to='status.Incident')),
                ('status', models.ForeignKey(to='status.Status')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Incident Update',
                'verbose_name_plural': 'Incident Updates',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='incident',
            options={'ordering': ['-created'], 'verbose_name': 'Incident', 'verbose_name_plural': 'Incidents'},
        ),
    ]
