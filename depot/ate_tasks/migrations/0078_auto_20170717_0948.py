# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 01:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0077_bustype_message_schema'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bustype',
            old_name='message_schema',
            new_name='icd_message_schema',
        ),
    ]
