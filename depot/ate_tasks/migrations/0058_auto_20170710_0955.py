# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 01:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0057_channelbindingformstructure'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChannelBindingFormStructure',
            new_name='DeviceFormStructure',
        ),
    ]
