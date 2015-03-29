# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0016_auto_20150328_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, editable=False, blank=True)),
                ('updated', models.DateTimeField(null=True, editable=False, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('uptime_robot_id', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incident',
            name='component',
            field=models.ForeignKey(blank=True, to='status.Component', null=True),
            preserve_default=True,
        ),
    ]
