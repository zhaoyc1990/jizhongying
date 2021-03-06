# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-12 09:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0007_auto_20160912_1440'),
        ('LogSplit', '0007_auto_20160912_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='servicename',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_path', models.CharField(max_length=100, verbose_name='\u65e5\u5fd7\u8def\u5f84')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_set', to='host.hostinfo')),
            ],
        ),
        migrations.AddField(
            model_name='logsplit',
            name='server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicename_set', to='LogSplit.servicename'),
        ),
    ]
