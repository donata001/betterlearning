# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_sessions_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentlookup',
            name='course',
            field=models.IntegerField(null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='course',
            field=models.IntegerField(null=True, db_index=True),
        ),
    ]
