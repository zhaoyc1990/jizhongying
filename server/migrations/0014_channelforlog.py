# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-22 03:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0013_auto_20161214_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channelforlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.IntegerField(blank=True, null=True, verbose_name='\u6bcf\u4e2a\u901a\u9053\u7ec4\u7684\u4eba\u6570')),
            ],
        ),
    ]