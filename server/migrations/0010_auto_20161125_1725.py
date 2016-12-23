# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-25 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20161125_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_conf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='configurefile', to='server.ConfigureFile'),
        ),
        migrations.AlterField(
            model_name='configurefile',
            name='newline',
            field=models.CharField(default='\r\n', max_length=10, verbose_name='\u6362\u884c\u7b26'),
        ),
    ]
