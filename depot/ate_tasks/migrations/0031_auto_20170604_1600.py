# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0030_auto_20170604_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icdmessage',
            name='message_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='icdproduct',
            name='project_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='icdproject',
            name='project_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='id'),
        ),
    ]
