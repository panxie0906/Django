# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 05:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0015_auto_20170408_1947'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskresult',
            options={'ordering': ('created', 'task_instance'), 'verbose_name': '测试任务结果', 'verbose_name_plural': '测试任务结果列表'},
        ),
    ]