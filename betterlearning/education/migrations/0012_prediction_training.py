# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0011_auto_20160411_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='training',
            field=models.ForeignKey(to='education.Training', null=True),
        ),
    ]
