# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 02:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('depotapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcdDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', models.TextField(blank=True, default='{}')),
                ('name', models.CharField(max_length=255)),
                ('domain_type', models.CharField(max_length=255)),
                ('start_bits', models.IntegerField()),
                ('end_bits', models.IntegerField()),
                ('remark', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IcdMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', models.TextField(blank=True, default='{}')),
                ('name', models.CharField(max_length=255)),
                ('message_id', models.CharField(max_length=255, unique=True)),
                ('bus', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IcdProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', models.TextField(blank=True, default='{}')),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IcdProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', models.TextField(blank=True, default='{}')),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('project_id', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IcdSignal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', models.TextField(blank=True, default='{}')),
                ('name', models.CharField(max_length=255)),
                ('length', models.IntegerField()),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signals', to='depotapp.IcdMessage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '产品列表', 'verbose_name_plural': '产品清单'},
        ),
        migrations.AddField(
            model_name='icdproduct',
            name='icd_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='depotapp.IcdProject'),
        ),
        migrations.AddField(
            model_name='icdmessage',
            name='icd_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='depotapp.IcdProduct'),
        ),
        migrations.AddField(
            model_name='icddomain',
            name='signal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='depotapp.IcdSignal'),
        ),
    ]
