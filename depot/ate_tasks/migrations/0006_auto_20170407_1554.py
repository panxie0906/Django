# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ate_tasks', '0005_taskstep_test_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstep',
            options={'ordering': ('task', 'order'), 'verbose_name': '\u6d4b\u8bd5\u4efb\u52a1\u6b65\u9aa4', 'verbose_name_plural': '\u6d4b\u8bd5\u4efb\u52a1\u6b65\u9aa4\u5217\u8868'},
        ),
    ]