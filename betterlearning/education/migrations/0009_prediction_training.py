# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0008_auto_20160403_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_personal', models.FloatField(default=0, null=True)),
                ('base_general', models.FloatField(default=0, null=True)),
                ('accumalated', models.FloatField(default=0, null=True)),
                ('current_level', models.IntegerField(null=True)),
                ('correct_num', models.IntegerField(null=True)),
                ('max_currect_momentum', models.IntegerField(null=True)),
                ('aver_speed_at_correct', models.FloatField(default=0, null=True)),
                ('best_speed_at_correct', models.FloatField(default=0, null=True)),
                ('score', models.FloatField(default=0, null=True)),
                ('next_level', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('training_accuracy', models.FloatField(default=0, null=True)),
                ('sample_size', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
