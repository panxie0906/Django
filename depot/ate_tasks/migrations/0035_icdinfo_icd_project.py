# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 05:57
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0034_auto_20170621_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='icdinfo',
            name='icd_project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='icd_info', to='ate_tasks.IcdProject'),
            preserve_default=False,
        ),
    ]
