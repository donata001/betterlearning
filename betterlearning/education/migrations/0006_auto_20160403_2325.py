# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_auto_20160403_0404'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentlookup',
            name='answer',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='correct',
            field=models.BooleanField(default=False),
        ),
    ]
