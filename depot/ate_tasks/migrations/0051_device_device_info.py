# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0050_auto_20170707_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_info',
            field=models.TextField(blank=True, verbose_name='设备信息'),
        ),
    ]
