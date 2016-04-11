# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_prediction_training'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='uuid',
            field=models.CharField(max_length=64, null=True, db_index=True),
        ),
    ]
