# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-08 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0008_group_docker_registry'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostinfo',
            name='host_status',
            field=models.BooleanField(default=True, verbose_name='\u4e3b\u673a\u8fd0\u884c\u72b6\u6001'),
        ),
    ]