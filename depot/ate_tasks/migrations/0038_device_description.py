# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0037_auto_20170621_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
