# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20160321_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='session',
            field=models.ForeignKey(to='education.Sessions', null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
