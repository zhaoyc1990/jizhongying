# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-14 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0010_hostinfo_docker_remote_api_port'),
        ('server', '0006_httpchannel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='environment',
            name='env_group',
        ),
        migrations.AddField(
            model_name='environment',
            name='env_group',
            field=models.ManyToManyField(blank=True, null=True, related_name='Env_Group', to='host.Group'),
        ),
    ]