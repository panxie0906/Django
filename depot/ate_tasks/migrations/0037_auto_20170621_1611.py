# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 08:11
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0036_auto_20170621_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('device_id', models.CharField(max_length=255, unique=True, verbose_name='id')),
                ('bus', models.CharField(max_length=255, verbose_name='bus_type')),
            ],
        ),
        migrations.AddField(
            model_name='servicenode',
            name='ip',
            field=models.GenericIPAddressField(default='127.0.0.1', verbose_name='ip'),
        ),
        migrations.AddField(
            model_name='device',
            name='service_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='ate_tasks.ServiceNode'),
        ),
    ]
