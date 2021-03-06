# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-15 05:42
from __future__ import unicode_literals

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0016_auto_20170409_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskresult',
            name='task_instance',
        ),
        migrations.AlterModelOptions(
            name='taskinstance',
            options={'ordering': ('task', 'created'), 'verbose_name': '测试任务实例', 'verbose_name_plural': '测试任务实例列表'},
        ),
        migrations.RemoveField(
            model_name='taskinstance',
            name='description',
        ),
        migrations.RemoveField(
            model_name='taskinstance',
            name='name',
        ),
        migrations.AddField(
            model_name='taskinstance',
            name='detail',
            field=models.TextField(blank=True, help_text='从每一个测试项收集相应的变量，并统一保存在字典里。', verbose_name='任务相关变量明细表'),
        ),
        migrations.AddField(
            model_name='taskinstance',
            name='result',
            field=models.TextField(blank=True, default='[]', help_text='用于各测试项是否通过。', verbose_name='测试结果列表'),
        ),
        migrations.AddField(
            model_name='taskstep',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid1, unique=True, verbose_name='步骤ID'),
        ),
        migrations.AlterField(
            model_name='testitem',
            name='parameters',
            field=models.TextField(blank=True, help_text='测试项的参数只要与代码对应，任何格式都可以,由测试项代码直接读取字符串。', verbose_name='测试项参数'),
        ),
        migrations.DeleteModel(
            name='TaskResult',
        ),
    ]
