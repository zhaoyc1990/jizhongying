# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-11 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0007_auto_20160912_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='docker_registry',
            field=models.CharField(default='\u7a7a', max_length=50, verbose_name='docker\u4ed3\u5e93\u5730\u5740\u53ca\u7aef\u53e3'),
        ),
    ]
