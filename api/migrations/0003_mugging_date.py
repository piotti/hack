# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-18 02:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cuckuser_reputation'),
    ]

    operations = [
        migrations.AddField(
            model_name='mugging',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 9, 18, 2, 37, 3, 295696, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
