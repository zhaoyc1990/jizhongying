# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-09 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_server_curr_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='server_english',
            new_name='name_En',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_chinese',
            new_name='name_Zh',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='curr_tag',
            new_name='tag',
        ),
        migrations.AddField(
            model_name='configurefile',
            name='is_download',
            field=models.BooleanField(default=False, verbose_name='\u66f4\u6539\u540e\u662f\u5426\u4e0b\u8f7d'),
        ),
    ]
