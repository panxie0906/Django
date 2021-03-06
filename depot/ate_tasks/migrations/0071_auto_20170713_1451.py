# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 06:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0070_bustype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bustype',
            name='device_binding_option',
            field=models.TextField(blank=True, help_text='option需要经过网页进一步加工，如增加button选项，之后才能使用'),
        ),
        migrations.AlterField(
            model_name='bustype',
            name='device_binding_schema',
            field=models.TextField(blank=True, help_text='schema原封不动地传递到网页'),
        ),
    ]
