# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 11:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0012_taskinstance_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskinstance',
            options={'ordering': ('task', 'created', 'name'), 'verbose_name': '测试任务实例', 'verbose_name_plural': '测试任务实例列表'},
        ),
    ]
