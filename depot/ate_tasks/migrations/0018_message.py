# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0017_auto_20170415_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(unique=True)),
                ('message_type', models.CharField(choices=[('1553', 'MILSTD1553B'), ('429', 'ARINC429'), ('FC', 'Fibre Channel')], max_length=60)),
                ('content', models.TextField()),
            ],
        ),
    ]
