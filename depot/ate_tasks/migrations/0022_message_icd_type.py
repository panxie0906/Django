# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 14:32
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0021_icdinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='icd_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ate_tasks.IcdInfo', verbose_name='所属ICD类别'),
            preserve_default=False,
        ),
    ]
