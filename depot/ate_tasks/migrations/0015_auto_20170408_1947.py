# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0014_auto_20170408_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskresult',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建日期'),
        ),
    ]