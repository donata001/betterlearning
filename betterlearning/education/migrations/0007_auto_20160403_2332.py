# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20160403_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='begin',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='end',
            field=models.DateTimeField(db_index=True),
        ),
    ]
