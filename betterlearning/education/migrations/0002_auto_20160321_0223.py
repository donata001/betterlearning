# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentLookUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField(null=True, db_index=True)),
                ('step', models.IntegerField(null=True, db_index=True)),
                ('content_pk', models.IntegerField(null=True)),
                ('content_type', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='sessions',
            name='step',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
