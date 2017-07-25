# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0056_delete_stimulateformformat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelBindingFormStructure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_type', models.CharField(max_length=255, unique=True, verbose_name='总线类型')),
                ('content', models.TextField(blank=True, verbose_name='表单结构')),
            ],
            options={
                'ordering': ('bus_type',),
                'verbose_name': '通道绑定表单结构',
                'verbose_name_plural': '通道绑定表单结构列表',
            },
        ),
    ]