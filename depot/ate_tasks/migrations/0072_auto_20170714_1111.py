# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0071_auto_20170713_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bustype',
            name='device_binding_option',
            field=models.TextField(blank=True, help_text='option一般原封不动传递'),
        ),
        migrations.AlterField(
            model_name='bustype',
            name='device_binding_schema',
            field=models.TextField(blank=True, help_text='schema需要经过处理才能传递'),
        ),
    ]
