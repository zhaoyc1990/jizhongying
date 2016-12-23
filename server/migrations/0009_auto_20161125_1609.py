# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-25 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_auto_20161116_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configurefile',
            name='conf_group',
        ),
        migrations.RemoveField(
            model_name='configurefile',
            name='conf_server',
        ),
        migrations.AddField(
            model_name='configurefile',
            name='file_type',
            field=models.CharField(default='txt', max_length=10, verbose_name='\u6587\u4ef6\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='configurefile',
            name='newline',
            field=models.TextField(default='\r\n', max_length=10, verbose_name='\u6362\u884c\u7b26'),
        ),
    ]