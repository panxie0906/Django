# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0064_auto_20170713_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icddomain',
            name='attrs',
            field=models.TextField(blank=True, default='{}'),
        ),
        migrations.AlterField(
            model_name='icdmessage',
            name='attrs',
            field=models.TextField(blank=True, default='{}'),
        ),
        migrations.AlterField(
            model_name='icdsignal',
            name='attrs',
            field=models.TextField(blank=True, default='{}'),
        ),
    ]
