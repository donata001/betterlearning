# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_sessions_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='fold',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='subset_accuracy',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='test_accuracy',
            field=models.FloatField(default=0, null=True),
        ),
    ]
