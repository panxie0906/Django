# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0020_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcdInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='名称')),
                ('creator', models.CharField(max_length=255, verbose_name='创建者')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='修改日期')),
                ('description', models.TextField(blank=True, verbose_name='描述信息')),
            ],
            options={
                'verbose_name': 'ICD分类信息',
                'verbose_name_plural': 'ICD分类信息表',
            },
        ),
    ]