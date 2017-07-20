# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 15:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20170619_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='publish',
            field=models.DateField(default=datetime.datetime(2017, 6, 28, 15, 3, 24, 688429, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
