# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 02:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0044_monitor_is_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='icddomain',
            name='attrs',
            field=models.TextField(blank=True, verbose_name='属性信息'),
        ),
        migrations.AddField(
            model_name='icdmessage',
            name='attrs',
            field=models.TextField(blank=True, verbose_name='属性信息'),
        ),
        migrations.AddField(
            model_name='icdsignal',
            name='attrs',
            field=models.TextField(blank=True, verbose_name='属性信息'),
        ),
    ]
