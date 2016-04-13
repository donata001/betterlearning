# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0012_prediction_training'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='score',
        ),
        migrations.AddField(
            model_name='prediction',
            name='predict',
            field=models.BooleanField(default=False),
        ),
    ]
