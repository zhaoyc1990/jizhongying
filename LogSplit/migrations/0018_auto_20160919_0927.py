# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-19 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LogSplit', '0017_auto_20160919_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicename',
            name='is_botnet',
            field=models.BooleanField(default=False, verbose_name='\u670d\u52a1\u662f\u5426\u9700\u8981\u8df3\u677f\u673a\u64cd\u4f5c'),
        ),
    ]
