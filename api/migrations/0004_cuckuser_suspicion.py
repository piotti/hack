# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-18 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_mugging_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuckuser',
            name='suspicion',
            field=models.IntegerField(default=0),
        ),
    ]