# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 07:05
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0046_auto_20170705_1249'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ate_tasks.Product', verbose_name='所属产品'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ate_tasks.Project', verbose_name='所属项目'),
            preserve_default=False,
        ),
    ]
